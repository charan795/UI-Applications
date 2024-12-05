#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 21:25:54 2024

@author: charanmakkina
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import date

def fetch_factor_data(db):
    conn=sqlite3.connect(db)
    query_macro="select * FROM macro_variables2"
    df=pd.read_sql_query(query_macro,conn)
    df.set_index('observation_date',inplace=True)
    df.index=pd.to_datetime(df.index)
    df=df.astype(float)
    df=df.iloc[df.index>'1997-07-31']
    df_monthly=df.resample('MS').asfreq()
    df_monthly_interpolated=df_monthly.interpolate()
    df_monthly_factors=df_monthly_interpolated.copy()
    df_monthly_factors=df_monthly_factors.rename(columns={'CPALTT01USM657N':'Consumer_Price_Index',
                                       'BUSINV':'Business_Inventories',
                                       'INDPRO':'Industrial_Production',
                                       'PPIACO':'Producer_Price_Index',
                                       'UNRATE':'Unemployment_Rate',
                                       'BOPGSTB':'Trade_Balance',
                                       'CIVPART':'Labor_Force_Participation_Rate',
                                       'FEDFUNDS':'Federal_Funds_Effective_Rate',
                                       'GFDEBTN':'Federal_Debt',
                                       'M1SL':'Money_Supply_M1',
                                       'M2SL':'Money_Supply_M2',
                                       'MRTSSM44000USS':'Retail_Sales',
                                       'PCE':'Personal_Consumption_Expenditures',
                                       'UMCSENT':'Consumer_Sentiment_Index'}
                              )
    factor_return_variables=['GDP','Consumer_Price_Index','Producer_Price_Index','Industrial_Production',
                             'Retail_Sales','Trade_Balance','Money_Supply_M1','Money_Supply_M2',
                             'Personal_Consumption_Expenditures','Business_Inventories','Federal_Debt']
    df_monthly_factors_returns=df_monthly_factors.copy()
    df_monthly_factors_returns[factor_return_variables]=df_monthly_factors_returns[factor_return_variables].pct_change()
    return df_monthly_factors_returns

def fetch_index_data(db):
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor
    query_index="select * FROM index_data"

    
    #macro_df.dtypes
    #macro_df['CPALTT01USM657N']=macro_df['CPALTT01USM657N'].astype(float)
    
    index_df=pd.read_sql_query(query_index,conn)
    index_df.set_index('Date',inplace=True)
    index_df.index=pd.to_datetime(index_df.index)

    index_df.columns
    index_df=index_df.rename(columns={'^GSPC':'S&P 500 Index',
                                      '^DJI':'Dow Jones Industrial Average',
                                      '^IXIC':'Nasdaq Composite',
                                      '^RUT':'Russell 2000 Index',
                                      '^FTSE':'FTSE 100 Index',
                                      '^GDAXI':'DAX-Performance Index',
                                      '^FCHI':'France 40 Index',
                                      '^N225':'Nikkei 225 Index',
                                      '^HSI':'Hang Send Index',
                                      '000001.SS':'SSE Composite Index',
                                      '^AXJO':'S&P/ASX 200',
                                      '^GSPTSE':'S&P/TSX Composite Index',
                                      '^KS11':'KOSPI Index'})
    #index_df.dtypes
    
    np.random.seed(42)
    n_assets=len(index_df.columns)
    random_weights=np.random.uniform(0.1,0.2,n_assets)
    
    normalized_weights=random_weights/random_weights.sum()
    
    returns_indices_df=index_df.pct_change()
    weighted_returns_indices_df=returns_indices_df.mul(normalized_weights,axis=1)
    portfolio_returns=weighted_returns_indices_df.sum(axis=1)
    return index_df,random_weights,returns_indices_df,portfolio_returns
#fetch_index_macro_data('sqlite (2).db')






