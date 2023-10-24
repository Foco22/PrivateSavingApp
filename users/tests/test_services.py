from users.models import User, Plan, Subscription
from django.contrib.auth.models import Group

from users import services as user_services
from django.test import TestCase


class UserHasGroupTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='test_group')
        self.user_in_group = User.objects.create_user(username='user_in_group', email='user_in_group@example.com', password='testpassword')
        self.user_not_in_group = User.objects.create_user(username='user_not_in_group', email='user_not_in_group@example.com', password='testpassword')
        self.group.user_set.add(self.user_in_group)

    def test_user_in_group(self):
        self.assertTrue(user_services.user_has_group(self.user_in_group.id, 'test_group'))

    def test_user_not_in_group(self):
        self.assertFalse(user_services.user_has_group(self.user_not_in_group.id, 'test_group'))


class UserServiceTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='test_group')
        self.user_1 = User.objects.create_user(username='user1', email='user1@example.com', password='testpassword')
        self.user_2 = User.objects.create_user(username='user2', email='user2@example.com', password='testpassword', is_active=False)
        self.group.user_set.add(self.user_1)

    def test_get_user_by_id(self):
        self.assertEqual(user_services.get_user_by_id(self.user_1.id), self.user_1)

    def test_get_enabled_user_by_id(self):
        self.user_1.is_active = True
        self.user_1.save()
        self.assertEqual(user_services.get_enabled_user_by_id(self.user_1.id), self.user_1)

    def test_get_users_by_group(self):
        users_in_group = user_services.get_users_by_group('test_group')
        self.assertIn(self.user_1, users_in_group)
        self.assertNotIn(self.user_2, users_in_group)


class UserGroupServiceTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup')
        self.group2 = Group.objects.create(name='testgroup2')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_add_user_to_group(self):
        with self.assertNumQueries(5):
            user_services.add_user_to_group(self.user.id, self.group.name)
        self.assertTrue(user_services.user_has_group(self.user.id, self.group.name))

    def test_add_user_to_groups_by_user_id_and_group_ids(self):
        user_services.add_user_to_groups_by_user_id_and_group_ids(self.user.id, [self.group.id, self.group2.id])
        self.assertTrue(user_services.user_has_group(self.user.id, self.group.name))
        self.assertTrue(user_services.user_has_group(self.user.id, self.group2.name))

    def test_remove_user_from_group(self):
        user_services.add_user_to_group(self.user.id, self.group.name)
        self.assertTrue(user_services.user_has_group(self.user.id, self.group.name))
        user_services.remove_user_from_group(self.user.id, self.group.name)
        self.assertFalse(user_services.user_has_group(self.user.id, self.group.name))

    def test_get_users_by_ids(self):
        user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')
        users = user_services.get_users_by_ids([self.user.id, user2.id])
        self.assertEqual(len(users), 2)
