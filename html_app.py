import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from io import BytesIO
import os

st.set_page_config(page_title="Predictive Pulse AI", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

.stApp{
background: linear-gradient(120deg,#f5f7fa,#c3cfe2);
}

.title{
font-size:50px;
font-weight:bold;
text-align:center;
}

label{
color:black !important;
font-weight:bold !important;
}

.stButton>button{
background:#1976d2;
color:white;
font-weight:bold;
border-radius:8px;
padding:10px 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- CREATE USER DATABASE ----------
if not os.path.exists("users.csv"):
    df = pd.DataFrame(columns=["name","email"])
    df.to_csv("users.csv",index=False)

# ---------- SESSION ----------
if "login" not in st.session_state:
    st.session_state.login=False

# ---------- MENU ----------
menu = ["Login","Register"]
choice = st.sidebar.selectbox("Menu",menu)

# ---------- REGISTER ----------
if choice == "Register":

    st.markdown("""
    <div class="title">
    ❤️ <span style="color:blue">Predictive</span>
    <span style="color:red">Pulse</span>
    <span style="color:green">AI</span>
    </div>
    """,unsafe_allow_html=True)

    st.subheader("Register")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Gmail")

    if st.button("Register"):

        users = pd.read_csv("users.csv")

        if email in users["email"].values:
            st.warning("User already registered")

        else:
            new_user = pd.DataFrame([[name,email]],columns=["name","email"])
            users = pd.concat([users,new_user],ignore_index=True)
            users.to_csv("users.csv",index=False)

            st.success("Registration successful. Please login.")

# ---------- LOGIN ----------
if choice == "Login":

    st.markdown("""
    <div class="title">
    ❤️ <span style="color:blue">Predictive</span>
    <span style="color:red">Pulse</span>
    <span style="color:green">AI</span>
    </div>
    """,unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966483.png",width=150)

    st.subheader("Login")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Gmail")

    if st.button("Login"):

        users = pd.read_csv("users.csv")

        if ((users["name"] == name) & (users["email"] == email)).any():

            st.session_state.login=True
            st.session_state.name=name
            st.session_state.email=email
            st.success("Login successful")

        else:
            st.error("User not registered. Please register first.")

# ---------- MAIN APP ----------
if st.session_state.login:

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Menu",
        ["Health Form","Dashboard","Download Report"]
    )

    if "report" not in st.session_state:
        st.session_state.report=None

    # ---------- HEALTH FORM ----------
    if page == "Health Form":

        st.title("Enter Health Information")

        age = st.number_input("Age",1,120)
        systolic = st.number_input("Systolic Blood Pressure")
        diastolic = st.number_input("Diastolic Blood Pressure")
        weight = st.number_input("Weight (kg)")
        height = st.number_input("Height (cm)")
        sugar = st.number_input("Blood Sugar")

        if st.button("Generate Health Report"):

            bmi = weight / ((height/100)**2)

            risk = "Normal"

            if systolic > 140 or diastolic > 90:
                risk = "Hypertension Risk"

            st.session_state.report = {
                "age":age,
                "systolic":systolic,
                "diastolic":diastolic,
                "bmi":round(bmi,2),
                "sugar":sugar,
                "risk":risk
            }

            if risk == "Hypertension Risk":

                st.error("⚠ High Blood Pressure Risk")

                st.write("### Recommendations")

                st.write("""
• Reduce salt intake  
• Exercise regularly  
• Maintain healthy weight  
• Monitor blood pressure  
• Reduce stress  
""")

            else:
                st.success("Blood Pressure Normal")

    # ---------- DASHBOARD ----------
    if page == "Dashboard":

        st.title("Health Dashboard")

        if st.session_state.report is None:

            st.warning("Please fill Health Form first")

        else:

            r = st.session_state.report

            labels = ["Systolic","Diastolic","BMI","Sugar"]
            values = [
                r["systolic"],
                r["diastolic"],
                r["bmi"],
                r["sugar"]
            ]

            fig = plt.figure()

            plt.bar(labels,values)

            plt.title("Health Metrics")

            st.pyplot(fig)

            st.write("### Health Summary")

            st.write(r)

    # ---------- DOWNLOAD REPORT ----------
    if page == "Download Report":

        st.title("Download Health Report")

        if st.session_state.report is None:

            st.warning("No report generated yet")

        else:

            r = st.session_state.report

            buffer = BytesIO()

            c = canvas.Canvas(buffer)

            c.drawString(100,800,"Predictive Pulse Health Report")

            c.drawString(100,760,f"Name: {st.session_state.name}")
            c.drawString(100,740,f"Email: {st.session_state.email}")

            c.drawString(100,700,f"Age: {r['age']}")
            c.drawString(100,680,f"Systolic BP: {r['systolic']}")
            c.drawString(100,660,f"Diastolic BP: {r['diastolic']}")
            c.drawString(100,640,f"BMI: {r['bmi']}")
            c.drawString(100,620,f"Sugar: {r['sugar']}")

            c.drawString(100,580,f"Risk: {r['risk']}")

            c.save()

            buffer.seek(0)

            st.download_button(
                "Download PDF Report",
                buffer,
                "health_report.pdf",
                "application/pdf"
            )