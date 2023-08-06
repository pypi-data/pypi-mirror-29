import numpy as np
from scipy import ndimage, misc
from skimage import transform

def sigmoid(x):
    """
    Compute the sigmoid of x
    Arguments:
    x -- A scalar or numpy array of any size
    Return:
    s -- sigmoid(x)
    """

    s = 1 / (1 + np.exp(-x))

    return s

def sigmoid_derivative(x):
    """
    Compute the gradient (also called the slope or derivative) of the sigmoid function with respect to its input x.
    You can store the output of the sigmoid function into variables and then use it to calculate the gradient.
    Arguments:
    x -- A scalar or numpy array
    Return:
    ds -- Your computed gradient.
    """

    s = sigmoid(x)
    ds = s * (1 - s)

    return ds

def normalize(x):
    """
    Implement a function that normalizes each row of the matrix x (to have unit length).
    Argument:
    x -- A numpy matrix of shape (n, m)
    Returns:
    x -- The normalized (by row) numpy matrix. You are allowed to modify x.
    """

    x_norm = np.linalg.norm(x, axis=1, keepdims=True)
    print(x_norm)
    x = x / x_norm
    ### END

    return x

def logloss(self, predicted, actual, eps=1e-14):
    probability = np.clip(predicted, eps, 1-eps)
    loss = -1 * np.mean(actual * np.log(probability)
                        + (1 - actual)
                        * np.log(1 - predicted))
    return loss


# GRADED FUNCTION: softmax
def softmax(x):
    """Calculates the softmax for each row of the input x.
    Your code should work for a row vector and also for matrices of shape (n, m).
    Argument:
    x -- A numpy matrix of shape (n,m)
    Returns:
    s -- A numpy matrix equal to the softmax of x, of shape (n,m)
    """

    x_exp = np.exp(x)
    x_sum = np.sum(x_exp, axis=1, keepdims=True)
    s = x_exp / x_sum

    return s

# GRADED FUNCTION: L1
def L1(y, y_pred):
    """
    Arguments:
    y -- vector of size m (true labels)
    y_pred -- vector of size m (predicted labels)
    Returns:
    loss -- the value of the L1 loss function defined above
    """

    loss = np.sum(np.abs(y - y_pred))

    return loss


def L2(y, y_pred):
    """
    Arguments:
    y_pred -- vector of size m (predicted labels)
    y -- vector of size m (true labels)
    Returns:
    loss -- the value of the L2 loss function defined above
    """

    loss = np.sum((y - y_pred) ** 2)

    return loss


# GRADED FUNCTION: image2vector
def image2vector(image):
    """
    Argument:
    image -- a numpy array of shape (length, height, depth)
    Returns:
    v -- a vector of shape (length*height*depth, 1)
    """

    v = image.reshape((image.shape[0] * image.shape[1] * image.shape[2], 1))

    return v


def propagate(w, b, X, Y):
    """
    Implement the cost function and its gradient for the propagation explained above

    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of size (num_px * num_px * 3, number of examples)
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat) of size (1, number of examples)

    Return:
    cost -- negative log-likelihood cost for logistic regression
    dw -- gradient of the loss with respect to w, thus same shape as w
    db -- gradient of the loss with respect to b, thus same shape as b
    """

    m = X.shape[1]

    A = sigmoid((w.T.dot(X)) + b)  # compute activation
    cost = -(np.sum((Y * np.log(A)) + (1 - Y) * np.log(1 - A))) / m  # compute cost

    dw = (np.dot(X, (A - Y).T)) / m
    db = np.sum(A - Y) / m

    assert (dw.shape == w.shape)
    assert (db.dtype == float)
    cost = np.squeeze(cost)
    assert (cost.shape == ())

    grads = {"dw": dw,
             "db": db}

    return grads, cost


def optimize(w, b, X, Y, num_iterations, learning_rate, print_cost=False):
    """
    This function optimizes w and b by running a gradient descent algorithm
    theta = theta - (alpha * d_theta)

    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of shape (num_px * num_px * 3, number of examples)
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat), of shape (1, number of examples)
    num_iterations -- number of iterations of the optimization loop
    learning_rate -- learning rate of the gradient descent update rule
    print_cost -- True to print the loss every 100 steps

    Returns:
    params -- dictionary containing the weights w and bias b
    grads -- dictionary containing the gradients of the weights and bias with respect to the cost function
    costs -- list of all the costs computed during the optimization, this will be used to plot the learning curve.

    Tips:
    You basically need to write down two steps and iterate through them:
        1) Calculate the cost and the gradient for the current parameters. Use propagate().
        2) Update the parameters using gradient descent rule for w and b.
    """

    costs = []

    for i in range(num_iterations):
        grads, cost = propagate(w, b, X, Y)

        dw = grads["dw"]
        db = grads["db"]

        w = w - (learning_rate * dw)
        b = b - (learning_rate * db)

        # Record the costs
        if i % 100 == 0:
            costs.append(cost)

        # Print the cost every 100 training iterations
        if print_cost and i % 10 == 0:
            print("Cost after iteration %i: %f" % (i, cost))

    params = {"w": w,
              "b": b}

    grads = {"dw": dw,
             "db": db}

    return params, grads, costs

def prepare_image(img_name):
    import os
    from PIL import Image
    img_path = os.path.join(os.getcwd(), '..', 'images', f'{img_name}.jpg')
    img = Image.open(img_path)
    img = img.resize((64, 64))
    image = np.array(ndimage.imread(img_path, flatten=False))
    # my_image = misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
    my_image = transform.resize(image, output_shape=(num_px, num_px))
    my_image = my_image.reshape((1, num_px * num_px * 3))
    my_image = my_image.T
    return my_image


def predict(w, b, X):
    '''
    Predict whether the label is 0 or 1 using learned logistic regression parameters (w, b)

    Arguments:
    w -- weights, a numpy array of size (num_px * num_px * 3, 1)
    b -- bias, a scalar
    X -- data of size (num_px * num_px * 3, number of examples)

    Returns:
    Y_prediction -- a numpy array (vector) containing all predictions (0/1) for the examples in X
    '''

    m = X.shape[1]
    Y_prediction = np.zeros((1, m))
    w = w.reshape(X.shape[0], 1)

    A = sigmoid(w.T.dot(X) + b)

    for i in range(A.shape[1]):
        # Convert probabilities A[0,i] to actual predictions p[0,i]
        Y_prediction[0, i] = 1 if A[0, i] >= 0.5 else 0

    assert (Y_prediction.shape == (1, m))

    return Y_prediction


def initialize_with_zeros(dim):
    """
    This function creates a vector of zeros of shape (dim, 1) for w and initializes b to 0.

    Argument:
    dim -- size of the w vector we want (or number of parameters in this case)

    Returns:
    w -- initialized vector of shape (dim, 1)
    b -- initialized scalar (corresponds to the bias)
    """

    w = np.zeros(shape=(dim, 1), dtype=np.float32)
    b = 0

    assert (w.shape == (dim, 1))
    assert (isinstance(b, float) or isinstance(b, int))

    return w, b

def load_dataset():
    import h5py
    import os
    data_dir = os.path.join(os.getcwd(), '..', 'data')
    train_path = os.path.join(data_dir, 'train_catvnoncat.h5')
    test_path = os.path.join(data_dir, 'test_catvnoncat.h5')
    train_dataset = h5py.File(train_path, "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])  # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])  # your train set labels

    test_dataset = h5py.File(test_path, "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])  # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])  # your test set labels

    classes = np.array(test_dataset["list_classes"][:])  # the list of classes

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


import matplotlib.pyplot as plt

num_iterations = 2000
learning_rate = 0.005
print_cost = True
train_set_x_orig, Y_train, test_set_x_orig, Y_test, classes = load_dataset()
m_train = train_set_x_orig.shape[0]
m_test = test_set_x_orig.shape[0]
num_px = train_set_x_orig.shape[2]
train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T

X_train = train_set_x_flatten/255.
X_test = test_set_x_flatten/255.
w, b = initialize_with_zeros(X_train.shape[0])
parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost)
# Retrieve parameters w and b from dictionary "parameters"
w = parameters["w"]
b = parameters["b"]

# Predict test/train set examples
Y_pred_test = predict(w, b, X_test)
Y_pred_train = predict(w, b, X_train)

# Print train/test Errors
print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_pred_train - Y_train)) * 100))
print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_pred_test - Y_test)) * 100))

d = {"costs": costs,
     "Y_prediction_test": Y_pred_test,
     "Y_prediction_train": Y_pred_train,
     "W": w,
     "b": b,
     "learning_rate": learning_rate,
     "num_iterations": num_iterations}

index = 1
plt.imshow(X_test[:,index].reshape((num_px, num_px, 3)))
print("y = " + str(Y_test[0,index]) + ", you predicted that it is a \"" +
      classes[int(d["Y_prediction_test"][0,index])].decode("utf-8") +  "\" picture.")

costs = np.squeeze(d['costs'])
plt.clf()
plt.plot(costs)
plt.ylabel('cost')
plt.xlabel('iterations (per hundreds)')
plt.title("Learning rate =" + str(d["learning_rate"]))
#plt.show()

#make prediction
imgs = ('Cat', 'Cat_Drawing', 'Cat_Cartoon', 'Cat_Felix', 'Dog', 'Dog_Drawing', 'Man', 'Woman', 'Man_Drawing', 'Woman_Drawing' )
for img_name in imgs:
    my_image = prepare_image(img_name)
    pred = predict(d['W'], d['b'], my_image)
    print(f'Prediction: {img_name}: {pred}')


# Example of a picture
index = 25
example = train_set_x_orig[index]
plt.imshow(train_set_x_orig[index])
print ("y = " + str(Y_train[:, index]) + ", it's a '" + classes[np.squeeze(train_set_y[:, index])].decode("utf-8") +  "' picture.")

w, b, X, Y = np.array([[1.],[2.]]), 2., np.array([[5., 6.5, 1.,2.,-1.],[2., 1.1, 3.,4.,-3.2]]), np.array([[1,0,1]])

print(X)
grads, cost = propagate(w, b, X, Y)
print(grads)
print(cost)



'''
print(train_set_x.shape)           #(12288, 209)
print ("dw = " + str(grads["dw"])) 
print ("db = " + str(grads["db"]))
print(test_set_x.shape)
print ("cost = " + str(cost))#(12288, 50)
d = model(train_set_x, train_set_y, test_set_x, test_set_y, num_iterations = 2000, learning_rate = 0.005, print_cost = True)
'''