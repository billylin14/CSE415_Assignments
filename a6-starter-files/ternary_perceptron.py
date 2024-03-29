'''ternary_perceptron.py
Complete this python file as part of Part B.
You'll be filling in with code to implement:

a 3-way classifier
a 3-way weight updater

This program can be run from the given Python program
called run_3_class_4_feature_iris_data.py.

 
'''
def student_name():
  return "Billy Lin" # Replace with your own name.
  

def classify(W, x_vector):
  '''Assume W = [W0, W1, W2] where each Wi is a vector of
     weights = [w_0, w_1, ..., w_{n-1}, biasweight]
     Assume x_vector = [x_0, x_1, ..., x_{n-1}]
       Note that y (correct class) is not part of the x_vector.
     Return 0, 1, or 2,
       depending on which weight vector gives the highest
       dot product with the x_vector augmented with the 1 for bias
       in position n.
  '''
  n = [0, 0, 0]
  for i in range(len(W)):
    for j in range(len(x_vector)):
      n[i] += W[i][j]*x_vector[j]
    n[i] += W[i][-1]
  return argmax(n)

# Helper function for finding the arg max of elements in a list.
# It returns the index of the first occurrence of the maximum value.
def argmax(lst):
  idx, mval = -1, -1E20
  for i in range(len(lst)):
    if lst[i]>mval:
      mval = lst[i]
      idx = i
  return idx

def train_with_one_example(W, x_vector, y, alpha):
  '''Assume weights are as in the above function classify.
     Also, x_vector is as above.
     Here y should be 0, 1, or 2, depending on which class of
     irises the example belongs to.
     Learning is specified by alpha.
  '''
  idx = classify(W, x_vector)
  if idx == y: #if correctly classified
    return (W, False) # No, there was no change to the weights
  else: #if misclassified
    for i in range(len(x_vector)):
      W[idx][i] -= alpha*x_vector[i]  #punish the wrong guess
      W[y][i] += alpha*x_vector[i]    #raise score of right answer
    W[idx][-1] -= alpha
    W[y][-1] += alpha
    return (W, True) # Yes, there was a change to the weights

WEIGHTS = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
ALPHA = 1.0
n_epochs = 0

def train_for_an_epoch(training_data, reporting=False):
  '''Go through the given training examples once, in the order supplied,
  passing each one to train_with_one_example.
  Return the weight vector and the number of weight updates.
  (If zero, then training has converged.)
  '''
  global WEIGHTS, ALPHA, n_epochs
  changed_count = 0
  for example in training_data:
    x_vector = example[:-1]
    y = example[-1]
    (new_weight, changed) = train_with_one_example(WEIGHTS, x_vector, y, ALPHA)
    if changed:
      WEIGHTS = new_weight
      changed_count += 1
    if reporting:
      print(WEIGHTS, changed_count)
  n_epochs += 1
  if reporting:
    print("n_epochs=", n_epochs)
  return changed_count

# THIS MAY BE HELPFUL DURING DEVELOPMENT:
TEST_DATA = [
[20, 25, 1, 1, 0],
[-2, 7, 2, 1, 1],
[1, 10, 1, 2, 1],
[3, 2, 1, 1, 2],
[5, -2, 1, 1, 2] ]

def test():
  print("Starting test with 3 epochs.")
  for i in range(10):
    train_for_an_epoch(TEST_DATA, True)
  print("End of test.")
  print("WEIGHTS: ", WEIGHTS)

if __name__=='__main__':
  test()

