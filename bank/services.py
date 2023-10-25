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

class ExtractFintoc():  
    def __init__(self, link_token, security_token):
        self.link_token = link_token
        self.security_token = security_token

    def get_accounts(self):
        url = "https://api.fintoc.com/v1/accounts/?link_token={}".format(self.link_token)
        headers = {
            "accept": "application/json",
            "Authorization": self.security_token
        }
        response = requests.get(url, headers=headers)
        json_account = json.loads(response.text)
        table_account = []
        for i in range(len(json_account)):
            id_account = json_account[i]['id']
            name = json_account[i]['name']
            number = json_account[i]['number']
            type_account = json_account[i]['type']
            tupla = {'id_account': id_account, 'name': name, 'number': number, 'type_account': type_account}
            table_account.append(tupla)    
        return table_account
    
    def months_table_iso(self):

        current_date = datetime.utcnow()
        table_months = []
        for i in range(12):
            month = {
                "year": current_date.year,
                "month": current_date.month,
                "date_start": current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z",
                "date_end": (current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=1, seconds=-1)).isoformat() + "Z"
            }
            table_months.append(month)
            current_date -= relativedelta(months=1)

        return table_months

    def get_category(self, description):

        pattern_cine = constants.CINE
        pattern_debt_payments = constants.DEBT_PAYMENTS
        pattern_education = constants.EDUCATION
        pattern_healthcare = constants.HEALTHCARE
        pattern_travel_hotel = constants.TRAVEL_HOTEL
        pattern_income_work = constants.WORK_INCOME
        pattern_income_house = constants.INCOME_HOUSE
        pattern_insurance = constants.INSURANCE
        pattern_lullaby = constants.LULLABY
        pattern_pharmacy = constants.PHARMACY
        pattern_restaurant_bar = constants.RESTAURANT_BAR
        pattern_supermarket_retails = constants.SUPERMARKET_RETAILS
        pattern_sports = constants.SPORT
        pattern_suscription = constants.SUSCRIPTIONS
        pattern_sii = constants.SII
        pattern_utilities = constants.UTILITIES
        pattern_transfers = constants.WIRE_TRANSFERS
        pattern_transport = constants.TRANSPORT

        if pattern_cine.search(description):
            return 'Cine & Casino'
        elif pattern_debt_payments.search(description):
            return 'Debt Payments'
        elif pattern_education.search(description):
            return 'Education'
        elif pattern_healthcare.search(description):
            return 'Healthcare'
        elif pattern_travel_hotel.search(description):
            return 'Travel & Hotel'
        elif pattern_income_work.search(description):
            return 'Income'
        elif pattern_income_house.search(description):
            return 'Income'
        elif pattern_insurance.search(description):
            return 'Insurance'
        elif pattern_lullaby.search(description):
            return 'Lullaby'
        elif pattern_pharmacy.search(description):
            return 'Pharmacy'
        elif pattern_restaurant_bar.search(description):
            return 'Restaurant & Bar'
        elif pattern_supermarket_retails.search(description):
            return 'Supermarket & Retails'
        elif pattern_sports.search(description):
            return 'Sports'
        elif pattern_suscription.search(description):
            return 'Suscription'
        elif pattern_sii.search(description):
            return 'SII'
        elif pattern_transfers.search(description):
            return 'Transfers'
        elif pattern_transport.search(description):
            return 'Transport'                
        elif pattern_utilities.search(description):
            return 'Utilities'
        else:
            return 'Others'                
        
    def get_movements(self):
        table_mov = []
        table_account = self.get_accounts()
        table_last_12_months = self.months_table_iso()
        df = pd.DataFrame()
        for month in table_last_12_months:
            since_date = month['date_start']
            until_date = month['date_end']
            for i in range(len(table_account)):
                account_number = table_account[i]['id_account']
                account_name = table_account[i]['name']
                type_account = table_account[i]['type_account']
                url = "https://api.fintoc.com/v1/accounts/{}/movements?link_token={}&since={}&until={}&per_page=300".format(account_number, self.link_token, since_date, until_date)
                headers = {
                "accept": "application/json",
                "Authorization": self.security_token}
                response = requests.get(url, headers=headers)
                json_mov = json.loads(response.text)
                for i in range(len(json_mov)):
                    id_mov = json_mov[i]['id']
                    amount = json_mov[i]['amount']
                    currency = json_mov[i]['currency']
                    description = json_mov[i]['description']
                    post_date = str(json_mov[i]['post_date'])[:10]
                    post_date = datetime.strptime(post_date, '%Y-%m-%d')
                    if amount < 0:
                        type_account_expenses = 'Egreso'
                        amount = abs(amount)
                    else:
                        type_account_expenses = 'Ingreso'
                        amount = abs(amount)
                    tupla = {'id_mov': id_mov, 'amount': amount, 'currency': currency, 'description': description, 'date': post_date, 'type_expenses': type_account_expenses, 'account_name': account_name, 'account_number': account_number}
                    table_mov.append(tupla)

        df = pd.DataFrame(table_mov, columns=['id_mov', 'amount', 'currency', 'description', 'date', 'type_expenses', 'account_name', 'account_number'])
        df = df.reset_index().drop(columns = ['index'])
        df['category_expenses'] = ''
        for index in range(len(df)):
            description = df['description'][index]
            category_description = self.get_category(description)
            df['category_expenses'][index] = category_description
        
        df['indicator_not_category'] = False
        for index in range(len(df)):
            category_expenses = df['category_expenses'][index]
            amount = df['amount'][index]
            if category_expenses == 'Others' and amount > 100000:
                df['indicator_not_category'][index] = True
            else:
                df['indicator_not_category'][index] = False
        
        
        return df
    
    
@transaction.atomic
def update_transactions_table(transaction_data: pd.DataFrame):
    models_bank.DataBanks.objects.all().delete()
    for index, row in transaction_data.iterrows():
        transaction_instance = models_bank.DataBanks(
            currency=row['currency'],
            description=row['description'],
            amount = row['amount'],
            date=row['date'],
            type_expenses=row['type_expenses'],
            account_name=row['account_name'],
            account_number=row['account_number'],
            category_description=row['category_expenses'],
            indicator_not_category=row['indicator_not_category']
        )
        transaction_instance.save()


