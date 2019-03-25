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

For this project, I observed four prices: the high, open, low, and close for each of the 50 days.

Tweets were collected through Twitter's developer-friendly API, that simplifies the search for relevent Tweets. Using tweepy, I searched twitter for the very uninspired tokens "(company name) stock". This brutish method proved effective.

Mining news data was dreamy when using RapidAPI's Yahoo Finance endpoints. This enabled me to get stock data data and relevant news headlines by simply provding the stock ticker. One minor drawback was that the packages they were using are not supported in python, and so I had to use (read: learn) ruby to access these endpoints. The payoff, however, was a tremendous amount of useful data for each stock, as well as live market updates.
 ------ End of preprocessing
 
## Data preprocessing
There were two central components of in this stage: Sentiment Polarity and MinMax Scaling.
To translate the tweets and news articles to tangible features, I used Textblob's sentiment polarity.


<strong>TextBlob</strong> uses a Naive Bayes NLP model to calculate sentiment polarity. When the method is called, it will first tokenize each word in the input text, then uses a Bag of Words technique to get a count of how many times each word appears. From that, it generates a polarity score in range [-1,1],  representing how "positive" or negative" a text is. Each article and tweet got its own polarity score before being added to the feature matrix.

From its sparse beginnings, I assembled these 6 features into a dataset to be pass to the last stage of preprocessing. Here is a glimpse at Bank of America's data:
![](https://github.com/j-c-carr/Stock-Analysis/blob/master/.extras/sampData.png)

Lastly, I used sklearn's MinMax scaler to normalize the data before feeding my Neural Network. The algorithm is as follows:

![](https://github.com/j-c-carr/Stock-Analysis/blob/master/.extras/minmax.png)

## Model
This model was implemented in pytorch. The code is contained within ######This document. Evidently, this data called for a neural net that considers the time dependance of its data. I found my best results with a double layered GRU. This [video](https://www.youtube.com/watch?v=pYRIOGTPRPU) describes the process very well. Below is a simplified version of the flow of data through the net.
###### image of flow of data through the net

###### Optimizer
To update my parameters, I used the world famous, made-in-Canada Adam optimizer. Due to it's individualistic learning reates for each parameter and as well as its computational efficiency.
Done in pytorch

Lastly, I computed my losses with mean squared error. Most sources I found used this metric and I wanted to be able to compare my results.

## Results
Compared to Kaggle projects on similar datasets, this model shines bright, outperforming even the most critically acclaimed models. I believe that both the news and tweets were tantamount to the model's performance, as none of the other models I could find incorporated thses added dimension. The best error I could find on Kaggle was from Rohit Verma. His project is [here](https://github.com/deadskull7/New-York-Stock-Exchange-Predictions-RNN-LSTM).

<center>

|           | Best on Kaggle | This model |
|-----------|----------------|------------|
| Train MSE | 1.91x10^-4     | 4.02x10^-7 |
| Test MSE  | 3.28x10^-4     | 1.08x10^-6 |

</center>


Test MSE:
![](https://github.com/j-c-carr/Stock-Analysis/blob/master/.extras/errs.png)



## Challenges
Though the model performs well, there is plenty of room for improvement! Here are a few areas I would like to focus on:
#### 1. Training a more suitable NLP classifier for input text
The polarity score is a vague and much too generalized for my data. I would like to add some language processing that would return a score for how the news impacts the stock market, not just if the news sounds good or bad.

#### 2. Expanding News sources
There are many APIs that are eager to provide financial news enpoints. Through the Yahoo subscrption wiht RapidAPI, I am limited to just yahoo finance. I would like to expand my horizons in this regard, as there are more influential news sources.

#### 3. Longer range predictions
My model performs extremely well on simple one-day stock forecasts, but in practice this means very little. It would be nice if my model made longer range forecasts.

## References
Lastly, I would like to give another thanks to the McGill AI society for helping out along the way

