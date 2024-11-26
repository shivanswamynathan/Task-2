from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from base.models import Task

#Test User Login
class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        
        self.assertEqual(response.status_code, 302)

        
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.username)  # Verify username is displayed on the redirected page


#Test Task Creation - This test will check that a logged-in user can create a task.
class TaskCreationTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_task_creation(self):
        # Log in the test user
        self.client.login(username=self.username, password=self.password)

        # Define task data
        task_data = {
            'title': 'New Test Task',
            'description': 'This is a test task created by the user.'
        }

        # Send a POST request to create the task
        response = self.client.post(reverse('task-create'), task_data)

        # Check for redirect after task creation (302)
        self.assertEqual(response.status_code, 302)

        # Verify the task exists in the database
        task = Task.objects.get(title='New Test Task')
        self.assertEqual(task.description, 'This is a test task created by the user.')
        self.assertEqual(task.user, self.user)  # Ensure the task is associated with the logged-in user


#Test Task Deletion - This test will check that an authenticated user can delete a task.
class TaskDeletionTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Create a test task for deletion
        self.task = Task.objects.create(
            title='Task to Delete',
            description='This task will be deleted.',
            user=self.user
        )

    def test_task_deletion(self):
        # Log in the test user
        self.client.login(username=self.username, password=self.password)

        # Send a POST request to delete the task
        response = self.client.post(reverse('task-delete', args=[self.task.id]))

        # Check for redirect after task deletion (302)
        self.assertEqual(response.status_code, 302)

        # Verify that the task no longer exists in the database
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)


