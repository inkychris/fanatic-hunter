from robobrowser import RoboBrowser
from settingsparser import Settings
import logging, os


class SiteAccessor:
    def __init__(self, settings_file):
        self.logger = logging.getLogger(__name__)
        self.session = RoboBrowser(parser='html.parser')
        self._settings = Settings(yaml_file=settings_file)
        self._count_store = 'count.store'

    @property
    def count(self):
        if not os.path.isfile(self._count_store):
            self.count = 0
            return 0

        with open(self._count_store, 'r') as count:
            return int(count.read())

    @count.setter
    def count(self, val):
        with open(self._count_store, 'w') as count:
            count.write(str(val))

    def login(self):
        self.logger.info('Logging in')
        try:
            self.logger.debug('Navigating to login page')
            self.session.open('https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f')
        except Exception:
            self.logger.exception('Failed to navigate to login page')
            return False

        try:
            self.logger.debug('Retrieving login form')
            login_form = self.session.get_form('login-form')
            login_form['email'] = self._settings.email
            login_form['password'] = self._settings.password
        except Exception:
            self.logger.exception('Failed to retrieve login form from login page')
            return False

        try:
            self.logger.debug('Submitting login form')
            self.session.submit_form(login_form)
        except Exception:
            self.logger.exception('Failed to submit login form')

        if not self.session.find('div', title=self._settings.username):
            self.logger.error('Login attempt failed after submitting login form (likely due to recaptcha)')
            return False
        self.logger.debug('Login successful')
        return True

    def logout(self):
        self.logger.info('Logging out')
        try:
            self.logger.debug('Navigating to logout page')
            self.session.open('https://stackoverflow.com/users/logout')
        except Exception:
            self.logger.exception('Failed to navigate to logout page')
            return False

        try:
            self.logger.debug('Retrieving logout form')
            logout_form = self.session.get_form(action='/users/logout')
        except Exception:
            self.logger.exception('Failed to retrieve logout form')
            return False

        try:
            self.logger.debug('Submitting logout form')
            self.session.submit_form(logout_form)
        except Exception:
            self.logger.exception('Failed to submit logout form')
            return False

        self.logger.info('Log out successful')
        return True

    def retrieve_badge_value_count(self):
        self.logger.info('Retrieving badge value count')
        try:
            self.logger.debug('Navigating to user profile')
            self.session.open(self._settings.profile)
        except Exception:
            self.logger.exception('Failed to navigate to user profile')
            return 0

        try:
            current_count = int(self.session.find("span", class_="grid--cell ml-auto fs-caption").get_text().split('/')[0])
            self.logger.info('"Fanatic" count value: {}'.format(current_count))
        except Exception:
            self.logger.exception('Could not find badge count value in response')
            return 0

        self.logger.info('Retrieve badge value successful')
        return current_count

    def check_badge_status(self):
        self.logger.info('Checking badge value status')
        try:
            self.logger.debug('Retrieving badge count')
            current_badge_value = self.retrieve_badge_value_count()
        except Exception:
            self.logger.exception('Failed to retrieve badge count')
            return 0

        try:
            self.logger.debug('Checking badge value is not less than previous retrieved value')
            if current_badge_value < self.count:
                self.logger.warning('"Fanatic" count value retrieved ({}) is less than previous value ({})'.format(
                    current_badge_value, self.count))
                return 0
        except Exception:
            self.logger.exception('Failed to check badge value')

        self.logger.info('Badge value status ok')
        self.count = current_badge_value
