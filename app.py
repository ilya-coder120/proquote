import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import random

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="ProQuote AI",
    page_icon="🧾",
    layout="wide"
)

# ======================
# WARNING BANNER
# ======================
st.warning("""
⚠️ TESTSYSTEM

Diese Anwendung ist ein Test- und Demo-Tool.
Bitte keine echten personenbezogenen Daten oder sensiblen Informationen eingeben.

Alle Inhalte dienen nur zu Demonstrationszwecken.
""")

# ======================
# SESSION STATE
# ======================
if "angebote" not in st.session_state:
    st.session_state.angebote = []

# ======================
# HEADER / UI
# ======================
st.markdown("""
# 🧾 ProQuote AI

### Angebote in Sekunden erstellen – einfach, schnell, professionell
""")

colA, colB, colC = st.columns(3)

with colA:
    st.markdown("### ⚡ Schnell")
    st.write("Angebote in unter 1 Minute erstellen.")

with colB:
    st.markdown("### 🧠 Einfach")
    st.write("Kein kompliziertes Tool – direkt loslegen.")

with colC:
    st.markdown("### 📄 PDF Export")
    st.write("Sofort fertige Angebote als PDF downloaden.")

st.divider()

# ======================
# GEWERKE + PREISLOGIK
# ======================
gwerke = {
    "Maler": {
        "text": "Wände streichen, Abdeckung, Vorbereitung",
        "preis": (300, 1500)
    },
    "Elektriker": {
        "text": "Steckdosen, Leitungen, Installation",
        "preis": (500, 3000)
    },
    "Sanitär": {
        "text": "Rohrarbeiten, Badinstallation",
        "preis": (600, 3500)
    },
    "Gartenbau": {
        "text": "Rasen, Hecken, Außenarbeiten",
        "preis": (200, 2000)
    }
}

# ======================
# PDF GENERATOR
# ======================
def create_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "ProQuote AI Angebot")

    y -= 40
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Angebotsnr: {data['nr']}")

    y -= 20
    pdf.drawString(50, y, f"Datum: {data['datum']}")

    y -= 30
    pdf.drawString(50, y, f"Kunde: {data['kunde']}")

    y -= 20
    pdf.drawString(50, y, f"Adresse: {data['adresse']}")

    y -= 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Leistung:")

    y -= 20
    pdf.setFont("Helvetica", 11)

    for line in data["auftrag"].split("\n"):
        pdf.drawString(50, y, line[:90])
        y -= 20

    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Gesamtpreis: {data['preis']} €")

    pdf.save()
    buffer.seek(0)
    return buffer

# ======================
# LAYOUT
# ======================
col1, col2 = st.columns(2)

# ======================
# INPUT
# ======================
with col1:
    st.subheader("🧾 Neues Angebot")

    firma = st.text_input("Firma", "Meine Firma GmbH")
    kunde = st.text_input("Kunde")
    adresse = st.text_input("Adresse")

    gewerk = st.selectbox("Gewerk", list(gwerke.keys()))

    min_p, max_p = gwerke[gewerk]["preis"]

    use_slider = st.checkbox("Preisvorschlag nutzen")

    if use_slider:
        preis = st.slider(
            "Preis wählen",
            min_value=min_p,
            max_value=max_p,
            value=int((min_p + max_p) / 2)
        )
    else:
        preis = st.number_input(
            "Eigener Preis",
            min_value=0,
            value=min_p
        )

    auftrag = st.text_area(
        "Beschreibung",
        value=gwerke[gewerk]["text"],
        height=150
    )

    if st.button("🚀 Angebot erstellen"):

        angebot_nr = f"A-{random.randint(1000,9999)}"
        datum = datetime.now().strftime("%d.%m.%Y")

        neues_angebot = {
            "firma": firma,
            "kunde": kunde,
            "adresse": adresse,
            "auftrag": auftrag,
            "nr": angebot_nr,
            "datum": datum,
            "preis": preis
        }

        st.session_state.angebote.append(neues_angebot)
        st.session_state["data"] = neues_angebot

# ======================
# OUTPUT
# ======================
with col2:
    st.subheader("📄 Vorschau")

    if "data" in st.session_state:

        d = st.session_state["data"]

        st.success("Angebot erstellt!")

        st.write(f"🏢 Firma: {d['firma']}")
        st.write(f"👤 Kunde: {d['kunde']}")
        st.write(f"🛠️ Auftrag: {d['auftrag']}")
        st.write(f"💰 Preis: {d['preis']} €")

        pdf = create_pdf(d)

        st.download_button(
            "📥 PDF herunterladen",
            data=pdf,
            file_name=f"angebot_{d['nr']}.pdf",
            mime="application/pdf"
        )

    else:
        st.info("Noch kein Angebot erstellt")

# ======================
# HISTORY
# ======================
st.divider()
st.subheader("📚 Angebots-Historie")

if len(st.session_state.angebote) == 0:
    st.info("Noch keine Angebote erstellt")
else:
    for a in st.session_state.angebote[::-1]:

        with st.expander(f"🧾 {a['nr']} – {a['kunde']} – {a['preis']}€"):

            st.write(f"🏢 Firma: {a['firma']}")
            st.write(f"👤 Kunde: {a['kunde']}")
            st.write(f"📍 Adresse: {a['adresse']}")
            st.write(f"🛠️ Auftrag: {a['auftrag']}")
            st.write(f"💰 Preis: {a['preis']} €")
            st.write(f"📅 Datum: {a['datum']}")
