#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 22:24:30 2024

@author: charanmakkina
"""

import sys
sys.path.append('MultiFactorModel')
import Retrive_Data as rd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score,mean_squared_error
import pandas as pd
from sklearn.linear_model import Ridge,Lasso
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.decomposition import PCA
rolling_window=24

def factors_preprocessing(factors):
    #factors=factors.iloc[:,:-1]
    factors=factors.dropna()
    factors.replace([np.inf,-np.inf],np.nan,inplace=True)
    factors=factors.dropna()
    return factors

def feature_selection_random_forest_regressor(window_df,factors,n_estimators=100,importance_threshold=0.9):
    X=window_df.drop('Portfolio',axis=1)
    y=window_df['Portfolio']
    #window_df=s_df
    rf_model=RandomForestRegressor(n_estimators=n_estimators,
                                   random_state=42)
    rf_model.fit(X,y)
    #y_pred=rf_model.predict(X)
    #r2=r2_score(y,y_pred)
    #print(r2)
    feature_importances=rf_model.feature_importances_
    feature_importance_pairs=sorted(zip(feature_importances,factors),reverse=True)
    cumulative_importance=0
    selected_features=[]
    for importance,feature in feature_importance_pairs:
        if cumulative_importance>=importance_threshold:
            break
        selected_features.append(feature)
        cumulative_importance+=importance
    return selected_features

def rolling_regression_using_OLS(df,factors,rolling_window):
    results=[]
    r2_list=[]
    #window_df=s_df
    selected_features_list=[]
    for end in range(rolling_window,len(df)+1):
        window_df=df.iloc[end-rolling_window:end]
        #print(window_df.columns)
        selected_features=feature_selection_random_forest_regressor(window_df,factors)
        X=window_df[selected_features]
        y=window_df['Portfolio']
        model=sm.OLS(y,X)
        result=model.fit()
        result.summary()
        feature_betas=result.params[1:]
        feature_betas=pd.DataFrame([feature_betas],columns=selected_features)
        feature_betas['Const']=result.params.iloc[0]
        results.append(feature_betas)
        r2_list.append(result.rsquared)
        selected_features_list.append(selected_features)
    results_df=pd.concat(results)
    results_df.index=df.index[rolling_window-1:]
    r2_df=pd.DataFrame(r2_list,index=df.index[rolling_window-1:],columns=['r2_score'])

                            #columns=['const']+X.columns)
    return results_df,r2_df,selected_features_list


#return_attribution=rolling_results.sum(axis=1)
def calculate_rolling_attribution(df,rolling_results):
    attribution=[]
    contributions=[]
    
    for i,end in enumerate(range(rolling_window,len(df)+1)):
        #print(end,i)
        #window_df=df.iloc[end-rolling_window:end]
        betas=rolling_results.iloc[end-rolling_window]
        betas=betas[~np.isnan(betas)]
        cols=[x for x in betas.index if x!='Const']

        X_current=df.iloc[end-1][cols]
        cols=cols+['Const']
        betas=betas.reindex(cols)
        X_current_with_constant=np.concatenate((X_current,[1]))
        attribution.append(np.dot(X_current_with_constant,betas))
        contributions.append(X_current*betas.drop('Const'))
    
    attribution_df=pd.DataFrame(attribution,index=df.index[rolling_window-1:],
                                columns=['Attributed Returns'])
    factor_contributions_df=pd.DataFrame(contributions,index=df.index[rolling_window-1:])
                                #columns=['Attributed Returns'])
    return attribution_df,factor_contributions_df

def return_attribution_factor_contribution(portfolio_returns,factors):


    #portfolio_returns=rd.portfolio_returns
    portfolio_returns=portfolio_returns.iloc[1:]
    portfolio_returns=portfolio_returns[portfolio_returns.index.isin(factors.index)]
    scaler=StandardScaler()
    s_portfolio_returns=scaler.fit_transform(pd.DataFrame(portfolio_returns))
    #factor_return_variables=['GDP','Consumer_Price_Index','Producer_Price_Index','Industrial_Production',
    #                         'Retail_Sales','Trade_Balance','Money_Supply_M1','Money_Supply_M2',
    #                         'Personal_Consumption_Expenditures','Business_Inventories','Federal_Debt']
    #factors.loc[:,factor_return_variables]=factors.loc[:,factor_return_variables]*100
    s_factors=scaler.fit_transform(pd.DataFrame(factors))
    s_factors=pd.DataFrame(s_factors,columns=factors.columns,index=factors.index)
    s_portfolio_returns=pd.Series(s_portfolio_returns.flatten(),index=portfolio_returns.index)

    s_df=pd.concat([s_portfolio_returns,s_factors],axis=1)
    s_df.rename(columns={0:'Portfolio'},inplace=True)
    
    rolling_results,r2_df,selected_features_list=rolling_regression_using_OLS(s_df,factors,rolling_window=24)


    return_attribution,factor_contri=calculate_rolling_attribution(s_df, rolling_results)
    
    return return_attribution,factor_contri,rolling_results,r2_df


#return_attribution,factor_contri,rolling_results,r2_df=return_attribution_factor_contribution(rd.portfolio_returns)
        

    
    
        
        
        
        
        
        
        
        
        
