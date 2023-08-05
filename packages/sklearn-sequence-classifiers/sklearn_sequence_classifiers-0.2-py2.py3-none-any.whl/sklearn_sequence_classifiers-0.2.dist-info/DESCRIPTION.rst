Sequence classifiers for scikit-learn
=====================================

Convolutional neural network sequence classifier with a scikit-learn interface.

Usage example
-------------

Predicting IMDB review sentiments.::

    from keras.datasets import imdb
    from keras.preprocessing import sequence
    from sequence_classifiers import CNNSequenceClassifier

    maxlen = 400
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=5000)
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

    clf = CNNSequenceClassifier(epochs=2)
    clf.fit(x_train, y_train)
    print(clf.score(x_test, y_test))


