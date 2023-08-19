import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import capm_func 

st.set_page_config(page_title="CAPM",
                   page_icon="chart_with_upwards_trend",
                   layout='wide') #In config there are 3 things :1)page_title 2)page_icon 3)layout if we skip layout=wide then the title wll come in center but we want it in our whole page therefore use layout

st.title("Capital Asset Pricing Model")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


st.markdown(hide_st_style, unsafe_allow_html=True)
col1,col2 =st.columns([1,1]) #[1,1] is width ratio u can also take [10,3],etc
with col1:
    stocks_list = st.multiselect("choose 4 stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:
    yr=st.number_input("Number of Years",1,10)

#downloading data
try:
    end =datetime.date.today()
    start=datetime.date(datetime.date.today().year-yr,datetime.date.today().month,datetime.date.today().day)
    SP500 =web.DataReader(['sp500'],'fred',start,end)
    #print(SP500.tail())
    stocks_df=pd.DataFrame()

    for stock in stocks_list:
        data=yf.download(stock,period=f'{yr}y')
        #print(data.head())
        stocks_df[f'{stock}']=data['Close'] 
    #print(stocks_df.tail()) 
    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    #print(stocks_df.dtypes)
    #print(SP500.dtypes)
    SP500.columns=['Date','sp500']
    stocks_df=pd.merge(stocks_df,SP500,on='Date',how='inner')
    #print(stocks_df)

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(),use_container_width=True)
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(),use_container_width=True)

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown("### Price of all stocks")
        st.plotly_chart(capm_func.interactive_plot(stocks_df))
    with col2:
        print(capm_func.normalize(stocks_df))
        st.markdown("### Price of all stocks After Normalization")
        st.plotly_chart(capm_func.interactive_plot(capm_func.normalize(stocks_df)))

    stocks_daily_returns=capm_func.daily_returns(stocks_df)
    print("Daily Returns Table\n",stocks_daily_returns.head())

    #create dict
    beta={}
    alpha={}
    for i in stocks_daily_returns.columns:
        if i!='Date' and i !='sp500': #skip these 2 cloumns
            b,a=capm_func.calc_beta(stocks_daily_returns,i) #we will pass i becoz it is name of the stock

            beta[i]=b #name of the stock will be KEY and beta value will be passed in VALUE
            alpha[i]=a
    print(beta,alpha)  

    #now we will display it in df 
    beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
    beta_df['Stock']=beta.keys()
    beta_df['Beta Value']=[str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df,use_container_width=True)

    rf=0 #rf=eisk free
    rm=stocks_daily_returns['sp500'].mean()*252 #252 is days

    return_df=pd.DataFrame()
    return_value=[]
    for stock,value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))
    return_df['Stock']=stocks_list

    return_df['Return Value']=return_value

    with col2:
        st.markdown('### Calculated Return Using CAPM')
        st.dataframe(return_df,use_container_width=True)

except:
    st.write("Please select valid inputs!")
