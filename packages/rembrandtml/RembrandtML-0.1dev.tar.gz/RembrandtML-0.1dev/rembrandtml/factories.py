from rembrandtml.core import RMLContext
from rembrandtml.data import DataContainer
from rembrandtml.entities import MLLogger
from rembrandtml.model_implementations.model_impls_cntk import MLModelImplementationCntk
from rembrandtml.model_implementations.model_impls_keras import MLModelImplementationKeras
from rembrandtml.model_implementations.model_impls_sklearn import MLModelSkLearn, MLModelSkLearnLinReg, \
    MLModelSkLearnSVC
from rembrandtml.model_implementations.model_impls_tensorflow import MLModelTensorflow, MLModelTensorflowCNN
from rembrandtml.models import MLModel, MathModel, ModelType, VotingModel
from rembrandtml.nnmodels import ConvolutionalNeuralNetwork, RecurrentNeuralNetwork, LstmRNN, GruNN
from rembrandtml.utils import Instrumentation


class ContextFactory(object):
    @staticmethod
    def create(config):
        '''
        Factory method to instantiate a new machine learning context
        :param ContextConfig:
        :return: RMLContext
        '''

        logger = MLLogger(config.instrumentation_config)
        instrumentation = Instrumentation(config.instrumentation_config, logger)
        data_container = DataContainerFactory.create(config.data_config, instrumentation)
        models = {}
        for model_config in config.model_configs:
            models[model_config.name] = ModelFactory.create(model_config, data_container, instrumentation)
        context = RMLContext(models, data_container, instrumentation, config)
        return context

class DataContainerFactory(object):
    @staticmethod
    def create(data_config, instrumentation):
        data_container = DataContainer(data_config, instrumentation)
        return data_container

class ModelImplFactory(object):
    model_impl_map = {'sklearn-logreg': MLModelSkLearn, 'sklearn-linreg': MLModelSkLearnLinReg,
                      'sklearn-svc': MLModelSkLearnSVC,
                      'sklearn-hvote': MLModelSkLearn, 'sklearn-rndf': MLModelSkLearn,
                      'tensorflow-linreg': MLModelTensorflow, 'tensorflow-cnn': MLModelTensorflowCNN,
                      'keras': MLModelImplementationKeras,
                      'cntk': MLModelImplementationCntk}
    @staticmethod
    def create(model_config, instrumentation):
        key = f'{model_config.framework_name}-{model_config.model_type}'
        if key not in ModelImplFactory.model_impl_map.keys():
            raise TypeError(f'The requested framework, {key}, is not implemented.')

        ctor = ModelImplFactory.model_impl_map[key]
        model_impl = ctor(model_config, instrumentation)

        return model_impl


class ModelFactory(object):
    ModelsMap = {ModelType.CNN: ConvolutionalNeuralNetwork,
                 ModelType.MATH: MathModel,
                 ModelType.LINEAR_REGRESSION: MLModel,
                 ModelType.SIMPLE_CLASSIFICATION: MLModel,
                 ModelType.MULTIPLE_CLASSIFICATION: MLModel,
                 ModelType.KNN: MLModel,
                 ModelType.LOGISTIC_REGRESSION: MLModel,
                 ModelType.SGD_CLASSIFIER: MLModel,
                 ModelType.RANDOM_FOREST_CLASSIFIER: MLModel,
                 ModelType.NAIVE_BAYES: MLModel,
                 ModelType.PERCEPTRON: MLModel,
                 ModelType.SVC: MLModel,
                 ModelType.DECISTION_TREE_CLASSIFIER: MLModel,
                 ModelType.RNN:RecurrentNeuralNetwork,
                 ModelType.LSTM:LstmRNN,
                 ModelType.GRU:GruNN,
                 ModelType.VOTING_CLASSIFIER: VotingModel}

    @staticmethod
    def instantiate_class(model_class, model_config, instrumentation):
        cls = model_class(model_config, instrumentation)
        return cls

    @staticmethod
    def create(model_config, data_container, instrumentation):
        '''
        Factory method for creating ML models.
        This method first creates a DataContainer from the parameters specified in ContextConfig.DataConfig.
        :param name: The name of this model, e.g. SkLearnLinearRegression
        :param ml_config: An instance of ContextConfig, containing the parameters for this model and it's DataContainer.
        :return:
        '''
        # I'm not sure if a DataContain should be in __init__ for the models.
        # So, for now, we'll set the property
        if model_config.model_type not in ModelFactory.ModelsMap:
            raise TypeError(f'Network type {model_config.model_type} is not defined.')

        network = ModelFactory.instantiate_class(model_class=ModelFactory.ModelsMap[model_config.model_type], model_config=model_config, instrumentation=instrumentation)
        network.data_container = data_container
        return network

class ModelBuilder(object):
    @staticmethod
    def build_model(cls, model_parameters):
        from rembrandtml.model_implementations.model_impls_keras import MLModelImplementationKeras
        model = models.Sequential()
        for i in range(len(model_parameters.layers)):
            layer_params = model_parameters.layers[i]
            model.add(layers.Dense(layer_params.node_count,
                                   activation=layer_params.activation,
                                   input_shape=layer_params.input_shape))
        model.compile(optimizer=model_parameters.optimizer, loss=model_parameters.loss_function,
                      metrics=model_parameters.metrics)
        return model



def multilabel_sample(y, size=1000, min_count=5, seed=None):
    """ Takes a matrix of binary labels `y` and returns
        the indices for a sample of size `size` if
        `size` > 1 or `size` * len(y) if size =< 1.
        The sample is guaranteed to have > `min_count` of
        each label.
    """
    try:
        if (np.unique(y).astype(int) != np.array([0, 1])).all():
            raise ValueError()
    except (TypeError, ValueError):
        raise ValueError('multilabel_sample only works with binary indicator matrices')

    if (y.sum(axis=0) < min_count).any():
        raise ValueError('Some classes do not have enough examples. Change min_count if necessary.')

    if size <= 1:
        size = np.floor(y.shape[0] * size)

    if y.shape[1] * min_count > size:
        msg = "Size less than number of columns * min_count, returning {} items instead of {}."
        warn(msg.format(y.shape[1] * min_count, size))
        size = y.shape[1] * min_count

    rng = np.random.RandomState(seed if seed is not None else np.random.randint(1))

    if isinstance(y, pd.DataFrame):
        choices = y.index
        y = y.values
    else:
        choices = np.arange(y.shape[0])

    sample_idxs = np.array([], dtype=choices.dtype)

    # first, guarantee > min_count of each label
    for j in range(y.shape[1]):
        label_choices = choices[y[:, j] == 1]
        label_idxs_sampled = rng.choice(label_choices, size=min_count, replace=False)
        sample_idxs = np.concatenate([label_idxs_sampled, sample_idxs])

    sample_idxs = np.unique(sample_idxs)

    # now that we have at least min_count of each, we can just random sample
    sample_count = int(size - sample_idxs.shape[0])

    # get sample_count indices from remaining choices
    remaining_choices = np.setdiff1d(choices, sample_idxs)
    remaining_sampled = rng.choice(remaining_choices,
                                   size=sample_count,
                                   replace=False)

    return np.concatenate([sample_idxs, remaining_sampled])
