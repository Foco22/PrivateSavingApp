import pandas as pd
from os import listdir
from os.path import join, isfile
from dateutil.relativedelta import relativedelta
from bank import models as models_bank
from django.db import transaction
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import requests
import re
from bank import constants
import openai
from sqlalchemy import create_engine, text
import base64


class Preprocessing():

    def  __init__(self, text):
        self.text = text
        openai.api_key =  ''
        self.table_transaction_banks = models_bank.DataBanks.objects.all()
 
    def get_processing_transaccions(self):
        table_expenses = []
        for transaction in self.table_transaction_banks:
            currency = transaction.currency
            description = transaction.description
            amount = transaction.amount
            date = transaction.date
            type_expenses = transaction.type_expenses
            account_name = transaction.account_name
            account_number = transaction.account_number
            category_description = transaction.category_description
            tupla = (currency, description, amount, date, type_expenses, account_name, account_number, category_description)
            table_expenses.append(tupla)
        df = pd.DataFrame(table_expenses, columns=['currency', 'description', 'amount', 'date', 'type', 'account_name', 'account_number', 'category'])
        df = df[['currency','amount','date','type','category']]
        return df
    
    def start_and_end(self,x):

        if x in [1,2,3,4,5, 26,27,28,29,30,31]:
            return 1
        else:
            return 0 

    def months_expenses(self,x):

        if x in [12,9]:
            return 1
        else:
            return 0 

    def contributions(self,x):

        if x in [4,6,9,11]:
            return 1
        else:
            return 0 
            
    def day_of_week(self,x):

        if x in ['Friday','Sunday','Saturday']:
            return 1
        else:
            return 0 
    
    def main(self):

        df = self.get_processing_transaccions()
        df['date'] = df['date'].apply(lambda x: str(x))
        df = df.loc[df['type'] == 'Egreso']
        df = df[['amount','date']]
        df = df.groupby(['date']).sum('amount').reset_index()
        df['date'] = pd.to_datetime(df['date'])
        start_date = df['date'].min()
        end_date = df['date'].max()
        date_range = pd.date_range(start_date, end_date)
        date_df = pd.DataFrame({'date': date_range})
        df = date_df.merge(df, on='date', how='left')
        df['date'] = df['date'].apply(lambda x: str(x)[:10])
        df['amount']  = df['amount'].fillna(0)
        df['day'] = df['date'].apply(lambda x : int(x[8:]))
        df['year'] = df['date'].apply(lambda x : int(x[:4]))
        df['month'] = df['date'].apply(lambda x : int(x[5:7]))
        df['start_and_end'] =  df['day'].apply(lambda x: self.start_and_end(x))     
        df['Months_expenses'] = df['month'].apply(lambda x: self.months_expenses(x))  
        df['contributions'] = df['month'].apply(lambda x: self.contributions(x))  
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.day_name()
        one_hot = pd.get_dummies(df['day_of_week'], prefix='day')
        df = pd.concat([df, one_hot], axis=1)
        df = df.replace(False, 0)
        df = df.replace(True, 1)
        list_day = ['day_Friday','day_Monday','day_Thursday','day_Tuesday','day_Wednesday','day_sunday','day_saturday']
        for day in list_day:
            if day not in list(df.columns):
                df[day] = 0
        df = df.drop(columns = ['day_sunday','day_of_week'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        for i in range(1, 8):
            df[f'amount_lag_{i}'] = df['amount'].shift(i)
        df = df.iloc[7:,:]
        df = df.drop(columns = ['date'])
        df = df.reset_index().drop(columns =['index'])
        return {
            'dataframe': df,
            'columns': list(df.columns)
        }