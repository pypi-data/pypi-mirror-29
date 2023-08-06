from jutil.installation import SetupController, FileSetupController, installation_database_singleton

from ScopusWp.config import PATH, Config

from ScopusWp.scopus.persistency import ScopusMySQLDatabase, BASE

import pathlib
import os


class Db(installation_database_singleton(
    Config.get_instance()['MYSQL']['username'],
    Config.get_instance()['MYSQL']['password'],
    Config.get_instance()['MYSQL']['host']
)):
    pass


class ScopusSetup(SetupController):

    def __init__(self, project_path):
        self.path = pathlib.Path(project_path) / 'scopus'

        self.authors_setup = FileSetupController(
            str(self.path),
            'authors.ini',
            os.path.join(PATH, 'scopus', 'templates', 'authors.ini'),
            shorthand='SHORTHAND',
            ids=[],
            first_name='',
            last_name='',
            keywords=[],
            whitelist=[],
            blacklist=[]
        )

    def run(self):
        self.setup_files()
        self.setup_database()

    def create_folder(self):
        if not self.path.exists():
            self.path.mkdir()
            print('CREATED SCOPUS FOLDER IN PROJECT FOLDER')

    def setup_files(self):
        print('[SCOPUS FILE SETUP]')
        self.create_folder()

        self.authors_setup.run()

    def setup_database(self):
        print('[SCOPUS DATABASE SETUP]')
        try:
            # Creating the database
            Db.create_database('__scopus')
            print('"__scopus" DATABASE CREATED')
            # Creating all the tables according to the models
            session = ScopusMySQLDatabase.get_session()
            ScopusMySQLDatabase.create_database(BASE)
            print('SCOPUS DATABASE TABLES CREATED')

        except Exception as e:
            print('FAILED TO INSTALL SCOPUS DATA BASE DUE TO EXCEPTION: "{}"'.format(str(e).strip('\n')))

