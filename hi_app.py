import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Pulse BP Analysis", layout="wide")

# Session login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar menu
menu = ["Home","Login","Prediction","Dashboard","About"]
choice = st.sidebar.selectbox("Navigation", menu)

# Sample dataset
data = {
"age":[25,30,45,50,35,60,55],
"pulse":[72,80,95,100,78,110,105],
"weight":[60,65,80,85,70,90,88],
"height":[165,170,168,172,169,160,158],
"bp":[0,0,1,1,0,1,1]
}

df = pd.DataFrame(data)

X = df[["age","pulse","weight","height"]]
y = df["bp"]

model = LogisticRegression()
model.fit(X,y)

# HOME PAGE
if choice == "Home":

    st.title("Predictive Pulse Blood Pressure Analysis")

    st.write("""
    Welcome to the AI-based health prediction system.

    This system analyzes pulse rate and health parameters
    to predict possible blood pressure risk.
    """)

# LOGIN PAGE
elif choice == "Login":

    st.header("Patient Login")

    name = st.text_input("Enter Your Name")
    age_user = st.number_input("Enter Your Age",1,100)
    email = st.text_input("Email")

    if st.button("Login"):

        if name != "" and email != "":
            st.session_state.logged_in = True
            st.success("Login Successful")
        else:
            st.error("Please enter details")

# PREDICTION PAGE
elif choice == "Prediction":

    if not st.session_state.logged_in:
        st.warning("Please login first")
    else:

        st.header("Enter Health Details")

        age = st.number_input("Age",1,100)
        pulse = st.number_input("Pulse Rate",40,150)
        weight = st.number_input("Weight (kg)",30,150)
        height = st.number_input("Height (cm)",100,220)

        if height > 0:
            bmi = weight / ((height/100)**2)
            st.write("BMI:", round(bmi,2))

        if st.button("Predict Blood Pressure Risk"):

            prediction = model.predict([[age,pulse,weight,height]])

            if prediction[0] == 1:
                st.error("High Blood Pressure Risk")
            else:
                st.success("Normal Blood Pressure")

# DASHBOARD PAGE
elif choice == "Dashboard":

    st.header("Health Data Dashboard")

    fig, ax = plt.subplots()
    ax.plot(df["age"], df["pulse"], marker="o")
    ax.set_xlabel("Age")
    ax.set_ylabel("Pulse")
    ax.set_title("Pulse vs Age")

    st.pyplot(fig)

# ABOUT PAGE
elif choice == "About":

    st.header("About Project")

    st.write("""
    Hackathon Project: Predictive Pulse Blood Pressure Analysis

    Technologies Used:
    - Python
    - Streamlit
    - Machine Learning
    """)