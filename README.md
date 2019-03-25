# Stock-Analysis

This project is meant to explore the potential in today's big data enterprises. Though a heavily standardized approach is taken here to a benign problem, this project harps upon the wonderous possibilities with big data. This project combines stock prices as well as relevant news articles and tweets to predict future stock prices. The news and twitter data bring novelty to an otherwise benign approach to this problem. ----- Mention neural network

This project was done through the McGill AI Society's Accelrated ML bootcamp. Checkout their blogpost here #####insert blogpost

Contianed in this document is the journey that the data takes in order to become a prediction.

#### Table of contents:
1. [Data Mining](https://github.com/j-c-carr/Stock-Analysis/blob/master/README.md#data-mining)
2. [Data preprocessing](https://github.com/j-c-carr/Stock-Analysis/blob/master/README.md#data-preprocessing)
3. [Model](https://github.com/j-c-carr/Stock-Analysis/blob/master/README.md#model)
4. [Results](https://github.com/j-c-carr/Stock-Analysis/blob/master/README.md#results)
5. [Challenges](https://github.com/j-c-carr/Stock-Analysis/blob/master/README.md#challenges)
6. [Next Steps](https://github.com/j-c-carr/Stock-Analysis/blob/master/README.md#references)

## Data mining
This step was made easy with special thanks to the good grace of pandas datareader, Twitter, and RapidAPI. This project uses three sources of data; pandas datareader (for Yahoo Finance), RapidAPI (for news), and Twitter (for tweets).

Aquiring stock prices was done with the code below. I was interested in the stock prices from the last 50 days.

```
    prices = pd.datareader.get_data_yahoo(stock, since, today)
```

For this project, I observed four prices: the high, open, low, and close for each of the 50 days.

I collected tweets using Twitter's pyhton library, tweepy. This made it easy to search and collect tweets mentioning a given company and thier stock.

To get news articles I used RapidAPI's Yahoo Finance endpoint. It was an excellent source for all my heart's desires.
 ------ End of preprocessing
 
## Data preprocessing
There were two central components of in this stage: Sentiment Polarity and MinMax Scaling.
To translate the tweets and news articles to tangible features, I used Textblob's sentiment polarity.


<strong>TextBlob</strong> uses a Naive Bayes NLP model to calculate sentiment polarity (ie. score in range [-1,1],  representing how "positive" or negative" a text is). Each article and tweet got its own polarity score before being added to the feature matrix.

Here is a glimpse at Bank of America's data:
![](https://github.com/j-c-carr/Stock-Analysis/blob/master/.extras/sampData.png)

Lastly, I used sklearn's MinMax scaler to normalize the data before feeding my Neural Network. The algorithm is as follows:

![](https://github.com/j-c-carr/Stock-Analysis/blob/master/.extras/minmax.png)

## Model
The model was implemented in pytorch, which can be found [here](https://github.com/j-c-carr/Stock-Analysis/blob/master/src/model.py). I used two Gated Recurrent Units stacked on top of one another followed by a fully connected layer that mapped to the output dimension.

I stayed true to my Canadian roots and used the <strong>Adam optimizer</strong>.

## Results
This model outperforms the toughest Kaggle competitor (Kaggle projects used only the stock prices). Clearly see that the news and tweets were key to the model's performance. The best error I could find on Kaggle was from Rohit Verma. His project is [here](https://github.com/deadskull7/New-York-Stock-Exchange-Predictions-RNN-LSTM).

<center>

|           |    Best on Kaggle    |    This model    |
|-----------|----------------------|------------------|
| Train MSE | 1.91 x 10<sup>-4     | 4.02 x 10<sup>-4 |
| Test MSE  | 3.28 x 10<sup>-4     | 1.08 x 10<sup>-6 |

</center>


#### Test MSE on normalized stock prices:

| High       | Low        | Close      |
|------------|------------|------------|
| 8.74x10^-7 | 1.40x10^-6 | 8.50x10^-7 |




## Challenges
Though the model performs well, there is plenty of room for improvement! Here are a few areas I would like to focus on:
#### 1. Training a more refined NLP classifier for data preprocessing
The polarity score is a vague and much too generalized for my data. I would like to add some language processing that would return a score for how the news impacts the stock market, not just if the news sounds good or bad.

#### 2. Exploring other influences
Since the news and tweets clearly influenced the model's performance, I'd love to tap into other news and social media websites and see if I can improve the predictions.

#### 3. Longer forecast
The fact that the model currently only predicts to prices for the next day overshadows its impressive performacen thus far. It would be nice to accurately predict further into the future.


Thanks again to the McGill AI society for a great course and stellar support!
