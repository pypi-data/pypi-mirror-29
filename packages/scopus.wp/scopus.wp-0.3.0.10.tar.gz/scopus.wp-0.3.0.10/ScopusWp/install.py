import importlib
import threading
import configparser
import pathlib
import pickle
import os
import MySQLdb

from jutil.installation import FileSetupController, SetupController, installation_database_singleton
from ScopusWp.config import TEMPLATE_PATH, Config, PATH

from ScopusWp.register import *


class ProjectPathInputController:

    def __init__(self):
        self._path = None

    @property
    def path(self):
        self.run()
        return self._path

    def run(self):
        if not self.check_config():
            self.prompt_path()

    def prompt_path(self):
        while True:
            inp = input('\nENTER PROJECT PATH: ')
            try:
                path = pathlib.Path(inp)
                if path.exists() and path.is_dir():
                    self._path = str(path)
                    break
                else:
                    print('INVALID PATH, TRY AGAIN')
                    continue
            except:
                print('INVALID INPUT, TRY AGAIN')
                continue

    def check_config(self):
        import ScopusWp.config as _config
        # In case the project path value is not empty, it is save to assume it has been set already and the path is
        # still valid
        if _config.PROJECT_PATH == '':
            print('NO PATH HAS BEEN SET')
            return False

        # Asking the user if he wants to keep that path or change it
        print('CURRENT PATH:\n{}'.format(_config.PROJECT_PATH))
        inp = input('\nDo you want to keep that path? Type "N" to change...')
        if inp.lower() == 'n' or inp.lower() == 'no':
            return False
        else:
            self._path = _config.PROJECT_PATH
            return True


class Db(installation_database_singleton(
    Config.get_instance()['MYSQL']['username'],
    Config.get_instance()['MYSQL']['password'],
    Config.get_instance()['MYSQL']['host']
)):
    pass


def write_project_path(project_path):
    # Reading the config.py file of the package
    with open(os.path.join(PATH, 'config.py')) as file:
        lines = file.readlines()

    # Changing the line with the project path
    count = 0
    for i in range(len(lines)):
        line = lines[i]
        if 'PROJECT_PATH' in line:
            break
        count += 1

    lines[count] = 'PROJECT_PATH = "{}"'.format(project_path)
    # writing the new lines into the file
    with open(os.path.join(PATH, 'config.py'), mode='w+') as file:
        file.write('\n'.join(lines))


class PubControlSetup(SetupController):

    def __init__(self, project_path):
        # Getting the path of the whole thing
        self.path = project_path

        # The file setup for the config ini
        self.config_setup = FileSetupController(
            self.path,
            'config.ini',
            os.path.join(TEMPLATE_PATH, 'config.ini'),
            mysql_host='',
            mysql_username='',
            mysql_password='',
            mysql_database=''
        )

    def run(self):
        self.info()
        self.setup_files()
        self.setup_database()

    def setup_files(self):
        print('\n[PUBCONTROL FILE SETUP]')
        self.config_setup.run()

    def setup_database(self):
        print('\n[PUBCONTROL DATABASE SETUP]')
        try:
            from ScopusWp.database import MySQLDatabase, BASE
            # Creating the database
            Db.create_database('__pubcontrol')
            print('"__pubcontrol" DATABASE CREATED')
            # Creating all the tables according to the models
            session = MySQLDatabase.get_session()
            MySQLDatabase.create_database(BASE)
            print('PUBCONTROL DATABASE TABLES CREATED')

        except Exception as e:
            print('FAILED TO INSTALL SCOPUS DATA BASE DUE TO EXCEPTION: "{}"'.format(str(e).strip('\n')))

    @staticmethod
    def info():
        import ScopusWp.config as _config
        import os

        print('\nCURRENT VERSION:\n{}'.format(_config.VERSION))
        print('\nRUNNING IN FOLDER:\n{}'.format(_config.PATH))
        print('\nPACKAGE CONTENT:\n{}'.format(os.listdir(_config.PATH)))


def main():
    from ScopusWp.wordpress.install import WordpressSetup
    from ScopusWp.scopus.install import ScopusSetup

    project_path = ProjectPathInputController().path
    write_project_path(project_path)

    PubControlSetup(project_path).run()
    ScopusSetup(project_path).run()
    WordpressSetup(project_path).run()

