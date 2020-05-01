from main.model.models import Absence


class AbsenceDAO:

    def set_absence_for_user(self, user, absenceFrom, absenceTo, reason):
        Absence.objects.create(user=user,
                               absenceFrom=absenceFrom,
                               absenceTo=absenceTo,
                               reason=reason.value)

    def get_absences_from_user(self, user):
        return Absence.objects.select_related('user').filter(user=user)

    def get_absences_from_team_for_reason(self, reason, team):
        return Absence.objects.select_related('user').filter(reason=reason.value).filter(user__team=team)

    def get_absences(self):
        return Absence.objects.all()

    def delete_absence(self, absence):
        if isinstance(absence, Absence):
            absence.delete()
