import os, dill
from enum import Enum
import numpy as np

from rembrandtml.configuration import RunMode
from rembrandtml.core import FunctionNotImplementedError
from rembrandtml.entities import MLEntityBase

_model_names = ('math', 'linreg', 'cls', 'mltcls', 'knn', 'logreg', 'sgd', 'rndf', 'nbay', 'pcpt', 'svc',
                'dtree', 'cnn', 'rnn', 'lstm', 'gru', 'hvote', 'stckd')
class ModelType(Enum):
    MATH = 0
    LINEAR_REGRESSION = 1
    SIMPLE_CLASSIFICATION = 2
    MULTIPLE_CLASSIFICATION = 3
    KNN = 4
    LOGISTIC_REGRESSION = 5
    SGD_CLASSIFIER = 6
    RANDOM_FOREST_CLASSIFIER = 7
    NAIVE_BAYES = 8
    PERCEPTRON = 9
    SVC = 10
    DECISTION_TREE_CLASSIFIER = 11
    CNN = 12
    RNN = 13
    LSTM = 14
    GRU = 15
    VOTING_CLASSIFIER = 16
    STACKED = 17

    def __str__(self):
        return _model_names[self.value]

class MLModelBase(MLEntityBase):
    """
    The MLModel represents the type of model, e.g. Linear Regression, K Nearest Neighbor, etc.
    The private field, _model_impl is the selected framework's implementation of that model.
    """
    def __init__(self, model_config, instrumentation):
        super(MLModelBase, self).__init__(instrumentation)
        self.model_config = model_config
        self._model_file_attribute = 0
        self._weights_file_attribute = 0
        self._tokenizer_file_attribute = 0
        self._history_file_attribute = 0
        self._tokenizer = None

    @property
    def name(self):
        return self.model_config.name

    @property
    def coefficients(self):
        return self._model_impl.coefficients


    @property
    def intercepts(self):
        return self._model_impl.intercepts

    @property
    def Model(self):
        if (self._model == None):
            raise ValueError(f'The model is not initialize and we are in {self.model_config.Mode} mode.')

        return self._model

    @Model.setter
    def Model(self, model):
        self._model = model

    def get_file_name(self, directory, file_type, class_name, attribute, extension):
        attribute_divider = ''
        attribute_str = ''
        if (attribute > 0):
            attribute_divider = '_'
            attribute_str = str(attribute)
        if (extension[0] != '.'):
            extension = '.' + extension
        path = os.path.join(directory, f'{file_type}_{class_name}{attribute_divider}{attribute_str}{extension}')
        return path

    '''
    These file attribute should be move to a File class to handle name management (e.g. When we need to find
    a unique name).
    I just wnted to see what Python properties are capable of.
    '''

    @property
    def ModelFileAttribute(self):
        return self._model_file_attribute

    @ModelFileAttribute.setter
    def ModelFileAttribute(self, value):
        self._model_file_attribute = value

    @property
    def WeightsFileAttribute(self):
        return self._weights_file_attribute

    @WeightsFileAttribute.setter
    def WeightsFileAttribute(self, value):
        self._weights_file_attribute = value

    @property
    def HistoryFileAttribute(self):
        return self._history_file_attribute

    @HistoryFileAttribute.setter
    def HistoryFileAttribute(self, value):
        self._history_file_attribute = value

    @property
    def TokenizerFileAttribute(self):
        return self._model_file_attribute

    @TokenizerFileAttribute.setter
    def TokenizerFileAttribute(self, value):
        self._token_file_attribute = value

    @property
    def TokenizerFile(self):
        return self.get_file_name(os.path.join(self.Base_Directory, 'models'), 'Tokenizer', self.__class__.__name__,
                                  self.TokenizerFileAttribute, 'pkl')

    @property
    def WeightsFile(self):
        return self.get_file_name(os.path.join(self.Base_Directory, 'models'),
                                  'Weights', self.__class__.__name__,
                                  self.WeightsFileAttribute, 'h5')

    @property
    def ModelFile(self):
        return self.get_file_name(os.path.join(self.Base_Directory, 'models'),
                                  'Model', self.__class__.__name__,
                                  self.ModelFileAttribute, 'h5')

    @property
    def HistoryFile(self):
        return self.get_file_name(os.path.join(self.Base_Directory, 'models'),
                                  'History', self.__class__.__name__,
                                  self.HistoryFileAttribute, 'h5')

    @property
    def Tokenizer(self):
        if (self._tokenizer == None):
            if (os.path.isfile(self.TokenizerFile) == False):
                raise FileNotFoundError(
                    f'The Tokenizer is null(prepare_data() hasn\'t been called) and there is no tokenizer file at: {tokenizer_file}')
            with open(self.TokenizerFile, 'rb') as file_handle:
                self._tokenizer = dill.load(file_handle)
        return self._tokenizer

    @Tokenizer.setter
    def Tokenizer(self, tokenizer):
        self._tokenizer = tokenizer
        with open(self.TokenizerFile, 'wb') as file_handle:
            dill.dump(self._tokenizer, file_handle, protocol=dill.HIGHEST_PROTOCOL)
    '''
    def validate_fit_call(self):
        if self._model_impl == None:
            raise TypeError(f'{self.name}: The model implementation has not been initialized')
        if self.data_container.X_train is None:
            self.log(f'{self.name}: X_train is not populated, using X.')
            if self.data_container.X is None:
                raise TypeError(f'{self.name}: Training data has not been prepared.  Both X_train and X and empty.')
    '''
        #if self.data_container == None:
        #    raise AttributeError('This model had no DataContainer, please call build_model(data_container) first.')
        #if self.data_container.train_generator == None:
        #    raise AttributeError('This model does not have a training generator.  Please check your configuration')

    def build_model(self):
        pass

    def load_from_file(self, file_name = None):
        pass

    def fit(self, X, y, save=False):
        """

        :param X: The feature dataset to fit against
        :param y: The labels to fit against
        :param features: A tuple of the features to be included in X.  If X and y are not supplied, this parameter will be used to retrieve data from the DataContainer
        :param weights_file:
        :param model_file:
        :param save: A boolean indicating whether or not to save the fitted model to a file
        :return: The path of the saved file if 'save' was 'True'
        """
        self.log(f'Running fit with implementation: {self._model_impl.__class__.__name__} X: {X.shape} y: {y.shape}')
        self._model_impl.fit(X, y)


    def train(self):
        pass

    def evaluate(self, X, y):
        score = None
        #if X == None:
        #    self.log(f'X and y were not passed as parameters.  Using DataContainer.')
        #    loss = self.Model.evaluate_generator(self.data_container.val_generator, steps=self.data_container.val_steps)
        #else:
        score = self._model_impl.evaluate(X, y)
        return score



    def tune(self, parameters):
        raise FunctionNotImplementedError(self.__class__.__name__, 'tune')

    def predict(self, X, with_probabilities):
        prediction = self._model_impl.predict(X, with_probabilities)
        return prediction

class MLSingleModelBase(MLModelBase):
    def __init__(self, model_config, instrumentation):
        super(MLSingleModelBase, self).__init__(model_config, instrumentation)
        from rembrandtml.factories import ModelFactory, ModelImplFactory
        self._model_impl = ModelImplFactory.create(model_config, instrumentation)

class MLSimpleModel(MLSingleModelBase):
    def __init__(self, model_config, instrumentation):
        super(MLSimpleModel, self).__init__(model_config, instrumentation)

    def fit(self):
        pass

    def evaluate(self):
        pass

    def predict(self, X):
        pass

class MathModel(MLSingleModelBase):
    def __init__(self, model_config):
        super(MathModel, self).__init__(model_config)
        self.model_config = model_config

    def evaluate(self, data_container):
        self.log(f'MathModel.evaluate(): steps: {data_container.val_steps}')
        batch_maes = []
        for step in range(data_container.val_steps):
            samples, targets = next(data_container.val_generator)
            preds = samples[:, -1, 1]
            mae = np.mean(np.abs(preds - targets))
            batch_maes.append(mae)
        print(np.mean(batch_maes))
        return batch_maes



class MLModel(MLSingleModelBase):
    def __init__(self, model_config, instrumentation):
        super(MLModel, self).__init__(model_config, instrumentation)

    # Requires a DataContainer because we might need to know the data shape to initialize layers
    def build_model(self, data_container):
        # Should to a state change to a data-bound model
        self.data_container = data_container
        self.Model = Sequential()
        lookback = 1440
        step = 6
        self.Model.add(Flatten(input_shape=(lookback // step, self.data_container.Data.shape[-1])))
        self.Model.add(Dense(32, activation='relu'))
        self.Model.add(Dense(1))
        self.Model.compile(optimizer=self.model_config.ModelConfig.optimizer,
                           loss=self.model_config.ModelConfig.loss_function,
                           metrics=self.model_config.ModelConfig.metrics)

    def tune(self, tuning_parameters, parameters):
        X, y = self.get_data_from_data_container(RunMode.PREDICT)
        results = self._model_impl.tune(X, y, tuning_parameters, parameters)
        return results


    def fit_gen(self, regularize=True, validate=False, weights_file=None, model_file=None, save=False):
        """

        :param X: The feature dataset to fit against
        :param y: The labels to fit against
        :param features: A tuple of the features to be included in X.  If X and y are not supplied, this parameter will be used to retrieve data from the DataContainer
        :param weights_file:
        :param model_file:
        :param save: A boolean indicating whether or not to save the fitted model to a file
        :return: The path of the saved file if 'save' was 'True'
        """
        X, y = self.get_data_from_data_container()
        self.log(f'Running fit with implementation: {self._model_impl.__class__.__name__} X: {X.shape} y: {y.shape}')
        self._model_impl.fit(X, y, validate)


        return None

        '''
        lookback = 1440
        step = 6
        model = Sequential()
        model.add(layers.Flatten(input_shape=(lookback // step, self.DataContainer.Data.shape[-1])))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(1))

        model.compile(optimizer=RMSprop(), loss='mae', metrics=['acc'])
        history = model.fit_generator(self.DataContainer.train_generator,
        history = model.fit_generator(self.DataContainer.train_generator,
                                      steps_per_epoch=500,
                                      epochs=self.Config.Epochs,
                                      validation_data=self.DataContainer.val_generator,
                                      validation_steps=self.DataContainer.val_steps)

        '''
        self.log(f'Training model: {self.name}')
        history = self.Model.fit_generator(self.data_container.train_generator,
                                           steps_per_epoch=500,
                                           epochs=self.Config.Epochs,
                                           validation_data=self.data_container.val_generator,
                                           validation_steps=self.data_container.val_steps,
                                           verbose=2)

        weights_file = self.unique_file_name(MLModelBase.__dict__['WeightsFile'], MLModelBase.__dict__['WeightsFileAttribute'])
        self.Model.save_weights(weights_file)
        model_file = self.unique_file_name(MLModelBase.__dict__['ModelFile'], MLModelBase.__dict__['ModelFileAttribute'])
        self.Model.save(model_file)
        history_file = self.unique_file_name(MLModelBase.__dict__['HistoryFile'], MLModelBase.__dict__['HistoryFileAttribute'])

        '''
        # Hiting recursion depth exceeded errors
        with open(history_file, 'bw') as f:
            dill.dump(history, f, protocol=dill.HIGHEST_PROTOCOL)
        f.close()
        '''

        return history
        ''' Once file management has been refactored into it's own class
        if weights_file != None:
            self.Model.save_weights(weights_file)
        if model_file != None:
            self.Model.save(model_file)
        '''


    def load_from_file(self, data_container, file_name = None):
        # for testing
        model_file = 'D:\code\ML\models\Model_MLModel.h5'
        self.log(f'Loading model from {model_file}')
        self.Model = load_model(model_file)
        self.log(f'Loaded model: {self.Model.summary()}')
        self.data_container = data_container
        self.log('Added DataContainer')

class EnsembleModelBase(MLModelBase):
    """
    Handles common functionality of all type of ensemble models, such as estimator validation, data slicing, and looping over estimators
    """
    def __init__(self, model_config, data_provider, instrumentation):
        super(EnsembleModelBase, self).__init__(model_config, data_provider, instrumentation)
        #self.validate_estimators()
        #self.build_estimators()
        from rembrandtml.factories import ModelImplFactory
        self._model_impl = ModelImplFactory.create(model_config, instrumentation)


    def validate_estimators(self):
        if self.model_config.estimators is None or len(self.model_config.estimators) < 1:
            raise TypeError(f'{self.__class__.__name__} is an ensembles model.  All ensemble models must be configured with estimators.')

    def build_estimators(self):
        from rembrandtml.factories import ModelFactory
        for model_config in self.model_config.ensemble_config.estimator_configs:
            pass #self.estimators[model_config.name] = ModelFactory.create(model_config, data_provider, instrumentation)


class VotingModel(EnsembleModelBase):
    def __init__(self, model_config, data_provider, instrumentation):
        super(VotingModel, self).__init__(model_config, data_provider, instrumentation)
