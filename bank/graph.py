from bank import models as models_bank
import pandas as pd
import datetime
from llama_index import Document
import calendar

class GraphExpenses():

    def __init__(self):
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
        df = pd.DataFrame(table_expenses, columns=['currency', 'description', 'amount', 'date', 'type_expenses', 'account_name', 'account_number', 'category_description'])
        return df
    
    def get_last_date_table(self,all_accounts):
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        last_date = df['date'].max()
        return {
            'date': last_date,
        }
    
    def get_expenses(self,all_accounts):
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_expenses = df[df['type_expenses'] == 'Egreso']['amount'].sum()
        return df_expenses
    
    def get_incomes(self,all_accounts):

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_income = df[df['type_expenses'] == 'Ingreso']['amount'].sum()
        return df_income

    def get_line_expenses_graph(self,all_accounts):
        
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(weeks=12)
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df.loc[df['type_expenses'] == 'Egreso']
        df = df.loc[df['date'] >= start_date]
        df = df.loc[df['date'] <= end_date]      
        df['date_week'] = df['date'].apply(lambda x: str(x.isocalendar()[0]) + '-' + str(x.isocalendar()[1]) )
        df = df[['date_week','amount']]
        df = df.groupby(['date_week']).sum()['amount'].reset_index()
        data = df['amount'].to_list()
        label = df['date_week'].to_list()
        return {
            'data': data,
            'label': label,
        }
    

    def get_bar_expense_month(self,all_accounts):
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Egreso']
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        df = df[['month','amount']]
        df = df.groupby(['month']).sum()['amount'].reset_index()
        data = df['amount'].to_list()
        label = df['month'].to_list()
        return {
            'data': data,
            'label': label,
        }
    

    def get_bar_income_month(self,all_accounts):
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Ingreso']
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        df = df[['month','amount']]
        df = df.groupby(['month']).sum()['amount'].reset_index()
        data = df['amount'].to_list()
        label = df['month'].to_list()
        return {
            'data': data,
            'label': label,
        }
    
    def get_bar_saving_month(self, all_accounts):
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
 
        df_expense = df[df['type_expenses'] == 'Egreso']
        df_expense['month'] = df_expense['date'].apply(lambda x: str(x)[:7])
        df_expense = df_expense[['month','amount']]
        df_expense = df_expense.groupby(['month']).sum()['amount'].reset_index()
        df_expense.rename(columns={'amount': 'Egreso'}, inplace=True)
 
        df_income = df[df['type_expenses'] == 'Ingreso']
        df_income['month'] = df_income['date'].apply(lambda x: str(x)[:7])
        df_income = df_income[['month','amount']]
        df_income = df_income.groupby(['month']).sum()['amount'].reset_index()
        df_income.rename(columns={'amount': 'Ingreso'}, inplace=True)
 
        df_total = pd.merge(df_expense, df_income, on='month')
        df_total['saving'] = df_total['Ingreso'] - df_total['Egreso']
        data = df_total['saving'].to_list()
        label = df_total['month'].to_list()
        return {
            'data': data,
            'label': label,
        }
    
    def get_details_expenses_graph(self, all_accounts):

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
 
        df = df[df['type_expenses'] == 'Ingreso']
        df_top_expenses = df[['amount','category_description']]
        df_top_expenses = df_top_expenses.groupby(['category_description']).sum()['amount'].reset_index()
        df_top_expenses['Percentaje'] = df_top_expenses['amount'].apply(lambda x: (x / df_top_expenses['amount'].sum()) * 100)
        df_top_expenses = df_top_expenses.sort_values(by=['Percentaje'], ascending=False)
        table_category_description = df_top_expenses['category_description'].iloc[:5].to_list()
           
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        df = df.loc[df['category_description'].isin(table_category_description)]
        df_expense = df[['month','amount']]
        df_expense = df_expense.groupby(['month']).sum()['amount'].reset_index()
        pivot_df = pd.pivot_table(df, values='amount', index='category_description', columns='month', aggfunc='sum')
        pivot_df.fillna(0, inplace=True)
        pivot_df = pivot_df.T
        return {
            'pivot_percentage_index': list(pivot_df.columns),
            'pivot_percentage_columns': list(pivot_df.index),
            'pivot_percentage_values': pivot_df.values.tolist(),
        }
    

    def get_pie_expenses_graph(self, all_accounts):

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=29)
        start_date = str(start_date.strftime('%Y-%m-%d'))[:10]

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Egreso']
        df['date'] = df['date'].apply(lambda x: str(x)[:10])
        df = df.loc[df['date'] > start_date]
        df = df[['amount','category_description','date']]
        df = df.groupby(['category_description']).sum()['amount'].reset_index()
        df['Percentaje'] = df['amount'].apply(lambda x: (x / df['amount'].sum()) * 100)
        data = df['Percentaje'].to_list()
        label = df['category_description'].to_list()
        return {
            'data': data,
            'label': label,
        }
    

    def get_expenses_top_three_line_graph(self,tarjet_expenses,all_accounts):

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=29)
        start_date = str(start_date.strftime('%Y-%m-%d'))[:10]
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Egreso']
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        df_expenses = df[['amount','month']]
        df_expenses = df_expenses.groupby(['month']).sum()['amount'].reset_index()
        df_expenses['Target'] = tarjet_expenses
        df_expenses['Porcentual_Difference'] = df_expenses.apply(lambda row: -((row['amount'] - row['Target'])/ row['Target']) * 100, axis = 1)
        data_expenses = df_expenses['amount'].to_list()
        data_target = df_expenses['Target'].to_list()
        date = df_expenses['month'].to_list()
        data_porcentual = df_expenses['Porcentual_Difference'].to_list()

        return {
            'date': date,
            'expenses': data_expenses,
            'target': data_target,
            'porcentual': data_porcentual,

        }
    
    def get_table_expenses_by_day(self, all_accounts):

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=29)
        start_date = str(start_date.strftime('%Y-%m-%d'))[:10]
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Egreso']
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        df_expenses = df[['amount','category_description','month']]
        pivot_df = pd.pivot_table(df_expenses, values='amount', index='category_description', columns='month', aggfunc='sum')
        pivot_df = pivot_df.fillna(0)

        sum_df = pd.DataFrame(pivot_df.sum(axis=0)).transpose()
        sum_df.index = ['Total'] 
        pivot_df = pd.concat([pivot_df,sum_df], axis = 0)
        values = pivot_df.values.tolist()
        columns = list(pivot_df.columns)
        categories = pivot_df.index.to_list()
        return {
            'values': values,
            'columns': columns,
            'categories': categories,            
        }
    

    def get_last_month_expenses(self, all_accounts):

        start_date = datetime.date.today()
        last_day_of_last_month = start_date.replace(day=1) - datetime.timedelta(days=1)
        formatted_date = last_day_of_last_month.strftime('%Y-%m')

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Egreso']
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        formatted_date = last_day_of_last_month.strftime('%Y-%m')
        df = df.loc[df['month'] == formatted_date]        
        amount_last_month = df['amount'].sum()
        amount_last_month = str("{:,.0f}".format(amount_last_month)).replace(',','.')
        return {
            'value': amount_last_month,
            'date_month': formatted_date
        }
    
    def get_last_month_income(self, all_accounts):

        start_date = datetime.date.today()
        last_day_of_last_month = start_date.replace(day=1) - datetime.timedelta(days=1)
        formatted_date = last_day_of_last_month.strftime('%Y-%m')
    
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[df['type_expenses'] == 'Ingreso']
        df['month'] = df['date'].apply(lambda x: str(x)[:7])
        formatted_date = last_day_of_last_month.strftime('%Y-%m')
        df = df.loc[df['month'] == formatted_date]        
        amount_last_month = df['amount'].sum()
        amount_last_month = str("{:,.0f}".format(amount_last_month)).replace(',','.')
        return {
            'value': amount_last_month,
            'date_month': formatted_date
        }
    

    def get_last_month_saving(self, all_accounts):
        
        start_date = datetime.date.today()
        end_date_last_month = start_date.replace(day=1) - datetime.timedelta(days=1)
        start_date_last_12_months = (end_date_last_month - datetime.timedelta(days=365)).replace(day=1)

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df[(df['date'] >= start_date_last_12_months) & (df['date'] <= end_date_last_month)]

        df_expense = df[df['type_expenses'] == 'Egreso']
        df_expense['month'] = df_expense['date'].apply(lambda x: str(x)[:7])
        df_expense = df_expense[['month','amount']]
        df_expense = df_expense.groupby(['month']).sum()['amount'].reset_index()
        df_expense.rename(columns={'amount': 'Egreso'}, inplace=True)
        df_income = df[df['type_expenses'] == 'Ingreso']
        df_income['month'] = df_income['date'].apply(lambda x: str(x)[:7])
        df_income = df_income[['month','amount']]
        df_income = df_income.groupby(['month']).sum()['amount'].reset_index()
        df_income.rename(columns={'amount': 'Ingreso'}, inplace=True)
        df_total = pd.merge(df_expense, df_income, on='month')
        df_total['saving'] = df_total['Ingreso'] - df_total['Egreso']
        #df_total = df_total.loc[df_total['month'] == formatted_date]        

        amount_last_month = df_total['saving'].sum()
        amount_last_month = str("{:,.0f}".format(amount_last_month)).replace(',','.')
        
        return {
            'value': amount_last_month,
            'date_month': start_date_last_12_months
        }    

    def get_expense_last_day(self, all_accounts):
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df = df.loc[df['date'] == df['date'].max()]
        df_expense = df[df['type_expenses'] == 'Egreso']
        df_expense = df_expense[['date','amount']]
        df_expense = df_expense.groupby(['date']).sum()['amount'].reset_index()
        df_expense['date'] = df_expense['date'].apply(lambda x: str(x)[:10])
        if df_expense.shape[0] == 0:
            data =  df['date'].max().strftime('%Y-%m-%d')
            label = 0
            return {
                'data': data,
                'label': label,
            }
        else:
            data = df_expense['date'].values[0]
            label =  df_expense['amount'].values[0]
            label_formatted = "{:,.3f}".format(label / 1000)
            return {
                'data': data,
                'label': label_formatted,
            }

    def get_expense_last_week(self, all_accounts):
        
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        last_day_data = df['date'].max()
        start_date = last_day_data - pd.Timedelta(days=6)
        df_expense = df[df['type_expenses'] == 'Egreso']
        df_expense = df_expense[['date','amount']]
        df_expense = df_expense.groupby(['date']).sum()['amount'].reset_index()
        df_expense = df_expense.loc[df_expense['date'] > start_date]
        last_day_data = last_day_data.strftime('%b. %d, %Y')
        start_date = start_date.strftime('%b. %d, %Y')
        if df_expense.shape[0] == 0:
            data = "{} to {}".format(start_date, last_day_data)
            label = 0
            return {
                'data': data,
                'label': label,
            }
        else:
            data =  "{} to {}".format(start_date, last_day_data)
            label  = df_expense['amount'].sum()
            formatted = "{:,.3f}".format(label / 1000)
            return {
                'data': data,
                'label': formatted,
            }
    
    def get_ratio_saving_last_month(self, all_accounts):

        start_date = datetime.date.today()
        last_day_of_last_month = start_date.replace(day=1) - datetime.timedelta(days=1)
        formatted_date = last_day_of_last_month.strftime('%Y-%m')

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_expense = df[df['type_expenses'] == 'Egreso']
        df_expense['month'] = df_expense['date'].apply(lambda x: str(x)[:7])
        df_expense = df_expense[['month','amount']]
        df_expense = df_expense.groupby(['month']).sum()['amount'].reset_index()
        df_expense.rename(columns={'amount': 'Egreso'}, inplace=True)
        df_income = df[df['type_expenses'] == 'Ingreso']
        df_income['month'] = df_income['date'].apply(lambda x: str(x)[:7])
        df_income = df_income[['month','amount']]
        df_income = df_income.groupby(['month']).sum()['amount'].reset_index()
        df_income.rename(columns={'amount': 'Ingreso'}, inplace=True)
        df_total = pd.merge(df_expense, df_income, on='month')
        df_total['saving'] = df_total['Ingreso'] - df_total['Egreso']
        df_total = df_total.loc[df_total['month'] == formatted_date]        
        ratio_saving = round(100 * df_total['saving'].sum()/df_total['Ingreso'].sum(),2)
        formatted = "{} %".format(ratio_saving)     
        return {
            'data': formatted_date,
            'label': formatted,
        }       
    

    def get_all_records(self):

        start_date = datetime.date.today()
        last_day_of_last_month = start_date.replace(day=1) - datetime.timedelta(days=120)
        formatted_date = last_day_of_last_month.strftime('%Y-%m-%d')

        df = self.get_processing_transaccions()
        df = df[['date','amount','description','type_expenses','category_description']]
        df = df.groupby(['date','type_expenses','category_description']).sum()['amount'].reset_index()
        df = df.reset_index().drop(columns=['index'])

        df['date'] = df['date'].apply(lambda x: str(x)[:10])
        df = df.loc[df['date'] >= str(formatted_date)]
        df = df.reset_index().drop(columns=['index'])
        
        table_documents =  []
        for index, row in df.iterrows():
            #description=row['description'],
            amount = row['amount'],
            date=row['date'],
            type_expenses=row['type_expenses'],
            category_description=row['category_description'],
            dicc = {
                'ID': index,
                'amount': amount[0],
                'date': date[0],
                'type': type_expenses[0],
                'category': category_description[0],
            }
            
            table_documents.append(dicc)

        return {
            'text_records': table_documents,
        }       
    


    def get_investment_inputs(self):


        df = self.get_processing_transaccions()
        df = df[['date','amount','description','type_expenses','category_description']]
        df = df.groupby(['date','category_description','type_expenses']).sum()['amount'].reset_index()
        df = df.loc[df['category_description'] == 'Inversiones']
        df = df.reset_index().drop(columns=['index'])
        
        if df.shape[0] == 0:
            return {
                'Indicator': False,
                 'Values': [
                            {
                            'type': 'Income',
                            'data': 0,
                            'label': 0,
                        },{
                            'type': 'Egreso',
                            'data': 0,
                            'label': 0,
                        },
                        {
                            'type': 'Neto',
                            'data': 0,
                            'label': 0,
                        }           
                    ]
                }       
        
        elif df.shape[0] > 0:

            df_income = df[df['type_expenses'] == 'Ingreso']
            df_income = df_income[['date','amount']]
            df_income['Month'] = df_income['date'].apply(lambda x: str(x)[:7])
            df_income = df_income[['Month','amount']]
            df_income = df_income.groupby(['Month']).sum()['amount'].reset_index()
            df_income = df_income.reset_index().drop(columns=['index'])
            df_income = df_income.rename(columns={'amount': 'Ingreso'}, axis = 1)


            df_expense = df[df['type_expenses'] == 'Egreso']
            df_expense = df_expense[['date','amount']]
            df_expense['Month'] = df_expense['date'].apply(lambda x: str(x)[:7])
            df_expense = df_expense[['Month','amount']]
            df_expense = df_expense.groupby(['Month']).sum()['amount'].reset_index()
            df_expense = df_expense.reset_index().drop(columns=['index'])
            df_expense = df_expense.rename(columns={'amount': 'Egreso'}, axis = 1)

            df_total = pd.merge(df_income, df_expense, on='date')
            df_total['Neto'] = df_total['Ingreso'] - df_total['Egreso']

            return {
                'Indicator': True,
                'Values': [
                            {
                            'type': 'Income',
                            'data': df_total['Ingreso'].to_list(),
                            'label': df_total['Ingreso'].to_list(),
                        },{
                            'type': 'Egreso',
                            'data': df_total['Egreso'].to_list(),
                            'label': df_total['Egreso'].to_list(),
                        },
                        {
                            'type': 'Neto',
                            'data': df_total['Neto'].to_list(),
                            'label': df_total['Neto'].to_list(),
                        }           
                    ]
                }
   
    def get_investment_inputs(self):

        df = self.get_processing_transaccions()
        df = df[['date','amount','description','type_expenses','category_description']]
        df = df.groupby(['date','category_description','type_expenses']).sum()['amount'].reset_index()
        df = df.loc[df['type_expenses'] == 'Inversiones']
        df = df.reset_index().drop(columns=['index'])

        if df.shape[0] == 0:
            
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month + 1
            date_range = pd.date_range(start='2023-01', end=f'{current_year}-{current_month:02}', freq='M')
            dummy_data = {'Month': date_range.strftime('%Y-%m'),
                          'Ingreso': 0.0,
                          'Egreso': 0.0,
                          'Neto': 0.0}           
            merged_df = pd.DataFrame(dummy_data)
            return {
                'Indicator': False,
                'Values': [
                            {
                            'type': 'Income',
                            'data': merged_df['Ingreso'].to_list(),
                            'label': merged_df['Month'].to_list(),
                        },{
                            'type': 'Egreso',
                            'data': merged_df['Egreso'].to_list(),
                            'label': merged_df['Month'].to_list(),
                        },
                        {
                            'type': 'Neto',
                            'data': merged_df['Neto'].to_list(),
                            'label': merged_df['Month'].to_list(),
                        }           
                    ]
                }    
        
        elif df.shape[0] > 0:

            df_income = df[df['category_description'] == 'Ingreso']
            df_income = df_income[['date','amount']]
            df_income['Month'] = df_income['date'].apply(lambda x: str(x)[:7])
            df_income = df_income[['Month','amount']]
            df_income = df_income.groupby(['Month']).sum()['amount'].reset_index()
            df_income = df_income.reset_index().drop(columns=['index'])
            df_income = df_income.rename(columns={'amount': 'Ingreso'})


            df_expense = df[df['category_description'] == 'Egreso']
            df_expense = df_expense[['date','amount']]
            df_expense['Month'] = df_expense['date'].apply(lambda x: str(x)[:7])
            df_expense = df_expense[['Month','amount']]
            df_expense = df_expense.groupby(['Month']).sum()['amount'].reset_index()
            df_expense = df_expense.reset_index().drop(columns=['index'])
            df_expense = df_expense.rename(columns={'amount': 'Egreso'})

            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month + 1
            df_total = pd.merge(df_income, df_expense, on='Month', how = 'outer')
            df_total = df_total.fillna(0) 
            df_total['Neto'] = df_total['Ingreso'] - df_total['Egreso']
            df_total = df_total.fillna(0) 
            date_range = pd.date_range(start='2023-01', end=f'{current_year}-{current_month:02}', freq='M')
            dummy_data = {'Month': date_range.strftime('%Y-%m'),
                          'Ingreso': 0.0,
                          'Egreso': 0.0,
                          'Neto': 0.0}           
            dummy_df = pd.DataFrame(dummy_data)
            merged_df = pd.concat([df_total, dummy_df], ignore_index=True)
            merged_df = merged_df.drop_duplicates(subset='Month')
            merged_df = merged_df.sort_values('Month')
            merged_df.reset_index(drop=True, inplace=True)
            return {
                'Indicator': True,
                'Values': [
                            {
                            'type': 'Income',
                            'data': merged_df['Ingreso'].to_list(),
                            'label': merged_df['Month'].to_list(),
                        },{
                            'type': 'Egreso',
                            'data': merged_df['Egreso'].to_list(),
                            'label': merged_df['Month'].to_list(),
                        },
                        {
                            'type': 'Neto',
                            'data': merged_df['Neto'].to_list(),
                            'label': merged_df['Month'].to_list(),
                        }           
                    ]
                }
            
    def get_income_median(self, all_accounts):

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_income = df[df['type_expenses'] == 'Ingreso']
        df_income['month'] = df_income['date'].apply(lambda x: str(x)[:7])
        df_income = df_income[['month','amount']]
        df_income = df_income.groupby(['month']).sum()['amount'].reset_index()
        df_income = df_income.rename(columns={'amount': 'Ingreso'})
        #income_median = "{:,.0f}".format(df_income['Ingreso'].median())
        #income_median_per_day = "{:,.0f}".format(df_income['Ingreso'].median()/30)
        income_median = str("{:,.0f}".format(df_income['Ingreso'].median())).replace(',','.')        
        income_median_per_day = str("{:,.0f}".format(df_income['Ingreso'].median()/30)).replace(',','.')
        return {
            'data': income_median,
            'data_per_day': income_median_per_day,
            'label': 'Nediam Income',
        }     
    

    def get_expenses_median(self, all_accounts):

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_expenses = df[df['type_expenses'] == 'Egreso']
        df_expenses['month'] = df_expenses['date'].apply(lambda x: str(x)[:7])
        df_expenses = df_expenses[['month','amount']]
        df_expenses = df_expenses.groupby(['month']).sum()['amount'].reset_index()
        df_expenses = df_expenses.rename(columns={'amount': 'Egresos'})
        #expenses_median = "{:,.0f}".format(df_expenses['Egresos'].median())
        expenses_median = str("{:,.0f}".format(df_expenses['Egresos'].median())).replace(',','.')
        return {
            'data': expenses_median,
            'label': 'Nediam Expenses',
        }     
    

    def get_expenses_percentaje_per_day(self, all_accounts):

        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_expenses = df[df['type_expenses'] == 'Egreso']
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        df_expenses['day'] = df_expenses['date'].dt.day

        daily_expenses = df_expenses.groupby(['day']).agg({'amount': 'sum', 'date': 'count'}).reset_index()
        daily_expenses.rename(columns={'date': 'day_count'}, inplace=True)
        daily_expenses['AvgExpenses'] = daily_expenses['amount'] / daily_expenses['day_count']
        total_average = daily_expenses['AvgExpenses'].sum()
        daily_expenses['AvgExpenses_Percentaje'] = daily_expenses['AvgExpenses'].apply(lambda x: round((x / total_average) * 100,1))
        return {
            'data': daily_expenses['AvgExpenses_Percentaje'].to_list(),
            'label': daily_expenses['day'].to_list()
        }     
    

    def get_expenses_tends(self, all_accounts):

        current_date = datetime.datetime.now()
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        last_day_of_month = datetime.datetime(current_date.year, current_date.month, last_day)
        last_day_of_month = int(last_day_of_month.day)
 
        df = self.get_processing_transaccions()
        df = df.loc[df['account_name'] == all_accounts]
        df_expenses = df[df['type_expenses'] == 'Egreso']
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        df_expenses['day'] = df_expenses['date'].dt.day
       
        max_day_data = df_expenses['date'].max()
        first_day_of_month = datetime.datetime(max_day_data.year, max_day_data.month, 1)

        daily_expenses = df_expenses.groupby(['day']).agg({'amount': 'sum', 'date': 'count'}).reset_index()
        daily_expenses.rename(columns={'date': 'day_count'}, inplace=True)
        daily_expenses['AvgExpenses'] = daily_expenses['amount'] / daily_expenses['day_count']
        total_average = daily_expenses['AvgExpenses'].sum()
        daily_expenses['AvgExpenses_Percentaje'] = daily_expenses['AvgExpenses'].apply(lambda x: round((x / total_average) * 100,1))
         
        current_year = max_day_data.year
        current_month = max_day_data.month
        df_current_month = df_expenses[(df_expenses['date'].dt.year == current_year) & (df_expenses['date'].dt.month == current_month)]
        df_current_month = df_current_month.loc[df_current_month['date'] <= max_day_data]
        expenses_current_month = df_current_month['amount'].sum()
        
        daily_expenses = daily_expenses.loc[daily_expenses['day'] > int(max_day_data.day)]
        daily_expenses = daily_expenses.loc[daily_expenses['day'] <= last_day_of_month]
        percentaje_expenses_sum = 100 - daily_expenses['AvgExpenses_Percentaje'].sum()
        expenses_current_month_projected = expenses_current_month*100/percentaje_expenses_sum
        expenses_current_month_projected_format = str("{:,.0f}".format(expenses_current_month_projected)).replace(',','.')

        daily_expenses['projected_expenses'] = daily_expenses['AvgExpenses_Percentaje'].apply(lambda x: round((x * expenses_current_month_projected) / 100,1))
        daily_expenses['date'] = daily_expenses['day'].apply(lambda x: str(current_year) + '-'+ str(current_month)+ '-'+ str(x))
        df_expenses = df[df['type_expenses'] == 'Egreso']
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        df_expenses = df_expenses[['date','amount']]
        df_expenses = df_expenses.groupby(['date']).sum()['amount'].reset_index()
        df_expenses = df_expenses.rename(columns={'amount': 'Egresos'})
        df_expenses = df_expenses.loc[df_expenses['date'] >= first_day_of_month]
        df_expenses['date'] = df_expenses['date'].apply(lambda x: str(x)[:10])
        df_expenses = df_expenses[['date','Egresos']]
        daily_expenses = daily_expenses.rename(columns = {'projected_expenses':'Egresos'})
        daily_expenses['Tipo'] = True
        df_expenses['Tipo'] = False

        df_expenses = df_expenses[['date','Egresos','Tipo']]
        df_expenses = df_expenses.reset_index().drop(columns=['index'])
        daily_expenses = daily_expenses[['date','Egresos','Tipo']]
        daily_expenses = daily_expenses.reset_index().drop(columns=['index'])
        df_total_month = pd.concat([df_expenses,daily_expenses], ignore_index=True)
        
        ## month by expenses

        df_expenses = df[df['type_expenses'] == 'Egreso']
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
        df_expenses['day'] = df_expenses['date'].dt.day
        max_day_data = df_expenses['date'].max()
        max_month = max_day_data.month
        end_date = max_day_data.replace(day=1) - pd.DateOffset(days=1)
        start_date = end_date - pd.DateOffset(months=3) + pd.DateOffset(days=1)
        df_last_3_months = df_expenses[(df_expenses['date'] >= start_date) & (df_expenses['date'] <= end_date)]
        df_last_3_months['month'] = df_last_3_months['date'].apply(lambda x: str(x)[:7])
        df_last_3_months = df_last_3_months[['month','amount']]
        df_last_3_months = df_last_3_months.groupby(['month']).sum()['amount'].reset_index()
        df_last_3_months = df_last_3_months.rename(columns={'amount': 'Egresos'})
        df_last_3_months['Tipo'] = False
        df_last_3_months['date'] = df_last_3_months['month'].apply(lambda x: str(x)[:10])
        df_last_3_months = df_last_3_months[['date','Egresos','Tipo']]
        df_last_3_months = df_last_3_months.reset_index().drop(columns=['index'])
        
        max_month_previous = int(max_day_data.month)
        max_month = str(current_year) + '-' + str(max_month)
        previous_month = str(current_year) + '-' + str(max_month_previous-1)
        new_row = ({'date': max_month, 'Egresos': expenses_current_month_projected, 'Tipo': True})
        df_last_3_months_projected = pd.DataFrame([new_row])
        df_last_3_months = pd.concat([df_last_3_months,df_last_3_months_projected], ignore_index=True)


        
        return {
            'expenses_current_month_projected': expenses_current_month_projected_format,
            'data_per_day': df_total_month['Egresos'].to_list(),
            'label_per_day': df_total_month['date'].to_list(),
            'type_per_day': df_total_month['Tipo'].to_list(),
            'data_month': df_last_3_months['Egresos'].to_list(),
            'label_month': df_last_3_months['date'].to_list(),
            'type_month': df_last_3_months['Tipo'].to_list(),
            'current_period': max_month,
            'previous_period': previous_month,


        } 
    

