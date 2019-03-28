import json
import pandas as pd
import torch
import torch.nn as nn
import torch.utils.data as torch_utils
import sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")


def load_data(train_bound, val_bound, features, labels, batch_size=32):
    """
    :param train_bound: defines where we split data
    :param features: list matrix of features
    :param batch_size: nb of features too feed the net at each time point
    :return: nicely shuffled DataLoader objects
    """

    X = torch.tensor(features, requires_grad=True, dtype=torch.float)
    Y = torch.tensor(labels, requires_grad=False, dtype=torch.float)

    trainset = torch_utils.TensorDataset(X[:train_bound], Y[:train_bound])
    tr_load = torch_utils.DataLoader(trainset, batch_size=batch_size, shuffle=True, drop_last=True)

    val_set = torch_utils.TensorDataset(X[train_bound:val_bound], Y[train_bound:val_bound])
    val_load = torch_utils.DataLoader(val_set, batch_size=batch_size, shuffle=True, drop_last=True)

    test_set = torch_utils.TensorDataset(X[val_bound:], Y[val_bound:])
    te_load = torch_utils.DataLoader(test_set, batch_size=batch_size, shuffle=True, drop_last=True)

    return tr_load, val_load, te_load


class RNNClassifier(nn.Module):

    def __init__(self, input_dim, hidden_dim, output_dim):
        super(RNNClassifier, self).__init__()

        self.hidden_size = hidden_dim

        self.gru = nn.GRU(input_dim, hidden_dim, bias=False, dropout=0.3)

        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, days, h0):

        days = days.unsqueeze(0)

        h_out, hidden = self.gru(days, h0)

        h_out = h_out.squeeze(0)

        out = self.fc(h_out)

        return out, hidden

    def initHidden(self, batch_size):

        return torch.zeros(1, batch_size, self.hidden_size)


def train(trainloader, val_loader, in_size, N, learning_rate):
    """
    :param trainloader: train dataLoader object
    :param in_size: Input dimension
    :param N: Batch Size
    :return: Saves params, outputs hidden weights for fctn
    """

    epochs = 1000

    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
    optimizer.load_state_dict(checkpts["optim_state_dict"])

    loss_fn = nn.MSELoss()

    hn = net.initHidden(N)

    for epoch in range(epochs):

        average_loss = 0
        val_loss = 0

        for days, true_stats in trainloader:

            days = days.view(N, in_size)

            preds, hn = net(days, hn.detach())

            loss = loss_fn(preds, true_stats)

            optimizer.zero_grad()
            loss.backward(retain_graph=True)
            optimizer.step()

            average_loss += loss.item()

        for days, truth in val_loader:

            days = days.view(N, in_size)

            preds, hn = net(days, hn)

            loss = loss_fn(preds, truth)

            val_loss += loss.item()

        if (epoch % 2) == 0:

            print("(epoch, train_loss, val_loss) = ({0}, {1}, {2})".format(epoch, average_loss/N, \
                                                                       val_loss/N))

    torch.save({'model_state_dict':net.state_dict(), 'optim_state_dict':optimizer.state_dict(), 'hn': hn}, \
               PARAMS_FILEPATH)

    return hn


def normalize_data(df):
    """
    MinMax Scaling for input data
    """

    min_max_scaler = MinMaxScaler()

    df['Open'] = min_max_scaler.fit_transform(df.Open.values.reshape(-1,1))
    df['High'] = min_max_scaler.fit_transform(df.High.values.reshape(-1,1))
    df['Low'] = min_max_scaler.fit_transform(df.Low.values.reshape(-1,1))
    df['Close'] = min_max_scaler.fit_transform(df.Low.values.reshape(-1, 1))

    return df


def test(testloader, hn, delta, batch):

    loss_fn = nn.MSELoss()

    final_preds = []
    truths = []

    total_loss = 0
    nb_samples = 0
    for days, truth in testloader:

        days = days.view(batch, delta*6)
        preds, _ = net(days, hn)

        loss = loss_fn(preds, truth)
        truths += truth.tolist()
        final_preds += preds.tolist()


        nb_samples += 1

        total_loss += loss.item()

    return final_preds, truths


def unnormalize(df, n_v):
    """
    df: originial df
    n_v: normalized results
    """
    df = normalize_data(df)

    min_max_scaler = sklearn.preprocessing.MinMaxScaler()

    n_v['Open'] = min_max_scaler.inverse_transform(n_v.open.values.reshape(-1,1))
    n_v['High'] = min_max_scaler.inverse_transform(n_v.high.values.reshape(-1, 1))
    n_v['Low'] = min_max_scaler.inverse_transform(n_v.low.values.reshape(-1, 1))
    n_v['Close'] = min_max_scaler.inverse_transform(n_v.close.values.reshape(-1, 1))

    return n_v

def readbigData(delta):
    """
    :param delta: defines how far back in time you're looking at
    :return: nice features & labels
    """
    features = []
    labels = []

    # Text file containing all company names
    with open("../data/names1.txt", "r") as f:
        names = json.load(f)

        for ticker in names.keys():

            # for some companies I was not able to get the prices
            try:
                df = pd.read_csv(DATA_FOLDER/+ticker+".csv")
                df = df.drop(['Date', 'Unnamed: 0'], axis=1)

                normed = normalize_data(df)
                mat = normed.as_matrix()

                # TWO DAY PREDICTIONS (passing delta is 50, but only 49 days in feature matrix)
                for i in range(len(df.High) - delta):
                    features.append(mat[i:i+delta-1])
                    labels.append(mat[i+delta][:-2])

            except FileNotFoundError:
                continue
    return features, labels

# DELTA: HOW FAR BACK YOU HAVE STOCK INFO FOR
delta = 49

in_dim = delta*6 # EACH SAMPLE HAS 6 FEATURES
hidden_dim = 49
out_dim = 4
lr = 1e-4
batch = 32

feats, labels = readbigData(50)

# Days = number of samples that we have
days = len(feats)

trainloader, valloader, testloader = load_data(int(days*0.8), int(days*0.9), features=feats, labels=labels)

net = RNNClassifier(in_dim, hidden_dim, out_dim)

# load weights from previous session
checkpts = torch.load("checkpts/web_params2.pt")
net.load_state_dict(checkpts['model_state_dict'])
hidden_weight = checkpts['hn']

hidden_weight = train(trainloader, valloader, in_dim, batch, learning_rate=lr)


outputs, labels = test(testloader, hidden_weight, delta, batch)

