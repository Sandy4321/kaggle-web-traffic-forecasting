## Web Traffic Forecasting

This [model](web_traffic_forecasting_model.py) is my solution to Kaggle's "Web Traffic Time Series Forecasting" competition. It makes web traffic predictions using Facebook's [Prophet](https://github.com/facebook/prophet) package.

### Introduction

The competition asked participants to predict daily web traffic of 145,000 Wikipedia articles given actual web traffic data from the prior two years.

The competition consisted of two rounds. The first round was a preliminary training round that lasted for several months. In this round, training data from mid 2015 through 2016 was used to make predictions for the first three months in 2017. The second round lasted just one week, and predictions in this round were made for future dates (i.e., training data from the first round plus data through mid 2017 was used to make predictions for September 2017 through November 2017). 

Final scores and rankings were based on predictions from the second round only, and this particular model placed in the top 30% of all submissions.

For more detailed information, please visit the [competition website](https://www.kaggle.com/c/web-traffic-time-series-forecasting).

### Model Analysis

Prophet makes predictions on time series data by combining three distinct components: a linear or logistic trend, a weekly seasonal component, and a yearly seasonal component. 

As an example, actual and forecasted web traffic of the Wikipedia article on [Elon Musk](https://en.wikipedia.org/wiki/Elon_Musk) is shown below. The black dots (plotted in logarithmic scale) are the article's actual web traffic and the dark blue line is the article's forecasted web traffic.

<p align="center">
	<img src="images/example_plot.png" width="500">
</p>

The forecast is made from aggregating the three components, which are plotted below.

<p align="center">
	<img src="images/example_components.png" width="500">
</p>

- The **trend** line reveals that there has been a significant rise in interest in Elon Musk over the past couple of years
- The **weekly** graph reveals that the views to his Wikipedia article is high during the weekdays, yet it wanes during the weekends
- The **yearly** graph is likely related to his company's earnings and product announcements as well as his interactions with the news media

### Implementation Notes

1. Due to space limitations on Github, I do not include the input data files. To run the model, you will need to download and save the two input files ([train_2.csv and key_2.csv](https://www.kaggle.com/c/web-traffic-time-series-forecasting/data)) to the same directory as the model file.
2. Prophet can only make predictions for a single time series. Therefore, to obtain predictions on all 145,000 Wikipedia articles, it was necessary to loop through each individual article one at a time, and, on my MacBook Pro, the model took about four days to finish.