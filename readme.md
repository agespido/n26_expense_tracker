# N26 expense tracker

UPDATE 30/07/2024: This project is no longer maintained. The N26 Bank has changed the format of the CSV file, so the script is not working anymore. I will not update it, but feel free to fork it and make the necessary changes.

The column "Category" has been eliminated, making it impossible to classify the expenses.

## Description

This project is a custom tool that processes the CSV file that is available for download to all N26 Bank users. This information will be presented in two csv output files (``n26_year_balance_<year>.csv`` and ``n26_year_expenses_classified_<year>.csv``), than can be used as input data by other scripts, spreadsheets, etc.

This file, called `` n26-csv-transactions.csv `` contains all the banking transactions between two dates.

## How to run the script?

By running the following command, we will get the processed data for the given year.

`` python3 <path_to_project>/main.py <year> ``

Some considerations to be done:
   1. N26 space names are hardcoded in the `` main.py `` file.
   2. The text strings used for column names and expenses types in the code may vary, depending on the N26 Bank account language. In my case, for example, this information is in spanish. Check it in your n26-transactions.csv file
   3. All this variables are defined at the beginning of the `` main.py ``.

## Output files format

### n26_year_balance_xxxx.csv

The file has the following format:

||Anual total|January|February|March|April|May|June|July|August|September|October|November|December|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Income| | | | | | | | | | | | | |
|Expenses| | | | | | | | | | | | | |
|Difference| | | | | | | | | | | | | |

### n26_year_expenses_classified_xxxx.csv

The file has the following columns, being "Expense type" the categories used by N26 Bank to classify the expenses and incomes:

|Expense type|Annual total|January|February|March|April|May|June|July|August|September|October|November|December|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
