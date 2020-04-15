import structlog
from main.model.models import ChoicesOfTheWeek, Vote
from main.controller.logic import VoteLogic, AbsenceLogic
from users.models import Team

logger = structlog.getLogger(__name__)


def reset_things_from_last_vote_day():
    voteLogic = VoteLogic()
    absenceLogic = AbsenceLogic()
    for team in Team.objects.all():
        choiceOfTheDays = voteLogic.choice_of_the_day_for_team(team)
        logger.debug("Save Choice of the days for team %s " % team.team_name)
        for choice in choiceOfTheDays:
            ChoicesOfTheWeek.objects.create(restaurant=choice)

    logger.info("reset Votes")
    Vote.objects.all().delete()

    logger.info("Delete old absences")
    absenceLogic.delete_all_inactive_absences()
