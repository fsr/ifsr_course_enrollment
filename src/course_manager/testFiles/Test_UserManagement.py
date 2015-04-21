from django.test import TestCase
from django.contrib.auth.models import Group

from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.UserManagement import UserManagement
from course_manager.models.Users.Tutor import Tutor
from course_manager.models.Appointment import Appointment
from course_manager.models.Course import Course
from course_manager.models.Users.User import UserAccount


class TestUserManagement(TestCase):
    """
    test of UserManager class
    """
    def setUp(self):
        for t in Tutor.objects.all():
            t.delete()
        if not (Management.objects.all()):
            m = Management(None)
            m.save()
        if not (CourseManagement.objects.all()):
            cm = CourseManagement(my_management=Management.objects.all()[0])
            cm.save()
        if not (UserManagement.objects.all()):
            um = UserManagement(my_management=Management.objects.all()[0])
            um.save()

        gro = Group.objects.create(name='Tutors')
        gro.save()

    def test_user_account_manager(self):
        """
        test of user_account_manager functions
        :return:
        """
        if not(Management.objects.all()):
            m = Management(None)
            m.save()

        cpp = Course.objects.create(name='c++',
                                    my_course_management=CourseManagement.objects.all()[0])
        cpp.save()
        appum = Appointment(additional_information='test', attendance=2, current_count_of_participants=0,
                            my_course=cpp, location='location')
        appum.save()
        user = UserAccount.objects.create_user(username='user1', s_number='s0000001', name_of_user='user1',
                                               email='user1@tu-dresden.de')
        self.assertEqual(user.email, 'user1@tu-dresden.de')
        self.assertEqual(user.s_number, 's0000001')