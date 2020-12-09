from django.test import TestCase
from .views import register_view, login_view, logout_view
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import User

class UserRegisterTest(TestCase):

    def setUp(self) -> None:
        # SetUp group of information FIRST
        self.test_username_first = 'first_test_user'
        self.test_email_first = 'first_test_userer@testEmail.com'
        self.test_password_first = '123testpasswordtest123' 
        self.test_password_conf_first = '123testpasswordtest123'

        # SetUp group of information SECOND
        self.test_username_second = 'second_test_user'
        self.test_email_second = 'second_test_user@testGmail.com'
        self.test_password_second = '123testpasswordtest123' 
        self.test_password_conf_second = '123testpasswordtest123'

    def test_register_process(self):
        # Create First User
        self.first_test_user = User()
        self.first_test_user.username = self.test_username_first
        self.first_test_user.email = self.test_email_first
        self.first_test_user.password = self.test_password_first
        self.first_test_user.save()

        # Create Second User
        self.second_test_user = User()
        self.second_test_user.username = self.test_username_second
        self.second_test_user.email = self.test_email_second
        self.second_test_user.password = self.test_password_second
        self.second_test_user.save()

        # Now check if user saved successfully
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)
        first_user_saved = saved_users[0]
        second_user_saved = saved_users[1]
        self.assertEqual(first_user_saved.username, 'first_test_user')
        self.assertEqual(second_user_saved.username, 'second_test_user')

    def test_register_view_func_and_url_resolve(self):
        url_found = resolve('/register')
        self.assertEqual(url_found.func, register_view)

    def test_register_page_return_correct_html(self):
        request = HttpRequest()
        response = register_view(request)
        html = response.content.decode('utf8').strip() # User .strip() to remove extra white spaces from .html doc
        self.assertIn('<html>', html)
        self.assertIn('<title>Register Page</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_register_template(self):
        response = self.client.get('/register')
        self.assertTemplateUsed(response, 'register.html')
        self.assertTemplateNotUsed(response, 'login.html')
        self.assertTemplateNotUsed(response, 'dashboard.html')

    def test_post_save_on_form(self):
        response = self.client.post('/register', data={
            'username': self.test_username_first,
            'email': self.test_email_first,
            'password': self.test_password_first,
            'conf_password': self.test_password_conf_first
        })

class UserLoginTest(TestCase):
    def setUp(self):
    # SetUp group of information FIRST
        self.test_username_first = 'first_test_user'
        self.test_email_first = 'first_test_userer@testEmail.com'
        self.test_password_first = '123testpasswordtest123' 
        self.test_password_conf_first = '123testpasswordtest123'

    def test_login_view_func_and_url_resolve(self):
        url_found = resolve('/login')
        self.assertEqual(url_found.func, login_view)

    def test_login_page_return_correct_html(self):
        request = HttpRequest()
        response = login_view(request)
        html = response.content.decode('utf8').strip() # User .strip() to remove extra white spaces from .html doc
        self.assertIn('<html>', html)
        self.assertIn('<title>Login Page</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_login_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'login.html')
        self.assertTemplateNotUsed(response, 'register.html')
        self.assertTemplateNotUsed(response, 'dashboard.html')

    def test_post_save_on_form(self):
        response = self.client.post('/login', data={
            'username': self.test_username_first,
            'password': self.test_password_first,
        })
