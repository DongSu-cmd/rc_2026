'''
from pop import AI 

cnn = AI.CNN(output_size=10)

cnn.load_MNIST()
cnn.show_img(cnn.X_data[730])

import gym 
from pop import Util  
env = gym.make('CartPole-v1') 
env.reset()   
for _ in range(1000): 
     
    img = env.render(mode = 'rgb_array') 
     
    Util.imshow(“CartPole”, img, mode='RGB') 
     
    env.step(env.action_space.sample()) 
env.close()

import gym
from pop import AI, Util

DQN = AI.DQN(state_size=4)

env = gym.make('CartPole-v1')
for i_episode in range(1000):
    state = env.reset()
    step = 0
    total_reward = 0

    states, rewards, actions = [], [], []
    while True:
        img = env.render(mode='rgb_array')
        Util.imshow("CartPole", img, mode='RGB')

        action = DQN.run([state])

        state, reward, done, _ = env.step(action)

        states.append(state)
        rewards.append(reward)
        actions.append(action)

        total_reward += reward
        step += 1

        if done:
            print("Done after {} steps".format(step + 1))

            loss = DQN.train(states, rewards, actions)
            print('episode ' + str(i_episode + 1) + " reward : ", total_reward, ", loss : ", loss)
            break
'''
'''
import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior() 
 
C = tf.constant(10) 
V = tf.Variable(5) 
X = tf.placeholder(tf.int32) 
 
sess = tf.Session() 
sess.run(tf.global_variables_initializer()) 
 
F1 = C * X 
F2 = V * X 
 
R1 = sess.run(F1, feed_dict = {X : 2}) 
R2 = sess.run(F2, feed_dict = {X : 5}) 
 
 
print(R1) 
print(R2)

import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior() 
        
L1 = tf.matmul(arr_cds, arr_lux) #input – hidden 
L1 = tf.nn.relu(L1) 

model = tf.matmul(L2, W3) #hidden - output 
Loss = tf.reduce_mean(tf.reduce_mean(tf.sqaure(arr_lux - model))) 
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001) 
train_op = optimizer.minimize(Loss) 
 
sess = tf.Session() 
sess.run(tf.global_variables_initializer()) 

for i in range(500): 
 sess.run(train_op, feed_dict={X : X_data, Y : Y_data}) 
 loss = sess.run(Loss, feed_dict={X : X_data, Y : Y_data}) 
 print(loss) 
 
n = [[7], [-10], [358]] 
result = sess.run(model, feed_dict={X : n}) 
print(result)

from pop import Cds 
 
cds = Cds(7) 
 
value = cds.readAverage()
arr_cds = []
arr_lux = []

for i in range(10): 
    arr_cds.append(cds.readAverage()) 
    arr_lux.append(int(input("Lux: ")))
    from tensorflow import keras 

model = keras.models.Sequential() 
 
model.add(keras.layers.Input(shape=(1,))) 
model.add(keras.layers.Dense(1)) 
 
model.compile(loss='MAE', optimizer='Adam') 

 
model.fit(arr_cds, arr_lux, epochs=100) 
  
value = model.predict([[7], [-10], [358]]) 
print(value) 

import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior() 
        
L1 = tf.matmul(arr_cds, arr_lux) #input – hidden 
L1 = tf.nn.relu(L1) 

Loss = tf.reduce_mean(tf.reduce_mean(tf.sqaure(L1 - arr_lux))) 
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001) 
train_op = optimizer.minimize(Loss) 
 
sess = tf.Session() 
sess.run(tf.global_variables_initializer()) 
for i in range(500): 
 sess.run(train_op, feed_dict={arr_cds, arr_lux}) 
 loss = sess.run(Loss, feed_dict={arr_cds, arr_lux}) 
 print(loss) 
 
n = [[7], [-10], [358]] 
result = sess.run(L1, feed_dict={arr_cds : n}) 
print(result) 
'''
from pop import Pilot
import numpy as np
import time

Car = Pilot.AutoCar()

dataset = {'gyro': [], 'steer': []}

for n in np.arange(-1, 1.1, 0.2):
    n = round(n, 1)

    Car.steering = n
    Car.forward()

    time.sleep(0.5)

    m = Car.getGyro('z')

    time.sleep(0.5)

    Car.backward()

    time.sleep(1)

    Car.stop()

    dataset['gyro'].append(m)
    dataset['steer'].append(n)

    print({'gyro': m, 'steer': n})

from pop import AI

LR = AI.Linear_Regression(input_size=1, output_size=1)