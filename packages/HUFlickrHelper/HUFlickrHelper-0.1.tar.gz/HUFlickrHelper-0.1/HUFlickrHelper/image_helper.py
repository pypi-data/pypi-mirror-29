def load_imageID_list(filename):
    """
    This function reads a text file, which
    contains a list of image identifier.

    :param str filename: path to file

    :returns: list: image identifier
    """

    doc = load_file(filename)
    dataset = list()
    # read line by line
    for line in doc.split('\n'):
        # skip empty lines
        if len(line) < 1:
            continue
        # cut of the data type and only keed the ID
        identifier = line.split('.')[0]
        dataset.append(identifier)
    return set(dataset)


def save_features(features, filename):
    """
    Save features to file.

    :param dict features: contains extracted features
    :param str filename: path, including filename
    """
    # remove whitespaces from file name
    filename = filename.strip()
    # check if sufix exists otherwise append
    if (not filename.endswith('.pkl', len(filename) - 4)):
        filename = filename + '.pkl'

    dump(features, open(filename, 'wb'))


def load_image_features(file, images):
    """
    Load image features from file into memory.
    Only select features of images, which are
    part of the given dataset to reduce memory usage.

    :param str filename: filename
    :param set images: list of image identifier

    :return dict: dictionary with image ids, each is an array of 4096 rows 
    """

    # load all features
    all_features = load(open(file, 'rb'))
    # filter features
    features = {k: all_features[k] for k in images}
    return features
