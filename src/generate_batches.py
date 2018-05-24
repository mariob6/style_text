from sklearn.utils import shuffle


def batchesFromFiles(files: list, batchsize: int, inMemory: bool):
    if inMemory:
        return loadFilesAndGenerateBatches(files, batchsize)

    return yieldBatchesFromFiles(files, batchsize)


def yieldBatchesFromFiles(files, batchsize):
    """
    Generate batches without loading files in memory
    """
    openedFiles = []
    for fname in files:
        openedFiles.append(open(fname, 'r'))

    while True:
        inputs = []
        labels = []
        for label, fp in enumerate(openedFiles):
            for i in range(batchsize // len(files)):
                # remove final '\n'
                inputs.append(fp.readline()[:-1])
                labels.append(label)

        yield inputs, labels


def loadFilesAndGenerateBatches(files, batchsize, shuffleFiles=True):
    inputs = []
    lenLines = []
    for label, fileName in enumerate(files):
        with open(fileName, 'r') as fp:
            lines = fp.readlines()

        lines = list(map(lambda x: x[:-1], lines))
        lenLines.append(len(lines))
        if shuffleFiles:
            lines = shuffle(lines)

        inputs.append(lines)

    batches = []
    iterStep = batchsize // len(inputs)
    for index in range(0, min(lenLines), iterStep):
        currInputs = []
        currLabels = []
        for label, class_inputs in enumerate(inputs):
            currInputs.extend(class_inputs[index:index + iterStep])
            currLabels.extend([label] * iterStep)
        batches.append((currInputs, currLabels))
    return batches


def preprocessSentences(sentences):
    def addGo(sentence):
        out = ['<go>']
        out.extend(sentence)
        return out

    # TODO add padding ???
    encoder_inputs = sentences
    generator_inputs = list(map(addGo, sentences))
    targets = list(map(lambda x: x.append('<eos>'), sentences))
    return encoder_inputs, generator_inputs, targets
