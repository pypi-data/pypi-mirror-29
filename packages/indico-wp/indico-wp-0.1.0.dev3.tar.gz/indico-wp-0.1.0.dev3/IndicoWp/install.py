from IndicoWp.config import PATH

import pathlib
import MySQLdb

# THE FILE TEMPLATES

CONFIG_INI_TEMPLATE = (
    '[INDICO]\n'
    'observe = indico.ini\n\n'
    '[WORDPRESS]\n'
    'url = # Insert url to your wordpress site xmlrpc.php file\n'
    'username = # The username to the wordpress site\n'
    'password = # The password to the wordpress site\n\n'
    '[LOGGING]\n'
    'folder = logs\n\n'
    '[MYSQL]\n'
    'host = localhost\n'
    'database = # The name of the mysql database to use\n'
    'username = # The username to your mysql database\n'
    'password = # The password for the mysql user\n'
)

INDICO_INI_TEMPLATE = (
    '[SHORT NAME OF THE SITE]\n'
    'url = # The url to the indico site\n'
    'key = # The API Key to be used to request the information from the site\n'
    'categories = ["1", "3"] # A list of all the category ids to be observed\n\n'
    '# Multiple Indico sites can be observed by adding more sections like the example above, one for each site to\n'
    '# be monitored. The short name/ section title has to be unique for each one and also a new API key has to be \n'
    '# acquired on each site.'
)

# THE SQL TEMPLATES

EVENT_TABLE_SQL = (
    'CREATE TABLE event ('
    'id INT(11) PRIMARY KEY NOT NULL,'
    'starting DATETIME,'
    'location VARCHAR(200),'
    'address VARCHAR(200),'
    'description TEXT,'
    'type VARCHAR(200),'
    'title VARCHAR(200),'
    'creator_id INT(11)'
    'CONSTRAINT event_ibfk_1 FOREIGN KEY (creator_id) REFERENCES creator (id)'
    ');'
    'ALTER TABLE event ENGINE=INNODB;'
    'COMMIT;'
)

CREATOR_TABLE_SQL = (
    'CREATE TABLE creator ('
    'id INT(11),'
    'first_name VARCHAR(100),'
    'last_name VARCHAR(100),'
    'affiliation VARCHAR(300)'
    ');'
    'ALTER TABLE creator ENGINE=INNODB;'
    'COMMIT;'
)

EVENT_REFERENCE_TABLE_SQL = (
    'CREATE TABLE event_reference ('
    'internal_id INT(11),'
    'indico_id INT(11),'
    'wordpress_id INT(11)'
    ');'
    'ALTER TABLE event_reference ENGINE=INNODB;'
    'COMMIT;'
)

# SUPPORT CLASSES


class Db:

    _instance = None

    @staticmethod
    def get_cursor():
        conn = Db.get_instance()  # type: MySQLdb.Connection
        cursor = conn.cursor()
        return cursor

    @staticmethod
    def get_instance():
        if Db._instance is None:
            Db.new_instance()

        return Db._instance

    @staticmethod
    def new_instance():

        # Attempting to import the config of the project
        from IndicoWp.config import Config

        try:
            config = Config.get_instance()
            # Getting the values from the config
            host = config['MYSQL']['host']
            database = config['MYSQL']['database']
            username = config['MYSQL']['username']
            password = config['MYSQL']['password']
            connector = MySQLdb.connect(
                host=host,
                db=database,
                user=username,
                passwd=password
            )
            Db._instance = connector
        except:
            pass


# ACTUAL

class SetupController:

    def __init__(self):
        self.path = None
        self.prompt_path()

        self.config_controller = ProjectConfigController(str(self.path))
        self.file_controller = FilesSetupController(str(self.path))
        self.database_controller = DatabaseSetupController()

    def setup_database(self):
        self.database_controller.run()

    def setup_files(self):
        self.file_controller.run()
        self.config_controller.run()

    def prompt_path(self):
        while True:
            path_string = input('Enter project path:  ')
            path = pathlib.Path(path_string)
            if path.exists() and path.is_dir():
                break
            else:
                print('The path was not valid, please try again')

        self.path = path


class ConfigSetupController:

    def __init__(self, project_path):
        self.project_path = pathlib.Path(project_path)
        self.path = self.project_path / 'config.ini'  # type: pathlib.Path

    def run(self):
        if not self.exists():
            self.create()

    def create(self):
        with self.path.open(mode='w+') as file:
            file.write(CONFIG_INI_TEMPLATE)
            file.flush()

    def exists(self):
        return self.path.exists()


class IndicoSetupController:

    def __init__(self, project_path):
        self.project_path = pathlib.Path(project_path)
        self.path = self.project_path / 'indico.ini'

    def run(self):
        if not self.exists():
            self.create()

    def create(self):
        with self.path.open(mode='w+') as file:
            file.write(INDICO_INI_TEMPLATE)
            file.flush()

    def exists(self):
        return self.path.exists()


class ProjectConfigController:

    def __init__(self, project_path):
        self.project_path_string = project_path
        # Getting the file path for the config file of the project
        import IndicoWp.config as cfg
        self.config_path = pathlib.Path(cfg.__file__)
        self.content = ''

    def run(self):
        self.read()
        self.replace()
        self.write()

    def write(self):
        with self.config_path.open(mode='w') as file:
            file.write(self.content)
            file.flush()

    def read(self):
        with self.config_path.open(mode='r') as file:
            self.content = file.read()

    def replace(self):
        print(self.content)
        lines = self.content.split('\n')
        index = 0
        for line in lines:
            if 'PROJECT_PATH_REPLACE_MARKER' in line:
                break
            index += 1
        lines[index] = 'PROJECT_PATH = "{}"'.format(self.project_path_string)
        self.content = '\n'.join(lines)
        print(self.content)


class FilesSetupController:

    def __init__(self, project_path):
        self.config_setup_controller = ConfigSetupController(project_path)
        self.indico_setup_controller = IndicoSetupController(project_path)

    def run(self):
        self.indico_setup_controller.run()
        self.config_setup_controller.run()


class DatabaseSetupController:

    def __init__(self):
        self.cursor = Db.get_cursor()

    def run(self):
        if not self.exists('event'):
            self.execute(EVENT_TABLE_SQL)
        if not self.exists('creator'):
            self.execute(CREATOR_TABLE_SQL)
        if not self.exists('event_reference'):
            self.execute(EVENT_REFERENCE_TABLE_SQL)

    def exists(self, database_name):
        try:
            sql = 'SELECT * FROM {db};'.format(database_name)
            self.execute(sql)
            return True
        except:
            return False

    def execute(self, sql):
        self.cursor.execute(sql)
