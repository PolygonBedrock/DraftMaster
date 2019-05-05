import pickle


def save_to_file(obj, file):
    with open(file, 'wb') as file_pointer:
        pickle.dump(obj, file_pointer, protocol=pickle.HIGHEST_PROTOCOL)


def open_file(file):
    with open(file, 'rb') as file_pointer:
        return pickle.load(file_pointer)