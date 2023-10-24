from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from users import services as user_services
from web.lib import constants as web_constants
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from bank import services as bank_services
from bank import models as models_bank
from bank import graph as graph_bank
from django.shortcuts import render
from django.templatetags.static import static
import json
from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect
from bank.forms import LoginForm
from bank.tasks import update_transactions_table  
from django.urls import reverse
import requests
from bank.models import SavingTarget
import logging
from bank.models import DataBanks
import pandas as pd
from bank.models import ClassifiedData
from django.http import JsonResponse
import openai,os,sys
import tiktoken

logger = logging.getLogger(__name__)

template_name = '/django/web/templates/home.html'
template_details_name = '/django/web/templates/details.html'
template_tables_name = '/django/web/templates/tables.html'
template_start_name = '/django/web/templates/start.html'
template_clasification_name = '/django/web/templates/clasification.html'
template_chat_name = '/django/web/templates/chat.html'
template_inversions_name = '/django/web/templates/inversions.html'
template_inversions_name = '/django/web/templates/behavior.html'

def get_expenses_data(saving_target, all_accounts):
    graph_bank_class = graph_bank.GraphExpenses()
    total_expenses = graph_bank_class.get_expenses(all_accounts)
    total_income = graph_bank_class.get_incomes(all_accounts)
    inputs_graph_line = graph_bank_class.get_line_expenses_graph(all_accounts)
    inputs_graph_bar = graph_bank_class.get_bar_expense_month(all_accounts)
    inputs_graph_bar_income = graph_bank_class.get_bar_income_month(all_accounts)
    input_graph_saving = graph_bank_class.get_bar_saving_month(all_accounts)
    input_pivot_expenses = graph_bank_class.get_details_expenses_graph(all_accounts)
    input_pie_graph = graph_bank_class.get_pie_expenses_graph(all_accounts)
    data = {
    'pivot_percentage_index': input_pivot_expenses['pivot_percentage_index'],
    'pivot_percentage_columns': input_pivot_expenses['pivot_percentage_columns'],
    'pivot_percentage_values': input_pivot_expenses['pivot_percentage_values']
    }
    input_line_top_three_graph = graph_bank_class.get_expenses_top_three_line_graph(saving_target,all_accounts)
    table_expenses_by_day = graph_bank_class.get_table_expenses_by_day(all_accounts)
    last_month_expenses = graph_bank_class.get_last_month_expenses(all_accounts)
    last_month_income = graph_bank_class.get_last_month_income(all_accounts)
    last_month_saving = graph_bank_class.get_last_month_saving(all_accounts)
    get_expense_last_day = graph_bank_class.get_expense_last_day(all_accounts)
    get_expense_last_week = graph_bank_class.get_expense_last_week(all_accounts)
    get_ratio_saving_last_month = graph_bank_class.get_ratio_saving_last_month(all_accounts)
    get_last_date_table = graph_bank_class.get_last_date_table(all_accounts)
    get_investment_inputs = graph_bank_class.get_investment_inputs()
    get_income_median = graph_bank_class.get_income_median(all_accounts)
    get_expenses_median = graph_bank_class.get_expenses_median(all_accounts)
    get_expenses_percentaje_per_day = graph_bank_class.get_expenses_percentaje_per_day(all_accounts)
    
    get_expenses_tends = graph_bank_class.get_expenses_tends(all_accounts)
    file_path = os.path.join('/django/', 'web/static', 'img/picture.jpeg')
    print('file')
    print(file_path)
    return {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'data_line_plot': inputs_graph_line['data'],
        'label_line_plot': inputs_graph_line['label'],
        'data_bar_plot': inputs_graph_bar['data'],
        'label_bar_plot': inputs_graph_bar['label'],
        'data_bar_plot_income': inputs_graph_bar_income['data'],
        'label_bar_plot_income': inputs_graph_bar_income['label'],
        'data_bar_plot_saving': input_graph_saving['data'],
        'label_bar_plot_saving': input_graph_saving['label'],
        'pivot_data_index': data['pivot_percentage_index'],
        'pivot_data_columns': data['pivot_percentage_columns'],
        'pivot_data_values': data['pivot_percentage_values'],
        'pie_label_columns': input_pie_graph['label'],
        'pie_data_values': input_pie_graph['data'],
        'line_top_three_date': input_line_top_three_graph['date'],
        'line_top_three_expenses': input_line_top_three_graph['expenses'],
        'line_top_three_target': input_line_top_three_graph['target'],
        'line_top_three_porcentual': input_line_top_three_graph['porcentual'],
        'table_expenses_by_day_values': table_expenses_by_day['values'],
        'table_expenses_by_day_columns': table_expenses_by_day['columns'],
        'table_expenses_by_day_categories': table_expenses_by_day['categories'],
        'logo_url': file_path,
        'last_month_expenses_value': last_month_expenses['value'],     
        'last_month_expenses_date_month': last_month_expenses['date_month'],
        'last_month_income_value': last_month_income['value'],
        'last_month_income_date_month': last_month_income['date_month'],
        'last_month_saving_value': last_month_saving['value'],
        'last_month_saving_date_month': last_month_saving['date_month'],
        'get_expense_last_day_label': get_expense_last_day['label'], 
        'get_expense_last_day_data': get_expense_last_day['data'],
        'get_expense_last_week_label': get_expense_last_week['label'],
        'get_expense_last_week_data':get_expense_last_week['data'],
        'get_ratio_saving_last_month_label': get_ratio_saving_last_month['label'],
        'get_ratio_saving_last_month_data': get_ratio_saving_last_month['data'],
        'all_accounts': all_accounts,
        'last_update_date': get_last_date_table['date'],
        'get_investment_inputs_income_data': get_investment_inputs['Values'][0]['data'],
        'get_investment_inputs_income_label': get_investment_inputs['Values'][0]['label'],
        'get_investment_inputs_expenses_data': get_investment_inputs['Values'][1]['data'],
        'get_investment_inputs_expenses_label': get_investment_inputs['Values'][1]['label'],
        'get_investment_inputs_saving_data': get_investment_inputs['Values'][2]['data'],
        'get_investment_inputs_saving_label': get_investment_inputs['Values'][2]['label'],
        'get_income_median_data': get_income_median['data'],
        'get_income_median_label': get_income_median['label'],
        'get_expenses_median_data': get_expenses_median['data'],
        'get_expenses_median_label': get_expenses_median['label'],
        'get_income_median_data_por_day': get_income_median['data_per_day'],
        'get_expenses_percentaje_per_day_data': get_expenses_percentaje_per_day['data'],
        'get_expenses_percentaje_per_day_label': get_expenses_percentaje_per_day['label'],
        'expenses_current_month_projected': get_expenses_tends['expenses_current_month_projected'],
        'data_per_day_projected': get_expenses_tends['data_per_day'],
        'label_per_day_projected': get_expenses_tends['label_per_day'],
        'type_per_day_projected': get_expenses_tends['type_per_day'],
        'data_month_projected': get_expenses_tends['data_month'],
        'label_month_projected': get_expenses_tends['label_month'],
        'type_month_projected': get_expenses_tends['type_month'],
        'current_period': get_expenses_tends['current_period'],
        'previous_period': get_expenses_tends['previous_period'],
    }


def Home(request):
    selected_account_name = request.GET.get('account_name', None)

    if selected_account_name:
        table_transaction_banks = models_bank.DataBanks.objects.filter(account_name=selected_account_name)
    else:
        table_transaction_banks = models_bank.DataBanks.objects.all()
    try:
        saving_target = SavingTarget.objects.latest('created_at')  
    except SavingTarget.DoesNotExist:
        saving_target = None  

    all_accounts = table_transaction_banks.values('account_name').distinct()
    queryset = table_transaction_banks.all().values('account_name').distinct()
    account_name_value = selected_account_name or (queryset[0]['account_name'] if queryset else None)
    context = get_expenses_data(saving_target.saving_target if saving_target else 1, account_name_value)
    context['all_accounts'] = all_accounts
    context['selected_account_name'] = selected_account_name
    return render(request, 'home.html', context)

def inversions(request):
    selected_account_name = request.GET.get('account_name', None)

    if selected_account_name:
        table_transaction_banks = models_bank.DataBanks.objects.filter(account_name=selected_account_name)
    else:
        table_transaction_banks = models_bank.DataBanks.objects.all()
    try:
        saving_target = SavingTarget.objects.latest('created_at')  
    except SavingTarget.DoesNotExist:
        saving_target = None  

    all_accounts = table_transaction_banks.values('account_name').distinct()
    queryset = table_transaction_banks.all().values('account_name').distinct()
    account_name_value = selected_account_name or (queryset[0]['account_name'] if queryset else None)
    context = get_expenses_data(saving_target.saving_target if saving_target else 1, account_name_value)
    context['all_accounts'] = all_accounts
    context['selected_account_name'] = selected_account_name
    return render(request, 'inversions.html', context)

def Comportamiento(request):
    selected_account_name = request.GET.get('account_name', None)

    if selected_account_name:
        table_transaction_banks = models_bank.DataBanks.objects.filter(account_name=selected_account_name)
    else:
        table_transaction_banks = models_bank.DataBanks.objects.all()
    try:
        saving_target = SavingTarget.objects.latest('created_at')  
    except SavingTarget.DoesNotExist:
        saving_target = None  

    all_accounts = table_transaction_banks.values('account_name').distinct()
    queryset = table_transaction_banks.all().values('account_name').distinct()
    account_name_value = selected_account_name or (queryset[0]['account_name'] if queryset else None)
    context = get_expenses_data(saving_target.saving_target if saving_target else 1, account_name_value)
    context['all_accounts'] = all_accounts
    context['selected_account_name'] = selected_account_name
    return render(request, 'behavior.html', context)

def Details(request):
    selected_account_name = request.GET.get('account_name', None)

    if selected_account_name:
        table_transaction_banks = models_bank.DataBanks.objects.filter(account_name=selected_account_name)
    else:
        table_transaction_banks = models_bank.DataBanks.objects.all()
    try:
        saving_target = SavingTarget.objects.latest('created_at')  
    except SavingTarget.DoesNotExist:
        saving_target = None  

    all_accounts = table_transaction_banks.values('account_name').distinct()
    queryset = table_transaction_banks.all().values('account_name').distinct()
    account_name_value = selected_account_name or (queryset[0]['account_name'] if queryset else None)
    context = get_expenses_data(saving_target.saving_target if saving_target else 1, account_name_value)
    context['all_accounts'] = all_accounts
    context['selected_account_name'] = selected_account_name
    return render(request, template_details_name, context)

def Tables(request):
    selected_account_name = request.GET.get('account_name', None)

    if selected_account_name:
        table_transaction_banks = models_bank.DataBanks.objects.filter(account_name=selected_account_name)
    else:
        table_transaction_banks = models_bank.DataBanks.objects.all()
    try:
        saving_target = SavingTarget.objects.latest('created_at')  
    except SavingTarget.DoesNotExist:
        saving_target = None  

    all_accounts = table_transaction_banks.values('account_name').distinct()
    queryset = table_transaction_banks.all().values('account_name').distinct()
    account_name_value = selected_account_name or (queryset[0]['account_name'] if queryset else None)
    context = get_expenses_data(saving_target.saving_target if saving_target else 1, account_name_value)
    context['all_accounts'] = all_accounts
    context['selected_account_name'] = selected_account_name
    return render(request, template_tables_name, context)

#def send_message_to_chatgpt(conversation_history, user_message):
#    
#    conversation_history.append({"role": "user", "content": user_message})#

#    openai.api_key = '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'
#    endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
#    messages = [{"role": "system", "content": "You are a helpful assistant."}] + conversation_history
#    messages.append(
#                {"role": "user", "content": user_message},
#    )
#    chat_completion = openai.ChatCompletion.create(
#                model="gpt-3.5-turbo",
#                messages=messages
#    )
#    bot_response = chat_completion.choices[0].message.content
#    conversation_history.append({"role": "assistant", "content": bot_response})
#    return conversation_history, bot_response

def send_message_to_chatgpt(
    conversation_history,
    prompt,
    text_data,
    count_message
    ):
        
    openai.api_key =  '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'
    transactions = text_data
    if count_message == 1:
        dicc_transactions = {'transactions': []}
        for index in range(len(transactions)):
            if transactions[index]['type'] == 'Egreso':
                dicc = {
                    'ID': transactions[index]['ID'],
                    'amount': int(transactions[index]['amount']),
                    'date': transactions[index]['date'],
                    'type':'expenses',
                    'category': transactions[index]['category'],
                }
                dicc_transactions['transactions'].append(dicc)
            else:
                dicc = {
                    'ID': transactions[index]['ID'],
                    'amount': int(transactions[index]['amount']),
                    'date': transactions[index]['date'],
                    'type':'income',
                    'category': transactions[index]['category'],
                }
                dicc_transactions['transactions'].append(dicc)

        transaction_details = "\n".join([
            f"ID: {dicc['ID']}, Amount: {dicc['amount']}, Date: {dicc['date']}, Type: {dicc['type']}, Category: {dicc['category']}"
            for dicc in dicc_transactions['transactions']
        ])

        conversation_history = []   
        conversation_history = [
        {"role": "system", 
        "content": """You are a financial expert. You will recieve and analyze financial data of the income and expenses of a cliente from his bank. Based on this information, you must summary them, generate recommendation and detect insights in the data. 
                        You can make some operations as sum, average, count, etc with the financial data if you need a answer a question.
                        You will respond in Spanish and maintain a polite and friendly tone throughout the conversation.
                        If You can not answer a question based on the financial data, you will say: "Disculpa, no tengo la informacion suficiente".
                        Your answers must be always alineated with the financial data that you recieve.
                        The financial data is the following:
                        {}
                        You can groupby the data by date, category, type, etc, getting better insights of the data.
                    """.format(transaction_details)
        },
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=conversation_history,
                temperature=0
            )
            assistant_response = response.choices[0].message["content"]
        except openai.error.APIError as e:
            assistant_response = "Lo siento, pero hubo un error al procesar su solicitud. Por favor, inténtelo de nuevo más tarde."

        user_message = {"role": "user", "content": prompt}
        conversation_history.append(user_message)

        try:
            bot_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=conversation_history,
                temperature=0
            )
            bot_response = bot_response.choices[0].message["content"]
            return conversation_history, bot_response

        except openai.error.APIError as e:
            bot_response = "Lo siento, pero hubo un error al procesar su solicitud. Por favor, inténtelo de nuevo más tarde."
            return conversation_history, bot_response

    else:
        user_message = {"role": "user", "content": prompt}
        conversation_history.append(user_message)
        try:
            bot_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=conversation_history,
                temperature=0
            )
            bot_response = bot_response.choices[0].message["content"]
            return conversation_history, bot_response

        except openai.error.APIError as e:
            bot_response = "Lo siento, pero hubo un error al procesar su solicitud. Por favor, inténtelo de nuevo más tarde."
            return conversation_history, bot_response


def Chat(request):

    selected_account_name = request.GET.get('account_name', None)

    if selected_account_name:
        table_transaction_banks = models_bank.DataBanks.objects.filter(account_name=selected_account_name)
    else:
        table_transaction_banks = models_bank.DataBanks.objects.all()
    try:
        saving_target = SavingTarget.objects.latest('created_at')  
    except SavingTarget.DoesNotExist:
        saving_target = None  

    all_accounts = table_transaction_banks.values('account_name').distinct()
    queryset = table_transaction_banks.all().values('account_name').distinct()
    account_name_value = selected_account_name or (queryset[0]['account_name'] if queryset else None)
    context = get_expenses_data(saving_target.saving_target if saving_target else 1, account_name_value)
    
    graph_bank_class = graph_bank.GraphExpenses()
    get_all_records = graph_bank_class.get_all_records()
    get_all_records = get_all_records['text_records']
    
    conversation_history = request.session.get('conversation_history', [])
    count_message = request.session.get('count_message', 1)
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '') 
        conversation_history, bot_response = send_message_to_chatgpt(conversation_history, user_message, get_all_records, count_message)
        request.session['conversation_history'] = conversation_history
        count_message = count_message + 1
        request.session['count_message'] = count_message 
        return JsonResponse({'bot_response': bot_response})
    
    request.session['count_message'] = 1

    return render(request, template_chat_name, context)


def Start(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            link_token = form.cleaned_data['link_token']
            security_token = form.cleaned_data['security_token']  
            saving_target_value = int(form.cleaned_data['saving_target'].replace('.',''))
            st = SavingTarget(saving_target=saving_target_value)
            st.save()                            
            update_transactions_table(link_token, security_token)            
            return redirect(reverse('home'))

    else:
        form = LoginForm() 
    return render(request, template_start_name, {'form': form})

def Clasification(request):
     
    records = DataBanks.objects.all().values()
    df = pd.DataFrame.from_records(records)
    df = df.loc[df['indicator_not_category'] == True]
    df = df[['id','date','description','account_name','currency', 'amount','type_expenses','category_description']]
    df = df.reset_index().drop(columns = ['index'])
    df.rename(columns = {'date':'Fecha', 'description':'Descripción', 
                        'amount':'Monto', 'currency':'Moneda', 
                        'category_description':'SubCategoría', 
                        'account_name':'Cuenta',
                        'type_expenses':'Tipo'}, inplace = True)
    
    seaching_accounts = list(df['Descripción'].unique())
    values = df.values.tolist()
    columns = list(df.columns)
    categories = df.index.to_list()
    context =  {
        'values': values,
        'columns': columns,
        'categories': categories,    
        'accounts': seaching_accounts        
    }
    
    if request.method == 'POST':
            try:
                data = json.loads(request.body)
                for row in data:
                    data_bank_instance = DataBanks.objects.get(id=row['id'])  # use 'ID' as a unique identifier
                    data_bank_instance.type_expenses = row.get('TipoUsuario')
                    data_bank_instance.category_description = row.get('SubCategoriaUsuario')
                    data_bank_instance.save()
#               
                return JsonResponse({"success": True})
            
            except Exception as e:
                return render(request, template_clasification_name, context)
    
    return render(request, template_clasification_name, context)




