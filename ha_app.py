import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Predictive Pulse BP Analysis", layout="wide")

# Custom UI
st.markdown("""
<style>
.title{
text-align:center;
font-size:42px;
color:#1f4e79;
font-weight:bold;
}
.card{
background:#f7f9fc;
padding:25px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">Predictive Pulse Blood Pressure Analysis</p>', unsafe_allow_html=True)

# Sample dataset
data = {
"age":[25,30,45,50,35,60,55],
"pulse":[72,80,95,100,78,110,105],
"weight":[60,65,80,85,70,90,88],
"height":[165,170,168,172,169,160,158],
"bp":[0,0,1,1,0,1,1]
}

df = pd.DataFrame(data)

# Train ML model
X = df[["age","pulse","weight","height"]]
y = df["bp"]

model = LogisticRegression()
model.fit(X,y)

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Patient Health Input")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age",1,100)
    pulse = st.number_input("Pulse Rate",40,150)

with col2:
    weight = st.number_input("Weight (kg)",30,150)
    height = st.number_input("Height (cm)",100,220)

# BMI
if height > 0:
    bmi = weight / ((height/100)**2)
    st.metric("BMI", round(bmi,2))

    if bmi < 18.5:
        st.info("Underweight")
    elif bmi < 25:
        st.success("Normal Weight")
    elif bmi < 30:
        st.warning("Overweight")
    else:
        st.error("Obese")

# Heart rate status
st.subheader("Heart Rate Status")

if pulse < 60:
    st.warning("Low Heart Rate")
elif pulse <= 100:
    st.success("Normal Heart Rate")
else:
    st.error("High Heart Rate")

# Prediction
if st.button("Predict Blood Pressure Risk"):

    prediction = model.predict([[age,pulse,weight,height]])

    if prediction[0] == 1:
        st.error("High Blood Pressure Risk")
        st.write("Recommendation: Reduce salt intake, exercise regularly, monitor BP.")
    else:
        st.success("Normal Blood Pressure")
        st.write("Recommendation: Maintain healthy lifestyle.")

st.markdown('</div>', unsafe_allow_html=True)

# Dashboard Section
st.header("Health Data Dashboard")

col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots()
    ax.plot(df["age"], df["pulse"], marker="o")
    ax.set_title("Pulse vs Age")
    ax.set_xlabel("Age")
    ax.set_ylabel("Pulse")
    st.pyplot(fig)

with col4:
    fig2, ax2 = plt.subplots()
    ax2.bar(df["age"], df["weight"])
    ax2.set_title("Weight Distribution")
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Weight")
    st.pyplot(fig2)

# Upload dataset
st.header("Upload Patient Dataset")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Dataset Preview")
    st.dataframe(data)