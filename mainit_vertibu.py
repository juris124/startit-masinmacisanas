with open('dati/auto_imports.csv', mode="r") as datne:
    dati = datne.read()

#dati = dati.replace("gas", "1")
#dati = dati.replace("diesel", "2")
#print(dati)

dati = dati.replace("convertible", "1")
dati = dati.replace("hardtop", "2")
dati = dati.replace("sedan", "3")
dati = dati.replace("wagon", "4")
dati = dati.replace("hatchback", "5")

#with open('dati/auto_imports_degviela.csv', mode="w")  as datne:
with open('dati/auto_imports_tips.csv', mode="w")  as datne:
    datne.write(dati)
