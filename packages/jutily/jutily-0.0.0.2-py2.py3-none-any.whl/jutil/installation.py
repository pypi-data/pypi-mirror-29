import MySQLdb
import pathlib
import jinja2


def installation_database_singleton(username, password, host):

    class Db:

        _instance = None

        @staticmethod
        def create_database(name):
            try:
                cursor = Db.get_cursor()
                cursor.execute('CREATE DATABASE {}; COMMIT;'.format(name))
            except:
                print('COULD NOT CREATE DATABASE {}'.format(name))

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
            try:
                connector = MySQLdb.connect(
                    host=host,
                    user=username,
                    passwd=password
                )
                Db._instance = connector
                print('DATABASE CONNECTOR SUCCESSFULLY CREATED')
                return True
            except Exception as e:
                print('DURING THE ATTEMPT TO CREATE A DATABASE CONNECTION THE EXCEPTION OCCURRED\n"{}"'.format(str(e)))
                return False

        @staticmethod
        def test():
            return Db.new_instance()

    return Db


class SetupController:

    def run(self):
        raise NotImplementedError()


class FileSetupController(SetupController):

    def __init__(self, path, file_name, template_path, **kwargs):
        self.path = pathlib.Path(path) / file_name
        with open(template_path, mode='r') as file:
            self.template = jinja2.Template(file.read())
        self.content = self.template.render(**kwargs)

    def run(self):
        if not self.exists():
            self.create()

    def create(self):
        with self.path.open(mode='w+') as file:
            file.write(self.content)
            file.flush()

    def exists(self):
        return self.path.exists() and self.path.is_file()