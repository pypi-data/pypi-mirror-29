import os

from rembrandtml.configuration import InstrumentationConfig, Verbosity


class MLEntityBase(object):
    """
    Provided instrumentation functionality to all subclasses
    """
    def __init__(self, instrumentation):
        #self.Base_Directory = os.path.abspath(os.path.join(os.getcwd(), '..'))
        self.instrumentation = instrumentation

    def unique_file_name(self, file_property, attribute_property):
        while(os.path.isfile(file_property.__get__(self))):
            attribute_property.__set__(self, attribute_property.__get__(self) + 1)
        return file_property.__get__(self)

    # ToDo move to MLLogger
    def log(self, msg, verbosity=Verbosity.DEBUG):
        '''
        Write the msg parameter to the console if the verbosity parameter is >= this objects configured verbosity in ContextConfig.Verbosity
        :param msg:
        :param verbosity:
        :return: The msg parameter echoed back.  This allows nesting calls to log, e.g.raise TypeError(self.log(f'The features parameter was not supplied.')
        '''
        self.instrumentation.logger.log(msg, verbosity)
        return msg


class MLFile(MLEntityBase):
    def __init__(self):
        super(MLFile, self).__init__()
        self._base_dir = ''

    @property
    def BaseDir(self):
        return self._base_dir

    def unique_file_name(self):
        return 'file path'


class MLLogger(object):
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    verbosity_color = {Verbosity.SILENT: Colors.FAIL, Verbosity.QUIET: Colors.BOLD,
                       Verbosity.DEBUG: Colors.HEADER, Verbosity.NOISY: Colors.OKBLUE}

    def __init__(self, instrumentation_config = None):
        if instrumentation_config:
            self.instrumentation_config = instrumentation_config
        else:
            self.instrumentation_config = InstrumentationConfig('d')
        self.pyloggers = []

    def log(self, msg, verbosity = Verbosity.DEBUG):
        if verbosity > self.instrumentation_config.verbosity:
            return
        print(self.verbosity_color[verbosity] + msg + MLLogger.Colors.ENDC)
        self.write_to_loggers(msg, verbosity)


    def write_to_loggers(self, msg, verbosity):
        for pylogger in self.pyloggers:
            if verbosity == Verbosity.QUIET:
                pylogger.error(msg)
            elif verbosity == verbosity.SILENT:
                pylogger.critical(msg)
            elif verbosity == verbosity.NOISY:
                pylogger.debug(msg)
            elif verbosity == verbosity.DEBUG:
                pylogger.info(msg)
            elif verbosity == verbosity.WARNINGS:
                pylogger.warn(msg)