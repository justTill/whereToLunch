import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class UserDAO:

    def get_users_that_are_not_on_list(self, userList):
        return User.objects.all().select_related('profile').exclude(profile__user__in=userList)

    def get_image_from_user(self, user):
        user = User.objects.filter(profile__user__username=user.get('user__username')).select_related('profile')
        logger.info('get image from user: %s' % user)
        if user and user.get().profile and user.get().profile.userImage:
            return user.get().profile.userImage.url
        logger.warning('could not get Image URL, check if an image is deposited')
        return None
