from unittest import TestCase
from utils.update import reset_things_from_last_vote_day


class TestResetVotes(TestCase):

    def test_reset_things_from_last_vote_day(self):
        # Need two Users
        # Need a restaurant
        # Need a Vote for a Restaurant
        # Need absence for one user
        # check if everything is there

        reset_things_from_last_vote_day()

        # check if everything is gone
