import configparser
import os


def config_singleton(project_path, config_name='config.ini'):
    """
    This function returns a class, which represents a singleton for access to the projects config file. The project
    path and name of the config file are saved to the class by passing them as parameters to the function.

    USAGE:
    In a local project a singleton access class can be created by creating a new class, which inherits from the return
    of this function. And no further methods are needed. The child class can be accessed by calling the 'get_instance'
    method to retrieve the ConfigParser object:

    EXAMPLE:
    Class Config(config_singleton("my/path", "config.ini")): pass
    Config.get_instance()
    # <configparser.ConfigParser>

    :param project_path: The path to the folder where the config file is located
    :param config_name: The string file name of the config file to be subject of the class. DEFAULT: config.ini
    :return: Class:Config
    """
    class Config:
        """
        A singleton class for the access to the config object
        """
        _instance = None

        def __init__(self):
            pass

        @staticmethod
        def get_instance():
            if Config._instance is None:
                Config._instance = Config._create_instance()

            return Config._instance

        @staticmethod
        def _create_instance():
            # Getting the path to the config file
            path = Config._config_path()
            # Creating the config parser object and returning it
            config = configparser.ConfigParser()
            config.read(path)

            return config

        @staticmethod
        def _config_path():
            # Joining the config path
            path = os.path.join(project_path, 'config.ini')
            return path

    return Config
