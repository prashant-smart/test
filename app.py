from tkinter import Menu
from main import navigation
import pandas as pd
import streamlit as st





# def handle_login_and_logout(username):
#     welcome_text_block=st.sidebar.empty()
#     welcome_text_block.write(f'Welcome {username} 🤠 !')
#     logout_block=st.sidebar.empty()
#     logout_btn=logout_block.button("Logout")
#     if logout_btn:

#         # if user click logout btn then all text container will remove
#         localStorage.removeItem('email')
#         localStorage.removeItem('password')
#         localStorage.removeItem('username')
#         welcome_text_block.empty()
#         logout_block.empty()
#         authenticate()
#         return 
#     # if user only logged in then it redirected to homepage 
#     navigation()

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


menu=["Login","SignUp"]

choice_block=st.sidebar.empty()
choice= choice_block.selectbox("Menu",menu)


if choice =="SignUp":

	st.title("SignUp")
	new_user =st.text_input("User Name")
	new_password =st.text_input("Password",type='password')

	if st.button("SignUp"):
		create_usertable()
		add_userdata(new_user,make_hashes(new_password))
		st.success("You have succesfully created valid Account")
		st.info("Go to Login Menu to login")
		
if choice == 'Login':
	title_block=st.sidebar.empty()
	title_block.title("Login")
    
	username_block =st.sidebar.empty()
	password_block =st.sidebar.empty()


	username=username_block.text_input("User Name")
	password=password_block.text_input("Password",type='password')	
			
	checkbox_block =st.sidebar.empty()
	if checkbox_block.checkbox("Login"):
		create_usertable()
		result=login_user(username,make_hashes(password))
		if result:
			user_result=view_all_users()
			clean_db=pd.DataFrame(user_result,columns=['username','password'])

			title_block.empty()
			choice_block.empty()
			username_block.empty()
			password_block.empty()
			checkbox_block.empty()
			
			#st.dataframe(clean_db)
			st.success("logged in as {}".format(username)+" You can now access App")
			navigation()

		else:
			st.warning("Incorrect Username / Password")