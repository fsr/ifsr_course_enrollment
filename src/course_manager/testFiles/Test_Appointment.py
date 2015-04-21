from django.test import TestCase
from course_manager.models.Appointment import Appointment
from course_manager.models.Course import Course
from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.Users.Participant import Participant
from course_manager.models.Users.Tutor import Tutor
from django.contrib.auth.models import Group


class AppointmentTest(TestCase):
    """
    test for Appointment class
    """

    def setUp(self):
        """
        create course, appointment, tutor and participant objects in database
        :return:
        """
        global cpp
        for a in Appointment.objects.all():
            a.delete()
        for p in Participant.objects.all():
            p.delete()
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

        c = Course.objects.create(name='c',
                                    my_course_management=CourseManagement.objects.all()[0])
        c.save()
        gro = Group.objects.create(name='Tutors')
        gro.save()

        Appointment.objects.create(lesson='2.DS', additional_information='test',
                                   current_count_of_participants=0, my_course=cpp,
                                   weekday='Sunday', location='location')
        Appointment.objects.create(additional_information='test', current_count_of_participants=0,
                                   my_course=cpp, location='location')
        Appointment.objects.create(lesson='2.DS', additional_information='test',
                                   current_count_of_participants=0, my_course=c,
                                   weekday='Sunday', location='location')
        Participant.objects.create_user(name_of_user='participant1', email='participant1@tu-dresden.de',
                                        s_number='s4000001', username='participant1')
        Participant.objects.create_user(name_of_user='participant2', email='participant2@tu-dresden.de',
                                        s_number='s4000002', username='participant2')
        Participant.objects.create_user(name_of_user='participant3', email='participant3@tu-dresden.de',
                                        s_number='s4000003', username='participant3')
        Tutor.objects.create_user(name_of_user='tutor1', s_number='s5000001', email='tutor1@tu-dresden.de')

    def test_base_appointment(self):
        """
        test if you can get all appointment objects correct from database
        :return:
        """
        appointment1 = Appointment.objects.all()[0]
        appointment2 = Appointment.objects.all()[1]
        self.assertEqual(cpp, appointment1.my_course)
        self.assertEqual(cpp, appointment2.my_course)
        self.assertEqual(appointment1.weekday, 'Sunday')
        self.assertEqual(appointment2.weekday, 'Monday')
        self.assertEqual(appointment1.lesson, '2.DS')
        self.assertEqual(appointment2.lesson, '1.DS')

    def test_method_add_participant(self):
        """
        test of add_participant function, that participant gets inserted right and that attribute
        'current_count_of_participants' increases,
        as well as avoiding that a participant can enroll in the appointment again and again.
        :return:
        """
        p1 = Participant.objects.get(name_of_user='participant1')
        p2 = Participant.objects.get(name_of_user='participant2')
        p3 = Participant.objects.get(name_of_user='participant3')
        app = Appointment.objects.all()[0]
        number = app.current_count_of_participants
        app.add_participant(p1)
        app.save()
        self.assertEqual(app.current_count_of_participants, number + 1)
        app.add_participant(p2)
        app.save()
        self.assertEqual(app.current_count_of_participants, number + 2)
        app.add_participant(p3)
        app.save()
        self.assertEqual(app.current_count_of_participants, number + 3)
        app.add_participant(p3)
        app.save()
        self.assertEqual(app.current_count_of_participants, number + 3)
        new_app = Appointment.objects.all()[0]
        self.assertEqual(new_app.current_count_of_participants, 3)
        new_appointment = Appointment.objects.all()[0]
        self.assertEqual(new_appointment.current_count_of_participants, number + 3)
        app2 = Appointment.objects.all()[1]
        app2.add_participant(p1)
        app2.save()
        self.assertEqual(app2.current_count_of_participants, 1)
        app2.remove_participant(p1)
        app2.save()
        self.assertEqual(app2.current_count_of_participants, 0)
        self.assertEqual(app.current_count_of_participants, 3)


    def test_method_list_tutor_of_appointment(self):
        """
        test the list of tutors for an appointment
        when a tutor is inserted into an appointment, the length of the list must be increased
        :return:
        """
        app = Appointment.objects.all()[0]
        tutor = Tutor.objects.get(name_of_user='tutor1')
        tutorcheck = app.my_tutors.all()
        self.assertEqual(len(tutorcheck), 0)
        app.add_tutor(tutor)
        app.save()
        tutorcheck = app.my_tutors.all()
        self.assertEqual(len(tutorcheck), 1)

    def test_method_remove_participant(self):
        """
        test of remove_participant function
        :return:
        """
        '''
        appointment = Appointment.objects.all()[0]
        self.assertIsNotNone(appointment.my_participants)
        participant = Participant.objects.get(name_of_user='participant1')
        appointment.add_participant(participant)
        appointment.save()
        appointment.remove_participant(participant)
        appointment.save()
        self.assertEqual(appointment.current_count_of_participants, 0)
        new_appointment = Appointment.objects.all()[0]
        self.assertEqual(new_appointment.current_count_of_participants, 0)
        '''
        part1 = Participant.objects.get(name_of_user='participant1')
        part2 = Participant.objects.get(name_of_user='participant2')
        part3 = Participant.objects.get(name_of_user='participant3')
        appointment1 = Appointment.objects.all()[0]
        appointment2 = Appointment.objects.all()[2]
        appointment1.add_participant(part1)
        appointment2.add_participant(part1)
        appointment1.add_participant(part2)
        appointment2.add_participant(part2)
        appointment1.add_participant(part3)
        appointment2.add_participant(part3)

        appointment1.remove_participant(part1)

        self.assertNotIn(part1, appointment1.my_participants.all())
        self.assertIn(part1, appointment2.my_participants.all())



    def test_method_additional_information(self):
        """
        test of additional_information function
        :return:
        """
        appointment = Appointment.objects.all()[0]
        appointment.additional_information = 'new Description'
        self.assertEqual(appointment.additional_information, 'new Description')
