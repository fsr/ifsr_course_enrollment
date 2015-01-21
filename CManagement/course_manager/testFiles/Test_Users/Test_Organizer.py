from django.test import TestCase
from course_manager.models.Users.Organizer import Organizer
from course_manager.models.Appointment import Appointment
from course_manager.models.Course import Course
from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.UserManagement import UserManagement
from course_manager.models.Users.Participant import Participant
from django.contrib.auth.models import Group


class TestOrganizer(TestCase):
    """
    test of Organizer class
    """
    def setUp(self):
        """
        create three organizers in database
        :return:
        """
        for o in Organizer.objects.all():
            o.delete()
        for a in Appointment.objects.all():
            a.delete()
        for c in Course.objects.all():
            c.delete()
        if not (Management.objects.all()):
            m = Management(None)
            m.save()
        if not (CourseManagement.objects.all()):
            cm = CourseManagement(my_management=Management.objects.all()[0])
            cm.save()
        if not (UserManagement.objects.all()):
            um = UserManagement(my_management=Management.objects.all()[0])
            um.save()
        gro = Group.objects.create(name='Organizers')
        gro.save()
        Organizer.objects.create_user(name_of_user='organizer1', email='organizer1@tu-dresden.de',
                                      s_number='s2000001')
        Organizer.objects.create_user(name_of_user='organizer2', email='organizer2@tu-dresden.de',
                                      s_number='s2000002')
        Organizer.objects.create_user(name_of_user='organizer3', email='organizer3@tu-dresden.de',
                                      s_number='s2000003')

        cpp = Course.objects.create(name='c++',
                                    my_course_management=CourseManagement.objects.all()[0])
        cpp.save()
        Appointment.objects.create(my_course=cpp, current_count_of_participants=0)

    def test_base_organizer(self):
        """
        test that organizer objects can be returned with different attributes
        :return:
        """
        organizer1 = Organizer.objects.get(name_of_user='organizer1')
        self.assertEqual(organizer1.email, 'organizer1@tu-dresden.de')
        self.assertEqual(organizer1.s_number, 's2000001')
        organizer2 = Organizer.objects.get(email='organizer2@tu-dresden.de')
        self.assertEqual(organizer2.name_of_user, 'organizer2')
        self.assertEqual(organizer2.s_number, 's2000002')
        organizer3 = Organizer.objects.get(s_number='s2000003')
        self.assertEqual(organizer3.name_of_user, 'organizer3')
        self.assertEqual(organizer3.email, 'organizer3@tu-dresden.de')

    def test_method_sign_in_new_participant(self):
        """
        test that participant can be added to an appointment
        :return:
        """
        appoint = Appointment.objects.all()[0]
        part1 = Participant.objects.create_user(name_of_user='Test', email='test@test.de', username='Test', s_number="")
        appoint.add_participant(part1)
        self.assertIn(part1, appoint.my_participants.all())

