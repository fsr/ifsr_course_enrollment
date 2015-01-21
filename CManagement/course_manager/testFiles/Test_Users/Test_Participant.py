from django.test import TestCase
from course_manager.models.Users.Participant import Participant
from course_manager.models.Appointment import Appointment
from course_manager.models.Course import Course
from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from django.utils import timezone
import datetime


class ParticipantTest(TestCase):
    """
    test of Participant class
    """
    def setUp(self):
        """
        create three participant objects in database
        :return:
        """
        for p in Participant.objects.all():
            p.delete()
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
        cpp = Course.objects.create(name='c++',
                                    my_course_management=CourseManagement.objects.all()[0])
        cpp.save()

        Participant.objects.create_user(name_of_user='participant1', email='participant1@tu-dresden.de',
                                        username='participant1', s_number='s4000001')
        Participant.objects.create_user(name_of_user='participant2', email='participant2@tu-dresden.de',
                                        username='participant2', s_number='s4000002')
        Participant.objects.create_user(name_of_user='participant3', email='participant3@tu-dresden.de',
                                        username='participant3', s_number='s4000003')
        Appointment.objects.create(my_course=cpp, current_count_of_participants=0)

    def test_base_participant(self):
        """
        test that a participant object gets returned when called with different attributes
        :return:
        """
        participant1 = Participant.objects.get(name_of_user='participant1')
        self.assertEqual(participant1.email, 'participant1@tu-dresden.de')
        self.assertEqual(participant1.s_number, 's4000001')
        participant2 = Participant.objects.get(email='participant2@tu-dresden.de')
        self.assertEqual(participant2.name_of_user, 'participant2')
        self.assertEqual(participant2.s_number, 's4000002')
        participant3 = Participant.objects.get(s_number='s4000003')
        self.assertEqual(participant3.name_of_user, 'participant3')
        self.assertEqual(participant3.email, 'participant3@tu-dresden.de')

    def test_method_check_time_limit(self):
        """
        test of check_time_limit function
        :return:
        """
        participant = Participant.objects.get(name_of_user='participant2')
        #test, if participant registered less than 24h ago, has to be False
        self.assertEqual(participant.check_time_limit(timezone.now()), False)
        #participant registered 3h ago, has to be False
        self.assertEqual(participant.check_time_limit(timezone.now()+datetime.timedelta(hours=3)), False)
        # participant confirms registration one minute bfeore reaching the 24h limit after registration, has to be False
        self.assertEqual(participant.check_time_limit(timezone.now()+datetime.timedelta(minutes=1439)), False)
        # participant confirms registration seconds just after the limit is reached, has to be True
        self.assertEqual(participant.check_time_limit(timezone.now()+datetime.timedelta(minutes=1440)), True)
        # participant confirms registration 2 after mail has been sent, has to be True
        self.assertEqual(participant.check_time_limit(timezone.now()+datetime.timedelta(days=2)), True)




