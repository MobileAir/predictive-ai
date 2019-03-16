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
    ''' N is batch size '''


    epochs = 1000

    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)

    optimizer.load_state_dict(checkpts["optim_state_dict"])
    loss_fn = nn.MSELoss()

    hn = net.initHidden(N)

    for epoch in range(epochs):

        average_loss = 0
        val_loss = 0

        len_train = 0
        len_vali = 0
        for days, true_stats in trainloader:

            days = days.view(N, in_size)

            preds, hn = net(days, hn.detach())

            loss = loss_fn(preds, true_stats)

            optimizer.zero_grad()
            loss.backward(retain_graph=True)
            optimizer.step()

            average_loss += loss.item()
            len_train+=1

        for days, truth in val_loader:

            days = days.view(N, in_size)

            preds, hn = net(days, hn)

            loss = loss_fn(preds, truth)

            val_loss += loss.item()
            len_vali +=1

        if epoch %2==0:

            print("(epoch, train_loss, val_loss) = ({0}, {1}, {2})".format(epoch, average_loss/len_train, \
                                                                       val_loss/len_vali))

    torch.save({'model_state_dict':net.state_dict(), 'optim_state_dict':optimizer.state_dict(), 'hn': hn}, \
               "checkpts/all_params.pt")

    return hn


def normalize_data(df):

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
    tot = 0
    for days, truth in testloader:

        days = days.view(batch, delta*6)
        preds, _ = net(days, hn)

        loss = loss_fn(preds, truth)
        truths += truth.tolist()
        final_preds += preds.tolist()


        tot+=1

        total_loss += loss.item()
    print(total_loss/tot)

    return final_preds, truths


def unnormalize(df, n_v):

    df = normalize_data(df)

    min_max_scaler = sklearn.preprocessing.MinMaxScaler()

    n_v['Open'] = min_max_scaler.inverse_transform(n_v.open.values.reshape(-1,1))
    n_v['High'] = min_max_scaler.inverse_transform(n_v.high.values.reshape(-1, 1))
    n_v['Low'] = min_max_scaler.inverse_transform(n_v.low.values.reshape(-1, 1))
    n_v['Close'] = min_max_scaler.inverse_transform(n_v.close.values.reshape(-1, 1))

    return n_v

def readbigData(delta):
    '''Delta is how for back you want to predict from'''
    features = []
    labels = []
    with open("../data/names.txt", "r") as f:
        names = json.load(f)
        for ticker in names.keys():
            try:
                df = pd.read_csv("../data/bigdata/"+ticker+".csv")
                #df = pd.read_csv("../data/bigdata/"+name[:-1])
                df = df.drop(['Volume', 'Date', 'Adj Close'], axis=1)
                if ticker=="GOOG" or ticker=="AAPL" or ticker=="BAC" or ticker=="CAT":
                    df.drop(['Unnamed: 0'], axis=1)

                normed = normalize_data(df)
                mat = normed.as_matrix()

                if mat.shape == (54,6):

                    for i in range(len(df.High) - delta):
                        features.append(mat[i:i+delta])
                        labels.append(mat[i+delta][:-2])
            except FileNotFoundError:
                continue

    return features, labels

delta = 50
in_dim = delta*6
hidden_dim = 50
out_dim = 4
lr = .8e-5
batch = 32

feats, labels = readbigData(delta)

days = len(feats)
print(days)

# seqs are batch_size * seq_len * feats

trainloader, valloader, testloader = load_data(int(days*0.8), int(days*0.9), features=feats, labels=labels)

net = RNNClassifier(in_dim, hidden_dim, out_dim)

# load weights from previous session
checkpts = torch.load("checkpts/all_params.pt")
net.load_state_dict(checkpts['model_state_dict'])
hidden_weight = checkpts['hn']

#hidden_weight = train(trainloader, valloader, in_dim, batch, learning_rate=lr)

outputs, labels = test(testloader, hidden_weight, delta, batch)

high = []
low = []
open = []
close = []
for p, t in zip(outputs, labels):
    high.append(mean_squared_error(t[0],p[0]))
    low.append(mean_squared_error(t[1],p[1]))
    open.append(mean_squared_error(t[2],p[2]))
    close.append(mean_squared_error(t[3],p[3]))
print(sum(high)/len(high))
print(sum(low)/len(low))
print(sum(open)/len(open))
print(sum(close)/len(close))
