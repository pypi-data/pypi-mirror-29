def save_descriptions(descriptions, filename):
    """
    Save descriptions to file, one per line.

    :params dict descriptions: descriptions
    :params str filename: path including file name
    """

    lines = list()
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            lines.append(key + ' ' + desc)
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()


def flat_descriptions(descriptions):
    """
    Transform all descriptions of a dictionary
    into a list of descriptions.

    :param dict descriptions: descriptions

    :return list: list of all descriptions. ['desc1', 'desc2', ...]
    """

    all_desc = list()
    for key in descriptions.keys():
        [all_desc.append(d) for d in descriptions[key]]
    return all_desc


def load_descriptions(file, dataset, select_all=False):
    """
    This method reads a file and stores
    its content as a dictionary where image
    identifier are keys and their descriptions
    the corresponding values.

    :param str file: path to file
    :param list dataset: list of image identifier
    :param boolean select_all: ignore dataset

    :return dict: "image id" -> "description"
    """

    # read file in
    raw_data = load_file(file)
    descriptions = dict()

    # process line by line
    for line in raw_data.split('\n'):
        # split line by white space
        tokens = line.split()
        if len(line) < 2:
            continue
        # take the first token as the image id, the rest as the description
        image_id, image_desc = tokens[0], tokens[1:]
        # remove filename from image id
        image_id = image_id.split('.')[0]
        if image_id in dataset or select_all:
            # convert description tokens back to string
            image_desc = ' '.join(image_desc)
            # create the list if needed
            if image_id not in descriptions:
                descriptions[image_id] = list()
            # store description
            descriptions[image_id].append(image_desc)
    return descriptions


def prepare_descriptions(descriptions):
    """
    This method takes a dictionary of
    descriptions and applies several
    natural language processing operations
    to each:
        - transform to lowercase
        - remove puctuation
        - remove hanging 's' and 'a'
        - remove numbers

    :param dict description: descriptions

    :return dict: preprocessed descriptions
    """

    descriptions = copy.deepcopy(descriptions)
    # prepare translation table for removing punctuation
    table = str.maketrans('', '', string.punctuation)
    for key, desc_list in descriptions.items():
        for i in range(len(desc_list)):
            desc = desc_list[i]
            # tokenize
            desc = desc.split()
            # convert to lower case
            desc = [word.lower() for word in desc]
            # remove punctuation from each token
            desc = [w.translate(table) for w in desc]
            # remove hanging 's' and 'a'
            desc = [word for word in desc if len(word) > 1]
            # remove tokens with numbers in them
            desc = [word for word in desc if word.isalpha()]
            # store as string
            desc_list[i] = ' '.join(desc)

    return descriptions


def map_id_to_word(integer, tokenizer):
    """
    This methods retuns the english word, which
    corresponse to to given integer. If no
    word exists in the tokenizer the method returns None.

    :param int integer: numerical representation of a word
    :param Tokenizer tokenizer: Tokenizer

    :return str word: word OR None, if no matching word was found
    """
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None
