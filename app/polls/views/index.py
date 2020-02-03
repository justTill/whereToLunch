from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from polls.logic import RestaurantLogic, VoteLogic, UserLogic
from weather.logic import weather_context
from absenceCalendar.logic import AbsenceLogic
from utils.enum import Reasons
from utils.date import dateManager
from utils.customize.logic import CustomizeLogic
from django.conf import settings

restaurantLogic = RestaurantLogic()
voteLogic = VoteLogic()
userLogic = UserLogic()
absenceLogic = AbsenceLogic()
customize_logic = CustomizeLogic()


def index(request):
    template = loader.get_template('polls/index.html')
    choice_of_the_day = voteLogic.choice_of_the_day()
    voted_restaurants = get_voted_restaurants_from_user(request)
    supporters = get_choice_of_the_day_supporters(request, choice_of_the_day)
    not_voted = userLogic.get_users_that_not_voted_yet()
    user_that_are_out = userLogic.get_user_that_are_not_available_for_lunch()
    user_that_do_not_care = userLogic.get_users_that_do_not_care()
    website_name = customize_logic.get_website_name()
    background_image_url = customize_logic.get_background_image_url()
    context = {
        'restaurant_list': restaurantLogic.get_restaurants_with_votes(),
        'choice_of_the_day': choice_of_the_day,
        'voted_restaurants': voted_restaurants,
        'supporters': supporters,
        'is_after_noon': dateManager.is_after_noon(),
        'weather_context': weather_context(),
        'not_voted': not_voted,
        'user_that_are_out': user_that_are_out,
        'user_that_do_not_care': user_that_do_not_care,
        'website_name': website_name,
        'background_image_url': background_image_url,
        'django_static_url': settings.MEDIA_URL,
    }
    return HttpResponse(template.render(context, request))


@staff_member_required
def vote(request):
    user = request.user
    restaurant_names = request.POST.getlist('voteButton')
    if restaurant_names:
        voteLogic.save_vote_for_restaurants_with_names(restaurant_names, user)
        absenceLogic.delete_old_absence_for_user(user)

    return HttpResponseRedirect(reverse('polls:index'))


@staff_member_required
def iAmOut(request):
    user = request.user
    voteLogic.delete_votes_from_user(user)
    absenceLogic.set_vote_absence_for_user(user, Reasons.OUT)
    return HttpResponseRedirect(reverse('polls:index'))


@staff_member_required
def doNotCare(request):
    user = request.user
    voteLogic.delete_votes_from_user(user)
    absenceLogic.set_vote_absence_for_user(request.user, Reasons.DONOTCARE)
    return HttpResponseRedirect(reverse('polls:index'))


def get_voted_restaurants_from_user(request):
    voted_restaurants = None
    if request.user.is_authenticated:
        voted_restaurants = [vote.restaurant for vote in voteLogic.get_votes_from_user(request.user)]
        return voted_restaurants
    else:
        return voted_restaurants


def get_choice_of_the_day_supporters(request, choiceOfTheDay):
    supporters = []
    if len(choiceOfTheDay) == 1:
        supporters = voteLogic.get_supporters_todays_choice(choiceOfTheDay)
    return supporters
