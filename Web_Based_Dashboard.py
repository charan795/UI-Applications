#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 20:28:24 2024

@author: charanmakkina
"""

import dash
from dash import dcc,html,Input,Output,dash_table,State
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import Correlation_Analysis as ca
import Retrive_Data as rd
import Factor_Return_Attribution_OLS as fra
from sklearn.preprocessing import StandardScaler

app=dash.Dash(__name__)
index_df,random_weights,returns_indices_df,_=rd.fetch_index_data('sqlite (3).db')
macro_df=rd.fetch_factor_data('sqlite (3).db')
factors=fra.factors_preprocessing(macro_df)
numeric_weights=random_weights
returns=returns_indices_df

#return_attribution,attributions,betas,r2_scores=fra.return_attribution_factor_contribution(portfolio_returns)

app.layout=html.Div([
    html.H1("Portfolio Return Attribution Dashboard"),
    html.Label("Set asset allocations:"),
    html.Div([
        html.Div([
        html.Label(f'{returns.columns[i]}'),
        dcc.Input(id=f'input-weight{i}',type='number',
                  value=numeric_weights[i],step=0.01)],style={'display':'inline-block','margin':'5px'})
        for i in range(len(numeric_weights))
        ],id='weights-container'),
    html.Button('Update',id='update-button',n_clicks=0),
    html.Div([
        html.Label('Select factor to display correlations with other factors'),
        dcc.Dropdown(
            id='factor-dropdown',
            options=[{'label':factor,'value':
                      factor} for factor in factors.columns],
            value=factors.columns[0],
            style={'width':'50%'}
            ),
        ]),
    html.Div([
        html.Label('Select Index to display correlations with other Indices'),
        dcc.Dropdown(
            id='index-dropdown',
            options=[{'label':index,'value':
                      index} for index in returns.columns],
            value=returns.columns[0],
            style={'width':'50%'}
            ),
        ]),
    dcc.Graph(id='return-graph'),
    dcc.Graph(id='attribution-graph'),
    dcc.Graph(id='factor-correlations-graph'),
    dcc.Graph(id='index-correlations-graph'),
    dcc.Graph(id='factor-exposures-graph'),
    dcc.Graph(id='factor-beta-return-graph'),
    dcc.Graph(id='factor-exposures-outliers-graph'),


    html.Div(id='attribution-data',style={'display':'none'}),
    dcc.Tabs([
        dcc.Tab(label='Factor Betas',children=[
    html.Div([
        html.H2('Betas Table'),
        dash_table.DataTable(
            id='betas-table',
            columns=[],
            data=[],
            style_table={'overflow':'auto'},
            style_header={'backgroundColor':'rgb(230,230,230)','fontWeight':'bold'},
            style_cell={'textAlign':'left'}
            ),
    ])]),
    dcc.Tab(label='R-Squared',children=[

    html.Div([

    html.H2('R-Squared Table'),
    dash_table.DataTable(
        id='r-squared-table',
        columns=[],
        data=[],
        style_table={'overflow':'auto'},
        style_header={'backgroundColor':'rgb(230,230,230)','fontWeight':'bold'},
        style_cell={'textAlign':'left'}
        ),
    ])]),
    dcc.Tab(label='Correlations Factors',children=[

    html.Div([

    html.H2('Correlations Factor Table'),
    dash_table.DataTable(
        id='correlations-table',
        columns=[],
        data=[],
        style_table={'overflow':'auto'},
        style_header={'backgroundColor':'rgb(230,230,230)','fontWeight':'bold'},
        style_cell={'textAlign':'left'}
        ),
    ])]),
    ])
    ])
@app.callback(
    [Output('return-graph','figure'),
     Output('attribution-graph','figure'),
     Output('factor-correlations-graph','figure'),
     Output('index-correlations-graph','figure'),
     Output('factor-exposures-graph','figure'),
     Output('factor-beta-return-graph','figure'),
     Output('factor-exposures-outliers-graph','figure'),

     Output('betas-table','data'),
     Output('betas-table','columns'),
     Output('r-squared-table','data'),
     Output('r-squared-table','columns'),
     Output('correlations-table','data'),
     Output('correlations-table','columns'),
     ],
    
    [Input('update-button','n_clicks')],
    [Input('factor-dropdown','value')],
    [Input('index-dropdown','value')],
    [State(f'input-weight{i}','value') for i in range(len(numeric_weights))],
    )
def update_graph(n_clicks,selected_factor,selected_index,*weights_values):
    if n_clicks==0:
        return go.Figure(),go.Figure(),go.Figure(),go.Figure(),go.Figure(),go.Figure(),go.Figure(),[],[],[],[],[],[]
    weights=np.array(weights_values[:len(numeric_weights)])
    weights=weights/weights.sum()
    weighted_returns=returns.mul(weights,axis=1).sum(axis=1)
    scaler=StandardScaler()
    s_weighted_returns=scaler.fit_transform(pd.DataFrame(weighted_returns))
    s_weighted_returns=pd.Series(s_weighted_returns.flatten(),index=weighted_returns.index)
    
    _,attributions,betas,r2_scores=fra.return_attribution_factor_contribution(weighted_returns,factors)
    window_size=24
    #risk_factors=attributions.rolling(window=window_size).std()
    correlations=ca.rolling_corr_one_factors(factors,selected_factor,window_size)
    index_correlations=ca.rolling_corr_one_factors(returns,selected_index,window_size)
    
    rolling_corrs_df=ca.rolling_corr(factors,window_size=24)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=returns.index,y=s_weighted_returns,
                             mode='lines',name='Weighted Returns'))
    fig.update_layout(title='Normalized Portfolio Returns',
                      xaxis_title='Time',
                      yaxis_title='Return')

    
    attributions_fig=go.Figure()
    for factor in attributions.columns:
        attributions_fig.add_trace(go.Bar(x=attributions.index,
                                          y=attributions[factor],
                                          name=factor))
    attributions_fig.update_layout(barmode='stack',
                                   title='Normalized Return attribution by factor over time',
                                   xaxis_title='Date',
                                   yaxis_title='Attributed Returns',
                                   legend_title='Factors')
    correlations_fig=go.Figure()
    for factor2 in correlations.columns:
        correlations_fig.add_trace(go.Scatter(
            x=correlations.index,
            y=correlations[factor2],
            name=f'{factor2}'
            ))
    correlations_fig.update_layout(
        title=f'Correlations with {selected_factor}',
        xaxis_title='Date',
        yaxis_title='Correlation',
        legend_title='Factors'
        )
    index_correlations_fig=go.Figure()
    for index2 in index_correlations.columns:
        index_correlations_fig.add_trace(go.Scatter(
            x=index_correlations.index,
            y=index_correlations[index2],
            name=f'{index2}'
            ))
    index_correlations_fig.update_layout(
        title=f'Correlations with {selected_index}',
        xaxis_title='Date',
        yaxis_title='Correlation',
        legend_title='Indices'
        )
    factor_exposures_fig=go.Figure()
    for factor2 in betas.columns:
        factor_exposures_fig.add_trace(go.Scatter(
            x=betas.index,
            y=betas[factor2],
            name=f'{factor2}'
            ))
    factor_exposures_fig.update_layout(
        title='Factor Exposures',
        xaxis_title='Date',
        yaxis_title='Exposures',
        legend_title='Factors'
        )
    beta_return_fig=go.Figure()
    beta_return_fig.add_trace(go.Scatter(
        x=betas[selected_factor],
        y=attributions[selected_factor],
        mode='markers',
        marker=dict(size=8,color='blue',opacity=0.7),
        name=f'{selected_factor}'
        ))
    beta_return_fig.update_layout(
        title='Beta vs Return',
        xaxis_title='Beta',
        yaxis_title='Returns',
        legend_title='Factors'
        )
    factor_exposures_outliers_fig=go.Figure()
    for factor2 in betas.columns:
        factor_exposures_outliers_fig.add_trace(go.Box(
            y=betas[factor2],
            name=f'{factor2}',
            boxmean='sd'
            ))
    factor_exposures_outliers_fig.update_layout(
        title='Boxplot of Factor Exposures',
        yaxis_title='Exposures',
        xaxis_title='Factors',
        boxmode='group'        
        )
    betas.reset_index(inplace=True)
    r2_scores.reset_index(inplace=True)
    rolling_corrs_df.reset_index(inplace=True)  

    betas_columns=[{'name':i,'id':i} for i in betas.columns]
    r2_columns=[{'name':i,'id':i} for i in r2_scores.columns]
    rolling_corrs_columns=[{'name':i,'id':i} for i in rolling_corrs_df.columns]


    
    return fig,attributions_fig,correlations_fig,index_correlations_fig,factor_exposures_fig,beta_return_fig,factor_exposures_outliers_fig,betas.to_dict(
        'records'),betas_columns,r2_scores.reset_index().to_dict(
            'records'),r2_columns,rolling_corrs_df.to_dict('records'),rolling_corrs_columns


if __name__=='__main__':
    app.run_server(debug=True)
