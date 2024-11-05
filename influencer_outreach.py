import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import requests
import re
import pandas as pd
from instabot import Bot
import os

#Removing Config file created on last run
os.popen("rm -rf config")

# Setting page layout
st.set_page_config(layout='wide')

# Title
st.title("Agency Eight")

# Submit new influencer to database

with st.form("my_form"):

	st.write("Add new influencer")
	
	owner = st.text_input("Owner")

	influencer_IG_link = st.text_input("Influencer IG Link")

	influencer_TT_link = st.text_input("Influencer TikTok Link")

	submitted = st.form_submit_button("Submit to database")

## Instagram Handle Cleaner

try:
	influencer_IG_handle = influencer_IG_link.split('/')[3]
	st.write(influencer_IG_handle)

except:
	influencer_IG_handle = ""

## TikTok Handle Cleaner

try:
	influencer_TT_handle = influencer_TT_link.split('/')[3]
	if influencer_TT_handle.find('?') != -1:
		influencer_TT_handle = influencer_TT_handle.split('?')[0]
	st.write(influencer_TT_handle)

except:
	influencer_TT_handle = ""

# Adding the influencer to the new database
if submitted:

	#Instagram bot to get follower count
	bot = Bot()
	bot.login(username="agencyeight35@gmail.com", password="agencyeight2023", is_threaded=True)
	user_id = bot.get_user_id_from_username(influencer_IG_handle)
	user_info = bot.get_user_info(user_id)
	st.write(user_info)
	influencer_IG_follower_count = user_info["follower_count"]

	# Initialize connection to the DB
	conn = st.connection("supabase",type=SupabaseConnection)

	conn.table("InfluencerOutreach").insert(
	[{"owner_name": owner, "IG_link": influencer_IG_link, "TT_link": influencer_TT_link, "IG_handle": influencer_IG_handle, "TT_handle": influencer_TT_handle, "IG_follower_count": influencer_IG_follower_count}]
	).execute()

# Display database

if st.button("Show database", type="primary"):

	# Initialize connection to the DB
	conn = st.connection("supabase",type=SupabaseConnection)

	# Perform query
	rows = execute_query(conn.table("InfluencerOutreach").select("*"), ttl=0)
	df = pd.DataFrame(rows.data)
	st.dataframe(df, use_container_width=True)

#Reach out to influencer section
st.header("Reach out to influencer")


