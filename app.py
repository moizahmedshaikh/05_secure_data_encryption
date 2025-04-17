from random import choice
import streamlit as st
from utils import *


st.set_page_config(page_title="Secure Encryption App", layout="centered", initial_sidebar_state="collapsed")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0


if not st.session_state.logged_in:
    st.title("🔐 Secure Data Encryption System")
    auth_mode = st.radio("Choose Option", ["🔓 Login", "📝 Signup"], horizontal=True)

    if auth_mode == "📝 Signup":
        st.subheader("📝 Create an Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        if st.button("Signup"):
            if new_user and new_pass:
                users = load_users()
                if new_user in users:
                    st.warning("⚠️ Username already exists.")
                else:
                    users[new_user] = hash_password(new_pass)
                    save_users(users)
                    st.success("✅ Account created! Please login.")
            else:
                st.warning("⚠️ Fill all fields.")

    else:
        st.subheader("🔓 Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            users = load_users()
            if user in users and users[user] == hash_password(pwd):
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.session_state.failed_attempts = 0
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")



if st.session_state.logged_in :
    st.sidebar.markdown("---")
    st.sidebar.success(f"Logged in as: {st.session_state.current_user}")
    st.sidebar.markdown("## 🧰 Tools")
    app_menu = st.sidebar.radio("Select Option", ["🏠 Dashboard", "📥 Store Data", "🔐 Retrieve Data", "🚪 Logout"])

    all_data = load_data()
    username = st.session_state.current_user
    if username not in all_data:
        all_data[username] = []
    
    user_data = all_data[username]

    if app_menu == "🏠 Dashboard":
        st.markdown("## 👋 Welcome to the Secure Data Encryption System!")
        st.markdown(f"#### 🧑 Logged in as: **`{username}`**")

        st.markdown("---")
        
        st.markdown("### 🔐 What you can do here:")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📥 Store Data")
            st.markdown("Encrypt sensitive data and store it securely using your own passkey.")

        with col2:
            st.markdown("#### 🔓 Retrieve Data")
            st.markdown("Decrypt and view your stored data anytime using your passkey.")

        st.markdown("---")
        
        st.info("Use the sidebar menu to navigate between tools.")
        st.success("🔒 Your data is encrypted using advanced cryptography and stored securely.")

    elif app_menu == "📥 Store Data":
        st.subheader("📥 Store Encrypted Data")
        user_input = st.text_area("Enter Data to Encrypt")
        passkey = st.text_input("Create a Passkey for Decryption", type="password")

        if st.button("Encrypt & Save"):
            if user_input and passkey:
                encrypted = encrypt(user_input)
                passkey_hash = hash_password(passkey)

                user_data.append({
                    "encrypted": encrypted,
                    "passkey": passkey_hash
                })

                save_data(all_data)
                st.success("✅ Data encrypted and saved securely!")
            else:
                st.warning("⚠️ Please enter both fields.")

    elif app_menu == "🔐 Retrieve Data":
        st.subheader("📥 Retrieve Your Encrypted Data")

        if not user_data:
            st.info("ℹ️ No data stored yet.")
        else:
            for idx, item in enumerate(user_data):
                st.markdown(f"##### 🔒 Encrypted #{idx + 1}")
                st.code(item['encrypted'], language="text")

                input_passkey = st.text_input(f"Enter Passkey for #{idx + 1}", type="password", key=f"pk_{idx}")

                if st.button(f"Decrypt #{idx + 1}", key=f"decrypt_{idx}"):
                    if hash_password(input_passkey) == item["passkey"]:
                        st.success(f"✅ Decrypted: {decrypt(item['encrypted'])}")
                        st.session_state.failed_attempts = 0
                    else:
                        st.session_state.failed_attempts += 1
                        remaining = 3 - st.session_state.failed_attempts
                        st.error(f"❌ Incorrect passkey. Attempts left: {remaining}")

                        if st.session_state.failed_attempts >= 3:
                            st.warning("🔒 Too many failed attempts. Please re-login.")
                            st.session_state.logged_in = False
                            st.session_state.current_user = ""
                            st.session_state.failed_attempts = 0
                            st.rerun()

    elif app_menu == "🚪 Logout":
        st.subheader("🚪 Logout")
        st.write("Are you sure you want to logout?")
        
        if st.button("✅ Yes, Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.success("🔒 You have been logged out.")
            st.rerun()
