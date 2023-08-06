from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


def sqlalchemy_add_children(relationship_attribute, object_list):
    """
    EXAMPLE:
    There is a sqlalchemy model "Shepard" and he has a relationship 'sheeps' to a table to 'Sheep' models, than this
    function serves as a helper, because every Sheep has to be added by calling the 'append' method and in case
    one does not want to make a for loop every time that case occurs, this function simply appends all the given models
    in the list to the sqlalchemy relationship attribute
    :param relationship_attribute: A sqlalchemy relationship attribute of a Model, that is a list
    :param object_list: The list of actual Model objects to be appended to the list
    :return: void
    """
    for obj in object_list:
        relationship_attribute.append(obj)


def sqlalchemy_many_list_tuple(session, model_class, param_list, filter_function, object_function):
    """
    Given a list of parameter objects, this function will return a list of corresponding sqlalchemy model objects, by
    querying the database if there already exist some of the specified entries and then creating the remaining objects.
    The list of all those objects created, which are not represented in the database yet is also returned.

    :param session: The session for the database to use
    :param param_list: A list of objects, that each specify a database entry for the given model class
    :param model_class: The class of the model objects to return objects from
    :param filter_function: A function that accepts one item of the param_list as input and will return a sqlalchemy
        filter argument as return, that is used to possibly retrieve the object from the database, that was specified
        by the param item.
        function(param_item): <sqlalchemy filter argument>
    :param object_function: A function that accepts one item of the param_list as input and will return a model object
        for the given model class, that is based on the information the param item describes the object.#
        function(param_item): model_class
    :return: A tuple of two lists. The first being the list of all the model objects, that are based on the items
        given in the parameter list and the second list contains all the model objects for those model, which are not
        represented in the database yet and would still have to be added.
    """
    # This list will contain all items of the parameter list, that could not be retrieved by database query
    remaining_list = []
    # This list will contain all the actual model objects, either retrieved from the database or created
    object_list = []
    for list_item in param_list:
        # For each parameter item attempting to retrieve the corresponding model from the database by querying with
        # the filter function provided
        results = list(session.query(model_class).filter(filter_function(list_item)))
        if len(results) != 0:
            object_list.append(results[0])
        else:
            remaining_list.append(list_item)

    # This list will contain all the model objects, that have been created using the provided class function, but
    # are not already part of the database
    to_add_list = []
    for remaining_item in remaining_list:
        # Creating the model objects using the function provided
        obj = object_function(remaining_item)
        object_list.append(obj)
        to_add_list.append(obj)

    # Returning the list of all the model objects, that correspond to the input list of parameters and the list of
    # all those model objects, that yet have to be added to the database
    return object_list, to_add_list


def mysql_database_singleton(username, password, host, database):
    """
    This function returns a class. A class, that manages the access to a sqlalchemy(mysql) engine that is based on
    the mysql db credentials/parameters passed to this function.
    The class can be used to access the engine and create sessions, by singleton access, which means the actual
    objects for the database access are only created on the first call to the gets session method but from that
    point on session can be retrieved from the static methods of the class, which means there is no need to
    instanciate objects.

    :param username: The username to use for the database access
    :param password: The password to use for the database access
    :param host: The host of the database. Should be localhost
    :param database: The name of the database schema to use
    :return: The MySQLDatabase class
    """
    class MySQLDatabase:
        _engine = None
        _session_maker = None

        @staticmethod
        def get_session():
            if MySQLDatabase._session_maker is None:
                MySQLDatabase._create_session_maker()

            return MySQLDatabase._session_maker()  # type: Session

        @staticmethod
        def create_database(base):
            MySQLDatabase._create_engine()
            base.metadata.create_all(MySQLDatabase._engine)

        @staticmethod
        def _create_session_maker():
            MySQLDatabase._create_engine()

            MySQLDatabase._session_maker = sessionmaker(bind=MySQLDatabase._engine)

        @staticmethod
        def _create_engine():
            engine_string = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                username,
                password,
                host,
                database
            )

            MySQLDatabase._engine = create_engine(engine_string)

    return MySQLDatabase