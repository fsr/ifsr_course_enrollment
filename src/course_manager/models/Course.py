from django.db import models
from course_manager.models.CourseManagement import CourseManagement


class Course(models.Model):
    """
    This class represents a course which holds multiple (or none) appointments.\n
    Organizers may create a course without any appointments for announcement reasons.\n
    The class "Appointment" provides a Foreign Key (many-to-one) relationship with a single course.\n

    about parameters:
    -----------------

        - **my_course_management**
            + *deprecated!* unused ForeignKey relationship with one CourseManagement-object
            + management functionality is provided by views\n

        - **is_visible:**
            + any created course is always visible for admins, organizers and tutors in admins page. \n
            + If 'is_visible = False" (by default), the course isn't shown on the public enrollment page

        - **name**
            + a string (char field) which holds the course name
            + *max length:* 100
    """

    class Meta:
        app_label = 'course_manager'

    name = models.CharField(max_length=100)
    my_course_management = models.ForeignKey(CourseManagement)
    # set visibility
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name
