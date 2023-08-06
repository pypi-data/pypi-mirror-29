import pickle


def save(file, var):
    obj = pickle.dumps(var)
    with open(file, 'wb') as f:
        f.write(obj)

