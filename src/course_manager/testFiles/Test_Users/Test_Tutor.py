from django.test import TestCase
from course_manager.models.Users.Tutor import Tutor
from course_manager.models.Appointment import Appointment
from course_manager.models.Course import Course
from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from django.contrib.auth.models import Group


class TutorTest(TestCase):
    """
    test of Tutor class
    """
    app1 = None
    app2 = None

    def setUp(self):
        """
        create three Tutor objects in database
        :return:
        """
        global app1, app2
        for t in Tutor.objects.all():
            t.delete()
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
        gro = Group.objects.create(name='Tutors')
        gro.save()
        Appointment.objects.create(my_course=cpp, current_count_of_participants=0)
        Appointment.objects.create(my_course=cpp, current_count_of_participants=0)
        Tutor.objects.create_user(email='tutor1@tu-dresden.de',
                                  s_number='s3000001', name_of_user='tutor1')
        Tutor.objects.create_user(name_of_user='tutor2', email='tutor2@tu-dresden.de',
                                  s_number='s3000002')
        Tutor.objects.create_user(name_of_user='tutor3', email='tutor3@tu-dresden.de',
                                  s_number='s3000003')

    def test_base_tutor(self):
        """
        test that a tutor objects gets returned when called with  different attributes
        :return:
        """
        tutor1 = Tutor.objects.get(name_of_user='tutor1')
        self.assertEqual(tutor1.email, 'tutor1@tu-dresden.de')
        self.assertEqual(tutor1.s_number, 's3000001')
        tutor2 = Tutor.objects.get(email='tutor2@tu-dresden.de')
        self.assertEqual(tutor2.name_of_user, 'tutor2')
        self.assertEqual(tutor2.s_number, 's3000002')
        tutor3 = Tutor.objects.get(s_number='s3000003')
        self.assertEqual(tutor3.name_of_user, 'tutor3')
        self.assertEqual(tutor3.email, 'tutor3@tu-dresden.de')

    def test_method_create_tutor(self):
        """
        test of create_user function
        :return:
        """
        Tutor.objects.create_user(name_of_user='tutor4', s_number='s3000009',
                                  email='s3000009@mail.zih.tu-dresden.de')
        tutor = Tutor.objects.get(name_of_user='tutor4')
        self.assertIsNotNone(tutor)

    def test_method_delete_tutor(self):
        """
        test thst a tutor can be deleted by attribute name_of_user
        :return:
        """
        tutor = Tutor.objects.get(name_of_user='tutor1')
        tutor.delete()
        self.assertRaises(Tutor.DoesNotExist, Tutor.objects.get, name_of_user='tutor1')