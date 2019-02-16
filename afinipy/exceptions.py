class IllegalSetting(Exception):
    """Exception raised when unrecognised setting is passed"""
    def __init__(self, setting, value):
        """Raise IllegalSetting exception

        Parameters
        ----------
        setting : str
            The name of the setting
        value : T
            The value passed for the setting
        """
        m = "The vale for setting {0} is not unrecognised, value: {1}".format(setting, value)
        Exception.__init__(self, m)


class WrongSettingsType(Exception):
    """Exception raised if setting is of wrong type"""
    def __init__(self, setting, value, correct_type=None):
        """Raise the exception

        Parameters
        ----------
        setting : str
            The name of the setting
        value : T
            The value passed for the setting
        correct_type : T
            The expected type of the value, optional
        """
        if correct_type:
            m = 'Setting {0} is not of type {1} but {2}'.format(setting, correct_type, type(value))
        else:
            m = 'Setting {0} is of wrong type {1}'.format(setting, type(value))
        Exception.__init__(self, m)


class DirectoryNotFound(Exception):
    """Exception raised if directory cannot be found"""
    def __init__(self, path):
        """Raise the exception

        Parameters
        ----------
        path : str
            path to target directory
        """
        m = 'Directory {} does not exist, please specify the full path'
        Exception.__init__(self, m)


class FileNotFound(Exception):
    """Exception raised if file cannot be found"""
    def __init__(self, path):
        """Raise the exception

        Parameters
        ----------
        path : str
            path to target file
        """
        m = 'File {} does not exist, please specify the full path'
        Exception.__init__(self, m)
