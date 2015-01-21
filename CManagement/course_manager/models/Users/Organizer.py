from django.db import models
from course_manager.models.UserManagement import UserManagement, OrganizerAccountManager
from course_manager.models.Users.Executive import Executive


class Organizer(Executive):
    """
        This class represents an organizer-account with login permission.\n
        Role-specific functionality is provided by:\n
        *View_Login.py*\n
        *View_Organizer.py*\n
        *View_Organizer_Email.py*\n

        about parameters:
        -----------------

        - **my_user_management**
            + *deprecated!* unused ForeignKey relationship with one UserManagement-object

    """

    class Meta:
        app_label = 'course_manager'

    # bind object generation to our custom UserManager to set up this
    # object properly
    objects = OrganizerAccountManager()

    my_user_management = models.ForeignKey(UserManagement)

    def __str__(self):
        return self.name_of_user + " (Organizer)"