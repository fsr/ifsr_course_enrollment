from django.db import models
from course_manager.models.Users.Executive import Executive
from course_manager.models.UserManagement import TutorAccountManager


class Tutor(Executive):
    """
        This class represents a tutor-account with login permission.\n
        Role-specific functionality is provided by:\n
        *View_Login.py*\n
        *View_Tutor.py*\n
        *View_Tutor_Email.py*\n

        about parameters:
        -----------------

        - **is_visible**
            + defines, whether this account is visible to all other users
            + *True:* visible to all users
            + *False:* visible to organizers only
            + *default:* True

    """

    class Meta:
        app_label = 'course_manager'

    # bind object generation to our custom UserManager to set up this
    # object properly
    objects = TutorAccountManager()

    # set visibility
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name_of_user + " (Tutor)"