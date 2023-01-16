import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#Reading of the dataset
data = pd.read_csv("chirurgie.csv", encoding='latin-1')

#Modification to the dataset
data = data.replace(('RSS01','RSS02','RSS03','RSS04','RSS05','RSS06','RSS07','RSS08','RSS09','RSS10','RSS11','RSS12','RSS13','RSS14','RSS15','RSS16'),('Bas-Saint-Laurent','Saguenay - Lac-Saint-Jean','Capitale-Nationale','Mauricie et Centre-du-Québec','Estrie','Montréal','Outaouais','Abitibi-Témiscamingue','Côte-Nord','Nord-du-Québec','Gaspésie - Îles-de-la-Madeleine','Chaudière-Appalaches','Laval','Lanaudière','Laurentides','Montérégie'))
data = data.replace(('1920-P12', '1920-P13'),('2019/2020', '2019/2020'))
data = data.replace(('2021-P01','2021-P02','2021-P03','2021-P04','2021-P05','2021-P06','2021-P07','2021-P08','2021-P09','2021-P10','2021-P11','2021-P12','2021-P13'),('2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021','2020/2021',))
data = data.replace(('2122-P01','2122-P02','2122-P03','2122-P04','2122-P05','2122-P06','2122-P07','2122-P08','2122-P09','2122-P10','2122-P11','2122-P12','2122-P13'),('2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022','2021/2022',))
data = data.replace(('2223-P01','2223-P02','2223-P03','2223-P04','2223-P05','2223-P06','2223-P07','2223-P08'),('2022/2023', '2022/2023','2022/2023','2022/2023','2022/2023','2022/2023','2022/2023','2022/2023',))

#avoiding white spaces on both sides of the screen 
st.set_page_config(layout="wide")

#Title
st.title('Bio-Info Project: Waiting Times in Surgery in Québec Region\n')

#Variable creation
operation = ["Chirurgie_generale","Chirurgie_orthopedique","Chirurgie_plastique","Chirurgie_vasculaire","Neurochirurgie","Obstetrique_et_gynecologie","Ophtalmologie","ORL_chirurgie_cervico-faciale","Urologie","Autres"]
region = data["Region"].unique()
periode_att = data["PeriodeAttente"].unique()
delais = data["Delais_d'attente"].unique()

#Presentation of the dataset

st.header('Presentation of the dataset\n')
'''
The file presents a portrait of the list of interventions pending in the operating room in Quebec by period, region, waiting time and specialty, with a history since February 2, 2020.
'''
st.subheader('Source :\n')

'''
SIMASS is a data warehouse in which is registered a list of all the interventions pending and carried out in Quebec.
Data entry is done in real time by the personnel assigned to these functions in each of the establishments in Québec. A monthly update of the data set is made from this data.'''


#Display the Data set
url = "https://www.donneesquebec.ca/recherche/dataset/chirurgies-portrait-de-la-liste-d-attente"
st.subheader("The dataset from this [link](%s): " %url)
st.write("")
st.write(data)
st.write("")

#Display Key Data

st.header('Key KPIs : \n')

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    label="Number of Region",
    value= len(region),
)

kpi2.metric(
    label="Number of Operation",
    value= int(data['Total'].sum()),
)

column = ["Delais_d'attente","Total"]
data_temp = data[column].groupby("Delais_d'attente", as_index=False).sum()
max = data_temp["Total"].idxmax()

kpi3.metric(
    label="Average waiting times",
    value = data_temp["Delais_d'attente"][0],
)

kpi4.metric(
    label="Number of type of Operation",
    value = len(operation),
)

#Pie Chart of repartition of the waiting times

st.header('Repartition of the waiting times :\n')

column = ["Delais_d'attente","Total"]
data_temp = data[column].groupby("Delais_d'attente", as_index=False).sum()

delais_selected = st.selectbox("Délais d'attente", delais)

explode = [0,0,0]

for i in range (len(delais)):
    if delais[i] == delais_selected:
        explode[i] =0.3

fig1 = px.pie(data_temp, values = "Total", names = "Delais_d'attente" ,height=600, width=200)
fig1.update_layout(margin=dict(l=20, r=20, t=60, b=0))
fig1.update_traces(pull=explode)
st.plotly_chart(fig1, use_container_width=True, explode = explode)

#Pie Chart of repartition of the operations

st.header('Repartition of the operations :\n')

operation_selected = st.selectbox("Type d'opération", operation)

explode = [0,0,0,0,0,0,0,0,0,0]

for i in range (len(operation)):
    if operation[i] == operation_selected:
        explode[i] =0.3


fig1 = px.pie(data, values = data[operation].sum(), names = operation ,height=700, width=200)
fig1.update_layout(margin=dict(l=20, r=20, t=60, b=0))
fig1.update_traces(pull=explode)
st.plotly_chart(fig1, use_container_width=True, explode = explode)

#Repartition of the number of Operation according to the year

st.header('Number of Operation according to the year in ascending order :')

column = ['PeriodeAttente', "Delais_d'attente", 'Total']
data_temp = data[column].groupby(['PeriodeAttente', "Delais_d'attente"], as_index=False).sum()

fig3 = px.bar(data_temp, x='PeriodeAttente', y='Total', color="Delais_d'attente", height= 600, width=1300)
fig3.update_layout(xaxis={'categoryorder': 'total ascending'})
barplot_chart = st.write(fig3)

#2019/2020
column = ['PeriodeAttente', "Delais_d'attente", 'Total']
data_temp = data[column]

data_mask1=data_temp['PeriodeAttente']=='2019/2020'
filtered_df1 = data_temp[data_mask1]

fig4 = px.pie(filtered_df1, values = 'Total', names = "Delais_d'attente" ,height=300, width=200, title = '2019/2020')
fig4.update_layout(margin=dict(l=20, r=20, t=60, b=0))

#2020/2021
data_mask2=data_temp['PeriodeAttente']=='2020/2021'
filtered_df2 = data_temp[data_mask2]

fig5 = px.pie(filtered_df2, values = 'Total', names = "Delais_d'attente" ,height=300, width=200, title = '2020/2021')
fig5.update_layout(margin=dict(l=20, r=20, t=60, b=0))

#2021/2022
data_mask3=data_temp['PeriodeAttente']=='2021/2022'
filtered_df3 = data_temp[data_mask3]

fig6 = px.pie(filtered_df3, values = 'Total', names = "Delais_d'attente" ,height=300, width=200, title = '2021/2022')
fig6.update_layout(margin=dict(l=20, r=20, t=60, b=0))

#2022/2023

data_mask4=data_temp['PeriodeAttente']=='2022/2023'
filtered_df4 = data_temp[data_mask4]

fig7 = px.pie(filtered_df4, values = 'Total', names = "Delais_d'attente" ,height=300, width=200, title = '2022/2023')
fig7.update_layout(margin=dict(l=20, r=20, t=60, b=0))

cc1, cc2 = st.columns([1,1])

with cc1:
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)

with cc2:
    st.plotly_chart(fig6, use_container_width=True)
    st.plotly_chart(fig7, use_container_width=True)

#Number of Operation and their waiting times by region in ascending order

st.header('Number of Operation and their waiting times by region in ascending order :\n')

column1 = ["Region", "Total", "Delais_d'attente"]
data_cat = data[column1].groupby(["Region","Delais_d'attente"], as_index=False).sum()




fig2 = px.bar(data_cat, x='Region', y='Total', color="Delais_d'attente", height= 600, width=1300)
fig2.update_layout(xaxis={'categoryorder': 'total ascending'})
barplot_chart = st.write(fig2)

#Limits of the dataset

st.subheader("Limits of the dataset :\n")

'''
The dataset has some limitations that did not allow a more precise study:

The first is the labeling of time. The 'WaitingPeriod' argument does not allow a precise study of the periods of the year. In fact, in the original dataset, the years are broken down into financial periods, i.e. 13 periods.

The second limit is the waiting time. It is broken down into just 3 time periods: 0 to 6 months, 6 to 12 months and over a year. This does not allow a very precise study of waiting times for medical interventions'''