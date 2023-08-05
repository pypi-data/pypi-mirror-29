import unittest
from bonsai_gym_common import GymSimulator


# We only test the gym simulator if we have
# gym installed on the system.
try:
    import gym

    class TestGymSimulator(unittest.TestCase):

        def setUp(self):
            env = gym.make('Taxi-v2')
            self.gymsim = GymSimulator(env)

        def test_append_state(self):
            self.gymsim._append_state(1)
            assert (len(self.gymsim._state_deque)
                    is self.gymsim.DEQUE_SIZE)

        def test_set_deque_size(self):
            self.gymsim._append_state(1)
            self.gymsim._append_state(2)
            self.gymsim._append_state(3)

            # Upsizing
            prev = len(self.gymsim._state_deque)
            self.gymsim.set_deque_size(10)
            assert (len(self.gymsim._state_deque) == 10)
            assert (self.gymsim.DEQUE_SIZE == 10)

            # Downsizing
            self.gymsim.set_deque_size(2)
            assert (len(self.gymsim._state_deque) == 2)
            assert (self.gymsim.DEQUE_SIZE == 2)

            assert self.gymsim._state_deque[-1] == 3

        def test_set_properties(self):
            self.gymsim.set_properties(episode_length=10,
                                       deque_size=4)

            assert (len(self.gymsim._state_deque) == 4)
            assert (self.gymsim.DEQUE_SIZE == 4)
            assert (self.gymsim.EPISODE_LENGTH == 10)

    if __name__ == '__main__':
        unittest.main()
except ImportError:
    pass
