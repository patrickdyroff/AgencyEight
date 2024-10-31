import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import requests
import re

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


if submitted:

	# Initialize connection to the DB
	conn = st.connection("supabase",type=SupabaseConnection)

	# Perform query
	rows = execute_query(conn.table("InfluencerOutreach").select("*"), ttl=0)

	# Print results
	for row in rows.data:
	       st.write(row)
