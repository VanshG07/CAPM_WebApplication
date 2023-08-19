import plotly.express as px
import numpy as np

def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'],y=df[i],name=i)
    fig.update_layout(width =450,margin=dict(l=20,r=20,t=50,b=20),legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1,))
    return fig

#func to normalize prices based on initial price
def normalize(df_1):
    df=df_1.copy() #becoz there should not be any changes in original data
    for i in df.columns[1:]:
        df[i]=df[i]/df[i][0] #logic:Suppose TSLA it will first skip date column and then it will go into TSLA Column and after that the TSLA prices will be get divided by 1st price of TSLA(df[i][0])
    return df

#function to calculate daily returns
def daily_returns(df):
    df_daily_return=df.copy()
    for i in df.columns[1:]:
        for j in range(1,len(df)):
            df_daily_return[i][j]=((df[i][j]-df[i][j-1])/df[i][j-1])*100
        df_daily_return[i][0]=0
    return df_daily_return

#func to calculate beta
def calc_beta(stocks_daily_returns,stock):
    rm=stocks_daily_returns['sp500'].mean()*252

    b,a=np.polyfit(stocks_daily_returns['sp500'],stocks_daily_returns[stock],1) #we will pass stock so that it will create polyfit between 'SP500' and 'stock'
    return b,a #b=beta,a=alpha
