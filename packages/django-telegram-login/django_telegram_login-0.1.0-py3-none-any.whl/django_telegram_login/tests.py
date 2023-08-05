"""
Tests.
"""
# flake8: noqa
# pylint: disable-all
import unittest

from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.widgets.constants import (
    SMALL,
    MEDIUM,
    LARGE,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)


class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.bot_token = '459236585:AAEee0Ba4fRijf1BRNbBO9W-Ar15F2xgV98'

        self.request_data = {
            'id': '299661134',
            'first_name': 'Dmytro',
            'last_name': 'Striletskyi',
            'username': 'dmytrostriletskyi',
            'photo_url': 'https://t.me/i/userpic/320/dmytrostriletskyi.jpg',
            'auth_date': '1518392724',
            'hash': '92ee8156a1482919843bfbaed2a91839f6594b2b98d884046c48ff58fa3a5ace'
        }

    def test_ok_data(self):
        """
        Received data is correct.
        """
        expected = self.request_data.copy()
        expected.pop('hash', None)

        result = verify_telegram_authentication(self.bot_token, self.request_data)
        self.assertEqual(expected, result)

    def test_wrong_token(self):
        """
        Wrong token.
        """
        request_data = self.request_data.copy()
        request_data['hash'] = '92ee8156a1482919843bfbaed2a91839f6594b2b98d884046c48ff58fa3a13c29'

        with self.assertRaises(NotTelegramDataError):
            verify_telegram_authentication(self.bot_token, request_data)

    def test_outdatet_data(self):
        """
        Outdated data.
        """
        request_data = self.request_data.copy()
        request_data['auth_date'] = '10'

        with self.assertRaises(TelegramDataIsOutdatedError):
            verify_telegram_authentication(self.bot_token, request_data)


class TestWidgetGenerator(unittest.TestCase):

    def setUp(self):

        self.bot_name = 'test_bot'
        self.redirect_url = 'https://django-telegram-login.com'

        self.expected_callback_small = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="small" data-onauth="onTelegramAuth(user)" data-request-access="write"></script>"""
        self.expected_callback_medium = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="medium" data-onauth="onTelegramAuth(user)" data-request-access="write"></script>"""
        self.expected_callback_large = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="large" data-onauth="onTelegramAuth(user)" data-request-access="write"></script>"""
        self.expected_callback_no_photo = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="small" data-userpic="false" data-onauth="onTelegramAuth(user)" data-request-access="write"></script>"""

        self.expected_redirect_small = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="small" data-auth-url="https://django-telegram-login.com" data-request-access="write"></script>"""
        self.expected_redirect_medium = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="medium" data-auth-url="https://django-telegram-login.com" data-request-access="write"></script>"""
        self.expected_redirect_large = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="large" data-auth-url="https://django-telegram-login.com" data-request-access="write"></script>"""
        self.expected_redirect_no_photo = """<script async src="https://telegram.org/js/telegram-widget.js?2" data-telegram-login="test_bot" data-size="small" data-userpic="false" data-auth-url="https://django-telegram-login.com" data-request-access="write"></script>"""

    def test_create_callback_small(self):
        result = create_callback_login_widget(self.bot_name, size=SMALL)
        self.assertEqual(self.expected_callback_small, result)

    def test_create_callback_medium(self):
        result = create_callback_login_widget(self.bot_name, size=MEDIUM)
        self.assertEqual(self.expected_callback_medium, result)

    def test_create_callback_large(self):
        result = create_callback_login_widget(self.bot_name, size=LARGE)
        self.assertEqual(self.expected_callback_large, result)

    def test_create_callback_no_photo(self):
        result = create_callback_login_widget(self.bot_name, user_photo=DISABLE_USER_PHOTO)
        self.assertEqual(self.expected_callback_no_photo, result)

    def test_create_redirect_small(self):
        result = create_redirect_login_widget(self.redirect_url, self.bot_name, size=SMALL)
        self.assertEqual(self.expected_redirect_small, result)

    def test_create_redirect_medium(self):
        result = create_redirect_login_widget(self.redirect_url, self.bot_name, size=MEDIUM)
        self.assertEqual(self.expected_redirect_medium, result)

    def test_create_redirect_large(self):
        result = create_redirect_login_widget(self.redirect_url, self.bot_name, size=LARGE)
        self.assertEqual(self.expected_redirect_large, result)

    def test_create_redirect_no_photo(self):
        result = create_redirect_login_widget(self.redirect_url, self.bot_name, user_photo=DISABLE_USER_PHOTO)
        self.assertEqual(self.expected_redirect_no_photo, result)


if __name__ == '__main__':
    unittest.main()
