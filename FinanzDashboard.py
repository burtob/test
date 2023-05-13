#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import libraries
import pandas as pd
import numpy as np
import panel as pn
from panel.interact import interact
pn.extension()

import hvplot.pandas


# In[ ]:


# Function getDataFrame()

def getDataFrame(filename):

  # Create dataframe from *.csv
  df = pd.read_csv(filename, sep=";", encoding = 'ISO-8859-1', skiprows=6)

  # Delete columns
  df = df.drop(["Wertstellung","Buchungstext","Gläubiger-ID","BLZ","Kontonummer", 
              "Verwendungszweck","Mandatsreferenz","Kundenreferenz","Unnamed: 11"],axis=1)
  
  # Rename columns
  df = df.rename(columns={'Auftraggeber / Begünstigter':'Auftraggeber'})
  df = df.rename(columns={'Betrag (EUR)':'Betrag'})

  # Insert additional columns
  df['Kategorie'] = 'Sonstiges'
  df['Monat'] = 'Nicht definiert'
  df['Jahr'] = 'Nicht definiert'
  df['Ein/Ausgang'] = 'Eingang'

  # Format Ein/Ausgang
  df['Ein/Ausgang'] = np.where(df['Betrag'].str[0] == '-','Ausgang', df['Ein/Ausgang'])

  # Format Betrag
  df['Betrag'] = df['Betrag'].str.replace(r'\.', '', regex=True)
  df['Betrag'] = df['Betrag'].str.replace(r'\,', '.', regex=True)
  df['Betrag'] = df['Betrag'].astype(float)

  # Format Buchungstag
  df['Buchungstag'] = df['Buchungstag'].astype(str)

  # Get year and month
  df['Jahr'] = df['Buchungstag'].str.slice(6,10)
  df['Monat'] = df['Buchungstag'].str.slice(3,5) 
  df['Monat'] = np.where(df['Monat'] == '01','Januar', df['Monat'])           
  df['Monat'] = np.where(df['Monat'] == '02','Februar', df['Monat'])       
  df['Monat'] = np.where(df['Monat'] == '03','März', df['Monat'])
  df['Monat'] = np.where(df['Monat'] == '04','April', df['Monat'])
  df['Monat'] = np.where(df['Monat'] == '05','Mai', df['Monat'])
  df['Monat'] = np.where(df['Monat'] == '06','Juni', df['Monat']) 
  df['Monat'] = np.where(df['Monat'] == '07','Juli', df['Monat'])
  df['Monat'] = np.where(df['Monat'] == '08','August', df['Monat']) 
  df['Monat'] = np.where(df['Monat'] == '09','September', df['Monat'])
  df['Monat'] = np.where(df['Monat'] == '10','Oktober', df['Monat'])        
  df['Monat'] = np.where(df['Monat'] == '11','November', df['Monat'])
  df['Monat'] = np.where(df['Monat'] == '12','Dezember', df['Monat'])

  return df


# In[ ]:


# Get dataframes

# Tobias
df_T = getDataFrame("dkb.csv")

# Tobias & Julia
df_TJ = getDataFrame("dkb_TJ.csv")


# In[ ]:


# Categorization Tobias
# Lebensmittel

# Mittagessen
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('Kommod'),'Mittagessen', df_T['Kategorie'])

# Jause
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('Manga|MANGOLD|SPAR DANKT'),'Jause', df_T['Kategorie'])

# Handy
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('A1 Telekom'),'Handy', df_T['Kategorie'])

# Aktivitäten
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('Bergbahn'),'Aktivitäten', df_T['Kategorie'])

# Investments
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('FLATEX'),'Investments', df_T['Kategorie'])

# Sportartikel
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('SPORTH.|CYCLING SPORT'),'Sportartikel', df_T['Kategorie'])

# Krankenversicherung
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('GENERALI'),'Krankenversicherung', df_T['Kategorie'])

# Klamotten
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('Facona|Garzon|HM|Tretter-Schuhe|Oberpollinger|HIRMER'),'Klamotten', df_T['Kategorie'])

# Gemeinschaftskonto
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('JULIA BEER'),'Gemeinschaftskonto', df_T['Kategorie'])

# Pantec
df_T['Kategorie'] = np.where(df_T['Auftraggeber'].str.contains('Pantec'),'Pantec', df_T['Kategorie'])


# In[ ]:


# Categorization Tobias & Julia
# Lebensmittel
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('SPAR DANKT|foodspring'),'Lebensmittel', df_TJ['Kategorie'])

# Jause
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('Manga|MANGOLD|Jahnhalle|RUFFS|HELLDONES|Suppenkuche|Skihuette'),'Jause', df_TJ['Kategorie'])

# Aktivitäten
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('Bergbahn|Ski Arlberg'),'Aktivitäten', df_TJ['Kategorie'])

# Auto
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('JET|SHELL|PARKEN|PARKGARAGE'),'Auto', df_TJ['Kategorie'])

# Drogerie
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('DM-Fil'),'Drogerie', df_TJ['Kategorie'])

# Wohnungseinrichtung
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('Motel a Miio|VOSSEN|ROTHO-SHOP'),'Wohnungseinrichtung', df_TJ['Kategorie'])

# Julia
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('Julia Beer'),'Julia', df_TJ['Kategorie'])

# Tobias
df_TJ['Kategorie'] = np.where(df_TJ['Auftraggeber'].str.contains('TOBIAS BURTSCHER'),'Tobias', df_TJ['Kategorie'])


# In[ ]:


# Common dashboard widgets

ToggleInOut = pn.widgets.RadioButtonGroup(options=['Ausgaben','Einnahmen'], button_type='success')
Summe = pn.widgets.TextInput(name="Summe", value="0")
CheckSonstiges = pn.widgets.Checkbox(name='Details einblenden')


# In[ ]:


# Function getPlotData()

def getPlotData(df, myInOut, myYear, myMonth, myCategoryIn, myCategoryOut):

    # Income year total
    if myInOut == 'Einnahmen' and myMonth == 'Alle' and myCategoryIn == 'Alle':
        myData = df[(df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Eingang')]
        myData = myData.groupby('Kategorie')['Betrag'].sum().reset_index()
        myData = myData.sort_values(by='Betrag', ascending=True)
        myData = myData.hvplot.barh(x='Kategorie', y='Betrag', xlabel='', ylabel='', title="Einnahmen " + myYear, height=400, grid=True)
        myTable = df[(df['Jahr'] == myYear) & (df['Kategorie'] == 'Sonstiges') & (df['Ein/Ausgang'] == 'Eingang')]
        myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title="Kategorie Sonstiges", height=350, width = 500)

    # Expenses year total
    elif myInOut == 'Ausgaben' and myMonth == 'Alle' and myCategoryOut == 'Alle':
        myData = df[(df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Ausgang')]
        myData = myData.groupby('Kategorie')['Betrag'].sum().reset_index()
        myData = myData[myData['Kategorie'].str.contains("Investments") == False]
        myData['Betrag'] = myData['Betrag'].abs()
        myData = myData.sort_values(by='Betrag', ascending=True)
        myData = myData.hvplot.barh(x='Kategorie', y='Betrag', xlabel='', ylabel='', title="Ausgaben " + myYear, height=400, grid=True)   
        myTable = df[(df['Jahr'] == myYear) & (df['Kategorie'] == 'Sonstiges') & (df['Ein/Ausgang'] == 'Ausgang')]
        myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title="Kategorie Sonstiges", height=350, width = 500)

    # Income month total
    elif myInOut == 'Einnahmen' and myMonth != 'Alle' and myCategoryIn == 'Alle':
        myData = df[(df['Monat'] == myMonth) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Eingang')]
        myData = myData.groupby('Kategorie')['Betrag'].sum().reset_index()
        myData = myData.sort_values(by='Betrag', ascending=True)
        myData = myData.hvplot.barh(x='Kategorie', y='Betrag', xlabel='', ylabel='', title="Einnahmen " + myMonth + " " + myYear, height=400, grid=True)
        myTable = df[(df['Monat'] == myMonth) & (df['Jahr'] == myYear) & (df['Kategorie'] == 'Sonstiges') & (df['Ein/Ausgang'] == 'Eingang')]
        myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title="Kategorie Sonstiges", height=350, width = 500)

    # Expenses month total
    elif (myInOut == 'Ausgaben') and (myMonth != 'Alle') and (myCategoryOut == 'Alle'):
        myData = df[(df['Monat'] == myMonth) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Ausgang')]
        myData = myData.groupby('Kategorie')['Betrag'].sum().reset_index()
        myData = myData[myData['Kategorie'].str.contains("Investments") == False]
        myData['Betrag'] = myData['Betrag'].abs()
        myData = myData.sort_values(by='Betrag', ascending=True)
        myData = myData.hvplot.barh(x='Kategorie', y='Betrag', xlabel='', ylabel='', title="Ausgaben " + myMonth + " " + myYear, height=400, grid=True)
        myTable = df[(df['Monat'] == myMonth) & (df['Jahr'] == myYear) & (df['Kategorie'] == 'Sonstiges') & (df['Ein/Ausgang'] == 'Ausgang')]
        myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title="Kategorie Sonstiges", height=350, width = 500)

    # Income/Expenses category total
    elif myMonth == 'Alle' and (myCategoryIn != 'Alle' or myCategoryOut != 'Alle') :
        
        if myInOut == 'Einnahmen': 
            myData = df[(df['Kategorie'] == myCategoryIn) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Eingang')]
        elif myInOut == 'Ausgaben': 
            myData = df[(df['Kategorie'] == myCategoryOut) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Ausgang')]

        myData = myData.groupby('Monat')['Betrag'].sum().reset_index()
        myData['Betrag'] = myData['Betrag'].abs()
        
        if myInOut == 'Einnahmen': 
            myData = myData.hvplot.bar(x='Monat', y='Betrag', xlabel='', ylabel='', title="Einnahmen " + myCategoryIn + " " + myYear, height=400, grid=True)       
            myTable = df[(df['Kategorie'] == myCategoryIn) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Eingang')]
            myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title="Einnahmen " + myCategoryIn + " " + myYear, height=350, width = 500)
            
        elif myInOut == 'Ausgaben': 
            myData = myData.hvplot.bar(x='Monat', y='Betrag', xlabel='', ylabel='', title="Ausgaben " + myCategoryOut + " " + myYear, height=400, grid=True)
            myTable = df[(df['Kategorie'] == myCategoryOut) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Ausgang')]
            myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title="Ausgaben " + myCategoryOut + " " + myYear, height=350, width = 500)

     # Income category month
    elif (myInOut == 'Einnahmen') and (myMonth != 'Alle') and (myCategoryIn != 'Alle'):
        
        myData = df[(df['Monat'] == myMonth) & (df['Kategorie'] == myCategoryIn) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Eingang')]
        myData = myData.groupby('Kategorie')['Betrag'].sum().reset_index()
        myData = myData.sort_values(by='Betrag', ascending=True)
        myData = myData.hvplot.barh(x='Kategorie', y='Betrag', xlabel='', ylabel='', title= "Einnahmen " + myCategoryIn + " " + myMonth +  " " + myYear, height=400, grid=True)
        myTable = df[(df['Monat'] == myMonth) & (df['Kategorie'] == myCategoryIn) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Eingang')]
        myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title= "Einnahmen " + myCategoryIn + " " + myMonth +  " " + myYear, height=350, width = 500)

    # Expenses category month
    elif (myInOut == 'Ausgaben') and (myMonth != 'Alle') and (myCategoryOut != 'Alle'):
        
        myData = df[(df['Monat'] == myMonth) & (df['Kategorie'] == myCategoryOut) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Ausgang')]
        myData = myData.groupby('Kategorie')['Betrag'].sum().reset_index()
        myData['Betrag'] = myData['Betrag'].abs()
        myData = myData.sort_values(by='Betrag', ascending=True)
        myData = myData.hvplot.barh(x='Kategorie', y='Betrag', xlabel='', ylabel='', title= "Ausgaben " + myCategoryOut + " " + myMonth +  " " + myYear, height=400, grid=True)
        myTable = df[(df['Monat'] == myMonth) & (df['Kategorie'] == myCategoryOut) & (df['Jahr'] == myYear) & (df['Ein/Ausgang'] == 'Ausgang')]
        myTable = myTable.hvplot.table(['Auftraggeber', 'Betrag'], title= "Ausgaben " + myCategoryOut + " " + myMonth +  " " + myYear, height=350, width = 500)

    return(myData, myTable)


# In[ ]:


# Account Tobias
YearT = pn.widgets.Select(name='Jahr auswählen', options=['2023'])
MonthT = pn.widgets.Select(name='Monat auswählen', options=['Alle','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'])
CategoryInT = pn.widgets.Select(name='Kategorie auswählen', options=['Alle','Pantec','Krankenversicherung'])
CategoryOutT = pn.widgets.Select(name='Kategorie auswählen', options=['Alle','Mittagessen', 'Jause', 'Handy', 'Aktivitäten', 'Sportartikel', 'Krankenversicherung', 'Klamotten', 'Gemeinschaftskonto'])

# Callback function
@pn.depends(ToggleInOut, YearT.param.value, MonthT.param.value, CategoryInT.param.value, CategoryOutT.param.value, CheckSonstiges)
def update_accountT(InOut, year, month, categoryInT, categoryOutT, sonstiges):

    data, table = getPlotData(df_T, InOut, year, month, categoryInT, categoryOutT)

    if (sonstiges == True) and (InOut == 'Einnahmen'):
        plot = pn.Row(data, table, pn.Column(ToggleInOut, YearT, MonthT, CategoryInT, Summe, CheckSonstiges))
    elif (sonstiges == True) and (InOut == 'Ausgaben'):
        plot = pn.Row(data, table, pn.Column(ToggleInOut, YearT, MonthT, CategoryOutT, Summe, CheckSonstiges))
    elif (sonstiges == False) and (InOut == 'Einnahmen'):
        plot = pn.Row(data, pn.Column(ToggleInOut, YearT, MonthT, CategoryInT, Summe, CheckSonstiges))
    elif (sonstiges == False) and (InOut == 'Ausgaben'):
        plot = pn.Row(data, pn.Column(ToggleInOut, YearT, MonthT, CategoryOutT, Summe, CheckSonstiges)) 

    my_sum = data['Betrag'].sum()
    my_sum = int(my_sum)
    Summe.value = str(my_sum) + " €"
    
    return plot


# In[ ]:


# Account Tobias & Julia

YearTJ = pn.widgets.Select(name='Jahr auswählen', options=['2023'])
MonthTJ = pn.widgets.Select(name='Monat auswählen', options=['Alle','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'])
CategoryInTJ = pn.widgets.Select(name='Kategorie auswählen', options=['Alle','Julia','Tobias'])
CategoryOutTJ = pn.widgets.Select(name='Kategorie auswählen', options=['Alle','Lebensmittel','Jause','Aktivitäten','Drogerie','Auto','Wohnungseinrichtung', 'Miete', 'Stadtwerke', 'Internet und GIS'])

# Callback function
@pn.depends(ToggleInOut, YearTJ.param.value, MonthTJ.param.value, CategoryInTJ.param.value, CategoryOutTJ.param.value, CheckSonstiges)
def update_accountTJ(InOut, year, month, categoryInTJ, categoryOutTJ, sonstiges):

    data, table = getPlotData(df_TJ, InOut, year, month, categoryInTJ, categoryOutTJ)

    if (sonstiges == True) and (InOut == 'Einnahmen'):
        plot = pn.Row(data, table, pn.Column(ToggleInOut, YearTJ, MonthTJ, CategoryInTJ, Summe, CheckSonstiges))
    elif (sonstiges == True) and (InOut == 'Ausgaben'):
        plot = pn.Row(data, table, pn.Column(ToggleInOut, YearTJ, MonthTJ, CategoryOutTJ, Summe, CheckSonstiges))
    elif (sonstiges == False) and (InOut == 'Einnahmen'):
        plot = pn.Row(data, pn.Column(ToggleInOut, YearTJ, MonthTJ, CategoryInTJ, Summe, CheckSonstiges))
    elif (sonstiges == False) and (InOut == 'Ausgaben'):
        plot = pn.Row(data, pn.Column(ToggleInOut, YearTJ, MonthTJ, CategoryOutTJ, Summe, CheckSonstiges)) 

    my_sum = data['Betrag'].sum()
    my_sum = int(my_sum)
    Summe.value = str(my_sum) + " €"
    
    return plot


# In[ ]:


# Select account with radio button

ToggleAccount = pn.widgets.RadioButtonGroup(options=['Gemeinschaftskonto','Konto Tobias'], button_type='success')

# Callback function
@pn.depends(ToggleAccount)
def setMainArea(account):
    if account == 'Gemeinschaftskonto':
        return update_accountTJ
    if account == 'Konto Tobias':
        return update_accountT


# In[ ]:


# Show dashboard

dashboard = pn.template.FastListTemplate(
    title="Finanz Dashboard",
    sidebar=[
        pn.Column(ToggleAccount),
        pn.pane.PNG('money.png', sizing_mode='scale_width'),
        pn.pane.Markdown("## *Ein- und Ausgänge sind gesondert zu betrachten! <br><br> Julia Beer, 08.04.2023*")
    ],
    main=[
        pn.Row(setMainArea)
    ]
)

dashboard.show()

