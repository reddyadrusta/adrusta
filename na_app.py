import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Pulse BP AI", layout="wide")

# ----------- CUSTOM CSS -----------
st.markdown("""
<style>

body{
background: linear-gradient(120deg,#667eea,#764ba2);
}

.title{
text-align:center;
font-size:48px;
color:white;
font-weight:bold;
}

.subtitle{
text-align:center;
color:white;
font-size:20px;
margin-bottom:20px;
}

.card{
background:white;
padding:25px;
border-radius:15px;
box-shadow:0 6px 15px rgba(0,0,0,0.2);
}

.stButton>button{
background:linear-gradient(45deg,#ff416c,#ff4b2b);
color:white;
border-radius:10px;
height:3em;
width:150px;
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# Login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------- TITLE -----------
st.markdown('<p class="title">Predictive Pulse Blood Pressure Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Based Healthcare Monitoring System</p>', unsafe_allow_html=True)

# ----------- HOME PAGE LAYOUT -----------
col1, col2 = st.columns([2,1])

# Welcome section
with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("Welcome")

    st.write("""
    This AI system helps predict **blood pressure risk**
    using pulse rate and health parameters.

    Features:
    - Pulse Monitoring
    - BMI Calculation
    - Blood Pressure Risk Prediction
    - Health Dashboard
    """)

    # Images
    st.image("https://images.unsplash.com/photo-1584516150909-c43483ee7932")
    st.image("https://images.unsplash.com/photo-1579684385127-1ef15d508118")

    st.markdown('</div>', unsafe_allow_html=True)

# Login section
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("Login")

    name = st.text_input("Name")
    age = st.number_input("Age",1,100)
    email = st.text_input("Email")

    if st.button("Login"):

        if name != "" and email != "":
            st.session_state.logged_in = True
            st.success(f"Welcome {name}")
        else:
            st.error("Please enter details")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------- AFTER LOGIN -----------
if st.session_state.logged_in:

    st.header("Health Prediction")

    age = st.number_input("Patient Age",1,100)
    pulse = st.number_input("Pulse Rate",40,150)
    weight = st.number_input("Weight (kg)",30,150)
    height = st.number_input("Height (cm)",100,220)

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

    # BMI
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("BMI", round(bmi,2))

    if st.button("Predict BP Risk"):

        prediction = model.predict([[age,pulse,weight,height]])

        if prediction[0] == 1:
            st.error("High Blood Pressure Risk")
        else:
            st.success("Normal Blood Pressure")

    # Graph
    st.subheader("Pulse Analysis")

    fig, ax = plt.subplots()
    ax.plot(df["age"], df["pulse"], marker="o")
    ax.set_xlabel("Age")
    ax.set_ylabel("Pulse")
    ax.set_title("Pulse vs Age")

    st.pyplot(fig)
    