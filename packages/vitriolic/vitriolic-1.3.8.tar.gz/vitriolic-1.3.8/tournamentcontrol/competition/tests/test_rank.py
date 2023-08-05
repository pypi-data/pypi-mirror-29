import six
from django.test.utils import override_settings
from test_plus import TestCase
from tournamentcontrol.competition.tests import factories

ORIGINAL_BEHAVIOUR = 'tournamentcontrol.competition.rank.points_func'
CORRECT_BEHAVIOUR = 'tournamentcontrol.competition.rank.correct_points_func'


class RankingLadderEntryTests(TestCase):
    """
    The default implementation awards the following bonus multipliers:

    -   double the win points for wins > 15
    -   win points for wins > 10
    -   half win points for wins > 5
    -   half loss points for losses < 2

    The DYNAMIC_FIELDS are computed with annotations in the LadderEntryQuerySet
    using the function addressed by the `TOURNAMENTCONTROL_RANK_POINTS_FUNC`
    setting.

    Our original implementation had a bug where margin bonuses for winning
    would be accumulated if more than one condition was satisfied. We test both
    the original and desired behaviour.
    """
    DYNAMIC_FIELDS = ('margin', 'diff', 'rank_points')

    def assertLadderEntries(self, home_score, away_score, expected):
        match = factories.MatchFactory.create(
            rank_importance=1,
            home_team_score=home_score,
            away_team_score=away_score,
        )
        six.assertCountEqual(
            self,
            match.ladder_entries.values_list(*self.DYNAMIC_FIELDS),
            expected,
        )

    # Original Behaviour

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=ORIGINAL_BEHAVIOUR)
    def test_bug_win_no_margin_bonus(self):
        "win by <=5, loss by >=2"
        self.assertLadderEntries(3, 1, [(2, 2, 15), (2, -2, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=ORIGINAL_BEHAVIOUR)
    def test_bug_win_margin_bonus_small(self):
        "win by >5"
        self.assertLadderEntries(7, 1, [(6, 6, 22.5), (6, -6, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=ORIGINAL_BEHAVIOUR)
    def test_bug_win_margin_bonus_medium(self):
        "win by >10"
        self.assertLadderEntries(12, 1, [(11, 11, 37.5), (11, -11, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=ORIGINAL_BEHAVIOUR)
    def test_bug_win_margin_bonus_large(self):
        "win by >15"
        self.assertLadderEntries(17, 1, [(16, 16, 67.5), (16, -16, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=ORIGINAL_BEHAVIOUR)
    def test_bug_loss_margin_bonus(self):
        "loss by <2"
        self.assertLadderEntries(2, 1, [(1, 1, 15), (1, -1, 7.5)])

    # Correct Behaviour

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=CORRECT_BEHAVIOUR)
    def test_win_no_margin_bonus(self):
        "win by <=5, loss by >=2"
        self.assertLadderEntries(3, 1, [(2, 2, 15), (2, -2, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=CORRECT_BEHAVIOUR)
    def test_win_margin_bonus_small(self):
        "win by >5"
        self.assertLadderEntries(7, 1, [(6, 6, 22.5), (6, -6, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=CORRECT_BEHAVIOUR)
    def test_win_margin_bonus_medium(self):
        "win by >10"
        self.assertLadderEntries(12, 1, [(11, 11, 30), (11, -11, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=CORRECT_BEHAVIOUR)
    def test_win_margin_bonus_large(self):
        "win by >15"
        self.assertLadderEntries(17, 1, [(16, 16, 45), (16, -16, 5)])

    @override_settings(TOURNAMENTCONTROL_RANK_POINTS_FUNC=CORRECT_BEHAVIOUR)
    def test_loss_margin_bonus(self):
        "loss by <2"
        self.assertLadderEntries(2, 1, [(1, 1, 15), (1, -1, 7.5)])
