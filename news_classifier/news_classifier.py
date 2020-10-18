from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GRU
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
from os import listdir
import re


class NewsClassifier:
    MODEL_FILE = 'best_model.h5'

    # Максимальное количество слов
    num_words = 10000
    # Максимальная длина новости
    max_news_len = 500
    # Количество классов новостей
    nb_classes = 9

    def __init__(self):
        f = open('news_classifier/classes.txt', 'r')
        self.classes = f.read().title().split('\n')
        f.close()
        self.tokenizer = Tokenizer(num_words=NewsClassifier.num_words)
        if NewsClassifier.MODEL_FILE in listdir('news_classifier/'):
            self.model = load_model('news_classifier/' + NewsClassifier.MODEL_FILE)
        else:
            # NewsClassifier.txt_to_csv()
            x_train, y_train = self.prepare_data()
            self.model = self.create_model()
            checkpoint_callback_gru = ModelCheckpoint(
                NewsClassifier.MODEL_FILE, monitor='val_accuracy', save_best_only=True, verbose=1)
            history_gru = self.model.fit(
                x_train, y_train, epochs=5, batch_size=128, validation_split=0.1, callbacks=[checkpoint_callback_gru])
            print(f"[INFO] Доля верных ответов на обучающем наборе {history_gru.history['accuracy']}")
            print(f"[INFO] Доля верных ответов на проверочном наборе {history_gru.history['val_accuracy']}")

    async def predict(self, text):
        test_sequences = self.tokenizer.texts_to_sequences([text])
        x_test = pad_sequences(test_sequences, maxlen=NewsClassifier.max_news_len)
        pred = self.model.predict(x_test)[0]
        return self.classes[pred.argmax(pred)]

    @staticmethod
    def txt_to_csv():
        f_name = 'news_classifier/text.txt'
        csv = open('news_classifier/train.csv', 'w')
        f = open(f_name, 'r')
        for message in f.read().split('========'):
            print('===========================\n', message)
            a = input()
            if len(a) == 0:
                continue
            elif int(a) in range(1, 10):
                message = re.sub(r'[\n|-|—|.|,|:|\/|-]', '', message)
                message = re.sub(r'http\S+', '', message)
                csv.write(f'"{a}","{message[:100]}","{message}\n"')
            elif a == 'exit':
                break
        f.close()
        csv.close()

    def prepare_data(self):
        train = pd.read_csv('train.csv', header=None, names=['class', 'title', 'text'])
        news = train['text']
        y_train = utils.to_categorical(train['class'] - 1, NewsClassifier.nb_classes)
        self.tokenizer.fit_on_texts(news)
        sequences = self.tokenizer.texts_to_sequences(news)
        x_train = pad_sequences(sequences, maxlen=NewsClassifier.max_news_len)
        return x_train, y_train

    @staticmethod
    def create_model():
        model_gru = Sequential()
        model_gru.add(Embedding(NewsClassifier.num_words, 32, input_length=NewsClassifier.max_news_len))
        model_gru.add(GRU(16))
        model_gru.add(Dense(9, activation='softmax'))
        model_gru.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model_gru.summary()
        return model_gru


news_classifier = NewsClassifier()
