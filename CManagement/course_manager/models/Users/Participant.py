from course_manager.models.Users.User import UserAccount
from course_manager.models.UserManagement import ParticipantAccountManager
from django.utils import timezone
from django.db import models


class Participant(UserAccount):
    """
        This class represents a participant-account without login permission.\n
        Role-specific functionality is provided by:\n
        *View_Participants.py*\n

        about parameters:
        -----------------

        - **faculty**
            + optional string holding the participants' faculty
            + which can be set when enrolling to a course appointment
            + *default:* 'none'

        - **credit**
            + optional string holding the participants' credit type
            + which can be set when enrolling to a course appointment
            + *default:* 'none'

    """

    # bind object generation to our custom UserManager to set up this
    # object properly
    objects = ParticipantAccountManager()

    # additional enrollment information
    faculty = models.CharField(max_length=50, default='none', blank=True)
    credit = models.CharField(max_length=50, default='none', blank=True)

    def __str__(self):
        return self.name_of_user + " (Participant)"

    class Meta:
        ordering = ('name_of_user',)
        app_label = 'course_manager'

    def check_time_limit(self, testing_date):
        """
        checks for confirmation-link timeout
        :param testing_date: the current time when the test occurs
        :return: true if overtime, false otherwise
        """

        return testing_date > self.date_joined + timezone.timedelta(days=1)
