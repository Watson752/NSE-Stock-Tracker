#About Us Page

#streamlit run c:\Users\allen\Desktop\About Us Page.py

import streamlit as st

st.title('About Our Project')

st.write("""The initiative to build an interactive “stock market tracker” was undertaken by Srivatsan Murali and Mark Allen of grade XII, Arsha Vidya Mandir. 
An ambitious idea initially, it demanded a strong conceptual understanding of the stock market. 
We spent our initial days studying and coming to grips with the intricacies and complexities of the stock market.

The plan was to proceed with AlphaVantage, a “free” stock API, for the backend (collecting statistics) and Tkinter to build the user interface for our project. 
Unfortunately, we ran into a few issues early on with our project. 
The AlphaVantage API did offer its services for free, but an overwhelming majority of its important and more interesting features were restricted behind a steep paywall. 
We soon realised that AlphaVantage wasn’t the ideal API since we wished to incorporate as many features as we could. 
After scouring the Internet for a few days, we came across Yahoo! Finance API, a free and unrestricted API that allows us to access all varieties of stock information, history, and current trends. 
With the discovery of Yahoo! Finance, we had settled the issue with the backend. 

A strong backend is only as good as its front end. 
Our user interface, initially powered by Tkinter, had to be intuitive yet sophisticated, clean yet informative. 
Since our topic per se has an excess of information, it was critical we ensured all the data was understandable and interpretable by the uninitiated, our target audience. 
We were now in need of a module to process and present all of this data in the form of easy-to-understand graphs and charts. 
We immediately turned to the “pandas” and “Matplotlib” modules to create visual versions of raw data from the API. 
Since it was critical to lay out a rough idea for our home-page (position of buttons, search bars, scroll bars, widgets, frames, colours and many more), we began working on the user interface instead. 
Tkinter’s learning curve posed a challenge to us as we were not familiar with designing graphical user interfaces. 
Both us felt uncomfortable with Tkinter as it was entirely alien to us, and the amount of lines of code we had to write for even the simplest of functions seems inefficient. 
So we were on the hunt for a more efficient user interface module that also yielded more aesthetically pleasing results in comparison to Tkinter, which is rather rudimentary. 

We finally decided on utilizing the Streamlit module to design our user interface. 
Boasting much simpler commands, which equated to much higher functionality, Streamlit was ideal for our project since it not only replaced Tkinter (for the graphical user interface), it also pushed Matplotlib and pandas into redundancy. 
Streamlit was capable of data visualization as well, this largely reduced the complexity of our code, which saved us a lot of time. 
→ WE CAN FILL IN ABOUT SQL AFTER WE ARE DONE WITH IT ←
""")