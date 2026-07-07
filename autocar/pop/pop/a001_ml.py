import numpy as np

a1 = [60, 80, 100, 120, 140, 160, 180]
a2 = [0, 1, 0, 1, 1, 0, 1, 0, 1]
a3 = [1, 0, 1, 1, 0, 1, 1, 0, 1]
a4 = [0, 1, 1, 1, 1, 1, 1, 1, 0]

import tensorflow as tf

X_mean = X.mean()
X_std = X.std()

X_scaled = (X - X_mean) / X_std

model = tf.keras.Sequential(tf.keras.layers.Dense(3, input_shape=[1]), activation = "softmax")

model.compile(optimizer=tf.keras.layers.optimizers.Adam(learning_rate = 0.05), loss="categorical_crossentropy", metrics=["accuracy"])