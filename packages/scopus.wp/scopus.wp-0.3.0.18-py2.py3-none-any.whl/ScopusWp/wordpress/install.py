from jutil.installation import SetupController, FileSetupController, installation_database_singleton

from ScopusWp.config import PATH, Config

import pathlib
import os


class WordpressSetup(SetupController):

    def __init__(self, project_path):
        SetupController.__init__(self)

        self.path = pathlib.Path(project_path) / 'wordpress'

        self.config_setup = FileSetupController(
            str(self.path),
            'config.ini',
            os.path.join(PATH, 'wordpress', 'templates', 'config.ini'),
            url='',
            username='',
            password=''
        )

    def run(self):
        self.setup_files()
        self.setup_database()

    def setup_database(self):
        print('\n[WORDPRESS DATABASE SETUP]')
        try:
            class Db(installation_database_singleton(
                Config.get_instance()['MYSQL']['username'],
                Config.get_instance()['MYSQL']['password'],
                Config.get_instance()['MYSQL']['host']
            )):
                pass

            from ScopusWp.wordpress.reference import WordpressMySQLDatabase, BASE

            # Creating the database
            Db.create_database('__wordpress')
            print('"__wordpress" DATABASE CREATED')
            # Creating all the tables according to the models
            session = WordpressMySQLDatabase.get_session()
            WordpressMySQLDatabase.create_database(BASE)
            print('WORDPRESS DATABASE TABLES CREATED')

        except Exception as e:
            print('FAILED TO INSTALL SCOPUS DATA BASE DUE TO EXCEPTION: "{}"'.format(str(e).strip('\n')))

    def setup_files(self):
        print('\n[WORDPRESS FILE SETUP]')
        self.create_folder()

        self.config_setup.run()

    def create_folder(self):
        if not self.path.exists():
            self.path.mkdir()
            print('CREATED WORDPRESS FOLDER IN PROJECT FOLDER')
