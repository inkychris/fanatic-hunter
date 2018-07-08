from siteaccessor import SiteAccessor
import argparse, logging.config, yaml, os

os.makedirs('log', exist_ok=True)

parser = argparse.ArgumentParser(
    description="Simple service to log in to stackoverflow every day to get the 'Fanatic' badge.")
parser.add_argument('auth_config', type=str, help='YAML file containing "username" and "password" fields')
args = parser.parse_args()

with open('logging_config.yml', 'r') as yml:
    logging.config.dictConfig(yaml.safe_load(yml))

accessor = SiteAccessor('settings.yml')
if accessor.login():
    accessor.check_badge_status()
    accessor.logout()
