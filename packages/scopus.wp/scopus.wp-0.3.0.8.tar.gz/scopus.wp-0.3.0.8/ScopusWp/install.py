import importlib
import threading
import configparser
import pathlib
import pickle
import os
import MySQLdb

from jutil.installation import FileSetupController, SetupController, installation_database_singleton
from ScopusWp.config import TEMPLATE_PATH, Config

from ScopusWp.database import MySQLDatabase, BASE
from ScopusWp.register import *

# THE TEMPLATES FOR THE NON CODE FILES

CONFIG_INI_TEMPLATE = (
    '[SCOPUS]\n'
    '; YOUR SCOPUS API KEY'
    'api-key = \n'
    'url = https://api.elsevier.com/content\n'
    '\n'
    '[KITOPEN]\n'
    'url = https://publikationen.bibliothek.kit.edu/publikationslisten\n'
    '\n'
    '[WORDPRESS]\n'
    '; THE URL TO YOUR WORDPRESS "xmlrpc.php"\n'
    'url = \n'
    '; YOUR WP USER\n'
    'username = \n'
    '; YOUR WP PASSWORD\n'
    'password = \n'
    '; AMOUNT OF DAYS BETWEEN UPDATE\n'
    'update_expiration = \n'
    '\n'
    '[MYSQL]\n'
    'host = localhost\n'
    'database = \n'
    'username = \n'
    'password = \n'
    '\n'
    '[LOGGING]\n'
    'folder = logs\n'
    'debug_log_name = log\n'
    'activity_log_name = log\n'
)

AUTHORS_INI_TEMPLATE = (
    '[SHORTHAND]\n'
    '; LIST OF SCOPUS IDS ASSOCIATED WITH AUTHOR\n'
    'ids = []\n'
    ''
    'first_name = \n'
    'last_name = \n'
    '; WORDPRESS CATEGORIES TO ASSOCIATE AUTHOR PUBLICATIONS WITH\n'
    'keywords = [] \n'
    '; SCOPUS AFFILIATION IDS TO ACCEPT\n'
    'scopus_whitelist = [] \n'
    '; SCOPUS AFFILIATION IDS TO IGNORE\n'
    'scopus_blacklist = [] \n'
    '\n'
    '; You can add more authors by appending sections like the template above\n'
)

ID_JSON_TEMPLATE = (
    '{\n'
    '"counter": 0,\n'
    '"used": [],\n'
    '"unused": []\n'
    '}\n'
)

# THE SQL SCRIPTS NEEDED FOR THE SETUP

REFERENCE_SQL = (
    'CREATE TABLE reference '
    '('
    'id BIGINT PRIMARY KEY,'
    'wordpress_id BIGINT,'
    'scopus_id BIGINT,'
    'comments_updated_datetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') ENGINE INNODB;'
    'CREATE UNIQUE INDEX reference_id_uindex ON reference (id);'
    'COMMIT;'
)

CITATION_REFERENCE_SQL = (
    'CREATE TABLE comment_reference'
    '('
    'internal_id BIGINT PRIMARY KEY,'
    'wordpress_post_id BIGINT,'
    'wordpress_comment_id BIGINT,'
    'scopus_id BIGINT'
    ') ENGINE INNODB;'
    'CREATE UNIQUE INDEX comment_reference_inernal_id_uindex ON comment_reference (internal_id);'
    'COMMIT;'
)

AUTHOR_SQL = (
    'CREATE TABLE author ('
    'id BIGINT PRIMARY KEY NOT NULL,'
    'first_name VARCHAR(100),'
    'last_name VARCHAR(100),'
    'h_index INT,'
    'citation_count INT,'
    'publications TEXT,'
    'document_count INT,'
    'affiliation_country VARCHAR(100),'
    'affiliation_city VARCHAR(100),'
    'affiliation_name VARCHAR(300)'
    ') ENGINE INNODB;'
    'COMMIT;'
)

AUTHOR_SNAPSHOT_SQL = (
    'CREATE TABLE author_snapshot ('
    'id BIGINT PRIMARY KEY AUTO_INCREMENT,'
    'author_id BIGINT,'
    'first_name VARCHAR(100),'
    'last_name VARCHAR(100),'
    'affiliations TEXT,'
    'type VARCHAR(100)'
    ') ENGINE INNODB;'
    'COMMIT;'
)

PUBLICATION_SQL = (
    'CREATE TABLE publication ('
    'id BIGINT PRIMARY KEY NOT NULL,'
    'eid VARCHAR(100),'
    'doi VARCHAR(100),'
    'creator_id BIGINT,'
    'title TEXT,'
    'description TEXT,'
    'journal VARCHAR(500),'
    'volume VARCHAR(100),'
    '`date` DATETIME,'
    'author_ids TEXT,'
    'keywords TEXT,'
    'citations TEXT'
    ') ENGINE INNODB;'
    'COMMIT;'
)

PUBLICATION_REFERENCE_SQL = (
    'CREATE TABLE publication_reference ('
    'id BIGINT PRIMARY KEY,'
    'wordpress_id BIGINT,'
    'scopus_id BIGINT,'
    'update_datetime DATETIME,'
    'post_datetime DATETIME'
    ') ENGINE INNODB;'
    'COMMIT;'
)

COMMENT_REFERENCE_SQL = (
    'CREATE TABLE comment_reference ('
    'id BIGINT PRIMARY KEY,'
    'wordpress_post_id BIGINT,'
    'wordpress_comment_id BIGINT,'
    'external_id BIGINT,'
    'type INT,'
    'posted_datetime DATETIME'
    ') ENGINE INNODB;'
    'COMMIT;'
)

REFERENCE_TYPE_SQL = (
    'CREATE TABLE reference_type ('
    'id INT PRIMARY KEY,'
    'name VARCHAR(200)'
    ') ENGINE INNODB;'
    'COMMIT;'
)

# THE SQL SETUP FOR THE

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


class FolderSetupController:

    def __init__(self, project_path):
        self.path = project_path

        self.logs_path = pathlib.Path(self.path) / 'logs'
        self.temp_path = pathlib.Path(self.path) / 'temp'

    def run(self):
        if not self.logs_exists():
            self.create_logs_folder()
            print('CREATED LOGS FOLDER')
        else:
            print('LOGS FOLDER ALREADY EXISTS')

        if not self.temp_exists():
            self.create_temp_folder()
            print('CREATED TEMP FOLDER')
        else:
            print('TEMP FOLDER ALREADY EXISTS')

    def create_logs_folder(self):
        self.logs_path.mkdir()

    def create_temp_folder(self):
        self.temp_path.mkdir()

    def logs_exists(self):
        return self.logs_path.exists() and self.logs_path.is_dir()

    def temp_exists(self):
        return self.temp_path.exists() and self.temp_path.is_dir()


class ConfigSetupController:

    def __init__(self, project_path):
        self.project_path = project_path

        self.path = pathlib.Path(self.project_path) / 'config.ini'

    def run(self):
        if not self.exists():
            self.create()
            print('CREATED CONFIG.INI')
        else:
            print('CONFIG FILE ALREADY EXISTS. KEEPING THE EXISTING FILE')

    def create(self):
        with self.path.open(mode='w+') as file:
            file.write(CONFIG_INI_TEMPLATE)
            file.flush()

    def exists(self):
        return self.path.exists() and self.path.is_file()


class IdsJsonSetupController:

    def __init__(self, project_path):
        self.project_path = project_path

        self.path = pathlib.Path(self.project_path) / 'ids.json'

    def run(self):
        if not self.exists():
            self.create()
            print('CREATED IDS.JSON')
        else:
            print('IDS.JSON ALREADY EXISTS. KEEPING THE EXISTING FILE')

    def create(self):
        with self.path.open(mode='w+') as file:
            file.write(ID_JSON_TEMPLATE)
            file.flush()

    def exists(self):
        return self.path.exists() and self.path.is_file()


class ObservedAuthorsSetupController:

    def __init__(self, project_path):
        self.project_path = project_path

        self.path = pathlib.Path(self.project_path) / 'authors.ini'

    def run(self):
        if not self.exists():
            self.create()
            print('CREATED AUTHORS.INI')
        else:
            print('AUTHORS.INI EXISTS. KEEPING THE EXISTING FILE')

    def exists(self):
        return self.path.exists() and self.path.is_file()

    def create(self):
        with self.path.open(mode='w+') as file:
            file.write(AUTHORS_INI_TEMPLATE)


class Db(installation_database_singleton(
    Config.get_instance()['MYSQL']['username'],
    Config.get_instance()['MYSQL']['password'],
    Config.get_instance()['MYSQL']['host']
)):
    pass


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

    PubControlSetup(project_path).run()
    ScopusSetup(project_path).run()
    WordpressSetup(project_path).run()

