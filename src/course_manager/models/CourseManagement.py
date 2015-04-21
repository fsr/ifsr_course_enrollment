from django.db import models
from course_manager.models.Management import Management


class CourseManagement(models.Model):
    """
        deprecated! \n
        \n
        This class covers no functionality at all and should be removed with the next update.\n
        Mind possible cross-dependencies when applying changes.
    """

    class Meta:
        app_label = 'course_manager'

    my_management = models.OneToOneField(Management, primary_key=True)

    def __str__(self):
        return "the Course Management"
