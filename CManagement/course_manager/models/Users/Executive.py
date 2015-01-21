from django.db import models
from course_manager.models.Users.User import UserAccount
from course_manager.models.Management import Management


class Executive(UserAccount):
    """
        This is the base-class for all user-accounts with login permission.\n
        Role-specific functionality is provided by the respective views.\n
        \n abstract n\

        about parameters:
        -----------------

        - **the_management**
            + *deprecated!* unused ForeignKey relationship with one Management-object

    """

    class Meta:
        abstract = True
        app_label = 'course_manager'

    the_management = models.ForeignKey(Management)

    def __str__(self):
        return self.name_of_user + " (Executive)"