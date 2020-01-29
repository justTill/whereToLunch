from django.contrib.auth.models import User


class UserDAO:

    def get_users_that_are_not_on_list(self, userList):
        return User.objects.all().select_related('profile').exclude(profile__user__in=userList)

    def get_image_from_user(self, user):
        user = User.objects.filter(profile__user__username=user.get('user__username')).select_related('profile')
        if user and user.get().profile and user.get().profile.userImage:
            return user.get().profile.userImage.url
        return None
