import streamlit as sl
import pandas as pd
import requests
import snowflake.connector as sfc
from urllib.error import URLError

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
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

sl.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = sl.text_input('What fruit would you like info about?')
   if not fruit_choice:
      sl.error("please select a fruit to get info.")
   else:
      sl.write('The user entered ',fruit_choice)
      back_from_function = get_fruityvice_data(fruit_choice)  
      sl.dataframe(back_from_function)

except:
   sl.error()


   
   
   
# Get data from Snowflake
# Snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fdc_food_ingest")
      return my_cur.fetchall()

# Add a button to load the table
if sl.button('Get table load list'):
   my_cnx = sfc.connect(**sl.secrets["snowflake"])
   my_data_rows = my_cur.fetchall()
   sl.header("All table rows are:")
   sl.dataframe(my_data_rows)

sl.stop()
# Allow insert into Snowflake
add_my_fruit = sl.text_input('What row would you like to add?')

sl.write('Thanks for adding a record: ',add_my_fruit)
my_cur.execute("insert into fdc_food_ingest values ('from streamlit')")
