from absenceCalendar.persistence import AbsenceDAO
from utils.enum import Reasons
from utils.date import dateManager


class AbsenceLogic:
    absence_DAO = AbsenceDAO()

    def set_vote_absence_for_user(self, user, reason):
        current_vote_day = dateManager.current_vote_day()
        absences = self.absence_DAO.get_absences_from_user(user).filter(reason=reason.value)
        self.delete_old_absence_for_user(user)

        if not self.check_if_a_absence_is_active_for_date(absences, current_vote_day):
            self.absence_DAO.set_absence_for_user(user, current_vote_day, current_vote_day, reason)

    def get_absences_for_do_not_care(self):
        return self.absence_DAO.get_absences_for_reason(Reasons.DONOTCARE)

    def get_absences_for_out(self):
        return self.absence_DAO.get_absences_for_reason(Reasons.OUT)

    def get_absent_absences(self):
        return self.absence_DAO.get_absences_for_reason(Reasons.ABSENT)

    def get_sorted_absent_absences(self):
        absences_from_all_users = self.get_absent_absences()
        user_list = []
        for absence in absences_from_all_users:
            if absence.user.username not in user_list:
                user_list.append(absence.user.username)

        sorted_absences = {}
        for user in user_list:
            sorted_absences[user] = []
        for absence in absences_from_all_users:
            sorted_absences[absence.user.username].append(absence)

        return sorted_absences

    def get_active_absent_absences(self):
        current_vote_day = dateManager.current_vote_day()
        absences = self.absence_DAO.get_absences_for_reason(Reasons.ABSENT)
        active_absences = []
        for absence in absences:
            if self.check_if_a_absence_is_active_for_date([absence], current_vote_day):
                active_absences.append(absence)
        return active_absences

    def delete_old_absence_for_user(self, user):
        current_vote_day = dateManager.current_vote_day()
        reasons = [Reasons.OUT.value, Reasons.DONOTCARE.value, Reasons.ABSENT.value]
        user_absences_for_reason = self.absence_DAO.get_absences_from_user(user).filter(reason__in=reasons)

        for absence in user_absences_for_reason.filter(absenceFrom__lte=current_vote_day):
            self.absence_DAO.delete_absence(absence)

    def delete_absences_for_user(self, user, absences_str_list):
        absences_from_user = self.absence_DAO.get_absences_from_user(user)
        for absence in absences_from_user:
            if absence.__str__() in absences_str_list:
                self.absence_DAO.delete_absence(absence)

    def delete_vote_absence_for_user(self, user, absent_start_day):
        absences = self.absence_DAO.get_absences_from_user(user)
        for absence in absences:
            if absence.reason == Reasons.OUT.value or absence.reason == Reasons.DONOTCARE.value:
                if absence.absenceTo >= absent_start_day:
                    self.absence_DAO.delete_absence(absence)

    def delete_all_inactive_absences(self):
        current_vote_day = dateManager.current_vote_day()
        absences = self.absence_DAO.get_absences()
        for absence in absences:
            if absence.absenceTo < current_vote_day:
                self.absence_DAO.delete_absence(absence)

    def check_if_a_absence_is_active_for_date(self, absences, date):
        absence_active = False
        for absence in absences:
            if absence.absenceFrom <= date <= absence.absenceTo:
                absence_active = True
        return absence_active
