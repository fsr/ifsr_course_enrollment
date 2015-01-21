from django.test import TestCase
from course_manager.models.Users.User import UserAccount
from django.db.utils import IntegrityError


class UserAccountTest(TestCase):
    """
    test of UserAccount class
    """
    def setUp(self):
        """
        create a user object
        :return:
        """
        for u in UserAccount.objects.all():
            u.delete()
        UserAccount.objects.create_user(name_of_user='user1', email='user1@tu-dresden.de', s_number='s00000001',
                                        username='user1')

    def test_base_user(self):
        """
        get user with username from database and compare this user object with email and s_number
        :return:
            ***
        """
        user1 = UserAccount.objects.get(username='user1')
        self.assertEqual(user1.email, 'user1@tu-dresden.de')
        self.assertEqual(user1.s_number, 's00000001')

    def test_method_check_email_address(self):
        """
        create several users with wrong email, an exception must be raised.
        :return:
        """
        self.assertRaisesMessage(UserAccount.objects.create(name_of_user='user3', email='abc', username='user3',
                                                            s_number='s00000003'),
                                 'wrong email address')
        self.assertRaisesMessage(UserAccount.objects.create(name_of_user='user4', email='abc@', username='user4',
                                                            s_number='s00000004'),
                                 'wrong email address')
        self.assertRaisesMessage(UserAccount.objects.create(name_of_user='user5', email='abc@def', username='user5',
                                                            s_number='s00000005'),
                                 'wrong email address')
        self.assertRaisesMessage(UserAccount.objects.create(name_of_user='user6', email='@def.com', username='user6',
                                                            s_number='s00000006'),
                                 'wrong email address')

    def test_exception_existing_user_names(self):
        """
        create an existing user, an exception must be raised.
        :return:
        """
        with self.assertRaises(IntegrityError):
            UserAccount.objects.create_user(name_of_user='user1', email='user1@tu-dresden.de',
                                            username='user1', s_number='s00000001')
