import streamlit as st
st.image('.../imgs/vid3.gif')
st.title("US Stock Market vs Spanish Stock Market: NASDAQ 100 and IBEX 35")
st.subheader("By: Shahbab Ahmed, Amirul Miah, and Tanbirul Miah")

st.header("Motivation")
st.write('''The motivation for comparing the US and Spanish Stock Markets is to answer some questions in 
a hypothetical scenario where we suddenly inherited a generous amount of capital. In such a scenario, we
would want to make the money that was inherited work for us. To do that, it would be reasonable to assume
that investing would be the best course of action. It turns out that some of the inheritence includes shares 
of a company in the Spanish Stock Market, so now it comes down to deciding whether to focus your investments 
in the US or Spanish Stock Market. 

We decided to analyze the performance of the top 5 stocks of each market in 2015 and track their performance from
the last 10 years. Studying historical data can give insights into the stability of both stock markets and can 
help us decide which market would be safer to invest in. 

"_With a good perspective on history, we can have a better understanding of the past and present, 
and thus a clear vision of the future_" - Carlos Slim Helu''')

st.header("Data")
st.subheader("API")

st.write('''The data for the top 5 US stocks were retrieved using Aplha Vantage API in JSON format. The initial pull from the data
retrieved 1200 records, covering the periods from 1999 to 2021. After the cleaning, we cut that down to 660 records.

To process the NASDAQ 100 stock data, we created a function called get_monthly_data. This function takes in a list of 
stock symbols and returns a dictionary of monthly stock data for those specified stocks. It uses the function create_request_url 
to pass in the symbols and create the url that you must send the request to. After the request is made, what's returned is stock 
data in json format. We use json.loads to parse the json data into a readable python dictionary. Then we iterate over that dictionary 
in order to grab the data we want (high price, low price, etc.) and put all of that data into a new dictionary that is structured 
as such: key = stock symbols, values = list of tuples where elements within each tuple contains data.

The dictionary created by get_monthly_data is then returned to be used within create_sql_db. This function takes in a dictionary 
(specifically the dictionary returned by get_monthly_data) and returns a dataframe. We create an SQL database called "stocks" with 
the same columns as what the values in the dictionary are, in addition to the column "market" and "year". Then we execute a loop that 
iterates over the dictionary, each time inserting the values in their respective columns in the database. "market" was set to be "US" 
for later analysis and "year" was also set for filtering. After all the data has been inserted into the database, we used a select 
query alongside pd.read_sql in order to filter out all years outside of our 2005-2015 range and put the result into a dataframe, which 
is returned after we set the date into a datetime index.
''')

st.image('./imgs/get_monthly.png')

st.subheader("CSV")

st.write('''The data for the top 5 Spanish stocks were retrieved using the dataset, Spanish Stocks Historical Data, which was available on Kaggle.com. 
The csv file of each stock was downloaded which included six columns of data per stock: Date, Close, High, Low, Open, and Volume. We
kept these fields because they coincided with the fields we had for the API data.

To process the IBEX 35 stock data, we created a function called read_csv_files to combine the csv files together and another function called clean_df to 
clean the dataframe that is created. The function read_csv_files reads in 5 csv files (each containing stock data for an individual stock). It sets the 
symbols in each dataframes for the respective stock. Then we concatenate all 5 dataframes, create a new column called "Market" with the value "Spanish", 
and filter out all dates outside of our 2005-2015 range. The function clean_df is used to match the dataframe returned by read_csv_files with the dataframe 
returned by create_sql_db. We first renamed all of the columns so they match the column names for the api dataframe, convert the values in the csv dataframe into USD, 
set the date as a datetime index, then resampled the date to monthly since the data for all of the csv files were in daily format.
''')
st.image('./imgs/csv_data.png')

st.subheader("Merged")

st.write('''Then, the function merge_data takes in the two dataframes (one created from api, one created from csv), concatenates them together, 
creates a multilevel index using symbol and date, then returns that dataframe.
''')

st.header("Analysis")

st.subheader("T-Test")

st.write('''For our T test, we ran the test across all 10 years (2005-2015) and we wanted to see if there is a significant 
difference in average price between the US and Spanish market.

We created a helper function called avg_price, then applied it to a new column within our T-test function called t_test_accross_all_years. This column 
is the average price of the four different types of prices we have, and the dataframe which are open, close, high and low. 
Then we created two dataframes by masking the US and Spanish market and the avg_price column. So the new dataframe is 
basically just one column with all the average prices. We have one dataframe for the US market and one data frame for the 
Spanish market. We pass both of these dataframes into the T-test function with the equal variance set to false since we 
can't make that assumption here. The results showed that there is a significant difference in average price between the two 
market with a T-test statistic of around 17 and a p-value of less than .01. This was a two-sided t test. 
But if we look at the mean price for US stocks, we see there is much higher than the mean price for the Spanish stocks. $41.7 
compared to $20. So we can say that the average price for US stocks are significantly higher than the Spanish stocks because 
the p-value is really small.
''')

st.subheader("Recession")

st.write('''The next analysis is a graph looking at the recession periods, which is between 2007 and 2009.

The function recession_analysis takes in the merged dataframe, resets the indexes (since we will work with data 
frame without multi level indexing), and creates a new column of average prices using the average price helper 
function similar to the previous analysis. We create two dataframes using masks for the US and Spanish market and 
also filter out any dates outside of 2007 through 2009. We also sort by symbols followed by date so that the data 
is organized by symbols first then dates. We basically will have rows of the same stocks where the first row is 
first month of 2007, the next row is the second month of 2007 and so on. After that, we used groupby symbol and 
passed in a function called pct_change, which basically tracks the change in values between rows in percent format. 
This is put into a new column called monthly_performance. Essentially what we have in this column is a month to month 
change in average price for each stock. Finally, we plot monthly_performance using matplotlib for each market. For US 
stocks, it seems that the change stays between negative 20% and positive 20%, while the Spanish stocks stay between 
negative 30% and positive 40%. Although it's somewhat difficult to eyeball it seems that the price change between the 
years 2007 through 2009 dips below zero and to the negative quite a bit, especially during 2008. However, 
there are some outliers that have massive spikes.
''')
st.image('./imgs/recession.png')

st.subheader("Bollinger Band")

st.write('''Next we create a bollinger band analysis to illustrate the relative strength or momentum of a stock. 

This function takes in the merged data frame along with a single stock symbol (US or Spanish) from the data frame 
and crates Bollinger bands to illustrate the relative strength or momentum of a stock. We mask the merged dataset 
to create a new dataset that only has data regarding the stock symbol specified. We then create three Bollinger Bands 
in the form of columns to show the lower, middle, and upper bands of each stock at that specific month. A rolling window 
of 1 and 12 are used to indicate the passage of 1 and 12 months respectively. Then we plot the new columns, where the lower 
band shows the attractive value of the stock, the upper band shows the overpriced value of the stock, and the middle band shows 
the actual value of the stock. So for example from Microsoft, you can see that the price stays within the upper and lower bands 
throughout the entire period between 2005 and 2015. And we can do this for any stocks just by passing in the symbol.
''')
st.image('./imgs/Bollinger_band.png')

st.subheader("Top Yearly")

st.write('''The last analysis we graph we have is the average price trend across all years.

The top_yearly_stock function takes in the merged dataframe that contains the data of both the US and Spanish stocks. 
It then separates them by market and resamples by the year in order to create a multi-level index of year and symbol. This makes 
it possible for us to create a new data frame that has all the stocks’ average open prices based on the year. The function creates 
two bar graphs as visual visuals to show the performance of each stock from the years 2005 all the way to 2015 within their own markets. 
And just by looking at the two graphs ITX and AMGN seem to be the dominating stocks. For the Spanish market, the data for ITX and IBE 
started from 2009 because the CSV files we used did not contain their records for periods prior to 2009. This probably skewed our analysis 
overall, but I think we were able to see some of the trends in the two markets. 
''')
st.image('./imgs/bar.png')

st.header('Conclusion')

st.write('''There is strong evidence to suggest that it would be the best course of action to invest in stocks within the US stock market, although the volatile 
nature of the stock market itself may warrant some further research!''')
