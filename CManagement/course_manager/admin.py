from django.contrib import admin

from course_manager.models.Course import Course
from course_manager.models.Appointment import Appointment
from course_manager.models.Users.Participant import Participant
from course_manager.models.Users.Organizer import Organizer
from course_manager.models.Users.Tutor import Tutor

admin.site.register(Participant)
admin.site.register(Organizer)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Appointment)