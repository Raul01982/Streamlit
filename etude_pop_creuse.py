import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

link = "https://www.insee.fr/fr/statistiques/2011101?geo=DEP-23#chiffre-cle-1"
link_1 = "https://www.insee.fr/fr/statistiques/2407676#graphique-figure1_radio1"
pop_creuse = pd.read_html(link)
culturel_creuse = pd.read_html(link_1)


st.title('Etude de la population de Communauté de communes Creuse Sud-Ouest')

st.write("Cinéma Claude Miller")


def refaire_tx(df):
    df = df/10
    return df

# recuperer le tableau de la population de la creuse par CSP (2020) et le rendre exploitable

pop_creuse_csp = pop_creuse[7]
titre_1 = ['CSP_pop_creuse', '2009', '%_2009', '2014', '%_2014', '2020', '%_2020']
pop_creuse_csp.columns = titre_1
for x in pop_creuse_csp:
        if x == '%_2009' or x == '%_2014' or x == '%_2020':
                pop_creuse_csp[x] = pop_creuse_csp[x].apply(refaire_tx)

# recuperer le tableau de la population de la creuse par Age (2020) et le rendre exploitable

pop_creuse_age = pop_creuse[0]
titre_2 = ['Age_pop_creuse', '2009', '%_2009', '2014', '%_2014', '2020', '%_2020']
pop_creuse_age.columns = titre_2
for x in pop_creuse_age:
        if x == '%_2009' or x == '%_2014' or x == '%_2020':
                pop_creuse_age[x] = pop_creuse_age[x].apply(refaire_tx)

# recuperer le tableau fracantation cinemas par CSP (2022) et le rendre exploitable

culturel_creuse_csp = culturel_creuse[0]
for x in culturel_creuse_csp:
        if x == 'Catégorie socioprofessionnelle':
                pass
        else:
                culturel_creuse_csp[x] = culturel_creuse_csp[x].apply(refaire_tx)   

# recuperer le tableau fracantation cinemas par Age (2022) et le rendre exploitable

culturel_creuse_age = culturel_creuse[1]
titre = []
for x in culturel_creuse_age:
        x = x[1]
        titre.append(x)
print(titre)
print(type(titre))

culturel_creuse_age.columns = titre
culturel_creuse_age = culturel_creuse_age.drop(columns='Unnamed: 5_level_1').drop(columns='Unnamed: 6_level_1')
for x in culturel_creuse_age:
        if x == 'Âge et sexe':
                pass
        else:
                culturel_creuse_age[x] = culturel_creuse_age[x].apply(refaire_tx)
culturel_creuse_age['Âge et sexe'][16] = 'Tout ages'
titre_4 = ['Age', 'Genre', 'Aucune fois', 'De 1 à 3 fois', 'Plus de 3 fois', 'Ne sait pas / Refus']
culturel_creuse_age['Age'] = culturel_creuse_age['Âge et sexe']

col = culturel_creuse_age.pop("Age")
culturel_creuse_age.insert(loc=0, column="Age", value=col)

culturel_creuse_age.columns = titre_4
culturel_creuse_age['Age'] = culturel_creuse_age['Age'].replace('Femmes', 'X').replace('Hommes', 'X').replace('Ensemble', 'X')
culturel_creuse_age['Genre'] = culturel_creuse_age['Genre'].replace('16-24 ans', 'X').replace('25-39 ans', 'X').replace('40-59 ans', 'X').replace('60 ans ou plus', 'X').replace('Tout ages', 'X')

for x in range(0,20):
    if culturel_creuse_age['Age'][x] == 'X':
        culturel_creuse_age['Age'][x] = culturel_creuse_age['Age'][x-1]

liste = []
for x in range(0,20):
        if culturel_creuse_age['Genre'][x] == 'X':
            liste.append(x)
print(liste)

culturel_creuse_age = culturel_creuse_age.drop(culturel_creuse_age.index[liste], axis=0)          

st.write('La commune de Bourganeuf est située à 33 km de Guéret, à 50 km de Limoges et compte 2450 hab.')
st.write('la Communauté de communes Creuse Sud-Ouest dont elle fait partie compte 13500 hab.')

pop_creuse_age_CCCSO = pop_creuse_age[['Age_pop_creuse','%_2020']]
pop_creuse_age_CCCSO['pop_CCCSO'] = round((pop_creuse_age['%_2020']*13500)/100,0)

pop_creuse_csp_CCCSO = pop_creuse_csp[['CSP_pop_creuse','%_2020']]
pop_creuse_csp_CCCSO['pop_CCCSO'] = round((pop_creuse_csp['%_2020']*13500)/100,0)

# croisment tableau population CCCSO et cinemas par CSP :

culturel_creuse_csp = culturel_creuse_csp.replace('Autres inactifs','Autres personnes sans activité professionnelle')
culturel_creuse_csp = culturel_creuse_csp.replace('Ouvriers (y compris ouvriers agricoles)','Ouvriers')

fusion_cinema_CSP_CCCSO = pd.merge(pop_creuse_csp_CCCSO, culturel_creuse_csp, how='inner', left_on='CSP_pop_creuse',
         right_on='Catégorie socioprofessionnelle')
fusion_cinema_CSP_CCCSO = fusion_cinema_CSP_CCCSO.drop('Catégorie socioprofessionnelle',axis=1).drop('Aucune fois',axis=1).drop('Ne sait pas / Refus',axis=1)
fusion_cinema_CSP_CCCSO['CCCSO_1_à_3_fois'] = round((fusion_cinema_CSP_CCCSO['pop_CCCSO']*fusion_cinema_CSP_CCCSO['De 1 à 3 fois'])/100,0)
fusion_cinema_CSP_CCCSO['CCCSO_Plus_de_3_fois'] = round((fusion_cinema_CSP_CCCSO['pop_CCCSO']*fusion_cinema_CSP_CCCSO['Plus de 3 fois'])/100,0)
fusion_cinema_CSP_CCCSO = fusion_cinema_CSP_CCCSO [['CSP_pop_creuse', '%_2020', 'pop_CCCSO', 'De 1 à 3 fois', 'CCCSO_1_à_3_fois', 'Plus de 3 fois', 'CCCSO_Plus_de_3_fois']]
fusion_cinema_CSP_CCCSO['cinemas_total'] = fusion_cinema_CSP_CCCSO['CCCSO_1_à_3_fois'] + fusion_cinema_CSP_CCCSO['CCCSO_Plus_de_3_fois']

st.write("Sur les 13500 hab. de la communauté de communes en se basant sur les chiffres de l'INSEE on peut estimer que environ 3600 vont au cinemas de 1 à 3 fois par an et 1800 plus de 3 fois soit 5400 personnes")

df = fusion_cinema_CSP_CCCSO.drop([0],axis=0)

fig = px.pie(df, values='cinemas_total', names='CSP_pop_creuse',title='Répartition de la population qui va au cinemas', color='CSP_pop_creuse')

st.plotly_chart(fig, use_container_width=True)

fig_1 = px.bar(df, y=['CCCSO_1_à_3_fois','CCCSO_Plus_de_3_fois'], x='CSP_pop_creuse')

st.plotly_chart(fig_1, use_container_width=True)


