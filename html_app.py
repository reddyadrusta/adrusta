import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(page_title="Predictive Pulse AI", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

.stApp{
background: linear-gradient(120deg,#f5f7fa,#c3cfe2);
}

.title{
font-size:45px;
font-weight:bold;
text-align:center;
color:#0d47a1;
}

.card{
background:white;
padding:30px;
border-radius:15px;
box-shadow:0px 5px 15px rgba(0,0,0,0.2);
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

# ---------- SESSION ----------
if "login" not in st.session_state:
    st.session_state.login=False

if "report" not in st.session_state:
    st.session_state.report=None


# ---------- LOGIN PAGE ----------
if not st.session_state.login:

    st.markdown('<div class="title">❤️ Predictive Pulse AI</div>', unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966483.png", width=150)

    st.subheader("Login")

    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Gmail")

    if st.button("Login"):

        if name != "":
            st.session_state.login=True
            st.session_state.name=name
            st.session_state.email=email
            st.rerun()

        else:
            st.warning("Please enter name")


# ---------- MAIN APP ----------
else:

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Menu",
        ["Health Form","Dashboard","Download Report"]
    )

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

            # simple ML-like rule
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