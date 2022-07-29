<p align="center"><img src="https://user-images.githubusercontent.com/79036525/181636228-3bfdf955-4cf9-44dc-8c21-68a954390f63.png"></p>

---
<p align="center">USING AI AND MACHINE LEARNING FOR GOODNESS</p>

---

- **Invezto** is an ML-Based solution to one of the most demanding jobs in the present market scenario - `Stock Market Prediction and Analysis`. 
- The stocks in the market are updated every day. Invezto studies the stock data from various stock markets with the help of different machine learning algorithms. 
- It also gives predictions on the future of these stock markets and how their value can be improved.

---
### <p align="center"><span>Check out our Product [here](https://sarjitapatra-invezto-main-ih4fph.streamlitapp.com/).</span></p>
### <p align="center"><span>[Stock Market Prediction Product Demo](https://drive.google.com/file/d/1WMEkgI6sJ5021GPn240TgEhJWdan87Iw/view?usp=sharing).</span></p>
### <p align="center"><span>[Portfolio Optimization Product Demo](https://drive.google.com/file/d/1hkkVQ-KTMiDb-XmUhn3rI-iggHVyqHXj/view?usp=sharing).</span></p>
---

## FEATURES :

#### STOCK PRICE PREDICTION
* Upload custom dataset / Analyze dataset of Companies like Google, Microsoft, etc.
  >The Data to be predicted is uploaded in .csv/.xls/.xlsx formats. The Dataset can also be viewed depending on the number of rows the user chooses.
* Analyze various graphs based on the uploaded Dataset
  >Different Graphs are available based on the Stock data. Some of the them are displayed below :
  
---

  <p align="center"><img src="https://user-images.githubusercontent.com/79036525/181626594-b2c7817b-5368-48f3-8ea3-1e8399ead86a.png" width="400" height="200"/> 
  <img src="https://user-images.githubusercontent.com/79036525/181626659-22b94c91-e757-4972-bc65-6d0315d8f513.png" width="400" height="200"/></p>
  
  <p align="center"><img src="https://user-images.githubusercontent.com/79036525/181627923-fc073275-03ee-4b18-bd53-4ffe80fd78a7.png" width="400" height="200"/> 
  <img src="https://user-images.githubusercontent.com/79036525/181628322-0bc6c9ad-ef07-4d11-b68b-6b0b5e051357.png" width="400" height="180"/></p>
  
  <p align="center"><img src="https://user-images.githubusercontent.com/79036525/181628150-f6659720-a918-40fd-8f67-1a898ce06faf.png" width="400" height="200"/>  
  <img src="https://user-images.githubusercontent.com/79036525/181628947-93ab8216-ea88-4272-b3c9-5a0126293bfb.png" width="400" height="200"/></p>
  
---

  > These graphs can be downloaded and stored in the local storage.
  
  > Trading Tools Used:
  >- `OLHC CHARTS`: - For analyzing the day-to-day sentiment of the market and forecasting future value changes in the market.
  <p align="center"><img src="https://user-images.githubusercontent.com/79036525/181631175-af92de70-b555-4a10-9c5d-3c7924abc1be.png" width="600" height="300"/></p>

  >- `CANDLESTICK CHARTS`: - To visualize and analyze the price movements over time for securities, derivatives, currencies, stocks, etc., and also to determine if the market is "BULLISH" or "BEARISH".
  <p align="center"><img src="https://user-images.githubusercontent.com/79036525/181631232-b13f5637-b41f-427d-9ce9-802c0f4eb499.png" width="600" height="300"/></p>

* The Closing values of the Stocks are predicted. Graphs related to the future prices are displayed.
* The Predicted data can be downloaded in *.csv* or *.xlsx* formats

---

#### PORTFOLIO OPTIMIZATION
This is implemented to construct a diverse portfolio of stocks across different industries for a person interested in acquiring wealth.

* Select the Starting date, ending date and the list of the Companies. The Portfolio Optimization is done using 3 methods :
>*   Mean Variance Method
>*   HRP Method
>*   mCVAR Method
* The resultant output of each of these is displayed accordingly. In each of the methods the total amount of investment has to be entered by the User in USD.


## TECHSTACK
- [KAGGLE](https://github.com/sarjitapatra/invezto/tree/master/TS_Model) - To prepare the Machine Learning Notebook
- VSCode, Streamlit -> To write code and display the predicted data
- Plotly -> To display all the graphs
- Heroku-> To deploy the Product
- MongoDB-> To store Companies data
- Language Used: `Python`
- Libraries:
```r
joblib==1.1.0
numpy==1.23.0
openpyxl==3.0.10
pandas==1.4.3
pandas-datareader==0.10.0
plotly==5.9.0
pymongo==4.1.1
pymongo[srv]
pyportfolioopt==1.5.3
sklearn==0.0
statsmodels==0.13.2
streamlit==1.11.0
XlsxWriter==3.0.3
tensorflow-cpu==2.9.1
yahoofinancials==1.6
yfinance==0.1.74
```

---
