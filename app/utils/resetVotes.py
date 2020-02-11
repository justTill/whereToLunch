import structlog
from polls.models import Vote
from restaurantStatistics.models import ChoicesOfTheWeek
from polls.logic import VoteLogic
from absenceCalendar.logic import AbsenceLogic

logger = structlog.getLogger(__name__)


def reset_things_from_last_vote_day():
    """Before we delete all Votes, we need to save the Choice of The Day for the Statistics"""
    voteLogic = VoteLogic()
    absenceLogic = AbsenceLogic()
    choiceOfTheDays = voteLogic.choice_of_the_day()

    """in Case there is a 'Kopf and Kopf rennen' we save both"""
    logger.debug("Save Choice of the day ")
    for choice in choiceOfTheDays:
        ChoicesOfTheWeek.objects.create(restaurant=choice)

    logger.debug("reset Votes")
    Vote.objects.all().delete()

    logger.debug("Delete old absences")
    absenceLogic.delete_all_inactive_absences()
