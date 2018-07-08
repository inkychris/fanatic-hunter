from siteaccessor import SiteAccessor
import argparse, logging.config, yaml, os, schedule, time

# Monkey-patching logging to scheduler
def schedule_logging_decorator(function):
    def logged_call(self):
        function(self)
        schedule.logger.info('Scheduled job %s', self)
    return logged_call

schedule.Job._schedule_next_run = schedule_logging_decorator(schedule.Job._schedule_next_run)

os.makedirs('log', exist_ok=True)

parser = argparse.ArgumentParser(
    description="Simple service to log in to stackoverflow every day to get the 'Fanatic' badge.")
parser.add_argument('auth_config', type=str, help='YAML file containing "username" and "password" fields')
args = parser.parse_args()

with open('logging_config.yml', 'r') as yml:
    logging.config.dictConfig(yaml.safe_load(yml))

def login():
    accessor = SiteAccessor('settings.yml')
    if accessor.login():
        accessor.check_badge_status()
        accessor.logout()

schedule.every().day.at("20:00").do(login)
while True:
    schedule.run_pending()
    time.sleep(1)
