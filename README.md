# Saving App

## Overview

This is a Saving app that using your financial records from your bank, allow to identify income and expenses monthly. Addicionally, the app has a discharge classifier which it be usefull to identify in what items you spend more. This classifier was done based on bussines rule, without using a ML or AI models. 

Please taking in consideration that this web app has tested with single account, so it can work not so well in some cases. Addicionaly, it is very important to classifier very well the manually transactions before goingo to the dashboards

## Non-technical prerequisite

Before you begin, if you want to use this app, you must sign up in Fintoc. This is a FinTech Chile that allow you to extract your financial information from your bank account. You must following the next steps:

- Go to the https://fintoc.com/cl
- Sign in the website.
- Add a new connection (blue bottom in the dashboard)
- In the "Connect Live Link" windows, choose country, API and type of account. If it is a personal account, should be a "Individual"
- Choose your bank account.
- Add your RUT and password, and press "continuar"
- You will recieve your link token, what you can use it to extract your information.

After this, you also must get your secret key in the "Api Keys" section. With the Api Key and Secret key, you can use this app, because of those are the credencial neeeded to use Api of Fintoc.

## Technical prerequisite

As prerequisited, you must installed the next ones in your computer:

- Docker
- Docker-compose.

If you do not have a Docker installed in your computer, please go to this page:

https://www.docker.com/products/docker-desktop/


## ¿What does app contain?

The app contains several graphs and insights from your income and expenses in your bank account, getting worth information from your net results (income and expenses). The app contains the following page:

- **Inicio**: The home page is used to get the inputs from the user, as the name, target saving, link token and security token. Those inputs are used to extract the information by API (security and token), and also used as a input for some graph (target).

- **Clasificador**: This page is used to clasify manually some records that can not be classify by the logic of the app. You will have a table with information from the date, description movement, type of movements, amount, etc. As those are you movement, probably you must know better what they are.

- **Home**: The first page of the data, when you can look at information from your income, expenses and net flow from your bank account. This page is a summary of what you have spend of and your incomes.

- **Objetivo (Details)**: In this page, you can review the top 5 categories that you must spend of. Also, you can review your total expenses by month, target saving value (input getting from the start page) and your desviation. 

- **Gastos (Table)**: This page is used to show your total expenses by categories for each month, showing you how much you spend in each item by month.

- **Comportamiento (Tendency)**: This page is used to show some tendency in your data. Based on your distribution daily expenses by day of the month, you can look at how much you should spend in the current month by day and month. You can look at predicted forecast of the current month expenses, based on your past distribution. 

- **Inversiones**: This page is used to show your income and expenses movement from your investment. If you do not have any investment movement in your account, you should not see any information in this page.

I also hightligh that the logic was created based on your bank account as a the center, so if you are moving money in your bank products. If you move money to your investment, that is a money outflow from your bank account, in contract, if you move money from your investment to your bank account, that is a inflow of money in your bank account.

## Transaction Classifier

The classifier was done using regex, based on the description of the transaction. Those regex are in the constants.py file into the bank folder, with the following information:

```python
CINE = re.compile(r'(CINEPLANET|ENJOY CASINO|CINE HOYTS|CASINO|CINE MARK|CINEMARK|CINEPOLIS|CINEPOLIS CHILE)', re.IGNORECASE)
DEBT_PAYMENTS = re.compile(r'(TARJ CRED|TARJETA DE CREDITO|TARJ.CRED.|PAGO TC|PAGO TARJETA DE CREDITO)', re.IGNORECASE)
EDUCATION = re.compile(r'(COURSRA|PUC|UCH|UDEC|PUCV|USACH|UACH|UNAB|UTAL|UV|USM|UDD|UDP|UFRO|UNADES|UCN|UAI|UA|UBB|UTA|USS|ULS|UCSC|UCT|UBO|UCEN|UA|UCM|UAH|UPLA|UNAP|UTEM|ULAGOS|UST|UDLA|UMCE|INACAP|UVM|UNIACC|USEK|UAC|ULL)', re.IGNORECASE)
HEALTHCARE = re.compile(r'(CCC LAS CONDES|RADIOLOGIA|DERMATOLOGO|SALUD|CLINICA|HOSPITAL|ORTODONCIA)', re.IGNORECASE)
TRAVEL_HOTEL = re.compile(r'(HOTEL|HOSTAL|JETSMART|LATAM|HOTELES|LUNA DE PIRQUE|PUCON|SKY AIRLINE|SKY)', re.IGNORECASE)
WORK_INCOME = re.compile(r'(REMUNERACI|SUELDOS|SUELDO)', re.IGNORECASE)
INCOME_HOUSE = re.compile(r'(Luis Miguel Car|Marisol Parra R)', re.IGNORECASE)
INSURANCE = re.compile(r'(REDCOMPRA HDI SEGUROS|SEGUROS|INSURANCE|VIDA CAMAMRA|METLIFE|VIDA SECURITY)', re.IGNORECASE)
INVESTMENTS = re.compile(r'(FONDOS MUTUOS)', re.IGNORECASE)
PHARMACY = re.compile(r'(SALCOBRAND|AHUM|FARMACIA|CRUZ VER|DRSIMI|SIMI)', re.IGNORECASE)
RESTAURANT_BAR = re.compile(r'(PERU|SUSHI|RAPPI|TAKE EAT|CASTANO|SALAD|SUBWAY|CAFETERIA|STARBUCKS|GREENS|NIU SUSHI|DUNKIN DONUTS|COPPELIA|FOOD|JUAN MAESTRO|TOMMY BEANS|MC DONALDS|GELATERIA|JOHNNY ROCKETS|DOMINO FUENTE|GOLFO DI NAPOLE|RUBY TUESDAY|CHOCOLATE|FORK|DRINKS|TACO BELL|PIZZA|FUENTE CHICA|HARD ROCK|COFFE|OBELISCO|WORK CAFE|BONAFIDE|DOGGIS|RESTOBAR|BAR|FUENTE CHILENA|EL PATIO|TELEPIZZA|PIZZA|DOGGIS|PIZZA HUT|KENTUCKY|JUAN MAESTRO)', re.IGNORECASE)
SUPERMARKET_RETAILS = re.compile(r'(UNIMARC|ZARA|FALABELLA|PARIS|RIPLEY|WALMART|JUMBO|SANTA ISABEL|EASY|TOTTUS|ALVI|CASAIDEAS|MERCADO LIBRE|EASY|ABCDIN|LA POLAR|LAPOLAR|CORONA|ALIEXPRESS|CONSTRUMART|HITES|SODIMARC|DAFITI|ROSEN|HYM|H&M|COSTANERA|COSTANER)', re.IGNORECASE)
SPORT = re.compile(r'(PADEL|FUTBOL|STADE FRANCAIS|CIUDAD DEPORTIVA|ADIDAS|NIKE|DECATHLON|PUMAS)', re.IGNORECASE)
SUSCRIPTIONS = re.compile(r'(VAST|ZAPPING|CHATGPT|GOOGLE PAY|Spotify|GOOGLE CLOUD|GOOGLE)', re.IGNORECASE)
SII = re.compile(r'(SII|COMISION|IMPTO)', re.IGNORECASE)
UTILITIES = re.compile(r'(AGUAS|ENELSA|ELECTRICIDAD|MOVISTAR|VTR|CLARO|WOM|ENTEL|TELEFONICA|AGUAS ANDINAS|ENEL|COLMENA|METROGAS|COMUNIDAD EDIFIC)', re.IGNORECASE)
WIRE_TRANSFERS = re.compile(r'(TEF|TRANSF|TRASPASO|TRASPASO)', re.IGNORECASE)
TRANSPORT = re.compile(r'(UBER|TUR BUS|BUS|METRO|DIDI|CONDOR BUS|PULLMAN|BUSES)', re.IGNORECASE)
CREDIT_LINE = re.compile(r'(LINEA DE CREDITO|LINEA DE CRED)', re.IGNORECASE)
```


## Demo

You can look at a video of the app:

[![Demo Video](https://example.com/demo-video-screenshot.png)](https://www.youtube.com/watch?v=MlXP2_zF-O4)

## Getting Started (How to install it)

To get this project up and running on your local machine, follow these steps:

### Clone the Repository

```bash
git clone https://github.com/Foco22/PrivateSavingApp.git
cd PrivateSavingApp
```

### Start the container

Start the containers:

```bash
docker-compose up
```

You get in your: http://localhost:8000

### 

Stop the containers:

```bash
docker-compose down
```
