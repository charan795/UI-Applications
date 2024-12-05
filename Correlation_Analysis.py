#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:41:54 2024

@author: charanmakkina
"""

import sys
sys.path.append('MultiFactorModel')

import pandas as pd

def rolling_corr(df,window_size):
    rolling_corrs={}
    factors=df.columns
    for i in range(len(factors)):
        for j in range(i+1,len(factors)):
            factor1=factors[i]
            factor2=factors[j]
            rolling_corrs[f'{factor1}_{factor2}_corr']=df[factor1].rolling(
                window=window_size).corr(df[factor2])
    return pd.DataFrame(rolling_corrs)

def rolling_corr_one_factors(df,factor1,window_size):
    rolling_corrs={}
    factor_cols=[col for col in df.columns if col!=factor1]
    for factor2 in factor_cols:
        rolling_corrs[f'{factor2}_corr']=df[factor1].rolling(
            window=window_size).corr(df[factor2])
    return pd.DataFrame(rolling_corrs)
#rolling_corrs_df=rolling_corr(factors,window_size=24)
#window_size=24
#rolling_corrs_df=rolling_corr_one_factors(factors,window_size,factors.columns[0])



