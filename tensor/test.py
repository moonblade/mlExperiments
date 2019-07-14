import tensorflow as tf

sess = tf.Session()
a = tf.constant(10)
b = tf.constant(12)
print(sess.run(a+b))