import tensorflow as tf
import warnings
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from tqdm import tqdm
import time


warnings.filterwarnings('ignore')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

embed_model = SentenceTransformer("all-mpnet-base-v2" )

class Embed(Model):
    def __init__(self):
        super(Embed, self).__init__()
        self.dense1 = Dense(256)
        self.dense2 = Dense(128)
    
    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return x
    
class Siamese(Model):
    def __init__(self):
        super(Siamese, self).__init__()
        self.embed1 = Embed()
        self.embed2 = Embed()
    
    def call(self, inputs):
        x1 = self.embed1(inputs[:,0])
        x2 = self.embed2(inputs[:,1])
        return x1,x2


# eval(SystemPrompt, UserPrompt1, eval_mcon)
def eval(SystemPrompt, UserPrompt, model):
    t = time.time()
    sp = embed_model.encode(SystemPrompt)
    up = embed_model.encode(UserPrompt)
    mx = np.zeros((1,2,768))
    mx[0][0] = sp
    mx[0][1] = up
    es,eu = model(mx)
    dot = tf.squeeze(tf.matmul(es,tf.transpose(eu)))
    dx = tf.math.sqrt(tf.squeeze(tf.reduce_sum(tf.math.square(es),axis=-1)))
    dy = tf.math.sqrt(tf.squeeze(tf.reduce_sum(tf.math.square(eu),axis=-1)))
    cs = dot/(dx*dy)
    cs = (cs+1)/2
    print("Time taken for eval: ",time.time()-t)
    if cs > 0.5:
        return True
    else:
        return False

eval_model = Siamese()
visible = Input(shape=(2,768))
layer = eval_model(visible)
eval_mcon = Model(inputs=visible, outputs=layer)

