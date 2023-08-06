# Copyright 2018 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Metropolis-Hastings Transition Kernel."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import warnings

import tensorflow as tf

from tensorflow_probability.python.mcmc import kernel as kernel_base
from tensorflow_probability.python.mcmc import util as mcmc_util
from tensorflow.python.ops.distributions import util as distributions_util


__all__ = [
    'MetropolisHastings',
]


# Cause all warnings to always be triggered.
# Not having this means subsequent calls wont trigger the warning.
warnings.simplefilter('always')


MetropolisHastingsKernelResults = collections.namedtuple(
    'MetropolisHastingsKernelResults',
    [
        'accepted_results',
        'is_accepted',
        'log_accept_ratio',
        'proposed_state',
        'proposed_results',
    ])


class MetropolisHastings(kernel_base.TransitionKernel):
  """Runs one step of the Metropolis-Hastings algorithm.

  The [Metropolis-Hastings algorithm](
  https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm) is a
  Markov chain Monte Carlo (MCMC) technique which uses a proposal distribution
  to eventually sample from a target distribution.

  Note: `inner_kernel.one_step` must return `kernel_results` as a
  `collections.namedtuple` and must itself have the following members:

  - `target_log_prob`
  - `log_acceptance_correction` [Optional]

  The Metropolis-Hastings log acceptance-probability is computed as:

  ```python
  log_accept_ratio = (current_kernel_results.target_log_prob
                      - previous_kernel_results.target_log_prob
                      + current_kernel_results.log_acceptance_correction)
  ```

  If `current_kernel_results.log_acceptance_correction` does not exist, it is
  presumed `0.` (i.e., that the proposal distribution is symmetric)."

  The most common use-case for `log_acceptance_correction` is in the
  Metropolis-Hastings algorithm, i.e.,

  ```none
  accept_prob(x' | x) = p(x') / p(x) (g(x|x') / g(x|x'))

  where,
    p  represents the target distribution,
    g  represents the proposal (conditional) distribution,
    x' is the proposed state, and,
    x  is current state
  ```

  The log of the parenthetical term is the `log_acceptance_correction`.

  The `log_acceptance_correction` may not necessarily correspond to the ratio of
  proposal distributions, e.g, `log_acceptance_correction` has a different
  interpretation in Hamiltonian Monte Carlo.

  #### Examples

  ```python
  import tensorflow_probability as tfp
  hmc = tfp.mcmc.MetropolisHastings(
      tfp.mcmc.UncalibratedHamiltonianMonteCarlo(
          target_log_prob_fn=lambda x: -x - x**2,
          step_size=0.1,
          num_leapfrog_steps=3))
  # ==> functionally equivalent to:
  # hmc = tfp.mcmc.HamiltonianMonteCarlo(
  #     target_log_prob_fn=lambda x: -x - x**2,
  #     step_size=0.1,
  #     num_leapfrog_steps=3)
  ```

  """

  def __init__(self, inner_kernel, seed=None, name=None):
    """Instantiates this object.

    Args:
      inner_kernel: `TransitionKernel`-like object which has
        `collections.namedtuple` `kernel_results` and which contains a
        `target_log_prob` member and optionally a `log_acceptance_correction`
        member.
      seed: Python integer to seed the random number generator.
      name: Python `str` name prefixed to Ops created by this function.
        Default value: `None` (i.e., "hmc_kernel").

    Returns:
      metropolis_hastings_kernel: Instance of `TransitionKernel` which wraps the
        input transtion kernel with the Metropolis-Hastings algorithm.
    """
    self._inner_kernel = inner_kernel
    self._seed = seed
    self._name = name
    if inner_kernel.is_calibrated:
      warnings.warn('Supplied `TransitionKernel` is already calibrated. '
                    'Composing with `MetropolisHastings` `TransitionKernel` '
                    'may not be required.')

  @property
  def inner_kernel(self):
    return self._inner_kernel

  @property
  def seed(self):
    return self._seed

  @property
  def name(self):
    return self._name

  @property
  def is_calibrated(self):
    return True

  def one_step(self, current_state, previous_kernel_results):
    """Takes one step of the TransitionKernel.

    Args:
      current_state: `Tensor` or Python `list` of `Tensor`s representing the
        current state(s) of the Markov chain(s).
      previous_kernel_results: A (possibly nested) `tuple`, `namedtuple` or
        `list` of `Tensor`s representing internal calculations made within the
        previous call to this function (or as returned by `bootstrap_results`).

    Returns:
      next_state: `Tensor` or Python `list` of `Tensor`s representing the
        next state(s) of the Markov chain(s).
      kernel_results: A (possibly nested) `tuple`, `namedtuple` or `list` of
        `Tensor`s representing internal calculations made within this function.

    Raises:
      ValueError: if `inner_kernel` results doesn't contain the member
        "target_log_prob".
    """
    # Take one inner step.
    [
        proposed_state,
        proposed_results,
    ] = self.inner_kernel.one_step(
        current_state,
        previous_kernel_results.accepted_results)

    def has_target_log_prob(kr):
      return getattr(kr, 'target_log_prob', None) is not None

    if (not has_target_log_prob(proposed_results) or
        not has_target_log_prob(previous_kernel_results.accepted_results)):
      raise ValueError('"target_log_prob" must be a member of '
                       '`inner_kernel` results.')

    # Compute log(acceptance_ratio).
    to_sum = [proposed_results.target_log_prob,
              -previous_kernel_results.accepted_results.target_log_prob]
    try:
      to_sum.append(proposed_results.log_acceptance_correction)
    except AttributeError:
      warnings.warn('Supplied inner `TransitionKernel` does not have a '
                    '`log_acceptance_correction`. Assuming its value is `0.`')
    log_accept_ratio = mcmc_util.safe_sum(
        to_sum, name='compute_log_accept_ratio')

    # If proposed state reduces likelihood: randomly accept.
    # If proposed state increases likelihood: always accept.
    # I.e., u < min(1, accept_ratio),  where u ~ Uniform[0,1)
    #       ==> log(u) < log_accept_ratio
    # Note:
    # - We mutate seed state so subsequent calls are not correlated.
    # - We mutate seed BEFORE using it just in case users supplied the
    #   same seed to the inner kernel.
    self._seed = distributions_util.gen_new_seed(
        self.seed, salt='metropolis_hastings_one_step')
    log_uniform = tf.log(tf.random_uniform(
        shape=tf.shape(proposed_results.target_log_prob),
        dtype=proposed_results.target_log_prob.dtype.base_dtype,
        seed=self.seed))
    is_accepted = log_uniform < log_accept_ratio

    independent_chain_ndims = distributions_util.prefer_static_rank(
        proposed_results.target_log_prob)

    next_state = mcmc_util.choose(
        is_accepted,
        proposed_state,
        current_state,
        independent_chain_ndims)

    accepted_results = type(proposed_results)(**dict(
        [(fn,
          mcmc_util.choose(
              is_accepted,
              getattr(proposed_results, fn),
              getattr(previous_kernel_results.accepted_results, fn),
              independent_chain_ndims))
         for fn in proposed_results._fields]))

    return [
        next_state,
        MetropolisHastingsKernelResults(
            accepted_results=accepted_results,
            is_accepted=is_accepted,
            log_accept_ratio=log_accept_ratio,
            proposed_state=proposed_state,
            proposed_results=proposed_results,
        )]

  def bootstrap_results(self, init_state):
    """Returns an object with the same type as returned by `one_step`.

    Args:
      init_state: `Tensor` or Python `list` of `Tensor`s representing the
        a state(s) of the Markov chain(s).

    Returns:
      kernel_results: A (possibly nested) `tuple`, `namedtuple` or `list` of
        `Tensor`s representing internal calculations made within this function.

    Raises:
      ValueError: if `inner_kernel` results doesn't contain the member
        "target_log_prob".
    """
    pkr = self._inner_kernel.bootstrap_results(init_state)
    if 'target_log_prob' not in pkr._fields:
      raise ValueError(
          '"target_log_prob" must be a member of `inner_kernel` results.')
    x = pkr.target_log_prob
    return MetropolisHastingsKernelResults(
        accepted_results=pkr,
        is_accepted=tf.ones_like(x, dtype=tf.bool),
        log_accept_ratio=tf.zeros_like(x),
        proposed_state=init_state,
        proposed_results=pkr,
    )
