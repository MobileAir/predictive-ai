# Predictive Eye



Stock-Analysis is a semantic text analysis modeling engine for stock price prediction utilizing news articles, social medial, and stock price

and its past prices. model we developed in 2000. 
It was completed as part of the McGill AI Society's Accelrated ML bootcamp.

#### Table of contents:
1. [Data Aquisition](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#data-mining)
2. [Data Preprocessing](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#data-preprocessing)
3. [Model](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#model)
4. [Future Develppment](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#next-steps)
5. [Results](https://github.com/MobileAir/Stock-Analysis/blob/master/README.md#results)


## Data Aquisition

To collect data for each stock, I used pandas datareader, RapidAPI and Twitter to gather stock prices, news, and tweets.

Aquiring stock prices was done with the code below. I was interested in the stock prices from the last 50 days.

```
    prices = pd.datareader.get_data_yahoo(stock, since, today)
```

1.  Pricing includes: high, open, low, and close, for each of the 50 days,
3.  Twitter's python library (tweepy),
4.  RapidAPI's Yahoo Finance endpoint.

## Data Preprocessing
There were two central components of in this stage: TextBlob's sentiment polarity and MinMax Scaling.
    1.  Textblob's sentiment polarity encoded the tweets and news articles.
    2.  Naive Bayes model uses calculates polarity (in range [-1,1]), to define how "positive" or negative" a text is
 Each article and tweet got its own polarity score before being added to the feature matrix.

Bank of America's data:![](https://github.com/MobileAir/Stock-Analysis/blob/master/.extras/sampData.png)

sklearn's MinMax scaler to normalize the data before feeding my Neural Network. The algorithm is as follows:
<p align="center">
<img src="https://latex.codecogs.com/gif.latex?x%5E%7B%27%7D%20%3D%20%5Cfrac%7Bx%20-%20min%28x%29%7D%7Bmax%28x%29%20-%20min%28x%29%7D">
</p>

## Model
1.  Feature matrix: 49 rows x 6 columns, with each row being one day
2.  Best results using two Gated Recurrent Units followed by a fully connected layer. which can be found [Here](https://github.com/MobileAir/Stock-Analysis/blob/master/src/model.py) is the implementation.

## Future Development

##### 1. Training a more refined NLP classifier for data preprocessing
The polarity score is vague and much too generalized for my data. I would like to add some language processing that would return a score for how the news impacts the stock market, not just if the news sounds good or bad.

##### 2. Exploring other influences
Since the news and tweets boosted the model's performance, I'd love to tap into other news and social media outlets and see if I can improve the predictions.

##### 3. Longer forecast
The model corrently predicts for one day in advance. It would be nice to predict further into the future, though I get the feeling that if that was possible, someone might have beat me to it!

## Results
1. Performance: ourperforms most Kaggle competitors,
2. Semantic analysis improved performance,
3. Largest error on Kaggle was from Rohit Verma [Rohit Verma](https://github.com/deadskull7/New-York-Stock-Exchange-Predictions-RNN-LSTM)

|           |    Best on Kaggle    |    This model    |
|-----------|----------------------|------------------|
| Train MSE | 1.91 x 10<sup>-4     | 5.90 x 10<sup>-7 |
| Test MSE  | 3.28 x 10<sup>-4     | 6.21 x 10<sup>-7 |


#### Test MSE on normalized stock prices:

|    High          |    Low           |    Close         |
|------------------|------------------|------------------|
| 6.87 x 10<sup>-7 | 5.81 x 10<sup>-6 | 8.34 x 10<sup>-7 |


####McGill Ai [here](https://mcgillai.com/)
