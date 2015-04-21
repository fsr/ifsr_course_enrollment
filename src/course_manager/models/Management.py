from django.db import models


class Management(models.Model):
    """
        deprecated! \n
        \n
        This class covers no functionality at all and should be removed with the next update.\n
        Mind possible cross-dependencies when applying changes.
    """

    class Meta:
        app_label = 'course_manager'

    def __str__(self):
        return "the Management"