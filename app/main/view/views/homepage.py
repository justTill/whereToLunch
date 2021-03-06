import structlog
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.conf import settings
from main.controller.logic import RestaurantLogic, VoteLogic, UserLogic, weather_context, AbsenceLogic, CustomizeLogic
from utils.enum import Reasons
from utils.date import dateManager

restaurant_logic = RestaurantLogic()
vote_logic = VoteLogic()
user_logic = UserLogic()
absence_logic = AbsenceLogic()
customize_logic = CustomizeLogic()
logger = structlog.getLogger(__name__)


def index(request):
    default_context = get_default_context()
    if not request.user.is_anonymous:
        team = request.user.team
        template = loader.get_template('templates/index.html')
        choice_of_the_day = vote_logic.choice_of_the_day_for_team(team)
        voted_restaurants = vote_logic.get_voted_restaurants_from_user(
            request.user) if request.user.is_authenticated else None
        supporters = vote_logic.get_choice_of_the_day_supporters(choice_of_the_day)
        user_that_have_not_voted = user_logic.get_users_from_team_that_not_voted_yet(team)
        user_that_are_out = user_logic.get_user_from_team_that_are_not_available_for_lunch(team)
        user_that_do_not_care = user_logic.get_users_from_team_that_do_not_care(team)
        longest_absence_list = get_longest_list([user_that_have_not_voted, user_that_do_not_care, user_that_are_out])
        default_context.update({
            'restaurant_list': restaurant_logic.get_restaurants_with_votes_from_team(team),
            'choice_of_the_day': choice_of_the_day,
            'voted_restaurants': voted_restaurants,
            'supporters': supporters,
            'not_voted': user_that_have_not_voted,
            'user_that_are_out': user_that_are_out,
            'user_that_do_not_care': user_that_do_not_care,
            'django_static_url': settings.MEDIA_URL,
            'longest_absence_list': longest_absence_list
        })
        logger.debug('collected index view stuff')
    else:
        template = loader.get_template('templates/anonymousPage.html')
    return HttpResponse(template.render(default_context, request))


@staff_member_required
def vote(request):
    user = request.user
    logger.info('user: %s is voting' % user.username)
    restaurant_names = request.POST.getlist('voteButton')
    if restaurant_names:
        vote_logic.save_vote_for_restaurants_with_names(restaurant_names, user)
        absence_logic.delete_old_and_current_absences_for_user(user)
    return HttpResponseRedirect(reverse('main:index'))


@staff_member_required
def iAmOut(request):
    user = request.user
    logger.info('user: %s is out' % user.username)
    vote_logic.delete_votes_from_user(user)
    absence_logic.set_vote_absence_for_user(user, Reasons.OUT)
    return HttpResponseRedirect(reverse('main:index'))


@staff_member_required
def doNotCare(request):
    user = request.user
    logger.info('user: %s do not care' % user.username)
    vote_logic.delete_votes_from_user(user)
    absence_logic.set_vote_absence_for_user(request.user, Reasons.DONOTCARE)
    return HttpResponseRedirect(reverse('main:index'))


def get_longest_list(lists):
    longest = max(lists, key=lambda i: len(i))
    return longest


def get_default_context():
    admin_information = user_logic.get_admin_name_with_email()
    return {
        'website_name': customize_logic.get_website_name(),
        'is_after_noon': dateManager.is_after_noon(),
        'weather_context': weather_context(),
        'background_image_url': customize_logic.get_background_image_url(),
        'admin_name': admin_information['names'],
        'admin_mail': admin_information['mails']
    }
