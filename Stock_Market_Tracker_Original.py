#                                 -------- IMPORTS ----------

from turtle import goto, title, width

import streamlit as st

import urllib
import yfinance as yf
import sqlite3 as sq
import datetime as dt
import pandas as pd


import plotly.graph_objects as go
from plotly.subplots import make_subplots



#                                 -------- HTML INTEGRATION ----------

# Integration of Html and Python for the Row on the top of the app -> To access the About us and Stock Market for beginners page
# HTML Integration - Top Menu Bar - Video Courses
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #FF4B4B;">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>  
  

  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">       
        <a class="nav-link" href="https://www.youtube.com/playlist?list=PLyJjbvQFJHAEF4QukyMzBBCI0C_gujRoT" style="color: red; background-color: transparent;" target="_blank">Video Courses</a>
      </li>
    </ul>
  </div>
  
</nav>
""", unsafe_allow_html=True)
# Contains link for YouTube Playlist - Videos on Stock Market

# Addressing Sidebar
st.sidebar.title("Sidebar")



#Inputing Stock Id is the main gateway to use all the functions od the Yfinance library
st.sidebar.subheader('Input stock id:')

#The list of tickers displayed are from the source website, we will change it to a list of trackers from Yfinance itself
Tickers = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]
Tickers = Tickers.SYMBOL.to_list()

# Select box for easy access of the Nse stocks. 
# Note that the tickers are all NSE stocks and all are from a private website which may not be totally reliable
Stckinp = st.sidebar.selectbox('NSE Stocks',Tickers)

# All stock tickers applied to yfinance must contain .NS at the end
Stockid = Stckinp+'.NS'
Ticker = yf.Ticker(Stockid)

#                                 -------- FEATURES SELECT ----------


# The total amount of functions that we provide in this app is known through the feat_list
feat_list = ['None','Stock summary','General info','Historical data','Price plot','Volume plot','Calculator','Major Holders',
'Balance Sheet','Cash Flow','Earnings','Financials','Actions','Sustainability','Analyst recomendations',
'Earning Calendar','Latest News']

Function = st.sidebar.selectbox("Select any one of the features:",feat_list)

# The periods list has all the timeperiods that yfinance allows. 
# Storing the timeperiods as a list helps us later use them as selectbars for users to choose the timeframes as they like to get refined data
Periods = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

# The convert function is defined for easily accessing the pandas dataframe that yfinance provides in form of csv files
def convert_df(df):
    return df.to_csv().encode('utf-8')





#                                 -------- MARKS BEGINNING OF FUNCTIONALITIES PROVIDED ----------




def calc():

    total = 0
    st.subheader("Calculator")
    st.write("You have activated the simple stock value calculator. It requires two inputs, current share price and number of shares. It returns the value of your stock. Please enter the values in the appropriate slot in the sidebar")
    shpr = st.number_input("Current Share Price (Per)")
    shno = st.number_input("Current Holdings (Number of Shares)")
    total = shpr*shno
    st.write("The current value of your stock is ",total,"INR")




# We use Tickers info dictionary and access longbusinesssummary which easily lets us us display the description of every nse company
def Stockinfo():
    
    if len(Stockid) != 0:
        
        #Using try,except method helps us deal with key error where there is no summary for the chosen nse stock
        try:

            string_logo = '<img src=%s>' % Ticker.info['logo_url']
            st.markdown(string_logo, unsafe_allow_html=True)
            
            stckname = Ticker.info['longName']
            st.header('**%s**' % stckname)

            st.write(Ticker.info['longBusinessSummary'])

            Para = Ticker.info['longBusinessSummary'].split('.')

            for i in Para:
                if i != Para[-1]:
                    st.write(i,'.')
                else:
                    st.write(i)
                    # To make sure the last sentence doesn't end with two periods

        except KeyError:

            st.info("Please note that this stock doesn't have a summary response from Yahoo finance library")




#General info the Second function that we define which lets us access the info dictionary and display by key and value wise method.
def General_info():

    st.header('General Info')
    stckname = Ticker.info

    for i,j in stckname.items():
        # To make sure the summary is not just a huge paragraph, we use this simple for loop for making seperate sentences 
        if i!= 'longBusinessSummary' and len(str(j)) ==1:
            st.info(i.title()+':')
            st.info('Not Available')
        elif i!= 'longBusinessSummary': 
            st.info(i.title()+':') 
            
            st.info(j)




def Historical_data():
    st.header('**Historical Data**')

    today = dt.date.today()
    today_1yr= today - dt.timedelta(days=365)

    Start = st.date_input("Start date:",today_1yr)
    End = st.date_input("End date:",today)
    
    History = Ticker.history(start = Start,end = End)

    st.header('**Historical Data**')
    st.write(History)




# Price plot the Third Function that we define. It lets us access the price plot of stocks to track.
def Priceplt():

    st.header('**Price Chart**')
    st.subheader('Parameter:')

    today = dt.date.today()
    today_1yr= today - dt.timedelta(days=365)

    # This is where we use start and end as parameters to whichever dates the user wants for the plots plus the default dates are the current date and 1 year before the current date
    Start = st.date_input("Start date:",today_1yr)
    End = st.date_input("End date:",today)

    tperiod = st.selectbox('Time period:',Periods) # The graph is not refined even after reducing the period

    History = Ticker.history(period = tperiod,start = Start,end = End)
    # To change the history dataframe  as per the users wish of time period

    #Fig is the first plot figue that we make
    #It is a simple plot based on the closing prices of the stock
    fig = go.Figure(data= go.Scatter(x=History.index,y=History['Close'],mode = 'lines'))
    st.plotly_chart(fig)
    
    # We use the convert_df() to easily download the history dataframe as csv/ excel files
    csv = convert_df(History)
    st.download_button("Download History as csv file",csv,(Stckinp+"_History.csv"),"text/csv",key='download-csv')




    # We provide the option of displaying the graphs in forms of candle stick format
    Candle_resp = st.button('Candle stick graph?')

    if Candle_resp == True:
        #Fig2 is our second figure. 
        # The open, high and low are the parameters inside go.candlestick().
        # It easily allows us to make the candle stick graphs -> (a graph that displays ups and downs in green and red candles, The open is only at the start of the graph )
        
        # We use make_subplots which is part of plotly, It is used to refer the price plot and make the candle stock graph
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Candlestick(x=History.index,open=History['Open'],high=History['High'],low=History['Low'],close=History['Close']))
        st.plotly_chart(fig2)
    



    DMA_resp = st.button('20 Daily Moving Average')
    # DMA is the third graph. It is basically a graph which converts the close and open to price differents.
    # It graphs the differences as a continous plot
        
    if DMA_resp == True:
        
        # We take DMATab-> a pandasdataframe where we make a new column that accounts the difference
        # By making DMATab we don't disturb the History dataframe which is seperately used for plotting price and volume too
        
        DMATab = Ticker.history(period = tperiod,start = Start,end = End)
        DMATab['diff'] = DMATab['Close'] - DMATab['Open']
        DMATab.loc[DMATab['diff']>=0, 'color'] = 'green'
        DMATab.loc[DMATab['diff']<0, 'color'] = 'red'

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        
        # We combine the Candle stick graph and the DMA graph which is a common preference of a lot of stock analysts
        fig3.add_trace(go.Candlestick(x=DMATab.index,
                              open=DMATab['Open'],
                              high=DMATab['High'],
                              low=DMATab['Low'],
                              close=DMATab['Close'],
                              name='Price'))
        
        fig3.add_trace(go.Scatter(x=DMATab.index,y=DMATab['Close'].rolling(window=20).mean(),marker_color='blue',name='20 Day MA'))
        fig3.add_trace(go.Bar(x=DMATab.index, y=DMATab['Volume'], name='Volume', marker={'color':DMATab['color']}),secondary_y=True)
        
        # We use the range to scale the DMA plot as we wish
        fig3.update_yaxes(range=[0,700000000],secondary_y=True) #The range doesn't change when we use range FIX
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(xaxis_rangeslider_visible=True)
        fig3.update_layout(title={'text':Stckinp, 'x':0.5})
        
        st.plotly_chart(fig3)




    Volume_resp = st.button('Volume as subplot?')
    # We take History again for plotting the Volumns of tsock traded each day
    
    if Volume_resp == True: # Volume bars not the same for every stock, Fix the logical error

        # Make suplots is again used to show volume as bargraphs and prices as a plot where the correlation between the volumes and prices can be shown
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])

        fig4.add_trace(go.Scatter(x=History.index,y=History['Close'],name='Price'),secondary_y=False)
        fig4.add_trace(go.Bar(x=History.index,y=History['Volume'],name='Volume'),secondary_y=True)

        fig4.update_yaxes(range=[0,10500000],secondary_y=True)
        fig4.update_yaxes(visible=False, secondary_y=True)
        st.plotly_chart(fig4)




# Volume plot the Fourth function that we define. It can be confused with the already used price plot vaariations but volume as a seperate plot helps traders in other ways
def Volumeplt():

    st.header('**Volume Plot**')
    st.subheader('Parameters:')

    Start = st.date_input("Start date:",dt.date(2022,1,1))
    End = st.date_input("End date:",dt.date(2022,2,5))

    tperiod = st.selectbox('Time period:',Periods) # The graph is not refined even after reducing the period

    History = Ticker.history(period = Periods,start = Start,end = End)
    fig = go.Figure(data= go.Scatter(x=History.index,y=History['Volume'],mode = 'lines+markers')) #Using lines and markers show particulars points ->(markers where the volume takes a sharp or drastic turn while lines are to represent the volumes)
    st.plotly_chart(fig)






# Major Holders the Fifth function that we define. Major holders let us know about the categories of stakeholders in the company
def Major_Holders():
    st.header('**Major Holders**')

    Mhol_df = Ticker.major_holders
    st.write(Mhol_df)
    
    csv = convert_df(Mhol_df) #To download the pandas dataframe as csv file
    st.download_button("Download Major holders as csv file",csv,(Stckinp+"_Major_Holders.csv"),"text/csv",key='download-csv')

    Pie_Chart = st.button('Pie Chart of holders')

    #We create two lists -> labels and values, labels contains the names of the stakeholder types and values contain the percentage of each of the stakeholders
    labels = []
    for j in Mhol_df[1]: 
        labels+=[j]

    values = []
    for i in Mhol_df[0]:
        if i[-1] == '%':
            values+=[i[:-1]]
    
    if Pie_Chart == True:
        fig = go.Figure(go.Pie(labels = labels,values = values))
        st.write(fig)

        # We encountered in a difference in the representation of the pie chart and the values in the dataframe. 
        # Upon further understanding we believe the difference in the pie chart and the dataframe is due to the floating shares 
        # -> the floating shares are shares that are being traded and is not kept a constant record of since they can't be assessed easily
        # Only upon a concentration of these shares are they monitored and recognised

        st.warning('Please note that the pie chart information may vary from the table due to the presence of floating shares')




# Balance sheet is the Sixth function that we define. Balance sheets are the credit and debit of the company all documented into one table. 
# Also the balance sheet is updated based on every financial year denoted as FY<year> as in the current time it is FY<2020-21>
def Balance_Sheet():
    st.header('**Balance Sheet**')
    Balance_Sheet = Ticker.balance_sheet
    st.write(Balance_Sheet)

    csv = convert_df(Balance_Sheet)
    st.download_button("Download Balance Sheet as csv file",csv,(Stckinp+"_Balance_Sheet.csv"),"text/csv",key='download-csv')

    # Quaterly balance sheets can also be accessed. Every year is split into Q1,Q2,Q3,Q4 where every quarter is 3 months.
    Qbal_resp = st.button('Quaterly Balance Sheet')

    if Qbal_resp == True:
        st.write(Ticker.quarterly_balance_sheet)

        csv = convert_df(Balance_Sheet) # DuplicateWidgetID: There are multiple identical st.download_button widgets with key='download-csv'.
                                        #To fix this, please make sure that the key argument is unique for each st.download_button you create.
        st.download_button("Download Balance Sheet as csv file",csv,(Stckinp+"_Balance_Sheet.csv"),"text/csv",key='download-csv')




#Cashflow is the Seventh Function that we define. We 
def Cash_Flow():
    st.header('Cash Flow')
    Cash_Flow = Ticker.cashflow
    
    csv = convert_df(Cash_Flow)
    st.download_button("Download Cashflow as csv file",csv,(Stckinp+"_Cashflow.csv"),"text/csv",key='download-csv')
    st.write()

    Qbal_resp = st.button('Quaterly Cashflow')
    if Qbal_resp == True:
        Quaterly_Cashflow = Ticker.quarterly_cashflow
        st.write()

        csv = convert_df(Quaterly_Cashflow)
        st.download_button("Download Quaterly cashflow as csv file",csv,(Stckinp+"_Quaterly_cashflow.csv"),"text/csv",key='download-csv')




def Earnings():
    st.header('Earnings')
    if len(Ticker.earnings.index) != 0:
        Earning = st.write(Ticker.earnings)
        csv = convert_df(Earning)
        st.download_button("Download Earning as csv file",csv,(Stckinp+"_Earning.csv"),"text/csv",key='download-csv')
        
    else:
        st.warning('Not available in Yfinance Library')




    Qbal_resp = st.button('Quaterly Earnings')
    if Qbal_resp == True:
        if len(Ticker.quarterly_earnings.index) != 0:
            Quaterly_earning = Ticker.quarterly_earnings
            result = st.write(Quaterly_earning)
            
            csv = convert_df(Quaterly_earning)
            st.download_button("Download Quaterly earning as csv file",csv,(Stckinp+"_Quaterly_earning.csv"),"text/csv",key='download-csv')
        else:
            result = st.warning('Not available in Yfinance Library')




def Financials():
    st.header('Financials')
    if len(Ticker.financials.index) != 0:
        Financials = Ticker.financials
        st.write(Financials)

        csv = convert_df(Financials)
        st.download_button("Download Financials as csv file",csv,(Stckinp+"_Financials.csv"),"text/csv",key='download-csv')
    else:
        st.warning('Not available in Yfinance Library')




    Qfin_resp = st.button('Quaterly Earnings')
    if Qfin_resp == True:
        if len(Ticker.quarterly_financials.index) != 0:
            Quaterly_Financials = Ticker.quarterly_financials
            result = st.write(Quaterly_Financials)
            
            csv = convert_df(Quaterly_Financials)
            st.download_button("Download Financials as csv file",csv,(Stckinp+"_Quaterly_Financials.csv"),"text/csv",key='download-csv')
        else:
            result = st.warning('Not available in Yfinance Library')




def Actions():
    st.header('Actions (Dividends and splits)')
    Actions = Ticker.actions
    st.write(Actions)
    
    csv = convert_df(Actions)
    st.download_button("Download Actions as csv file",csv,(Stckinp+"_Actions.csv"),"text/csv",key='download-csv')




def Sustainability():
    st.header('Sustainability')
    
    st.info(Ticker.sustainability) 




def Analyst_Recommendations():
    st.header('Analyst Recommendations')
    if (Ticker.recommendations) == None:
        st.info('Please note that there are no Analyst reccomendations for this stock in the Yahoo finance library as now. Sorry for the incovenience')
    else:
        st.write(Ticker.recommendations)



def Earning_Calendar():
    st.header('Earning Calendar')
    if len(Ticker.calendar.index) < 1: # The info doesn't pop even though the condition is given
        st.info('Please note that there are no Earning calendars for this stock in the Yahoo finance library as now. Sorry for the incovenience')
    else:
        st.write(Ticker.calendar)




def News():
    st.header('**Latest News**')
    news = st.write(Ticker.news)
    link = news[0]["link"] # ERROR Type error - None type
    urllib.request.urlopen(link)




#                                 -------- SPECIFYING THE FUNCTIONALITIES ----------




def Function_operate():
    if Function == 'None':
        st.write("##") 
    elif Function == 'Stock summary':
        Stockinfo()
    elif Function == 'General info':
        General_info()
    elif Function == 'Historical data':
        Historical_data()
    elif Function == 'Price plot':
        Priceplt()
    elif Function == 'Volume plot':
        Volumeplt()
    elif Function == 'Calculator':
        calc()
    elif Function == 'Major Holders':
        Major_Holders()
    elif Function == 'Balance Sheet':
        Balance_Sheet()
    elif Function == 'Cash Flow':
        Cash_Flow()
    elif Function == 'Earnings':
        Earnings()
    elif Function == 'Financials':
        Financials()
    elif Function == 'Actions':
        Actions()
    elif Function == 'Sustainability':
        Sustainability()
    elif Function == 'Analyst recomendations':
        Analyst_Recommendations()
    elif Function == 'Earning Calendar':
        Earning_Calendar()
    elif Function == 'Latest News':
        News()



#                                 -------- STREAMLIT GUI ----------

st.title ("Stock Market Screener")

# The main image of our site displayed via st.image() which is very flexible in importing images
source = 'Source: https://www.huffpost.com/entry/why-the-market-keeps-goin_b_4466037'
st.image('https://i.huffpost.com/gen/1529947/images/o-STOCK-MARKET-facebook.jpg',width = 750,caption =source)

# Short introduction for any common layman
st.subheader('This stock tracker app is mainly for NSE stocks')
st.subheader('Made by Srivathsan Murali and Mark Allen')

#Important warning for making sure that this app is only made for exhibiting the python knowledge that we are using to make the app

st.warning('Please note that this app was made only for expanding the coding knowledge and is no way directed towards using in real life. We do not advise anyone to use this app for making any form of trading decisions')
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)


Function_operate()


#                                 -------- MARKS BEGINNING OF SIDEBAR FUNCTIONS ----------



# Subheader to define sidebar content
st.sidebar.subheader("Information")


#Sidebar function for project information
def infoside():
    menu1 = ["None","Introduction To The Stock Market", "About Us"]
    option1 = st.sidebar.selectbox("View", menu1)

    if option1 == "None":
        st.write('##')




#                                 -------- INTRO TO STOCKS PAGE ----------



    elif option1 == "Introduction To The Stock Market":
        st.subheader("Introduction To The Stock Market")

        st.write("""  The concept of the stock market is still alien to some. 
        The level of awareness has increased tremendously in recent times, thanks to active promotion on the Internet and the rise of mobile applications that simplify the investment process. 
        Despite the recent availability of such resources, there is no denying that such complex ideas are best understood when explained in simple terms, and that is exactly what this page wishes to accomplish: 
        Your layman’s guide to the world of stock trading. 


Let us begin with a quintessential question: What is a stock? 
If an establishment (or simply, “company”) is in need of money, it makes sense for them to turn to people who wish to give them the capital they require, in exchange for an equal percentage of the company’s return. 
Imagine the ownership of a company is depicted as a pie, every investor is a “shareholder”, hence they own a small slice of this pie. 
And this “slice” is a share, a fraction of the stock. 
But ownership of a share doesn’t directly translate into ownership of a fraction of the company. 
If the company owns offices and warehouses, a shareholder doesn’t own a part of these assets. 
Shareholders merely own the shares that the company has issued, not their assets. 
This is called “equity ownership”, which is the basic principle to understanding stock trading


So, what is a stock market? 
It is essentially a “marketplace” for trading shares. 
There are various corporations in the world that seek capital to undertake projects and ventures. 
And the people who believe that they too can profit off of a company’s success involve themselves in the stock market. 
The stock market doesn’t restrict investors to only owning shares in one company, they can diversify their investments by investing their money in any number of companies from various backgrounds as per their wish. 
The number of shares that a company wishes to sell to investors is decided by the company. 
These “issued shares” are put up for sale, and interested investors purchase them. 


After purchasing, the investor can decide if they want to hold on to the share or sell their shares. 
The value of the share increases/ decreases depending on the current condition of the company’s performance. 
If the company launches a product which has a lot of positive publicity, chances of sales increase, which is directly proportional to increase in the value of the company. 


The stock market and stock trading are strictly regulated and centralised, meaning the governmental bodies hold the authority to implement laws to eliminate risk of malpractice. 
Hopefully, this introduction to the wonderful world of stock trading has been sufficient. 
Remember, understanding the working of the stock market and its nuances and intricacies is critical to achieve success. 


An industry as complex as the stock market is overloaded with technical terms which are instrumental in one’s success. 
Unfortunately, the vocabulary is often difficult for the layman to fully comprehend. 
Here’s a list of stock trading jargon which we believe is absolutely essential:


→ Agent - An agent is a “brokerage” firm that acts as a middleman between an investor and the stock market.
They buy/ sell shares on the behalf of the investor, and they collect a small percentage of the returns as commission for their services.


→ “Bull Market” - Denotes a time of prosperity, when share prices are rising. 
Rising share prices mean that share owners can now sell their shares for a greater profit.


→ “Bear Market” - The antithesis to the Bull Market. 
It denotes a period when share prices start slumping from a high, this results in the share losing value.


→ “Blue Chip Stock” - Shares belonging to well established corporate giants (TCS, SBI, Coal India, etc). 
These shares are believed to be safer alternatives, since the chances of exponential loss are reduced.


→ Open/ Closing Price - The “opening price” of a stock refers to the value of a share when the market begins its operations for the day. 
The “closing price” of a stock refers to the value of a share when the market closes for the day. The prices fluctuate throughout the day and investors can trade when their shares reach their preferred value. 


→ Volume - As the name suggests, it is the term used to address the number of stocks traded within a time span (sold and bought).   """)


#                                 -------- ABOUT US PAGE ----------    



    elif option1 == "About Us":
        st.title('About Our Project')

        st.write("""


The initiative to build an interactive “stock market tracker” was undertaken by Srivatsan Murali and Mark Allen of grade XII, Arsha Vidya Mandir. An ambitious idea initially, it demanded a strong conceptual understanding of the stock market. We spent our initial days studying and coming to grips with the intricacies and complexities of the stock market.


The plan was to proceed with AlphaVantage, a “free” stock API, for the backend (collecting statistics) and Tkinter to build the user interface for our project. Unfortunately, we ran into a few issues early on with our project. The AlphaVantage API did offer its services for free, but an overwhelming majority of its important and more interesting features were restricted behind a steep paywall. We soon realised that AlphaVantage wasn’t the ideal API since we wished to incorporate as many features as we could. After scouring the Internet for a few days, we came across Yahoo! Finance API, a free and unrestricted API that allows us to access all varieties of stock information, history, and current trends. With the discovery of Yahoo! Finance, we had settled the issue with the backend. 


A strong backend is only as good as its front end. Our user interface, initially powered by Tkinter, had to be intuitive yet sophisticated, clean yet informative. Since our topic per se has an excess of information, it was critical we ensured all the data was understandable and interpretable by the uninitiated, our target audience. We were now in need of a module to process and present all of this data in the form of easy-to-understand graphs and charts. We immediately turned to the “pandas” and “Matplotlib” modules to create visual versions of raw data from the API. Since it was critical to lay out a rough idea for our home-page (position of buttons, search bars, scroll bars, widgets, frames, colours and many more), we began working on the user interface instead. Tkinter’s learning curve posed a challenge to us as we were not familiar with designing graphical user interfaces. Both us felt uncomfortable with Tkinter as it was entirely alien to us, and the amount of lines of code we had to write for even the simplest of functions seems inefficient. So we were on the hunt for a more efficient user interface module that also yielded more aesthetically pleasing results in comparison to Tkinter, which is rather rudimentary. 


We finally decided on utilizing the Streamlit module to design our user interface. Boasting much simpler commands, which equated to much higher functionality, Streamlit was ideal for our project since it not only replaced Tkinter (for the graphical user interface), it also pushed Matplotlib and pandas into redundancy. Streamlit was capable of data visualization as well, this largely reduced the complexity of our code, which saved us a lot of time.


As a form of integrating our SQL learning into our project, we decided to perform the SQLite3 connectivity to Python. We achieved this by creating a Login/ Sign Up function. SQL is effectively integrated into the program, by only allowing users to access the data if they have registered in the application. We created a database and table to store the user account information through SQL-Python connectivity. The feature is fully functional and is critical to the proper working of the application and its services.
""")
        
infoside()

st.sidebar.subheader("##")



#                                 -------- LOGIN / SIGN UP SIDEBAR ----------





# End of Function_operate
# Function Operate is later called


# Creating a Login/ Sign Up Module - Integrate Into Sidebar

# SQLite3 connectivity w/ database
conn = sq.connect('acc.db')
c = conn.cursor()

# Create table function
def table_create():
    
    c.execute('CREATE TABLE IF NOT EXISTS userdetails(username TEXT, password TEXT)')

# Insert user details into table
def add_data(username, password):
    
    c.execute('INSERT INTO userdetails(username, password) VALUES (?,?)', (username, password))
    conn.commit()

# Insert login details to verify membership
def login(username, password):
    
    c.execute('SELECT * FROM userdetails WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    

    return data

# Function to view registered users
def view_users():
    
    c.execute(' SELECT * FROM userdetails')
    data = c.fetchall()

    return data





#                                 -------- MARKS BEGINNING OF SIDEBAR FUNCTIONS ----------





# Membership Sidebar Function

# Subheader to define sidebar content
st.sidebar.subheader("Membership")

def member():
    #Login/ Sign Up Sidebar
    
    
    st.title("Login/ Sign Up Status")
    menu = ["Login","Sign Up"]
    option = st.sidebar.selectbox("Membership Function", menu)
    
    
    if option == "Login":
        st.subheader("Login Page")

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type = 'password')
        
        
        if st.sidebar.button("Login"):
            table_create()
            result = login(username, password)
            
            if result :
                st.success("Logged In Successfully. Welcome "+username+"!")

                
        
            else:
                st.warning("Incorrect Login Credentials")
        else:
            pass



            
    
    elif option == "Sign Up":
        st.subheader("Create New Account")

        newuser = st.sidebar.text_input("Username")
        newpass = st.sidebar.text_input("Password", type = 'password')

        if st.sidebar.button("Sign Up"):
            table_create()
            add_data(newuser, newpass)


            st.success("Account Created Successfully")
            st.info("You May Now Use These Credentials To Login")
            
member()
#End of Login/ Sign Up Modules

 # END OF CODE