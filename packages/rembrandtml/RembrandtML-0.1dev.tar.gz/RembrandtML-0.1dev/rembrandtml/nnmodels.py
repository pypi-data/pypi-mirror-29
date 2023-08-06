import os, time, dill
import numpy as np
from keras import models
from keras import layers
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Flatten, Dense, Embedding, LSTM

from rembrandtml.models import MLModel


class NeuralNetwork(MLModel):
    def __init__(self, model_config, data_container, instrumentation):
        super(NeuralNetwork, self).__init__(model_config, data_container, instrumentation)


    @staticmethod
    def plot_filter():
        from keras.applications import VGG16
        from keras import backend as K
        model = keras_models.ModelRepository.get_vgg16()


    @staticmethod
    def plot_activation():
        from keras.models import load_model
        from keras.preprocessing import image
        import numpy as np
        model_path = os.path.abspath(os.path.join(os.getcwd() ,"../../../models/DogsVsCats_small_1.h5"))
        model = load_model(model_path)
        print(model.summary())
        img_path =  os.path.abspath(os.path.join(os.getcwd() ,"../../../data/dogs_and_cats/test/dogs/dog.1045.jpg"))
        img = image.load_img(img_path, target_size=(150, 150))
        img_tensor = image.img_to_array(img)
        print(img_tensor.shape)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        print(img_tensor.shape)
        img_tensor /= 255
        import matplotlib.pyplot as plt
        plt.imshow(img_tensor[0])
        #plt.show()
        plt.clf()
        from keras import models
        layer_outputs = [layer.output for layer in model.layers[:8]]
        activation_model =models.Model(inputs=model.input, outputs=layer_outputs)
        activations = activation_model.predict(img_tensor)
        first_layer_activation = activations[0]
        plt.matshow(first_layer_activation[0,:,:,7], cmap='viridis')
        plt.show()
        #text = input('Press any key to continue...')



    @property
    def TestData(self):
        from keras.preprocessing.sequence import pad_sequences
        if(self.X_test == None):
            data_dir = os.path.join(self.Base_Directory, os.path.join('data','imdb','aclImdb','test'))
            raw_X_test, raw_y_test = self.get_test_data_from_file(data_dir, ['pos', 'neg'])
            tokens, word_index = self.tokenize_raw_data(raw_X_test)
            self.X_test = pad_sequences(tokens, maxlen=self._max_len)
            self.y_test = np.asarray(raw_y_test)
        return self.X_test, self.y_test

    ''' class_sub_dirs is a list of subdirectories where test files are stored.
    Each directory name is a class for the classification'''
    def get_test_data_from_file(self, data_dir, class_sub_dirs):
        texts = []
        labels = []
        for label_class in class_sub_dirs:
            files_dir = os.path.join(data_dir, label_class)
            data_files = os.listdir(files_dir)
            self.log(f'Found {len(data_files)} in {data_dir}')
            for fname in data_files:
                if(fname[-4:] == '.txt'):
                    with open(os.path.join(files_dir, fname), encoding='utf8') as f:
                        texts.append(f.read())
                    f.close()
                    # This is just a placehold for better logic
                    if(label_class == 'pos'):
                        labels.append(1)
                    else:
                        labels.append(0)
        return texts, labels

class ConvolutionalNeuralNetwork(NeuralNetwork):

    pass


class ConvnetDogsVsCats(NeuralNetwork):

    def __init__(self, name, ml_config, instrumentation):
        super(ConvnetDogsVsCats, self).__init__(name, ml_config, instrumentation)
        self.ValidationGenerator = None
        self.TrainGenerator = None
        self.ModelFile = 'DogsVsCats_small_1.h5'


    def build_model(self):
        self.Model = models.Sequential()

        self.Model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
        self.Model.add(layers.MaxPool2D((2,2)))
        self.Model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        self.Model.add(layers.MaxPool2D((2,2)))
        self.Model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        self.Model.add(layers.MaxPool2D((2,2)))
        self.Model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        self.Model.add(layers.MaxPool2D((2,2)))

        self.Model.add(layers.Flatten())
        self.Model.add(layers.Dense(512, activation='relu'))
        self.Model.add(layers.Dense(1, activation='sigmoid'))

        self.log(self.Model.summary())

        self.Model.compile(loss='binary_crossentropy',
                            optimizer=optimizers.RMSprop(lr=1e-4),
                            metrics=['acc'])


    def prepare_data(self):
        train_datagen = ImageDataGenerator(rescale=1./255)
        test_datagen = ImageDataGenerator(rescale=1./255)
        self.TrainGenerator = train_datagen.flow_from_directory(self.Config.TrainDir,
                                                            target_size=(150, 150),
                                                            batch_size=20,
                                                            class_mode='binary')
        self.ValidationGenerator = test_datagen.flow_from_directory(self.Config.ValidationDir,
                                                                target_size=(150, 150),
                                                                batch_size=20,
                                                                class_mode='binary')
    def fit_and_save(self):
        if(self.TrainGenerator == None) or (self.ValidationGenerator == None):
            self.prepare_data()

        conv_base = None
        if(self.Config.Mode == 'p'):
            start = time.time()
            conv_base = keras_models.ModelRepository().get_vgg16()
            self.log(f'elapsed: {time.time() - start}', 'd')

        history = self._model.fit_generator(self.TrainGenerator,
                                            steps_per_epoch=100,
                                            epochs=30,
                                            validation_data=self.ValidationGenerator,
                                            validation_steps=50)

        self._model.save(self.unique_file_name(self.ModelFile, self.ModelFileAttribute))

        '''
        if(self.Config.Verbose == True):
            with open(self.HistoryFile, 'wb') as file_handle:
                dill.dump(history, file_handle)
        '''

    def create_dir(base_dir, name):
        new_dir = os.path.join(base_dir, name)
        if(os.path.isdir(new_dir) == False):
            os.mkdir(new_dir)
        return new_dir

    def copy_files(file_name, index_range, src_dir, dest_dir):
        fnames = ['{}.{}.jpg'.format(file_name, i) for i in index_range]
        for fname in fnames:
            src = os.path.join(src_dir, fname)
            dest = os.path.join(dest_dir, fname)
            shutil.copyfile(src, dest)
        print(f'Copied {len(fnames)} files from {src_dir} to {dest_dir}')

    def copy_image_files(src, dest):
        if(os.path.isdir(dest) == False):
            os.mkdir(dest)

        train_dir = create_dir(dest, 'train')
        val_dir = create_dir(dest, 'validation')
        test_dir = create_dir(dest, 'test')
        train_cats_dir = create_dir(train_dir, 'cats')
        train_dogs_dir = create_dir(train_dir, 'dogs')
        val_cats_dir = create_dir(val_dir, 'cats')
        val_dogs_dir = create_dir(val_dir, 'dogs')
        test_cats_dir = create_dir(test_dir, 'cats')
        test_dogs_dir = create_dir(test_dir, 'dogs')

        copy_files('dog', range(1000), src, train_dogs_dir)
        copy_files('dog', range(1000, 1500), 'D:\code\ML\data\dogs_and_cats\kaggle\\train\dogs', test_dogs_dir)
        copy_files('dog', range(1500, 2000), 'D:\code\ML\data\dogs_and_cats\kaggle\\train\dogs', val_dogs_dir)


        copy_files('cat', range(1000), 'D:\code\ML\data\dogs_and_cats\kaggle\\train\cats', train_cats_dir)
        copy_files('cat', range(1000, 1500), 'D:\code\ML\data\dogs_and_cats\kaggle\\train\cats', test_cats_dir)
        copy_files('cat', range(1500, 2000), 'D:\code\ML\data\dogs_and_cats\kaggle\\train\cats', val_cats_dir)


class RecurrentNeuralNetwork(NeuralNetwork):

    def __init__(self, name, ml_config, instrumentation):
        super(RecurrentNeuralNetwork, self).__init__(name, ml_config, instrumentation)
        self._max_len = 20
        self._max_features = 10000
        self._max_words = 10000
        self._embeddings_dim = 100
        self._training_samples = 5#200
        self._validation_samples = 5#10000
        self._embeddings_matrix = None

    def get_text_data(self):
        train_dir = os.path.join(self.Base_Directory, os.path.join('data', 'imdb', 'aclImdb', 'train'))
        self.log(f'Reading files in {train_dir}', 'd')
        labels = []
        texts = []

        for label_type in ['neg', 'pos']:
            dir_name = os.path.join(train_dir, label_type)
            fnames = os.listdir(dir_name)
            self.log(f'Found {len(fnames)} files.  Sample size: {self._training_samples}', 'd')
            file_count = 0
            for fname in fnames:
                if (fname[-4:] == '.txt'):
                    if(file_count >= self._training_samples):
                        self.log(f'Breaking after {file_count} because training sample size is {self._training_samples}')
                        break;
                    file_count += 1
                    data_file = os.path.join(dir_name, fname)
                    self.log(f'Opening {data_file}', 'n')
                    with open(data_file, encoding='utf8') as f:
                        texts.append(f.read())
                    f.close()
                    if label_type == 'neg':
                        labels.append(0)
                    else:
                        labels.append(1)
        return texts, labels

    def tokenize_raw_data(self, raw_texts):
        sequences = self.Tokenizer.texts_to_sequences(raw_texts)
        word_index = self.Tokenizer.word_index

        self.log(f'Found {len(word_index)} unique tokens')
        return sequences, word_index

    def get_embeddings(self):
        glove_dir = os.path.join(self.Base_Directory, os.path.join('data', 'wordEmbeddings', 'GloVe'))
        glove_file = os.path.join(glove_dir, 'glove.6B.100d.txt')
        self.log(f'Reading word embeddings from {glove_dir}', 'd')
        embeddings_index = {}
        with open(glove_file, encoding='utf8') as f:
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs
        f.close()
        self.log(f'Found {len(embeddings_index)} word vectors.', 'd')
        return embeddings_index

    def build_embedding_matrix(self, words, embeddings):

        self._embeding_matrix = np.zeros((self._max_words, self._embeddings_dim))
        for word, i in words.items():
            if i < self._max_words:
                embedding_vector = embeddings.get(word)
                if(embedding_vector is not None):
                    self._embeding_matrix[i] = embedding_vector
        return self._embeding_matrix


    def predict(self, X):
        prediction = self.Model.predict(X, steps=1)
        return prediction
    def build_model(self):
        self.Model = models.Sequential()
        self.Model.add(Embedding(self._max_words, self._embeddings_dim, input_length = self._max_len))
        self.Model.add(Flatten())
        self.Model.add(Dense(32, activation='relu'))
        self.Model.add(Dense(1, activation='sigmoid'))

        # load word embeddings into the Embedding layer
        self.Model.layers[0].set_weights([self._embeddings_matrix])

        # freeze the pretrained layer
        self.Model.layers[0].trainable = False

        if(self.Config.Verbose):
            self.log(self.Model.summary(), 'd')

        self.Model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])

    def fit_and_save(self):
        history = self.Model.fit(self.X_train, self.y_train,
                                 epochs=self.Config.Epochs,
                                 batch_size=self.Config.BatchSize,
                                 validation_data=(self.X_val, self.y_val))

        weights_file = self.unique_file_name(NeuralNetwork.__dict__['WeightsFile'], NeuralNetwork.__dict__['WeightsFileAttribute'])
        self.Model.save_weights(self.WeightsFile)
        model_file = self.unique_file_name(NeuralNetwork.__dict__['ModelFile'], NeuralNetwork.__dict__['ModelFileAttribute'])
        self.Model.save(model_file)
        return history


class LstmRNN(RecurrentNeuralNetwork):

    def __init__(self, name, ml_config, instrumentation):
        super(LstmRNN, self).__init__(name, ml_config, instrumentation)

    def build_model(self):
        self.Model = models.Sequential()
        self.Model.add(Embedding(self._max_features, 32))
        self.Model.add(LSTM(32))
        self.Model.add(Dense(1, activation='sigmoid'))

        if(self.Config.Verbose):
            self.log(self.Model.summary(), 'd')

        self.Model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])

class GruNN(NeuralNetwork):
    def __init__(self, name, ml_config, instrumentation):
        super(GruNN, self).__init__(name, ml_config, instrumentation)
        self._max_len = 20
        self._max_features = 10000
        self._max_words = 10000
        self._embeddings_dim = 100
        self._training_samples = 5#200
        self._validation_samples = 5#10000
        self._embeddings_matrix = None

    def build_model(self, data_container):
        self.DataContainer = data_container
        self.Model = Sequential()
        self.Model.add(layers.GRU(32,
                                  input_shape=(None, self.DataContainer.Data.shape[-1]),
                                  dropout = self.Config.ModelConfig.Dropout,
                                  recurrent_dropout = self.Config.ModelConfig.RecurrentDropout))
        self.Model.add(layers.Dense(1))

        self.Model.compile(optimizer=self.Config.ModelConfig.optimizer,
                           loss=self.Config.ModelConfig.loss_function,
                           metrics=self.Config.ModelConfig.metrics)


def main():
    print('hellow from nn.py')
    NeuralNetwork.plot_activation()

if(__name__ == '__main__'):
    main()