import os
import numpy as np
#from keras.preprocessing.text import Tokenizer
#from keras.preprocessing.sequence import pad_sequences
from rembrandtml.configuration import RunMode
from rembrandtml.data_providers.data_provider_keras import KerasDataProvider
from rembrandtml.data_providers.data_provider_pandas import PandasDataProvider
from rembrandtml.data_providers.data_provider_sklearn import SkLearnDataProvider
from rembrandtml.data_providers.data_provider_tensorflow import TensorflowDataProvider
from rembrandtml.entities import MLEntityBase
from rembrandtml.core import ParameterError


class DataContainer(MLEntityBase):
    """
    DataContainer manages the structures that hold training and target data.
    """
    data_containers = {'sklearn': SkLearnDataProvider, 'pandas': PandasDataProvider,
                       'keras': KerasDataProvider, 'tensorflow': TensorflowDataProvider}

    def __init__(self, data_config, instrumentation):
        super(DataContainer, self).__init__(instrumentation)
        self.data_provider = self.get_data_provider(data_config)
        self.config = data_config
        self.data = None
        self.val_steps = 0
        self.test_steps = 0
        self.train_generator = None
        self.val_generator = None
        self.test_generator = None
        self.X = None
        self.X_columns = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.X_val = None
        self.y_train = None
        self.y_test = None
        self.y_val = None

    def get_data_provider(self, data_config):
        if data_config.framework_name not in self.data_containers:
            raise TypeError(f'The specified framework, {framework_name}, is not supported as a DataProvider.')

        ctor = self.data_containers[data_config.framework_name]
        return ctor(data_config, self.instrumentation)

    def get_data(self, mode = RunMode.TRAIN):
        """
        Retrieves X and y data from the DataContainer.
        :param train: Specifies which data tensors to retrun.  Default is 'True'.  If 'False', test tensors are returned
        :return: X and y tensors
        """
        if mode == RunMode.TRAIN:
            X = self.X_train
            y = self.y_train
        elif mode == RunMode.EVALUATE:
            X = self.X_test
            y = self.y_test
        else:
            raise ParameterError(f'The requested RunMode, {mode.name}, is not supported.')
        return X, y


    def get_prediction_data(self, features, prediction_file):
        return self.data_provider.get_prediction_data(features, prediction_file)

    def build_generator(self, data, lookback, delay, min_index, max_index, shuffle, batch_size, step):
        if(max_index is None):
            max_index = len(data) - delay - 1
        i = min_index + lookback
        while 1:
            if shuffle:
                rows = np.random.randomint(min_index + lookback, max_index, size = batch_size)
            else:
                if i + batch_size >= max_index:
                    i = min_index + lookback
                rows = np.arange(i, min(i + batch_size, max_index))
                i += len(rows)
            samples = np.zeros((len(rows),
                                lookback // step,
                                data.shape[-1]))
            targets = np.zeros((len(rows),))
            for j, row in enumerate(rows):
                indices = range(rows[j] - lookback, rows[j], step)
                targets[j]= data[rows[j] + delay][1]
            yield samples, targets

    def generator(self, data, lookback, delay, min_index, max_index, shuffle, batch_size, step):
        if max_index is None:
            max_index = len(data) - delay - 1
        i = min_index + lookback
        while 1:
            if shuffle:
                rows = np.random.randint(
                    min_index + lookback, max_index, size=batch_size)
            else:
                if i + batch_size >= max_index:
                    i = min_index + lookback
                rows = np.arange(i, min(i + batch_size, max_index))
                i += len(rows)

            samples = np.zeros((len(rows),
                                lookback // step,
                                data.shape[-1]))
            targets = np.zeros((len(rows),))
            for j, row in enumerate(rows):
                indices = range(rows[j] - lookback, rows[j], step)
                samples[j] = data[indices]
                targets[j] = data[rows[j] + delay][1]
            #print(f'lookback:{lookback}, delay:{delay}, min_index{min_index}, max_index:{max_index}, shuffle{shuffle}, batch_size:{batch_size}, step: {step}')
            #print(f'Sample: {samples[0,0,0]} Target: {targets[0]}')
            yield samples, targets

    def prepare_data(self, features = None, target_feature = None, split=True, sample_size=None):
        """
        Loads data from the DataContainers dataset, using the framework specified in the constructor.
        :param features: Tuple of features to be included in X.  If None, all features will be included.
        :param target_feature: The feaute in the dataset that will be removed from the training data(X) and assigned to the label data(y).
        :param sample_size:
        :return:
        """
        self.log(f'Preparing data from dataset: {self.config.dataset_name} using {self.data_provider.name}')
        self.X_columns, self.X, self.y = self.data_provider.prepare_data(features, target_feature)
        if split:
            self.split(features)


    def get_column_values(self, file_path, column_name):
        return self.data_provider.get_column_values(file_path, column_name)

    def split(self, features = None, test_size=0.3, random_state=42):
        (self.X_train, self.y_train), (self.X_test, self.y_test) = self.data_provider.split(self.X, self.y)

    def prepare_imdb_data(self):
        # Get X and y (training data and labels) from imdb dataset
        raw_texts, raw_labels = self.get_text_data()
        tokenizer = Tokenizer(num_words=self._max_words)
        tokenizer.fit_on_texts(raw_texts)
        self.Tokenizer = tokenizer
        tokens, word_index = self.tokenize_raw_data(raw_texts)
        data = pad_sequences(tokens, maxlen=self._max_len)
        labels = np.asarray(raw_labels)
        self.log(f'Shape of X: {data.shape}')
        self.log(f'Shape of y: {labels.shape}')

        # Shuffle data so that positive and negative reviews are not grouped together
        indeces = np.arange(data.shape[0])
        np.random.shuffle(indeces)
        data = data[indeces]
        labels = labels[indeces]

        # Splice validation set
        self.X_train = data[:self._training_samples]
        self.y_train = labels[:self._training_samples]
        self.X_val = data[self._training_samples:]
        self.y_val = labels[self._training_samples:]

        # Build word embeddings
        embeddings = self.get_embeddings()

        '''
        embedding_dim = 100
        embeddings_matrix = np.zeros((self._max_words, embedding_dim))
        for word, i in word_index.items():
            if i < self._max_words:
                embedding_vector = embeddings.get(word)
                if (embedding_vector is not None):
                    embeddings_matrix[i] = embedding_vector
        '''
        self._embeddings_matrix = self.build_embedding_matrix(word_index, embeddings)

    def prepare_dataOLD(self):
        from keras.datasets import imdb
        from keras import preprocessing
        (raw_X_train, self.y_train), (raw_X_test, self.y_test) = imdb.load_data()
        self.X_train = preprocessing.sequence.pad_sequences(raw_X_train, maxlen=self._max_len)
        self.X_test = preprocessing.sequence.pad_sequences(raw_X_test, maxlen=self._max_len)

    def prepare_file_data(self, sample_size):
        dir = os.path.join(self.Base_Directory, 'data', 'jena_climate')
        fname = os.path.join(dir, 'jena_climate_2009_2016.csv')
        with open(fname, 'r') as f:
            raw_data = f.read()
        f.close()
        all_lines = raw_data.split('\n')
        header = all_lines[0].split(',')
        lines = all_lines[1:]

        raw_data = np.zeros((len(lines), len(header) - 1))
        for i, line in enumerate(lines):
            values = [float(x) for x in line.split(',')[1:]]
            raw_data[i,:] = values

        mean = raw_data[:sample_size].mean(axis=0)
        regularized_data = raw_data - mean
        std = regularized_data[:sample_size].std(axis = 0)
        self.data = regularized_data / std

        lookback =1440
        step =6
        delay = 144
        batch_size = 128
        min_index = 0
        max_index = 200000
        self.train_generator = self.generator(self.data, lookback, delay, min_index, max_index, True, batch_size, step)
        min_index = 200001
        max_index = 300000
        self.val_steps = (max_index - min_index - lookback) // batch_size
        self.val_generator = self.generator(self.data, lookback, delay, min_index, max_index, False, batch_size, step)
        min_index = 300001
        max_index = None
        self.test_steps = (len(self.data) - min_index - lookback) // batch_size
        self.test_generator = self.generator(self.data, lookback, delay, min_index, max_index, False, batch_size, step)

        # temp = data[:,1]
        # #plt.plot(range(len(temp)), temp)
        # #plt.show()
        # plt.figure(2)
        # plt.plot(range(14400), temp[:14400])
        # plt.show()
