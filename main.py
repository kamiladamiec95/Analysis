import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def analysis_app():

    pd.options.display.float_format = '{:20,.2f}'.format

    # Loading and preparing data
    customers_orders = pd.read_csv('customer_orders.csv')
    orders = pd.read_csv('orders.csv')
    sports = pd.read_csv('sports.csv')
    orders_date = pd.read_csv('orders_date.csv')
    sports = sports.drop('Unnamed: 0', axis=1)
    sports = sports.drop_duplicates()
    sports['sport'] = np.select(
         [
              sports['sport'] == 'p3ywanie',
              sports['sport'].isin(['myslistwo', 'myolistwo']),
              sports['sport'] == '3ucznictwo',
              sports['sport'] == 'jeYdziectwo'
         ],
         [
              'pływanie',
              'myślistwo',
              'łucznictwo',
              'jeżdziectwo'
         ],
         default=sports['sport']
    )

    sports_clients = sports.groupby(['customer_id']).count()
    sports_clients = sports_clients.reset_index()
    sports_clients_q1 = sports_clients[(sports_clients['sport']) == 1].count()
    sports_clients_q2 = sports_clients[(sports_clients['sport']) == 2].count()
    sports_clients_q3 = sports_clients[(sports_clients['sport']) > 2].count()

    sports = sports.groupby(['sport']).count()
    sports = sports.reset_index()
    sports = sports.rename({'customer_id': 'Ilość klientów'}, axis='columns')
    sports = sports.sort_values(by=['Ilość klientów'], ascending=False)
    avg_sports_customer = round(sports['Ilość klientów'].mean())

    orders_date = orders_date.drop(['Id', 'order_id'], axis=1)
    orders_date = orders_date.groupby(['date']).sum('value')
    orders_date = orders_date.sort_values(by=['date'])
    orders_date = orders_date.reset_index()

    header = st.container()

    # Function to display numbers at pie chart
    def display_numbers(values):
        def numbers(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}'.format(v=val)
        return numbers

    # sports_clients = {'""': [],
    #                   '"customer_id"': [],
    #                   '"sport:': []
    #                   }
    #
    # sports_clients = pd.DataFrame(sports_clients)
    #
    # files = os.listdir()
    # sports_clients_list = []
    # for file in files:
    #     if 'sports' in file:
    #         sports_clients_list.append(file)
    #
    # for file in sports_clients_list:
    #     sports = pd.read_csv(f'{}file')
    #     sports_clients = pd.concat([sports_clients, s_c])

    with header:
        # Header text
        st.markdown("<h1 style='text-align: center; color: black;'>Raporty</h1>", unsafe_allow_html=True)
        st.text("")
        st.text("")

        # Sports per client bar chart
        ax = sports.plot(kind="barh")
        plt.subplots_adjust(bottom=0.19, left=0.19)
        fig, ax = plt.subplots()
        ax.barh(sports['sport'], sports['Ilość klientów'])
        fig.set_size_inches(20, 8)

        for container in ax.containers:
            ax.bar_label(container)

        plt.axvline(avg_sports_customer, color='red', linestyle='dashed', linewidth=2, label=f'średnia ({avg_sports_customer})')
        plt.legend(loc='upper right')
        plt.title("Sporty uprawiane przez klientów", fontsize=20)

        st.pyplot(fig)

        st.text("")
        st.text("")

        # Total orders value per year chart
        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(orders_date['date'], errors='coerce').dt.year, orders_date['value'])
        plt.grid()
        plt.title("Łączna roczna wartość zamówień (mld pln)")
        st.pyplot(fig)

        # Total orders value per year table
        orders_date['date'] = orders_date['date'].str[:4]
        orders_date['value'] = orders_date['value'].round()
        st.table(orders_date.rename({'date': 'Rok', 'value': 'Wartość zamówień'}, axis='columns'))

        st.text("")
        st.text("")
        st.text("")
        st.text("")

        # Clients practising one, two, more than two sports pie chart
        labels = ['Klienci uprawiający 1 sport', 'Klienci uprawiający 2 sporty', 'Klienci uprawiający więcej niż 2 sporty']
        fig, ax = plt.subplots()
        ax.pie([sports_clients_q1['sport'], sports_clients_q2['sport'], sports_clients_q3['sport']], labels=labels,\
               autopct=display_numbers([sports_clients_q1['sport'], sports_clients_q2['sport'], sports_clients_q3['sport']]))
        plt.title("Ilość klientów uprawiających jeden, dwa lub więcej niż dwa sporty")

        st.pyplot(fig)


if __name__ == "__main__":
    analysis_app()
