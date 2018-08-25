是一个问句或答句,每一行中的每一个 id 代表问
句或答句中对应位置的词,格式如下:
185 4 4 4 146 131 5 1144 39 313 53 102 1176 12042 4 2020 9 2691 9
792 15 4
7518 4
2993 49 88 109 54 13 765 466 252 4 4 4
(3)采用编码器-解码器框架进行训练。
1.定义训练参数
这里,我们将参数写到一个专门的文件 seq2seq.ini 中,如下:
[strings]
# 模式 : train , test , serve
mode = train
train _ enc = data/train.enc
train _ dec = data/train.dec第 11 章
自然语言处理 ee
test _ enc = data/test.enc
test _ dec = data/test.enc
# 模型文件和词汇表的存储路径
working _ directory = working _ dir/
[ints]
# 词汇表大小
enc _ vocab _ size = 20000
dec _ vocab _ size = 20000
# LSTM 层数
num _ layers = 3
# 每层大小,可以取值: 128, 256, 512, 1024
layer _ size = 256
max _ train _ data _ size = 0
batch _ size = 64
# 每多少次迭代存储一次模型
steps _ per _ checkpoint = 300
[floats]
learning _ rate = 0.5 # 学习速率
learning _ rate _ decay _ factor = 0.99 # 学习速率下降系数
max _ gradient _ norm = 5.0
2.定义网络模型
下面来定广 seq2seq 模型,该模型的代码在 seq2seq_model.py 中,这个代码基于 TensorFlow
1
0.12 版本,读者可以重新安装试验。定广一个 seq2seq+Attention 模型类 ,里面主要包含 3 个
函数:
(1)初始化模型的函数(__init__);
(2)训练模型的函数(step);
(3)获取下一批次训练数据的函数(get_batch)。
我们首先来看如何初始化模型,如下:
class Seq2SeqModel(object):
def __ init __ (self, source _ vocab _ size, target _ vocab _ size, buckets, size,
num _ layers, max _ gradient _ norm, batch _ size, learning _ rate,
learning _ rate _ decay _ factor, use _ lstm=False,
num _ samples=512, forward _ only=False):
""" 构建模型
参数:
source _ vocab _ size: 问句词汇表大小
target _ vocab _ size: 答句词汇表大小
buckets: (I,O), 其中 I 的定最大输入长度, O 的定最大输出长度
1 参本论文《Grammar as a Foreign Language》:http://arxiv.org/abs/1412.7449。
193194
ff 第二篇
实战篇
size: 每一层的神经元数量
num _ layers: 模型层数
max _ gradient _ norm: 梯度将被削减到最大的规范
batch _ size: 批次大小。用于训练和预测的批次大小,可以不同
learning _ rate: 学习速率
learning _ rate _ decay _ factor: 调整学习速率
use _ lstm: 使用 LSTM 的元来代替 GRU 的元
num _ samples: 使用 softmox 的样本数
forward _ only: 是否仅构建前向传播
"""
self.source _ vocab _ size = source _ vocab _ size
self.target _ vocab _ size = target _ vocab _ size
self.buckets = buckets
self.batch _ size = batch _ size
self.learning _ rate = tf.Variable(float(learning _ rate), trainable=False)
self.learning _ rate _ decay _ op = self.learning _ rate.assign(
self.learning _ rate * learning _ rate _ decay _ factor)
self.global _ step = tf.Variable(0, trainable=False)
output _ projection = None
softmax _ loss _ function = None
# 如果样本量比词汇表的量小,那么要用抽样的 softmax
if num _ samples > 0 and num _ samples < self.target _ vocab _ size:
w = tf.get _ variable("proj _ w", [size, self.target _ vocab _ size])
w _ t = tf.transpose(w)
b = tf.get _ variable("proj _ b", [self.target _ vocab _ size])
output _ projection = (w, b)
def sampled _ loss(inputs, labels):
labels = tf.reshape(labels, [-1, 1])
return tf.nn.sampled _ softmax _ loss(w _ t, b, inputs, labels, num _ samples,
self.target _ vocab _ size)
softmax _ loss _ function = sampled _ loss
# 构建 RNN
single _ cell = tf.nn.rnn _ cell.GRUCell(size)
if use _ lstm:
single _ cell = tf.nn.rnn _ cell.BasicLSTMCell(size)
cell = single _ cell
if num _ layers > 1:
cell = tf.nn.rnn _ cell.MultiRNNCell([single _ cell] * num _ layers)
# Attention 模型
def seq2seq _ f(encoder _ inputs, decoder _ inputs, do _ decode):
return tf.nn.seq2seq.embedding _ attention _ seq2seq(
encoder _ inputs, decoder _ inputs, cell,
num _ encoder _ symbols=source _ vocab _ size,
num _ decoder _ symbols=target _ vocab _ size,
embedding _ size=size,
output _ projection=output _ projection,
feed _ previous=do _ decode)第 11 章
自然语言处理 ee
# 给模型填充数据
self.encoder _ inputs = []
self.decoder _ inputs = []
self.target _ weights = []
for i in xrange(buckets[-1][0]):
self.encoder _ inputs.append(tf.placeholder(tf.int32, shape=[None],
name="encoder{0}".format(i)))
for i in xrange(buckets[-1][1] + 1):
self.decoder _ inputs.append(tf.placeholder(tf.int32, shape=[None],
name="decoder{0}".format(i)))
self.target _ weights.append(tf.placeholder(tf.float32, shape=[None],
name="weight{0}".format(i)))
# targets 的值是解码器偏移 1 位
targets = [self.decoder _ inputs[i + 1]
for i in xrange(len(self.decoder _ inputs) - 1)]
# 训练模型的输出
if forward _ only:
self.outputs, self.losses = tf.nn.seq2seq.model _ with _ buckets(
self.encoder _ inputs, self.decoder _ inputs, targets,
self.target _ weights, buckets, lambda x, y: seq2seq _ f(x, y, True),
softmax _ loss _ function=softmax _ loss _ function)
if output _ projection is not None:
for b in xrange(len(buckets)):
self.outputs[b] = [
tf.matmul(output, output _ projection[0]) + output _ projection[1]
for output in self.outputs[b]
]
else:
self.outputs, self.losses = tf.nn.seq2seq.model _ with _ buckets(
self.encoder _ inputs, self.decoder _ inputs, targets,
self.target _ weights, buckets,
lambda x, y: seq2seq _ f(x, y, False),
softmax _ loss _ function=softmax _ loss _ function)
# 训练模型时,更新梯度
params = tf.trainable _ variables()
if not forward _ only:
self.gradient _ norms = []
self.updates = []
opt = tf.train.GradientDescentOptimizer(self.learning _ rate)
for b in xrange(len(buckets)):
gradients = tf.gradients(self.losses[b], params)
clipped _ gradients, norm = tf.clip _ by _ global _ norm(gradients,
max _ gradient _ norm)
self.gradient _ norms.append(norm)
self.updates.append(opt.apply _ gradients(
zip(clipped _ gradients, params), global _ step=self.global _ step))
195196
ff 第二篇
实战篇
self.saver = tf.train.Saver(tf.all _ variables())
接着,定广运行模型的每一步:
def step(self, session, encoder _ inputs, decoder _ inputs, target _ weights,
bucket _ id, forward _ only):
""" 运行模型的每一步
参数 :
session: tensorflow session
encoder _ inputs: 问句向量序列
decoder _ inputs: 答句向量序列
target _ weights: target weights
bucket _ id: 输入的 bucket _ id
forward _ only: 是否只做前向传播
"""
encoder _ size, decoder _ size = self.buckets[bucket _ id]
if len(encoder _ inputs) != encoder _ size:
raise ValueError("Encoder length must be equal to the
" %d != %d." % (len(encoder _ inputs),
if len(decoder _ inputs) != decoder _ size:
raise ValueError("Decoder length must be equal to the
" %d != %d." % (len(decoder _ inputs),
if len(target _ weights) != decoder _ size:
raise ValueError("Weights length must be equal to the
" %d != %d." % (len(target _ weights),
one in bucket,"
encoder _ size))
one in bucket,"
decoder _ size))
one in bucket,"
decoder _ size))
# 输入填充
input _ feed = {}
for l in xrange(encoder _ size):
input _ feed[self.encoder _ inputs[l].name] = encoder _ inputs[l]
for l in xrange(decoder _ size):
input _ feed[self.decoder _ inputs[l].name] = decoder _ inputs[l]
input _ feed[self.target _ weights[l].name] = target _ weights[l]
last _ target = self.decoder _ inputs[decoder _ size].name
input _ feed[last _ target] = np.zeros([self.batch _ size], dtype=np.int32)
# 输出填充: 与是否有后向传播有关
if not forward _ only:
output _ feed = [self.updates[bucket _ id],
self.gradient _ norms[bucket _ id],
self.losses[bucket _ id]]
else:
output _ feed = [self.losses[bucket _ id]]
for l in xrange(decoder _ size):
output _ feed.append(self.outputs[bucket _ id][l])第 11 章
自然语言处理 ee
outputs = session.run(output _ feed, input _ feed)
if not forward _ only:
return outputs[1], outputs[2], None # 有后向传播下的输出: 梯度,损失值 , None
else:
return None, outputs[0], outputs[1:] # 仅有前向传播下的输出: None ,损失值 , outputs
接下来是 get_batch 函数,它的主要作用是为训练的每一步(step)产生一个批次的数据。
def get _ batch(self, data, bucket _ id):
"""
这个函数的作用是从的定的桶中获取一个批次的随机数据,在训练的每步( step )中使用
参数:
data :长度为( self.buckets )的元组,其中每个元素都包含用于创建批次的输入和输出数据对的列表
bucket _ id :整数,从哪个 bucket 获取本批次
返回:
一个包含三项的元组( encoder _ inputs , decode _ inputs , target _ weights )
"""
3.训练模型
修改 seq2seq.ini 文件中的 mode 值,当值为“train”时,可以运行 execute.py 进行训练。关
键逻辑代码如下:
def train():
# 准备数据集
print("Preparing data in %s" % gConfig['working _ directory'])
enc _ train, dec _ train, enc _ dev, dec _ dev, _ , _ = data _ utils.prepare _ custom _ data
(gConfig['working _ directory'],gConfig['train _ enc'],gConfig['train _ dec'],
gConfig['test _ enc'],gConfig['test _ dec'],gConfig['enc _ vocab _ size'],
gConfig['dec _ vocab _ size'])
config = tf.ConfigProto()
config.gpu _ options.allocator _ type = 'BFC'
with tf.Session(config=config) as sess:
# 构建模型
print("Creating %d layers of %d units." % (gConfig['num _ layers'], gConfig
['layer _ size']))
model = create _ model(sess, False)
# 把数据读入桶( bucket )中,并计算桶的大小
print ("Reading development and training data (limit: %d)."
% gConfig['max _ train _ data _ size'])
dev _ set = read _ data(enc _ dev, dec _ dev)
train _ set = read _ data(enc _ train, dec _ train, gConfig['max _ train _ data _ size'])
train _ bucket _ sizes = [len(train _ set[b]) for b in xrange(len( _ buckets))]
train _ total _ size = float(sum(train _ bucket _ sizes))
train _ buckets _ scale = [sum(train _ bucket _ sizes[:i + 1]) / train _ total _ size
for i in xrange(len(train _ bucket _ sizes))]
# 开始训练循环
197198
ff 第二篇
实战篇
step _ time, loss = 0.0, 0.0
current _ step = 0
previous _ losses = []
while True:
# 随机生成一个 0-1 的数,在生成 bucket _ id 中使用
random _ number _ 01 = np.random.random _ sample()
bucket _ id = min([i for i in xrange(len(train _ buckets _ scale))
if train _ buckets _ scale[i] > random _ number _ 01])
# 获取一个批次的数据,并进行一步训练
start _ time = time.time()
encoder _ inputs, decoder _ inputs, target _ weights = model.get _ batch(
train _ set, bucket _ id)
_ , step _ loss, _ = model.step(sess, encoder _ inputs, decoder _ inputs,
target _ weights, bucket _ id, False)
step _ time += (time.time() - start _ time) / gConfig['steps _ per _ checkpoint']
loss += step _ loss / gConfig['steps _ per _ checkpoint']
current _ step += 1
# 保存检查点文件,打印统计数据
if current _ step % gConfig['steps _ per _ checkpoint'] == 0:
perplexity = math.exp(loss) if loss < 300 else float('inf')
print ("global step %d learning rate %.4f step-time %.2f perplexity "
"%.2f" % (model.global _ step.eval(), model.learning _ rate.eval(),
step _ time, perplexity))
# 如果损失值在最近 3 次内没有再降低,就减小学习率 .
if len(previous _ losses) > 2 and loss > max(previous _ losses[-3:]):
sess.run(model.learning _ rate _ decay _ op)
previous _ losses.append(loss)
# 保存检查点文件,并把计数器和损失值归零
checkpoint _ path = os.path.join(gConfig['working _ directory'], "seq2seq.ckpt")
model.saver.save(sess, checkpoint _ path, global _ step=model.global _ step)
step _ time, loss = 0.0, 0.0
4.验证模型
修改 seq2seq.ini 文件中的 mode 值,当值为“test”时,可以运行 execute.py 进行测试。关
键逻辑代码如下:
def decode():
with tf.Session() as sess:
# 建立模型,并定广超参数 batch _ size
model = create _ model(sess, True)
model.batch _ size = 1 # 这里一次只解码一个句子
# 加载词汇表文件
enc _ vocab _ path = os.path.join(gConfig['working _ directory'],"vocab%d.enc" %第 11 章
自然语言处理 ee
gConfig['enc _ vocab _ size'])
dec _ vocab _ path = os.path.join(gConfig['working _ directory'],"vocab%d.dec" %
gConfig['dec _ vocab _ size'])
enc _ vocab, _ = data _ utils.initialize _ vocabulary(enc _ vocab _ path)
_ , rev _ dec _ vocab = data _ utils.initialize _ vocabulary(dec _ vocab _ path)
# 对标准输入的句子进行解码
sys.stdout.write("> ")
sys.stdout.flush()
sentence = sys.stdin.readline()
while sentence:
# 得到输入句子的 token-ids
token _ ids = data _ utils.sentence _ to _ token _ ids(tf.compat.as _ bytes(sentence),
enc _ vocab)
# 计算这个 token _ ids 属于哪一个桶( bucket )
bucket _ id = min([b for b in xrange(len( _ buckets))
if _ buckets[b][0] > len(token _ ids)])
# 将句子送入到模型中
encoder _ inputs, decoder _ inputs, target _ weights = model.get _ batch(
{bucket _ id: [(token _ ids, [])]}, bucket _ id)
_ , _ , output _ logits = model.step(sess, encoder _ inputs, decoder _ inputs,
target _ weights, bucket _ id, True)
# 这是一个贪心的解码器,输出只是 output _ logits 的 argmaxes 。
outputs = [int(np.argmax(logit, axis=1)) for logit in output _ logits]
# 如果输出中有 EOS 符号,在 EOS 处切断
if data _ utils.EOS _ ID in outputs:
outputs = outputs[:outputs.index(data _ utils.EOS _ ID)]
# 打印出与输出句子对应的法语句子
print(" ".join([tf.compat.as _ str(rev _ dec _ vocab[output]) for output in
outputs]))
print("> ", end="")
sys.stdout.flush()
sentence = sys.stdin.readline()
