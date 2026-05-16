import streamlit as st
from PyPDF2 import PdfMerger
import pandas as pd

st.title("Unisci PDF")

uploaded_files = st.file_uploader(
    "Carica i PDF", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    # Costruisco una tabella con nome file e posizione iniziale
    data = [
        {"Nome file": f.name, "Posizione": i + 1}
        for i, f in enumerate(uploaded_files)
    ]
    df = pd.DataFrame(data)

    st.write("Ordina i PDF impostando la colonna 'Posizione' (1, 2, 3, ...):")
    edited_df = st.data_editor(
        df,
        num_rows="fixed",
        column_config={
            "Posizione": st.column_config.NumberColumn(
                "Posizione",
                min_value=1,
                step=1
            )
        }
    )

    if st.button("Unisci PDF"):
        # Ordino in base alla colonna Posizione
        ordered = edited_df.sort_values("Posizione")

        merger = PdfMerger()
        for _, row in ordered.iterrows():
            filename = row["Nome file"]
            # Trovo il file corrispondente tra gli upload
            for f in uploaded_files:
                if f.name == filename:
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
