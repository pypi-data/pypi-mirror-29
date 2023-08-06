

class DictQuery:
    """
    This is a class, that is supposed to help with the processing of multi layered dictionary structures.
    This is a base class for a state object, that processes one such dictionary at a time, the dictionary being set or
    changed by the 'set' method. The class provides the query dict method, with which a nested value of the dict can
    be acquired by using a standard path query like 'key1/key2/key3'.
    It will be attempted to access the nested structure with this path, but in case there is an exception due to a none
    existing path or something else an exception will be caught and the method 'query_exception' will be executed,
    the query will then return whatever this method returns.
    There is the possibility to specify a default value for every query in case it fails and this is also passed to
    the exception method, wo it could be returned from there, for example

    :ivar dict: The currently processed dict of the object. All the queries will be applied to this dict until it is
        changed
    """
    def __init__(self):
        self.dict = None

    def process(self):
        raise NotImplementedError()

    def set(self, query_dict):
        """
        Sets/changes the currently processed dict of the object

        :param query_dict: The new dict to be processed
        :return: void
        """
        self.dict = query_dict

    def query_exception(self, query, query_dict, default):
        """
        This method is being called, when a query to the dict fails.

        :param query: The query string for which the exception occurred
        :param query_dict: The whole dict with which the exception occurred
        :param default: The default value given to the query method
        :return: The return will be the return of the query method in case of failure
        """
        raise NotImplementedError()

    def query_dict(self, dict_query, default):
        """
        Attempts to extract the value to the given query "path" from the nested dictionary structure, but in case it
        fails the method 'query_exception' will be executed.

        :param dict_query: The path-like query string defining the order of keys to apply to the nested dict
        :param default: A possible default value in case the query fails
        :return: The value form the dict
        """
        try:
            keys = dict_query.split('/')
            current_dict = self.dict

            for key in keys:
                current_dict = current_dict[key]

            return current_dict
        except (KeyError, ValueError) as excpetion:
            return self.query_exception(dict_query, self.dict, default)

