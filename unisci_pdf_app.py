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
    # Creiamo una tabella con i file
    df = pd.DataFrame({
        "Nome file": [f.name for f in uploaded_files]
    })

    st.write("Trascina le righe per riordinare i PDF:")

    edited_df = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        num_rows="fixed"
    )

    if st.button("Unisci PDF"):
        # L’ordine è quello risultante dal data_editor
        ordered = edited_df["Nome file"].tolist()

        merger = PdfMerger()
        for filename in ordered:
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
