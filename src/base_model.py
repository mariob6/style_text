import random
import torch
from torch import nn
from tqdm import tqdm


class BaseModel(nn.Module):
    _MAX_LOSS = 1e10

    def __init__(self, savefile):
        super().__init__()
        self.savefile = savefile

    def load(self):
        self.load_state_dict(self.savefile)

    def train(self, trainBatches, validBatch, shuffle=True):
        for epoch in range(self.params.epochs):
            if shuffle:
                random.shuffle(trainBatches)
            self.runEpoch(trainBatches, validBatch)

    def runEpoch(self, trainBatches, validBatch):
        bestLoss = self._MAX_LOSS
        progbar = tqdm(range(len(trainBatches)))
        for index in progbar:
            inputs, labels = trainBatches[index]
            loss = self.trainOnBatch(inputs, labels)
            progbar.set_description("Loss: {0}".format(loss))

        evaluationLoss = self.evaluate(*validBatch)
        print("Epoch {0}/{1}, Loss on evaluation set: {2}".format(
            index, len(trainBatches), evaluationLoss))
        if evaluationLoss < bestLoss:
            torch.save(self.state_dict())
