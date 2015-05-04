from django.test import TestCase
from course_manager.models.Course import Course
from course_manager.models.Management import Management
from course_manager.models.CourseManagement import CourseManagement
from course_manager.models.Appointment import Appointment


class CourseTest(TestCase):
    """
    test of Course class
    """

    def setUp(self):
        for c in Course.objects.all():
            c.delete()
        if not(Management.objects.all()):
            m = Management(None)
            m.save()
        if not(CourseManagement.objects.all()):
            cm = CourseManagement(my_management=Management.objects.all()[0])
            cm.save()
        Course.objects.create(name='c++', my_course_management=CourseManagement.objects.all()[0])

    def test_base_course(self):
        """
        test that you can get a course by name and a appointment by the course
        :return:
        """
        self.assertIsNotNone(Course.objects.get(name='c++'))
        course = Course.objects.get(name='c++')
        app = Appointment.objects.filter(my_course=course)
        self.assertEqual(len(app), 0)
        self.assertRaises(Course.DoesNotExist, Course.objects.get, name='c')