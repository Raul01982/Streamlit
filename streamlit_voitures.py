import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



st.title('Evolution of cars over the years')

st.write(" by continent")


link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)

option = st.selectbox(
    'Choose continent',
    options = df_cars['continent'].unique(),
    index=None,
    )

st.write('You selected:', option)

option_1 = st.selectbox(
    'Selected measurement units',
    options = ('US measure','Metric measure')
    )

st.write('You selected:', option_1)

if option is None:
        df_cars = df_cars
else:
        df_cars = df_cars[df_cars['continent'].str.contains(option, na=False)]

# 4 graphiques pour monter l'evolution des pussances, du poids et consomation au court des années
st.write('Number of models : ', len(df_cars['year']))

if option_1 is 'US measure':

        fig, axes = plt.subplots(2, 2 ,figsize = (20,20))
        fig.suptitle("Evolution of cars over the years", size = 16)

        ax = sns.lineplot(data = df_cars,
                        x = "year",
                        y = "cylinders",
                        color= 'blue',
                        ax = axes[0,0])
        ax.set_title("Evolution of cylinders ")
        plt.ylabel("cylinders")
        plt.xlabel("year")

        ax = sns.scatterplot(data = df_cars,
                        x='year',
                        y='weightlbs',
                        hue = "hp",
                        ax = axes[0,1])
        ax.set_title("Evolution of weightlbs")
        #plt.legend(loc=1, title= "hp")
        plt.ylabel("weightlbs")
        plt.xlabel("year")

        ax = sns.boxplot(data = df_cars,
                    x='year',
                    y='cubicinches',
                    color = 'green',
                    ax = axes[1,0])
        ax.set_title("Evolution of cubicinches")
        plt.ylabel("cubicinches")
        plt.xlabel("year")

        ax = sns.lineplot(data = df_cars,
                    x='year',
                    y='mpg',
                    color='red',
                    ax = axes[1,1]
                    )

        ax.set_title("Evolution of mpg")
        plt.ylabel("mpg")
        plt.xlabel("year")

        st.pyplot(ax.figure)

if option_1 is 'Metric measure':
                
        # mpg = Miles par gallon 
        # convertion mpg en l/100km = 282.48 / mpg
        def convertion_mpg_l100km(mpg):
                l = 282.4809363/mpg
                return round(l,2)

        # cubicinches = pouces cubes
        # convertion pouces cubes en cm cubes cm3 = in3*16,387064
        def convertion_in3_cm3(in3):
                cm3 = in3*16.387064
                return round(cm3,0) 

        # hp Puissance d’un moteur en HorsePower
        # 1hp = 1.014ch
        def convertion_hp_ch(hp):
                ch = hp*1.014
                return round(ch,0)

        # weightlbs = poids du vehicule en livres (us) 1livres = 0.453592 kg
        def convertion_lb_kg(lb):
                kg = lb*0.453592
                return round(kg,0)

        # time-to-60 = temps pour atteindre 60 miles/h : 1 miles = 1.609344km
        def convertion_miles_km(miles):
                km = (miles/60)*1.609344
                return (km*100)
        
        df_cars_euro = df_cars
        df_cars_euro['l_100km'] = df_cars['mpg'].apply(convertion_mpg_l100km)
        df_cars_euro['cm3'] = df_cars['cubicinches'].apply(convertion_in3_cm3)
        df_cars_euro['ch'] = df_cars['hp'].apply(convertion_hp_ch)
        df_cars_euro['kg'] = df_cars['weightlbs'].apply(convertion_lb_kg)
        df_cars_euro['time-to-100km_h'] = df_cars['time-to-60'].apply(convertion_miles_km)
        df_cars_euro = df_cars_euro[['l_100km','cylinders','cm3','ch','kg','time-to-100km_h','year','continent']]
        
        fig, axes = plt.subplots(2, 2 ,figsize = (20,20))
        fig.suptitle("Evolution of cars over the years", size = 16)

        ax = sns.lineplot(data = df_cars_euro,
                        x = "year",
                        y = "cylinders",
                        color= 'blue',
                        ax = axes[0,0])
        ax.set_title("Evolution of cylinders ")
        plt.ylabel("cylinders")
        plt.xlabel("year")

        ax = sns.scatterplot(data = df_cars_euro,
                        x='year',
                        y='kg',
                        hue = "ch",
                        ax = axes[0,1])
        ax.set_title("Evolution of kg")
        #plt.legend(loc=1, title= "hp")
        plt.ylabel("kg")
        plt.xlabel("year")

        ax = sns.boxplot(data = df_cars_euro,
                    x='year',
                    y='cm3',
                    color = 'green',
                    ax = axes[1,0])
        ax.set_title("Evolution of cm3")
        plt.ylabel("cm3")
        plt.xlabel("year")

        ax = sns.lineplot(data = df_cars_euro,
                    x='year',
                    y='l_100km',
                    color='red',
                    ax = axes[1,1]
                    )

        ax.set_title("Evolution of l_100km")
        plt.ylabel("l_100km")
        plt.xlabel("year")

        st.pyplot(ax.figure)






