from utils.customize.models import Customize


class CustomizeDAO:

    def get_customize_field_for_choice(self, choice):
        return Customize.objects.filter(key_name=choice.value)
