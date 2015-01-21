from django.test import TestCase
from course_manager.models.Users.Executive import Executive


class ExecutiveTest(TestCase):
    """
    test of Executive class
    """
    def setUp(self):
        """
        create two different executive objects.
        :return:
        """
        for e in Executive.objects.all():
            e.delete()
        Executive.objects.create_user(name_of_user='executive1', email='executive1@tu-dresden.de',
                                      s_number='s1000001', username='executive1')
        Executive.objects.create_user(name_of_user='executive2', email='executive2@tu-dresden.de',
                                      s_number='s1000002', username='executive2')

    def test_base_executives(self):
        """
        test different ways to get the right executive object
        :return:
        """
        executive1 = Executive.objects.get(name_of_user='executive1')
        self.assertEqual(executive1.email, 'executive1@tu-dresden.de')
        self.assertEqual(executive1.s_number, 's1000001')
        executive2 = Executive.objects.get(name_of_user='executive2')
        self.assertIsNot(executive1, executive2)
        executive3 = Executive.objects.get(s_number='s1000002')
        executive4 = Executive.objects.get(email='executive2@tu-dresden.de')
        self.assertEqual(executive3, executive4)
