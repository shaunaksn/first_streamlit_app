import streamlit
import pandas
import snowflake.connector

streamlit.title('My Parents new healthy diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Selects fruit name as index
my_fruit_list = my_fruit_list.set_index('Fruit')

#List created to pick fruits
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)




#New Section to show Fruityvice response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?' , 'Kiwi')
streamlit.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)


#Normalizing JSON
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

#Connecting to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit Load List Contains")
streamlit.dataframe(my_data_rows)

fruit_choice_2 = streamlit.text_input('What fruit would you like information about?' , 'Kiwi')
streamlit.write('Thanks for adding', fruit_choice_2)
