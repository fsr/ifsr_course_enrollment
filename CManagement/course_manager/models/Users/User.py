from django.db import models
from django.contrib.auth.models import User
from course_manager.models.UserManagement import UserAccountManager


class UserAccount(User):
    """
        This is the base-class for all user-accounts.\n

        about parameters:
        -----------------

        - **name_of_user:**
            + holds the user's full name from which its username is generated
            + char field
            + *max length:* 100

        - **s_number:**
            + holds the user's s-number, HTML site cares about validity
            + char field
            + *max length:* 200, don't care about it


    """

    class Meta:
        app_label = 'course_manager'

    # bind object generation to our custom UserManager to set up this
    # object properly
    objects = UserAccountManager()

    name_of_user = models.CharField(max_length=100)
    s_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name_of_user