Bonsai Gym Common
=================

A python library for integrating Bonsai BRAIN with Open AI Gym
environments.

Installation
------------

Install the latest stable from PyPI:

::

    $ pip install bonsai-gym-common

Install the latest in-development version:

::

    $ pip install https://github.com/BonsaiAI/bonsai-gym-common

Usage
-----

Once installed, import ``bonsai_gym_common`` in order to access base
class ``GymSimulator`` and ``GymImageSimulator``, which implement all of
the environment-independent Bonsai SDK integrations necessary to train a
Bonsai BRAIN to play an OpenAI Gym simulator.

::

    import gym

    from bonsai_gym_common import GymSimulator

    class CartPoleSimulator(GymSimulator):
        # Perform cartpole-specific integrations here.


