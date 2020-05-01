import structlog
from main.model.persistence import AbsenceDAO
from utils.enum import Reasons
from utils.date import dateManager

logger = structlog.getLogger(__name__)


class AbsenceLogic:
    absence_DAO = AbsenceDAO()

    def set_vote_absence_for_user(self, user, reason):
        logger.info("set (vote) absence for User: %s with reason %s" % (user.username, reason.value))
        current_vote_day = dateManager.current_vote_day()
        self.delete_old_and_current_absences_for_user(user)
        self.absence_DAO.set_absence_for_user(user, current_vote_day, current_vote_day, reason)

    def get_absences_from_team_that_do_not_care(self, team):
        logger.debug("get absences for do not Care")
        return self.absence_DAO.get_absences_from_team_for_reason(Reasons.DONOTCARE, team)

    def get_absences_from_team_that_are_out(self, team):
        logger.debug("get absences for out")
        return self.absence_DAO.get_absences_from_team_for_reason(Reasons.OUT, team)

    def get_absent_absences_from_team(self, team):
        logger.debug("get absences for just being Absent")
        return self.absence_DAO.get_absences_from_team_for_reason(Reasons.ABSENT, team)

    def get_sorted_absent_absences_for_team(self, team):
        logger.debug("get sorted absent Absences from all Users")
        absences_from_all_users = self.get_absent_absences_from_team(team)
        user_list = []
        logger.debug("collect all Users that have an absent Absences")
        for absence in absences_from_all_users:
            if absence.user.username not in user_list:
                user_list.append(absence.user.username)

        logger.debug("Sort all Users with their absent absences")
        sorted_absences = {}
        for user_name in user_list:
            sorted_absences[user_name] = []
        for absence in absences_from_all_users:
            sorted_absences[absence.user.username].append(absence)

        return sorted_absences

    def get_active_absent_absences_from_team(self, team):
        logger.debug("get active absent absences")
        current_vote_day = dateManager.current_vote_day()
        absences = self.absence_DAO.get_absences_from_team_for_reason(Reasons.ABSENT, team)
        active_absences = []
        for absence in absences:
            if self.check_if_a_absence_is_active_for_date([absence], current_vote_day):
                active_absences.append(absence)
        return active_absences

    def delete_old_and_current_absences_for_user(self, user):
        logger.debug("delete absences for user: %s that are old or current active" % user.username)
        current_vote_day = dateManager.current_vote_day()
        user_absences_for_reason = self.absence_DAO.get_absences_from_user(user)

        for absence in user_absences_for_reason.filter(absenceFrom__lte=current_vote_day):
            self.absence_DAO.delete_absence(absence)

    def delete_absences_for_user(self, user, absences_str_list):
        logger.debug("delete absences for user: %s that are on this list: %s" % (user.username, absences_str_list))
        absences_from_user = self.absence_DAO.get_absences_from_user(user)
        for absence in absences_from_user:
            if absence.__str__() in absences_str_list:
                self.absence_DAO.delete_absence(absence)

    def delete_vote_absence_for_user(self, user, absent_start_day):
        logger.debug("delete vote absences for user: %s where absent start day %s is bigger than that absences end day " % (user.username, absent_start_day))
        absences = self.absence_DAO.get_absences_from_user(user)
        for absence in absences:
            if absence.reason == Reasons.OUT.value or absence.reason == Reasons.DONOTCARE.value:
                if absence.absenceTo >= absent_start_day:
                    self.absence_DAO.delete_absence(absence)

    def delete_all_inactive_absences(self):
        logger.debug("delete all absences that are not active / old")
        current_vote_day = dateManager.current_vote_day()
        absences = self.absence_DAO.get_absences()
        for absence in absences:
            if absence.absenceTo < current_vote_day:
                self.absence_DAO.delete_absence(absence)

    def check_if_a_absence_is_active_for_date(self, absences, date):
        logger.debug("check if absence: %s ist active for date: %s" % (absences, date))
        absence_active = False
        for absence in absences:
            if absence.absenceFrom <= date <= absence.absenceTo:
                absence_active = True
        return absence_active
