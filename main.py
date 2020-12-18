import csv
import sys

# Debug = 1 to show debug traces
debug = 0
# Month names array
months = ["January", "February", "March",
		  "April",   "May",      "June",
		  "July",    "August",   "September",
		  "October", "November", "December"]
n_months = 12

# Used files: N26 export csv file and output csv file
n26_csv = "n26-csv-transactions.csv"
_of_balance = "n26_year_balance_"
_of_exp_clas = "n26_year_expenses_classified_"
of_extension = ".csv"

# Column names:
date     = "Fecha"
ben      = "Beneficiario"
account  = "Número de cuenta"
trans    = "Tipo de transacción"
ref      = "Referencia de pago"
category = "Categoría"	
qty_eur  = "Cantidad (EUR)"
qty_fc   = "Cantidad (Divisa extranjera)"
currency = "Tipo de divisa extranjera"
exc_rate = "Tipo de cambio"

# Expense types
exp_typ =  ["Ahorro & Inversión",
			"Bares y restaurantes",
			"Cajero",
			"CASH26",
			"Comida & Comestibles",
			"Compras",
			"Educación",
			"Familia & Amigos",
			"Gastos profesionales",
			"Impuestos y multas",
			"Ingresos",
			"Invitación a N26",
			"Multimedia & Electrónicos",
			"Ocio & Entretenimiento",
			"Otros",
			"Salario",
			"Salud y droguería",
			"Seguros & Finanzas",
			"Spaces",
			"Suscripciones & Donaciones",
			"Transporte & Coche",
			"Viajes & Vacaciones",
			"Vivienda & Servicios Públicos"]

exp_track = [[0 for i in range(n_months)] for j in range(len(exp_typ))]

# My N26 space names
n26_spaces = ["Hauptkonto", "Rettunschwimmer", "Kapitalistenschwein"]


def get_year(date):
	# Get the year from a YYYY-MM-DD format date
	return int(date.split("-")[0])


def get_month(date):
	# Get the month from a YYYY-MM-DD format date
	m = date.split("-")[1]
	if int(m) < 0:
		return -1
	if int(m) > n_months:
		return -1
	return int(m)

def get_balance(year, income, expenses):
	diff = [0] * n_months
	with open(n26_csv, mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			line_count = 0
			for row in csv_reader:
				if debug:
					if line_count == 0:
						print(f'Column names are {", ".join(row)}')
				if get_year(row[date]) == year:
					if(float(row[qty_eur]) > 0):
						if not (any(word in row[ben] for word in n26_spaces)): # Exclude transfers between N26 spaces.
							income[get_month(row[date])-1] += float(row[qty_eur])
					elif(float(row[qty_eur]) < 0):
						if not (any(word in row[ben] for word in n26_spaces)): # Exclude transfers between N26 spaces.
							month = get_month(row[date])
							expenses[month-1] += float(row[qty_eur])
							classify_expenses(row[category], row[qty_eur], month)
				else:
					print("ERROR: No data for the year " + str(year))
				line_count += 1
	if debug:
		print(f'Processed {line_count} lines + 1 header line.')
	
	for i in range(n_months):
		diff[i] = income[i] + expenses[i]

	return diff

def balance2file(file_name, income, expenses, diff):
	diff = [0] * n_months
	with open(file_name, mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(["","Anual total"] + months)
		csv_writer.writerow(["Income", sum(income)] + income)
		csv_writer.writerow(["Expenses", sum(expenses)] + expenses)
		for i in range(n_months):
			diff[i] = income[i] + expenses[i]
		csv_writer.writerow(["Difference", sum(diff)] + diff)
		# Todo: Add difference excluding savings & investment

	if debug:
		print(income)
		print(expenses)
		print(diff)

def classify_expenses(cat, qty, month):
	if debug:
		print("Category: " + cat + ", index:" + str(exp_typ.index(cat)))
		print("Month: " + months[month - 1] + ", " + str(month))
		print("Quantity (EUR): " + str(qty))
	exp_track[exp_typ.index(cat)][month - 1] += float(qty)

def expenses2file(file_name):
	with open(file_name, mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(["","Annual total"] + months)
		for i in range(len(exp_typ)):
			csv_writer.writerow([exp_typ[i], sum(exp_track[i])] + exp_track[i])

def main():
	year = int(sys.argv[1])
	if debug:
		print("Year: " + str(year))
	
	# Output file names
	of_balance = _of_balance + str(year) + of_extension
	of_exp_clas = _of_exp_clas + str(year) + of_extension

	# Arrays for monthly income and expenses
	expenses = [0] * n_months
	income = [0] * n_months
	balance = [0] * n_months

	balance = get_balance(year, income, expenses)
	balance2file(of_balance, income, expenses, balance)
	expenses2file(of_exp_clas)

if __name__ == "__main__":
	main()
	