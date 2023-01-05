# implement trainer, tester
import sys, os, random, shutil

import numpy as np
import torch
import torch.nn as nn

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def trainer(dataloader, model, criterion, optimizer):
    size = len(dataloader.dataset)
    
    correct = 0
    train_loss = 0

    for batch, (X, y) in enumerate(dataloader):
        X = X.to(DEVICE)
        y = y.type(torch.LongTensor)
        y = y.to(DEVICE)
        y_hat = model(X)
        loss = criterion(y_hat, y)

        ## Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        correct_batch = (y_hat.argmax(1) == y).type(torch.float).sum().item()
        correct += correct_batch

        if batch % 10 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{len(dataloader.dataset)}]")

    batch_accuracy = correct / size
    batch_loss = train_loss / len(dataloader)
    return batch_loss, batch_accuracy

def tester(dataloader, model, criterion, optimizer):
    size = len(dataloader.dataset)
    correct = 0
    test_loss = 0

    with torch.no_grad():
        for (X, y) in dataloader:
            X = X.to(DEVICE)
            y = y.type(torch.LongTensor)
            y = y.to(DEVICE)

            y_hat = model(X)
            loss = criterion(y_hat, y)
            test_loss += loss.item()
            correct_batch = (y_hat.argmax(1) == y).type(torch.float).sum().item()
            correct += correct_batch
            
    batch_accuracy = correct / size
    batch_loss = test_loss / len(dataloader)
    return batch_loss, batch_accuracy

