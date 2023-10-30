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

class ChatGPT():

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
    
    
    def get_agent_sql(self):
        
        conversation_history = [
            {
              "role": "system",
              "content": """
                Given the following SQL table, your job is to write queries given a user’s request.
                  CREATE TABLE BankAccounts (
                  currency int,
                  amount int,
                  date datetime,
                  type varchar(50),
                  category varchar(50)
                );
                  The table contains all of the bank transactions from the user bank. You can review her income, expenses and investments. The description of the columns are:
                  currency: currency of the transaction. The value is CLP. 
                  amount: amount of the transaction. The value is integer.
                  date: date of the transaction. The value is in YYYY-MM-DD format.
                  type: type of the transaction. The values can be: 'Ingreso', 'Egreso','Inversiones'. 
                  category: category of the transaction. The values can be: 'Cine & Casino', 'Pago de Deudas', 'Educacion','Salud','Viajes & Hoteles','Ingreso','Seguros','Aseo & Limpieza','Restaurant & Bar','Farmacias','Supermercado & Retails','Transporte','Otros','Deportes','Suscripciones', 'SII','Transferencias','Cuentas & Servicios','Transporte','Otros'"
                  Your results must be just SQL query. You do not provide any more information. The result must not be with any line break (\n).
                  The results must be compatible for SQLite, because it will be processed in this Database. 
             """                  
            },
            {
              "role": "user",
              "content": self.text
            }
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=conversation_history,
                temperature=0
            )
            get_response_sql = response.choices[0].message["content"]
            get_response_sql = {'SQL': get_response_sql}
        except:
            get_response_sql = {'SQL': False}
        return get_response_sql
    

    def get_agent_sql_dataframe(self, response_agent_sql, df):

        if response_agent_sql['SQL'] == False:
            return {'DataFrame': False}
        else:
            try:
                DATABASE_URL = "sqlite:///mydatabase.db"
                engine = create_engine(DATABASE_URL)
                table_name = "BankAccounts"
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                sql_query = text('{}'.format(response_agent_sql['SQL']))
                connection = engine.connect()
                result = connection.execute(sql_query)
                table = []
                for row in result:
                    table.append(row)
                df_results = pd.DataFrame(table)
                return {'DataFrame': df_results}
            except:
                return {'DataFrame': False}
    
    def get_agent_dataframe_graph(self, dict_dataframe):

        if dict_dataframe['DataFrame'].empty:
            return False
        
        json_data = dict_dataframe['DataFrame'].to_json(orient='records')
        json_data_list = json.loads(json_data)
        json_data_str = json.dumps(json_data_list)

        conversation_history = [
            {
              "role": "system",
              "content": """
                You have a Python project where you need to create visualizations from DataFrames. Your task is to generate encoded image using the given data and Python libraries like matplotlib or seaborn.
                Your ouput must be diccionary with this format:
                {'image_base64': ''}
                The Python script you generate should have the following format and structure:
                - Import necessary libraries.
                - Load the DataFrame from the JSON data.
                - Create the desired type of graph (e.g., bar, pie).
                - Set the X and Y axis based on column names.
                - Add a title to the graph.
                - Include a legend.
                - Choose an appropriate color scheme and size.
                - Output or display the graph.

                Regarding to the format of the graph, the graph must following the next conditions:
                -  transparent background. 
                -  Xticks at 90 rotation.
                -  Remove title (plt.title('', fontsize = 16)
                -  Use this line: sns.despine(left=True, bottom=True)
                -  Color of the graph must be '#66b3ff' 
                -  Add a label to the graph.
                -  Save it as a image base64.
                -  The graph must be saved as graph.png.
                -  The result must be the encoded image as output using base64 library.
                
                Your input will be a JSON-formatted DataFrame.
                Please the encoded image as output using base64 library.
                }
             """                  
            },
            {
              "role": "user",
              "content": f"Generate an encoded image from the given data: {json_data_str}"
            }
        ]

        json_data_str = json.dumps(json_data_list)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation_history,
                temperature=0
            )

            get_response_sql = response.choices[0].message["content"]
            get_response_sql = {'GraphCode': get_response_sql}
        except:
            get_response_sql = {'GraphCode': False}
        return get_response_sql
    
    def save_graph(self, graph_code):

        script_graph_code = exec(graph_code)
        print(script_graph_code)
        print(graph_code)
        with open('graph.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        return encoded_image

    def main(self):
        
        df_processing_transaccions = self.get_processing_transaccions()
        try:
            if self.get_agent_sql() == False:
                return False
            else:
                df_results = self.get_agent_sql_dataframe(self.get_agent_sql(), df_processing_transaccions)
                if df_results['DataFrame'].empty:
                    return False
                else:
                    df_results_graph = self.get_agent_dataframe_graph(df_results)

                    print('codi')
                    print(df_results_graph['GraphCode'])
                    exec(df_results_graph['GraphCode'])
                    print('sssssssssssss')
                    if df_results_graph['GraphCode'] == False:
                        return False
                    else:
                        return self.save_graph(df_results_graph['GraphCode'])
                        #return df_results_graph['GraphCode']
        except:
            return False
