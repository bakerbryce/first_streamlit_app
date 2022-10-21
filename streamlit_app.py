import streamlit as sl
import pandas as pd
import requests
import snowflake.connector as sfc

sl.title('My Parents New Healthy Diner')

sl.header('Breakfast Menu')
sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kale, Spinach & Rocket Smoothie')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Get fruit list from S3
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Pick list of fruits
fruits_selected = sl.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the list
sl.dataframe(fruits_to_show)

# Get fruityvice data and display
sl.header('Fruityvice Fruit Advice!')
fruit_choice = sl.text_input('What fruit would you like info about?','Kiwi')
sl.write('The user entered ',fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
sl.dataframe(fruityvice_normalized)



my_cnx = sfc.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
sl.text("Hello from Snowflake:")
sl.text(my_data_row)
