import structlog
from django.contrib.auth import get_user_model

User = get_user_model()
logger = structlog.getLogger(__name__)


class UserDAO:

    def get_users_from_team_that_are_not_on_list(self, userList, team):
        return User.objects.all().filter(team=team).exclude(username__in=userList)

    def get_image_from_user(self, user):
        user = User.objects.filter(username=user.get('user__username'))
        logger.debug('get image from user: %s' % user)
        if user and user.get() and user.get().user_image:
            return user.get().user_image.url
        logger.warning('could not get Image URL, check if an image is deposited')
        return None

    def get_admin_user(self):
        return User.objects.all().filter(is_superuser=True)
