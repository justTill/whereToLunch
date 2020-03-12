import structlog
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from polls.logic import RestaurantLogic, VoteLogic, UserLogic
from weather.logic import weather_context
from absenceCalendar.logic import AbsenceLogic
from utils.enum import Reasons
from utils.date import dateManager
from customize.logic import CustomizeLogic
from django.conf import settings

restaurant_logic = RestaurantLogic()
vote_logic = VoteLogic()
user_logic = UserLogic()
absence_logic = AbsenceLogic()
customize_logic = CustomizeLogic()
logger = structlog.getLogger(__name__)


def index(request):
    template = loader.get_template('polls/index.html')
    choice_of_the_day = vote_logic.choice_of_the_day()
    voted_restaurants = vote_logic.get_voted_restaurants_from_user(
        request.user) if request.user.is_authenticated else None
    supporters = vote_logic.get_choice_of_the_day_supporters(choice_of_the_day)
    user_that_have_not_voted = user_logic.get_users_that_not_voted_yet()
    user_that_are_out = user_logic.get_user_that_are_not_available_for_lunch()
    user_that_do_not_care = user_logic.get_users_that_do_not_care()
    website_name = customize_logic.get_website_name()
    background_image_url = customize_logic.get_background_image_url()
    longest_absence_list = get_longest_list([user_that_have_not_voted, user_that_do_not_care, user_that_are_out])
    context = {
        'restaurant_list': restaurant_logic.get_restaurants_with_votes(),
        'choice_of_the_day': choice_of_the_day,
        'voted_restaurants': voted_restaurants,
        'supporters': supporters,
        'is_after_noon': dateManager.is_after_noon(),
        'weather_context': weather_context(),
        'not_voted': user_that_have_not_voted,
        'user_that_are_out': user_that_are_out,
        'user_that_do_not_care': user_that_do_not_care,
        'website_name': website_name,
        'background_image_url': background_image_url,
        'django_static_url': settings.MEDIA_URL,
        'longest_absence_list': longest_absence_list
    }
    logger.debug('collected index view stuff')
    return HttpResponse(template.render(context, request))


@staff_member_required
def vote(request):
    user = request.user
    logger.info('user: %s is voting' % user.username)
    restaurant_names = request.POST.getlist('voteButton')
    if restaurant_names:
        vote_logic.save_vote_for_restaurants_with_names(restaurant_names, user)
        absence_logic.delete_old_and_current_absences_for_user(user)
    return HttpResponseRedirect(reverse('polls:index'))


@staff_member_required
def iAmOut(request):
    user = request.user
    logger.info('user: %s is out' % user.username)
    vote_logic.delete_votes_from_user(user)
    absence_logic.set_vote_absence_for_user(user, Reasons.OUT)
    return HttpResponseRedirect(reverse('polls:index'))


@staff_member_required
def doNotCare(request):
    user = request.user
    logger.info('user: %s do not care' % user.username)
    vote_logic.delete_votes_from_user(user)
    absence_logic.set_vote_absence_for_user(request.user, Reasons.DONOTCARE)
    return HttpResponseRedirect(reverse('polls:index'))


def get_longest_list(lists):
    longest = max(lists, key=lambda i: len(i))
    return longest
