from enum import Enum
import pandas as pd

from rembrandtml.configuration import Verbosity, RunMode
from rembrandtml.entities import MLEntityBase
from rembrandtml.visualization import Visualizer
from rembrandtml.utils import Instrumentation

score_names = ('loss', 'accuracy', 'r2', 'Precision', 'Recall', 'F1',
               'neg_mean_absolute_error', 'neg_mean_squared_error',
               'neg_log_loss', 'roc_auc')

class ScoreType(Enum):
    LOSS = 0
    ACCURACY = 1
    R2 = 2
    PRECISION = 3
    RECALL = 4
    F1 = 5
    MAE = 6
    MSE = 7
    LOG_LOSS = 8
    AUC = 9

    def __str__(self):
        return score_names[self.value]

class Score(object):
    def __init__(self, model_config, values={}, notes=''):
        self.values = values
        self._model_config = model_config
        self.notes = notes

    def __gt__(self, other):
        return self.value[self.values.keys()[0]] > other.value[self.values.keys()[0]]


    def __lt__(self, other):
        return self.value[self.values.keys()[0]] < other.value[self.values.keys()[0]]

    @property
    def model_name(self):
        return self._model_config.name


    @property
    def model_type(self):
        return self._model_config.model_type


    @property
    def model_framework(self):
        return self._model_config.framework_name

    def __str__(self):
        str = f'Name: {self.model_name} Model Type: {self.model_type} Framework:{self.model_framework}\n\t'
        for metric in self.values:
            str += f'{metric}: {self.values[metric]}\n\t'
        if self.notes:
            str += f'Notes: {self.notes}'
        return str


class TuningResults(object):
    def __init__(self, model_name, best_params):
        self.model_name = model_name
        self.best_params = best_params


class Prediction(object):
    def __init__(self, model_name, prediction):
        self.model_name = model_name
        self.values = prediction

    def __str__(self):
        str = f'Model: {self.model_name}\n\tPredictions: {self.values}'
        return str


class RMLContext(object):
    """The RMLContext object is an organizing structure to group the data, models, and Visualizer
    that are used in common ML tasks.
    To support easy experiementation with different model and dataset configurations, the RMLContext manages the data
    and passes that data to any models that it also manages.
    The RMLContext also holds singletons, such as Instrumentation and Timer.
    """

    def __init__(self, models, data_container, instrumentation, config):
        super(RMLContext, self).__init__()
        self.config = config
        self.models = models
        self.data_container = data_container
        # Start the timer to that we can log elapsed times
        self.instrumentation = instrumentation
        self.instrumentation.timer.start()

    def prepare_data(self, features=None, target_feature=None, use_cache=False):
        """
        Loads data from the configured DataProvider and splits the data into training and test sets.
        After this method is called, DataContainer.X_train, DataContainer.X_test, DataContainer.y_train, and DataContainer.y_test are populated.
        :param features:
        :param target_feature:
        :param use_cache:
        :return:
        """
        self.log(f'Preparing data with {self.model.data_container.__class__.__name__}')
        self.data_container.prepare_data(features, target_feature)
        self.log(f'Finished preparing data with {self.model.data_container.__class__.__name__}')

    def train_model(self, model):
        X, y = self.data_container.get_data()
        self.log(f'Training model: {model.name}')
        model.fit(X, y)
        self.log(f'Finished training model: {model.name}')

    def train(self, model_name=None):
        """
        Trains the model against the training set in the model's DataContainer.  If split() has been called, DataContainer.X_train will be populated and that training set will be used.  Otherwise, the DataContainer.X will be used.
        :return:
        """
        if model_name:
            model = self.models[model_name]
            self.train_model(model)
        else:
            for key in self.models:
                model = self.models[key]
                self.train_model(model)

    def evaluate_model(self, model):
        self.log(f'Evaluating model: {model.name}')
        X, y = self.data_container.get_data(RunMode.EVALUATE)
        score = model.evaluate(X, y)
        self.log(f'Finished evaluating model: {model.name}')
        return score

    def evaluate(self, model_name=None):
        """

        :return: A dictionary of Score objects populated with metrics specific to each model
        """
        scores = {}
        if model_name:
            model = self.models[model_name]
            scores[model.name] = self.evaluate_model(model)
        else:
            for key in self.models:
                model = self.models[key]
                scores[model.name] = self.evaluate_model(model)
        return scores

    def tune(self, tuning_parameters, model_parameters):
        """
        Tunes the model's hyperparameters.
        :param parameters: A dictionary of hyperparameters to be used.
        :return: A TuningResults instance.
        """
        self.log(f'Tuning model: {str(self.model)}')
        results = self.model.tune(tuning_parameters, model_parameters)
        self.log(f'Finished tuning model: {str(self.model)}')
        return results


    def predict_model(self, X, model, with_probabilities=False):
        self.log(f'Predicting: {model.name}')
        prediction = model.predict(X, with_probabilities)
        self.log(f'Finished predicting: {model.name}')
        return prediction

    def predict(self, X, model_name=None, with_probabilities=False):
        predictions = {}
        if model_name:
            model = self.models[model_name]
            predictions[model.name] = self.predict_model(X, model, with_probabilities)
        else:
            for key in self.models:
                model = self.models[key]
                predictions[model.name] = self.predict_model(X, model, with_probabilities)
        return predictions



    def plot(self, model_name = '', data_container_name = '', plotter_name = ''):
        pass

    def time_to_string(self, hrs, min, sec):
        return "%d:%02d:%02d" % (hrs, min, sec)

    def log(self, msg, verbosity = Verbosity.DEBUG):
        start_string = self.time_to_string(*self.instrumentation.timer.get_elapsed())
        split_string = self.time_to_string(*self.instrumentation.timer.get_split())
        instr_msg = f'{start_string} Split: {split_string}: {msg}'
        self.instrumentation.logger.log(instr_msg, verbosity)

class ParameterError(RuntimeError):
    def __init__(self, msg):
        super(StateError, self).__init__(self, msg)

class StateError(RuntimeError):
    def __init__(self, msg):
        super(StateError, self).__init__(self, msg)

class FunctionNotImplementedError(NotImplementedError):
    def __init__(self,  type_name, function_name):
        super(FunctionNotImplementedError, self).__init__(self, f'{type_name}.{function_name}')