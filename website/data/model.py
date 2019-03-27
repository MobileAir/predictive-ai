import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import torch.utils.data as torch_utils
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

def predict_price(data):

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

    def process_data(df):
        '''
        :param df: input with last 50 days of stocks + tweet and news scores
        :return: Tensor with data normalized w.r.t. the input df.
        '''
        min_max_scaler = MinMaxScaler()

        just_price = df.drop(['NewsData', 'TweetScore'], axis=1)

        jp = just_price.as_matrix()

        df['High'] = min_max_scaler.fit_transform(df.High.values.reshape(-1, 1))
        df['Low'] = min_max_scaler.fit_transform(df.Low.values.reshape(-1, 1))
        df['Open'] = min_max_scaler.fit_transform(df.Open.values.reshape(-1,1))
        df['Close'] = min_max_scaler.fit_transform(df.Low.values.reshape(-1, 1))

        df = df.as_matrix()

        min_max_scaler.fit(jp)

        return df, min_max_scaler

    def unnormalize(df, X, scalar):
        '''

        :param mat: input data matrix
        :param X: predictions
        :param scalar: MinMaxScalar
        :return: unnormalized data + new predicitons
        '''

        # Add the predictions to the dataframe
        X = X.detach().numpy()

        df = df.append({'High':X[0][0], 'Low':X[0][1], 'Open':X[0][2], 'Close':X[0][3]}, ignore_index=True)
        df = df.drop(['NewsData', 'TweetScore'], axis=1)
        df = df.tail(50)

        # invert the normalization
        df = (df/scalar.scale_) + scalar.data_min_

        return df
    # initialize net
    net = RNNClassifier(50*6, 50, 4)
    checkpts = torch.load("checkpts/all_params.pt")
    net.load_state_dict(checkpts['model_state_dict'])
    hidden_weights = checkpts['hn']

    hn = hidden_weights[0][31].view(1, 1, 50)

    # preprocess data
    normed_data, scalar = process_data(data)


    # Create the tensor
    X = torch.tensor(normed_data, requires_grad=True, dtype=torch.float)
    X = X.view(1, 50*6)

    preds, _ = net(X, hn)

    prices = unnormalize(data, preds, scalar)

    return prices

'''
dat = pd.read_csv("../data/bigdata/WMT.csv")
dat = dat.iloc[:-4]
dat = dat.drop(['Date', 'Volume', 'Adj Close'], axis=1)

print(dat)

p = predict_price(dat)


print(p)'''