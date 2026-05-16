import streamlit as st
from PyPDF2 import PdfMerger

st.title("Unisci PDF")

uploaded_files = st.file_uploader(
    "Carica i PDF",
    type="pdf",
    accept_multiple_files=True
)

# Inizializza lo stato
if "order" not in st.session_state:
    st.session_state.order = []

if "move" not in st.session_state:
    st.session_state.move = None  # (index, direction)

if uploaded_files:
    names = [f.name for f in uploaded_files]

    # Se cambia il set di file caricati, resetta l'ordine
    if set(names) != set(st.session_state.order):
        st.session_state.order = names.copy()

    st.write("Ordina i PDF usando i pulsanti Su / Giù:")

    # Mostra la lista con pulsanti
    for idx, name in enumerate(st.session_state.order):
        col1, col2, col3 = st.columns([6, 1, 1])

        with col1:
            st.write(f"{idx+1}. {name}")

        with col2:
            if st.button("▲", key=f"up_{name}") and idx > 0:
                st.session_state.move = (idx, -1)

        with col3:
            if st.button("▼", key=f"down_{name}") and idx < len(st.session_state.order) - 1:
                st.session_state.move = (idx, +1)

    # Applica lo spostamento UNA SOLA VOLTA
    if st.session_state.move is not None:
        idx, direction = st.session_state.move
        new_idx = idx + direction

        st.session_state.order[idx], st.session_state.order[new_idx] = (
            st.session_state.order[new_idx],
            st.session_state.order[idx],
        )

        st.session_state.move = None
        st.rerun()

    # Pulsante per unire i PDF
    if st.button("Unisci PDF"):
        merger = PdfMerger()

        for name in st.session_state.order:
            for f in uploaded_files:
                if f.name == name:
                    merger.append(f)
                    break

        output = "unito.pdf"
        merger.write(output)
        merger.close()

        with open(output, "rb") as f:
            st.download_button(
                "Scarica PDF Unito",
                f,
                file_name="unito.pdf"
            )
