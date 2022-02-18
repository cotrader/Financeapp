#cd C:\Users\cosn\OneDrive\Python\aktuelle_Arbeit\Streamlit\Financeapp
#Streamlit run Finance_app.py
import streamlit as st
import streamlit.components.v1 as stc 
from datetime import date
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
import pandas as pd
from PIL import Image
import cufflinks as cf
#import datetime
#import time
#Seitenformatierung
pd.set_option('display.max_colwidth', -1)
st.set_page_config(layout="wide")
c1, c2, c3= st.columns((1, 1, 1))
groesse=1500

#Pfadstruktur
pfad='http://cosnews.pythonanywhere.com/static/Aktien/'# Pythonanywhere /home/cosnews/mysite/static
pfadgrafik='http://cosnews.pythonanywhere.com/static/Aktien/Grafik/'
pfad_load='http://cosnews.pythonanywhere.com/static/ML_System/' #wird nicht verwendet ?


#Datenimport
#st.write('Start des Apps')
backtest=pd.read_csv('http://cosnews.pythonanywhere.com/static/Aktien/Grafik/Strategie1.csv') #noch Strategei1 einlesen
Liste=pd.read_csv('http://cosnews.pythonanywhere.com/static/Instrumentenliste.csv')
branche=sorted(Liste.Markt.unique()) 
#st.dataframe(Liste)
#st.dataframe(backtest)

#Radiobutton für Branche oder Einzeltitel
option = st.sidebar.radio('Auswahl:',['Branche','Einzeltitel','Alles','Portfolio'],index=0)

if option=='Branche':
    markt = st.sidebar.selectbox('Auswahl der Branche', branche,key="1") #Selectbox für Branche
    einzeltitel=Liste[(Liste['Markt']==markt)].Name
    einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel in der Branche', einzeltitel,index=0,key="2") #Selectbox für Einzeltitel in der Branche
    
if option=='Einzeltitel': #Selectbox für Einzeltitel aus allen
    einzeltitel=Liste.Name.sort_values(ascending=True) #Liste aller Einzeltitel
    einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel aus allen', einzeltitel,index=0,key="20") #Auswahl der Einzeltitel
    markt =Liste[(Liste['Name']==einzeltitelwahl)].Markt.values[0]
    einzeltitel=[einzeltitelwahl] #ein Einzeltitel

if  option=='Alles': #Selectbox für Einzeltitel aus allen
    einzeltitel=Liste.Name.sort_values(ascending=True) #Liste alle Einzeltitel
    einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel aus allen', einzeltitel,index=0,key="20") #Auswahl der Einzeltitel
    markt =Liste[(Liste['Name']==einzeltitelwahl)].Markt.values[0]

if option=='Portfolio':
    
    einzeltitel=Liste[Liste['Portfolio']==1].Name.sort_values(ascending=True)
    einzeltitelwahl= st.sidebar.selectbox('Auswahl Einzeltitel aus Portfolio', einzeltitel,index=0,key="20") #Auswahl der Einzeltitel
    markt =Liste[(Liste['Name']==einzeltitelwahl)].Markt.values[0]


new_df = Liste.loc[Liste['Name'].isin(einzeltitel)].Kuerzel #Konvertierung  der Auswahlliste in Kuerzel



#Ermittlung Kürzel, Einzeltitel und Branceh
#st.write('Kontrolle Kuerzel,einzeltitelwahl,markt') 
new_df = Liste.loc[Liste['Name'].isin(einzeltitel)].Kuerzel #Konvertierung  der Auswahlliste in Kuerzel
Kuerzel=Liste[(Liste['Name']==einzeltitelwahl)]#Kuerzel von dem langen Namen
Kuerzel=Kuerzel['Kuerzel'].tolist()[0]
#st.write(Kuerzel,einzeltitelwahl,markt)

user_input = st.text_input("Passwort eingeben",type='password')
mykey='Test'
#if True:
if user_input==mykey:
    st.write('Korrektes Passwort')
    st.write(Kuerzel,einzeltitelwahl,markt)
    #Backtestergenisse
    with st.expander("1: Backtestergebnisse Alles oder Branche von Datei df_Strategien.pkl "):
        #Bacltest
        #st.write(new_df)
        #st.write('Kontrolle Backtest alles')   
        #st.dataframe(backtest)
        #st.write('Kontrolle Backtest Auswahl')
        backtestauswahl=backtest.loc[backtest['Aktie'].isin(new_df)] #Backtestauswahl nach Aktien
        #st.dataframe(backtestauswahl)
        #Multiselect 
        #st.write('Multiselect')
        select_list =backtest.Backtest.unique() #vorhandene Backtests
        systemauswahl= st.multiselect("Auswahl der Systeme", select_list,select_list) #ausgewählte Systeme
        st.write(systemauswahl)
        backtestsystem=backtestauswahl.loc[backtestauswahl['Backtest'].isin(systemauswahl)]
        st.write(backtestsystem)
    with st.expander("1a: Backtestergebnisse Einzelwert"):
        
        backtestauswahl=backtest.loc[backtest['Aktie'].isin([Kuerzel])] #Backtestauswahl nach Aktien
        #st.dataframe(backtestauswahl)
        #Multiselect 
        #st.write('Multiselect')
        select_list =backtest.Backtest.unique() #vorhandene Backtests
        systemauswahl= st.multiselect("Auswahl der Systeme", select_list,select_list,key="D1") #ausgewählte Systeme
        st.write(systemauswahl)
        backtestsystem=backtestauswahl.loc[backtestauswahl['Backtest'].isin(systemauswahl)]
        st.write(backtestsystem)    

    #technische Analyse
    with st.expander("2: Charts technische Analyse"): 
        dokumentname1=str(pfad+'Seite'+Kuerzel+'.png')
        st.write(Kuerzel,einzeltitelwahl,dokumentname1)
        st.image(dokumentname1)


    #MA Grafiken
    with st.expander("3:Grafiken  MA Strategien Einzelwert"): 
        st.write(Kuerzel,einzeltitelwahl,markt)
        dokumentname1=str(pfadgrafik+'MA_Strat'+Kuerzel+'.png') 
        st.write(dokumentname1)
        st.image(dokumentname1,width=1800)

    #Links auf andere Seite
    with st.expander("4: Seitenlinks auf yahoo,finviz usw."):
    
    
        st.write(Kuerzel,einzeltitelwahl,markt)
        st.subheader('Links auf andere Seiten')
        
        seeking="[Seeking Alpha] (https://seekingalpha.com/search/?q="+einzeltitelwahl+")"
        yahoo="[Yahoo] (https://de.finance.yahoo.com/quote/"+Kuerzel+"?p=)"
        stocktwits="[stocktwits](https://stocktwits.com/symbol/"+Kuerzel+")"
        finviz="[finviz](https://www.finviz.com/quote.ashx?t="+Kuerzel+")"
        marketscreener="[marketscreener](https://de.marketscreener.com/suchen/?lien=recherche&mots="+einzeltitelwahl+"&RewriteLast=zbat&noredirect=0&type_recherche=0)"
        coinlink="https://coinmarketcap.com/currencies/"+einzeltitelwahl
        st.write(coinlink)
        
        #st.write(seeking,":",yahoo,stocktwits,finviz,marketscreener)
        st.write(seeking)
        st.write(yahoo)
        st.write(stocktwits)
        st.write(finviz)
        st.write(marketscreener)
        st.write(coinlink)
    
    with st.expander("Unternehmensbeschreibung"):
        tickerData = yf.Ticker(Kuerzel) # Get ticker data
        try:
            # Ticker information
            string_logo = '<img src=%s>' % tickerData.info['logo_url']
            st.markdown(string_logo, unsafe_allow_html=True)

            string_name = tickerData.info['longName']
            st.header('**%s**' % string_name)

            string_summary = tickerData.info['longBusinessSummary']
            st.info(string_summary)
            st.info(tickerData.info)
        except:
            st.write('nicht vorhanden ' )

    
else:
    st.write('Falsches Passwort')









