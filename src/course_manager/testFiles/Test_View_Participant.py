from django.test import Client
from django.test import TestCase

from course_manager.models.Users.Participant import Participant
from course_manager.models.Management import Management
from course_manager.models.Course import Course
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.Appointment import Appointment


class ViewParticipantsTest(TestCase):
    """
    test of the participant view
    """
    def setUp(self):
        self.client = Client()

    def test_index(self):
        """
        test that page call returns a status code 200 at /kurse/home/
        :return:
        """
        response = self.client.get('/kurse/home/')
        self.assertEqual(response.status_code, 200, 'test_urls_01')

    def test_show_enroll(self):
        """
        test of show_enroll function
        when appointment doesn't exist, the request must be to redirected to the homepage
        when the appointment exists, the web page can be loaded
        :return:
        """
        response = self.client.get('/kurse/1/signinapp/')
        self.assertEqual(response.status_code, 302, 'test_show_enroll_01')

        if not(Management.objects.all()):
            m = Management(None)
            m.save()
        if not (CourseManagement.objects.all()):
            cm = CourseManagement(my_management=Management.objects.all()[0])
            cm.save()
        cpp = Course.objects.create(name='c++',
                                    my_course_management=CourseManagement.objects.all()[0])
        cpp.save()
        Appointment.objects.create(lesson='2.DS', additional_information='test', current_count_of_participants=0,
                                   my_course=cpp, weekday='Sunday', location='location')
        Appointment.objects.create(additional_information='test', current_count_of_participants=0, my_course=cpp,
                                   location='location')

        response = self.client.get('/kurse/1/signinapp/')
        self.assertEqual(response.status_code, 200, 'test_show_enroll_02')

    def test_proc_enroll(self):
        """
        test of proc_enroll functions
        a participant enrolls to a appointment and the count of participants must be increased
        the existing participant enrolls again, the count doesn't increase
        :return:
        """
        if not(Management.objects.all()):
            m = Management(None)
            m.save()
        if not (CourseManagement.objects.all()):
            cm = CourseManagement(my_management=Management.objects.all()[0])
            cm.save()
        cpp = Course.objects.create(name='c++',
                                    my_course_management=CourseManagement.objects.all()[0])
        cpp.save()
        Appointment.objects.create(lesson='2.DS', additional_information='test', current_count_of_participants=0,
                                   my_course=cpp, weekday='Sunday', location='location')
        Appointment.objects.create(additional_information='test', current_count_of_participants=0, my_course=cpp,
                                   location='location')

        response = self.client.get('/kurse/1/signinappdone/')
        self.assertEqual(response.status_code, 302, 'test_proc_enroll_01')

        participants = Participant.objects.all()
        self.assertEqual(len(participants), 0, 'test_proc_enroll_02')

        response = self.client.post('/kurse/1/signinappdone/', {'snumber': 's40006'})
        self.assertEqual(response.status_code, 302, 'test_proc_enroll_03')

        participants = Participant.objects.all()
        self.assertNotEqual(len(participants), 1, 'test_proc_enroll_04')

        response = self.client.post('/kurse/1/signinappdone/', {'snumber': 's40006'})
        self.assertEqual(response.status_code, 302, 'test_proc_enroll_05')

        participants = Participant.objects.all()
        self.assertNotEqual(len(participants), 1, 'test_proc_enroll_06')

        response = self.client.post('/kurse/1/signinappdone/', {'snumber': 's40007'})
        self.assertEqual(response.status_code, 302, 'test_proc_enroll_07')

        participants = Participant.objects.all()
        self.assertNotEqual(len(participants), 2, 'test_proc_enroll_08')



