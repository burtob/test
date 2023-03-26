import csv

MONTH = 'march'

file = f"dkb_{MONTH}.csv"

with open(file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        date = row[0]   #Buchungstag
        name = row[3]   #Auftraggeber
        amount = row[7] #Betrag in EUR
        category = 'sonstiges'

        if name == "SPAR DANKT 1005":
            category = 'Lebensmittel'
        
        if name == "Hotel Kommod":
            category = 'Mittagessen'
        
        if name == "A1 Telekom Austria Aktiengesellschaft":
            category = 'Handy Rechnung'

        transaction = ((date, name, amount, category))
        print(transaction)