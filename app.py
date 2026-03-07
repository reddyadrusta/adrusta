import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression

st.title("Predictive Pulse Blood Pressure Analysis")

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

st.header("Enter Patient Details")

age = st.number_input("Age",1,100)
pulse = st.number_input("Pulse Rate",40,150)
weight = st.number_input("Weight (kg)",30,150)
height = st.number_input("Height (cm)",100,220)

if st.button("Predict"):

    prediction = model.predict([[age,pulse,weight,height]])

    if prediction[0] == 1:
        st.error("High Blood Pressure Risk")
    else:
        st.success("Normal Blood Pressure")