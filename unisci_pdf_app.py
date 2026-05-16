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
    # Creiamo una tabella con i file e la posizione iniziale
    df = pd.DataFrame({
        "Nome file": [f.name for f in uploaded_files],
        "Posizione": list(range(1, len(uploaded_files) + 1))
    })

    st.write("Trascina le righe per riordinare i PDF:")

    edited_df = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Posizione": st.column_config.NumberColumn(
                "Posizione",
                min_value=1,
                step=1,
                disabled=True
            )
        ),
        disabled=["Nome file"],  # impedisce modifiche al nome
        num_rows="fixed",
        key="editor",
        reorderable_rows=True  # ❤️ abilita il drag & drop
    )

    if st.button("Unisci PDF"):
        # L’utente ha riordinato le righe → usiamo l’ordine attuale
        ordered = edited_df.reset_index(drop=True)

        merger = PdfMerger()
        for _, row in ordered.iterrows():
            filename = row["Nome file"]
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
