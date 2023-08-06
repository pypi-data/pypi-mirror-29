import time, getopt
import logging
from rembrandtml.configuration import ModelConfig, ContextConfig, DataConfig, InstrumentationConfig


class CommandLineParser(object):
    @staticmethod
    def print_usage():
        # Vebosity Codes: 's', 'q', 'd', 'n'
        print(f'')

    @staticmethod
    def parse_command_line(params):
        layers = 3
        nodes = 16
        epochs = 10
        batch_size = 64
        nn_type = 'cnn'
        mode = 'p'
        verbosity_code = 'q'
        sample_size = 0
        dataset_name = ''
        framework = 'tensorflow'
        metrics = ['acc']
        model_config = ModelConfig()

        opts, args = getopt.getopt(params, shortopts='t:m:l:o:n:d:e:f:b:s:v:x:')
        for opt, arg in opts:
            if opt == '-b':
                batch_size = int(arg)
            elif opt == '-d':
                dataset_name = arg
            elif opt == '-e':
                epochs = int(arg)
            elif opt == '-f':
                framework = arg
            elif opt == '-l':
                model_config.loss_function = arg
            elif opt == '-o':
                model_config.optimizer = arg
            elif opt == '-m':
                mode = arg
            elif opt == '-n':
                nodes = int(arg)
            elif opt == '-s':
                sample_size = int(arg)
            elif opt == '-t':
                nn_type = arg
            elif opt == '-v':
                verbosity_code = arg
            elif opt == '-x':
                metrics = arg

        ml_config = ContextConfig(nn_type, framework, mode, layers, nodes, epochs, batch_size)
        model_config.metrics = metrics
        ml_config.model_config = model_config
        instr_config = InstrumentationConfig(verbosity_code)
        ml_config.instrumentation_config = instr_config
        data_config = DataConfig(dataset_name, sample_size)
        ml_config.data_config = data_config
        return ml_config


class Split(object):
    def __init__(self, name, start_time):
        self.Name = name
        self.StartTime = start_time

class Timer(object):
    def __init__(self):
        self.start_time = None
        self.splits = []
        self.last_split = None

    def start(self):
        self.start_time = time.time()
        self.last_split = self.start_time

    def get_start(self):
        if self.start_time == None:
            raise TypeError('The time has not yet been started.  It must be started to get the elapsed time.')
        return self.start_time

    def split_units(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return (h, m, s)

    def get_elapsed(self):
        return self.split_units(time.time() - self.start_time)

    def start_split(self, name):
        self.splits.append(Split(name, time.time()))

    def get_split(self, name = None):
        if name is None:
            now = time.time()
            split = self.split_units((now - self.last_split))
            self.last_split = now
            return split
        if self.splits[name] is None:
            raise KeyError(f'The Split {name} has not been created.')
        return self.splits[name].StartTime

class Instrumentation(object):
    def __init__(self, instrumentation_config = None, logger = None):
        self.timer = Timer()
        if instrumentation_config == None:
            self.config = InstrumentationConfig()
        else:
            self.config = instrumentation_config
        self.logger = logger
        if self.config.logging_config:
            for logger_config in instrumentation_config.logging_config.logger_configs:
                pylogger = logging.getLogger(logger_config.name)
                pylogger.setLevel(logger_config.level)
                for path, level in logger_config.handlers:
                    handler = logging.FileHandler(path)
                    handler.setLevel(level)
                    formatter = logging.Formatter(logger_config.formatter)
                    handler.setFormatter(formatter)
                    pylogger.addHandler(handler)
                self.logger.pyloggers.append(pylogger)


