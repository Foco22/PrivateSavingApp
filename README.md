# Saving App

## Overview

This is a Saving app that using your financial records from your bank, allow to identify income and expenses monthly. Addicionally, the app has a discharge classifier which it be usefull to identify in what items you spend more. This classifier was done based on bussines rule, without using a ML or AI models. 

## Non-technical prerequisite

Before you begin, if you want to use this app, you must sign up in Fintoc. This is a FinTech Chile that allow you to extract your financial information from your bank account. You must following the next steps:

- Go to the https://fintoc.com/cl
- Sign in the website.
- Add a new connection (blue bottom in the dashboard)
- In the "Connect Live Link" windows, choose country, API and type of account. If it is a personal account,      should be a "Individual"
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

## Demo

You can look at a video of the app:

<iframe width="560" height="315" src="https://www.youtube.com/watch?v=MlXP2_zF-O4" frameborder="0" allowfullscreen></iframe>


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
