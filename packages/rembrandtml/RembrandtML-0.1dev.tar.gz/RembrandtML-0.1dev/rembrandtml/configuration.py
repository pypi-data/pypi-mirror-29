import os
from enum import Enum


class RunMode(Enum):
    TRAIN = 0
    EVALUATE = 1
    PREDICT = 2


class Verbosity(Enum):
    SILENT = 0
    QUIET = 1
    WARNINGS = 2
    DEBUG = 3
    NOISY = 4

    @staticmethod
    def code_to_verbosity(code):
        if code == 's':
            return Verbosity.SILENT
        elif code == 'q':
            return Verbosity.QUIET
        elif code == 'd':
            return Verbosity.DEBUG
        elif code == 'n':
            return Verbosity.NOISY
        else:
            raise TypeError(f'Undefined verbosity code: {code}')

    # We have to define __hash__ because
    # we define __eq__ (http://docs.python.org/3.1/reference/datamodel.html#object.hash)
    def __hash__(self):
        return super(Verbosity, self).__hash__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented


class DataConfig(object):
    def __init__(self, framework_name, dataset_name, file_path=None, sample_size = -1):
        self.framework_name = framework_name
        self.dataset_name = dataset_name
        self.sample_size = sample_size
        self.dataset_file_path = file_path
        self.file_separator = ','

class LoggerConfig(object):
    """LoggerConfig describes an individual logger.
    Loggers are the entity where formatting is configured.
    A logger can be configured with different handlers to write to different destinations, such as different files and the console.
    Formatting is handled at the Logger level.
    Formatting allows additional information, such as a time stamp, to be added to the log message..
    """
    def __init__(self, name, level, handlers, formatter=None):
        """

        :param name: The name of the logger.
        :param name: The log level.  This can be overridden by the log level of handlers
        :param handlers: An interable of destinations that the logger will write to.
        :param formatter: A string containing data formatting and meta-data, such as timestamp.
        """
        self.name = name
        self.level = level
        self.handlers = handlers
        self.formatter = formatter

class LoggingConfig(object):
    """LoggingConfig is a organizing structure that hold meta data about the entire logging system."""
    def __init__(self, logger_configs = []):
        self.logger_configs = logger_configs

class InstrumentationConfig(object):
    def __init__(self, console_verbosity='d', logging_config=None):
        """
        Configuration data for the instrumentation system, which included logging, instrumentation, and auditing.
        :param console_verbosity: The logging level for messages to the console.  This parameter can be a Verbosity enum
         or a single-character verbosity code('s', 'q', 'd', 'n').
        :param logging_config: A LoggingConfig structure.  If this parameter is absent,
                logging will still be sent to the console based on the 'console_verbosity' parameter.
        """
        if isinstance(console_verbosity, str):
            self.verbosity = Verbosity.code_to_verbosity(console_verbosity)
        else:
            self.verbosity = console_verbosity
        self.logging_config = logging_config

class ContextConfig(object):
    def __init__(self, model_configs, data_config, mode = RunMode.TRAIN, verbosity = Verbosity.QUIET, base_dir = None, layers = 4, nodes = 16, epochs = 10, batch_size = 32):
        if not base_dir:
            self.base_dir = os.getcwd()
        else:
            self.base_dir = base_dir
        self.data_config = data_config
        self._verbosity = verbosity
        # Properties probably aren't necessary, so experimenting with public fields
        self.Layers = layers
        self.Nodes = nodes
        self._epochs = epochs
        self.BatchSize = batch_size
        self.TrainDir = ''
        self.TestDir = ''
        self.ValidationDir = ''
        self.Mode = mode
        if isinstance(model_configs, ModelConfig):
            self.model_configs = [model_configs]
        else:
            self.model_configs = list(model_configs)
        self.instrumentation_config = None

    @property
    def Verbosity(self):
        return self._verbosity

    @property
    def model_type(self):
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        self._model_type = model_type

    @property
    def Epochs(self):
        return self._epochs

class RunConfig(object):
    """
    Container for variables and collections associated with the root task.
    """
    def __init__(self, model_name, log_file = None):
        self.model_name = model_name
        self.log_file = log_file
        self.prediction_column = None
        self.prediction_index = None
        self.index_name = None


class ModelConfig(object):
    def __init__(self, name, framework_name, model_type):
        """
        Metadata for instantiating a model.
        :param name:
        :param framework_name:
        :param model_type:
        :param data_config:
        """
        self.name = name
        self.model_type = model_type
        self.framework_name = framework_name
        self._metrics = []
        self._layers = []
        self.LayerCount = 1
        self.Dropout = 0
        self.RecurrentDropout = 0
        self.parameters = {}


    @property
    def loss_function(self):
        return self._loss_function

    @loss_function.setter
    def loss_function(self, loss_function):
        self._loss_function = loss_function

    @property
    def optimizer(self):
        return self._optimizer

    @optimizer.setter
    def optimizer(self, optimizer):
        self._optimizer = optimizer

    @property
    def epochs(self):
        return self._epochs

    @epochs.setter
    def epochs(self, epochs):
        self._epochs = epochs

    @property
    def batch_size(self):
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size):
        self._batch_size = batch_size

    @property
    def validation_data(self):
        return self._validation_data
    @validation_data.setter
    def validation_data(self, validation_data):
        self._validation_data = validation_data

    @property
    def metrics(self):
        return self._metrics
    @metrics.setter
    def metrics(self, metrics):
        self._metrics = metrics

    @property
    def layers(self):
        return self._layers
    @layers.setter
    def layers(self, layers):
        self._layers = layers


class EnsembleConfig(object):
    def __init__(self, estimator_configs):
        self.estimator_configs = estimator_configs

class EnsembleModelConfig(ModelConfig):
    def __init__(self, name, framework_name, model_type, data_config, ensemble_config):
        super(EnsembleModelConfig, self).__init__(name, framework_name, model_type, data_config)
        self.estimators = []
        self.ensemble_config = ensemble_config


