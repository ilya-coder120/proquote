import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import random

st.set_page_config(
    page_title="ProQuote – Angebotssoftware",
    page_icon="🧾",
    layout="wide"
)

# ===== HERO SECTION =====
st.markdown("""
# 🧾 ProQuote

### Angebote in Sekunden erstellen – wie ein echtes Büro-Tool für Handwerker

""")

# ===== FEATURE BOXES =====
colA, colB, colC = st.columns(3)

with colA:
    st.markdown("### ⚡ Schnell")
    st.write("Erstelle komplette Angebote in unter 1 Minute.")

with colB:
    st.markdown("### 🧠 Smart")
    st.write("Automatische Vorschläge für Gewerke & Preise.")

with colC:
    st.markdown("### 📄 Export")
    st.write("PDF Angebote direkt downloaden & verschicken.")

st.divider()


# ===== SESSION INIT =====
if "angebote" not in st.session_state:
    st.session_state.angebote = []

# ===== GEWERKE =====
gwerke = {
    "Maler": {
        "text": "Wände streichen, Vorbereitung, Abdeckung, Reinigung",
        "preis": (300, 1500)
    },
    "Elektriker": {
        "text": "Steckdosen setzen, Leitungen prüfen, Installation",
        "preis": (500, 3000)
    },
    "Sanitär": {
        "text": "Rohrarbeiten, Badinstallation, Reparaturen",
        "preis": (600, 3500)
    },
    "Gartenbau": {
        "text": "Rasenarbeiten, Hecken schneiden, Pflasterarbeiten",
        "preis": (200, 2000)
    }
}

# ===== PDF =====
def create_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 800

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, data["firma"])

    y -= 30
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Angebotsnummer: {data['nr']}")
    y -= 20
    pdf.drawString(50, y, f"Datum: {data['datum']}")

    y -= 40
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
    pdf.drawString(50, y, f"Preis: {data['preis']} €")

    pdf.save()
    buffer.seek(0)
    return buffer


# ===== UI =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧾 Eingabe")

    firma = st.text_input("Firma", "Muster GmbH")
    kunde = st.text_input("Kunde")
    adresse = st.text_input("Adresse")

    gewerk = st.selectbox("Gewerk", list(gwerke.keys()))

    # 🔥 FIX: Preisrange funktioniert wieder sauber
    min_p, max_p = gwerke[gewerk]["preis"]

    use_auto = st.checkbox("Preisvorschlag nutzen (Slider)")

    if use_auto:
        preis = st.slider(
            "Preis wählen",
            min_value=min_p,
            max_value=max_p,
            value=int((min_p + max_p) / 2)
        )
    else:
        preis = st.number_input(
            "Eigener Preis (€)",
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


# ===== OUTPUT =====
with col2:
    st.subheader("📄 Ergebnis")

    if "data" in st.session_state:

        d = st.session_state["data"]

        st.success("✔ Angebot erstellt")

        st.write(f"🏢 Firma: {d['firma']}")
        st.write(f"👤 Kunde: {d['kunde']}")
        st.write(f"🛠️ Auftrag: {d['auftrag']}")
        st.write(f"💰 Preis: {d['preis']} €")

        pdf = create_pdf(d)

        st.download_button(
            label="📥 PDF herunterladen",
            data=pdf,
            file_name=f"angebot_{d['nr']}.pdf",
            mime="application/pdf"
        )

    else:
        st.info("Noch kein Angebot erstellt")


# ===== HISTORIE =====
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