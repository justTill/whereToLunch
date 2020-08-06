import structlog
from main.model.persistence import UserDAO, VoteDAO, AbsenceDAO
from .absenceLogic import AbsenceLogic

logger = structlog.getLogger(__name__)


class UserLogic:
    vote_dao = VoteDAO()
    user_dao = UserDAO()
    absence_dao = AbsenceDAO()
    absence_logic = AbsenceLogic()

    def get_users_from_team_that_not_voted_yet(self, team):
        logger.debug('process users that not voted')
        votes = self.vote_dao.get_all_votes_from_team(team)
        user_that_voted = [vote.user for vote in votes]
        not_available_users = self.get_user_from_team_that_are_not_available_for_lunch(team)
        do_not_care_user = self.get_users_from_team_that_do_not_care(team)

        user_that_did_something = user_that_voted + do_not_care_user + not_available_users

        return self.user_dao.get_users_from_team_that_are_not_on_list(user_that_did_something, team)

    def get_image_from_user(self, user):
        logger.debug('get image from user: %s' % user)
        return self.user_dao.get_image_from_user(user)

    def get_users_from_team_that_do_not_care(self, team):
        logger.debug('process users that do not care and only want to eat')
        absences = self.absence_logic.get_absences_from_team_that_do_not_care(team)
        users = [absence.user for absence in absences]
        return users

    def get_users_from_team_that_are_out(self, team):
        logger.debug('process users that do not lunch with the team')
        absences = self.absence_logic.get_absences_from_team_that_are_out(team)
        users = [absence.user for absence in absences]
        return users

    def get_users_from_team_that_have_a_active_absent_absence(self, team):
        logger.debug('process users are absent')
        absences = self.absence_logic.get_active_absent_absences_from_team(team)
        users = []
        for absence in absences:
            if absence.user not in users:
                users.append(absence.user)
        return users

    def get_user_from_team_that_are_not_available_for_lunch(self, team):
        logger.debug('process users that do not care and are out for lunch')
        users = self.get_users_from_team_that_have_a_active_absent_absence(
            team) + self.get_users_from_team_that_are_out(team)
        return users

    def get_admin_name_with_email(self):
        superusers = self.user_dao.get_admin_user()
        names = []
        mails = []
        for admin in superusers:
            names.append(admin.username)
            mails.append(admin.email)

        return {'names': names, 'mails': mails}

    def get_team_with_name_or_none(self, name):
        name = self.user_dao.get_team_with_name(name)
        if name:
            name = name[0]
        else:
            name = None
        return name
