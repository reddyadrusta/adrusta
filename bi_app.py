import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Pulse BP AI", layout="wide")

# Custom CSS for colorful UI
st.markdown("""
<style>

body{
background: linear-gradient(120deg,#89f7fe,#66a6ff);
}

.title{
text-align:center;
font-size:50px;
font-weight:bold;
color:white;
}

.card{
background:white;
padding:25px;
border-radius:15px;
box-shadow:0 8px 20px rgba(0,0,0,0.2);
margin-bottom:20px;
}

.stButton>button{
background:linear-gradient(45deg,#ff4b2b,#ff416c);
color:white;
border-radius:10px;
height:3em;
width:200px;
font-size:18px;
}

.sidebar .sidebar-content{
background:linear-gradient(#4facfe,#00f2fe);
}

</style>
""", unsafe_allow_html=True)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar menu
menu = ["Home","Login","Prediction","Dashboard","About"]
choice = st.sidebar.selectbox("Navigation", menu)

# Dataset
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

    st.markdown('<p class="title">Predictive Pulse Blood Pressure Analysis</p>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("""
    ### AI Based Healthcare Monitoring System
    
    This system analyzes:
    - Pulse Rate
    - Body Mass Index
    - Health Parameters
    
    and predicts **blood pressure risk using Machine Learning**.
    """)

    st.image("https://images.unsplash.com/photo-1584516150909-c43483ee7932")

    st.markdown('</div>', unsafe_allow_html=True)

# LOGIN PAGE
elif choice == "Login":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("Patient Login")

    name = st.text_input("Name")
    age_user = st.number_input("Age",1,100)
    email = st.text_input("Email")

    if st.button("Login"):

        if name != "" and email != "":
            st.session_state.logged_in = True
            st.success("Login Successful")
        else:
            st.error("Enter valid details")

    st.markdown('</div>', unsafe_allow_html=True)

# PREDICTION PAGE
elif choice == "Prediction":

    if not st.session_state.logged_in:
        st.warning("Please login first")

    else:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("Enter Health Details")

        age = st.number_input("Age",1,100)
        pulse = st.number_input("Pulse Rate",40,150)
        weight = st.number_input("Weight (kg)",30,150)
        height = st.number_input("Height (cm)",100,220)

        if height > 0:
            bmi = weight / ((height/100)**2)
            st.metric("BMI", round(bmi,2))

        if st.button("Predict Blood Pressure Risk"):

            prediction = model.predict([[age,pulse,weight,height]])

            if prediction[0] == 1:
                st.error("⚠ High Blood Pressure Risk")
            else:
                st.success("✅ Normal Blood Pressure")

        st.markdown('</div>', unsafe_allow_html=True)

# DASHBOARD
elif choice == "Dashboard":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("Health Dashboard")

    fig, ax = plt.subplots()
    ax.plot(df["age"], df["pulse"], marker="o")
    ax.set_title("Pulse vs Age")
    ax.set_xlabel("Age")
    ax.set_ylabel("Pulse")

    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ABOUT
elif choice == "About":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("About Project")

    st.write("""
    Hackathon Project
    
    **Predictive Pulse Blood Pressure Analysis**
    
    Technologies Used:
    - Python
    - Streamlit
    - Machine Learning
    - Data Visualization
    """)

    st.markdown('</div>', unsafe_allow_html=True)