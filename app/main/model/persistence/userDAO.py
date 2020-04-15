import structlog
from django.contrib.auth import get_user_model

User = get_user_model()
logger = structlog.getLogger(__name__)


class UserDAO:

    def get_users_that_are_not_on_list(self, userList):
        return User.objects.all().select_related('profile').exclude(profile__user__in=userList)

    def get_image_from_user(self, user):
        user = User.objects.filter(profile__user__username=user.get('user__username')).select_related('profile')
        logger.debug('get image from user: %s' % user)
        if user and user.get().profile and user.get().profile.userImage:
            return user.get().profile.userImage.url
        logger.warning('could not get Image URL, check if an image is deposited')
        return None
