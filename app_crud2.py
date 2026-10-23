import sqlite3
import streamlit as st

# 1. Database Connection
conn = sqlite3.connect("school_crud.db", check_same_thread=False)
cursor = conn.cursor()

# Table banavne
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT
    )
""")
conn.commit()

st.title("🎓 Advanced Student Management App")

# --- LOGIN SESSION STATE SETUP ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False

# Jar user login nsel zala, tar login page dakhavne
if not st.session_state.logged_in:
  st.subheader("🔐 Login Kara")
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")
  if st.button("Login"):
    # Ithe tumhi tumcha username ani password set karu shakta
    if username == "Admin" and password == "Akash@1234":
      st.session_state.logged_in = True
      st.success("Login Successful! 🎉")
      st.rerun()
    else:
      st.error("❌ Wrong Username Or password!")
else:
  # --- LOGIN ZALYANANTAR CHA MAIN APP ---
  # Sidebar madhe Logout button
  if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
  # Sidebar Menu (Pages switch karnyasathi)
  menu = st.sidebar.selectbox(
      "Navigation", ["Add New Student", "See All Students & Delete Student"]
  )
  if menu == "Add New Student":
    st.subheader("➕ Add New Student")
    with st.form("add_form"):
      name = st.text_input("Student Name:")
      age = st.number_input("Age:", min_value=1, max_value=100, value=20)
      city = st.text_input("City:")
      submit = st.form_submit_button("Save Into The Database")
      if submit:
        if name and city:
          cursor.execute(
              "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
              (name, age, city),
          )
          conn.commit()
          st.success(f"✅ {name} Saved Successfully! 🎉")
        else:
          st.warning("⚠️ Please Filled All The Detailes!")
  elif menu == "See All Students & Delete Student":
    st.subheader("📋 All Students List & Delete Options")
    # Database madhun data fetch karne
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if rows:
      for row in rows:
        col1, col2 = st.columns([4, 1])
        with col1:
          st.write(
              f"🆔 **ID:** {row[0]} | 👤 **Naav:** {row[1]} | 🎂 **Vay:**"
              f" {row[2]} | 🏙️ **City:** {row[3]}"
          )
        with col2:
          if st.button("Delete", key=f"del_{row[0]}"):
            cursor.execute("DELETE FROM students WHERE id = ?", (row[0],))
            conn.commit()
            st.success(f"Student ID {row[0]} delete zala!")
            st.rerun()
    else:
      st.info("There is no Student in The Database.")