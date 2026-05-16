import streamlit as st
from PyPDF2 import PdfMerger

st.title("Unisci PDF")

uploaded_files = st.file_uploader("Carica i PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.write("Ordine dei file:")
    filenames = [f.name for f in uploaded_files]
    order = st.multiselect("Riordina i PDF", filenames, default=filenames)

    if st.button("Unisci PDF"):
        merger = PdfMerger()
        for name in order:
            for f in uploaded_files:
                if f.name == name:
                    merger.append(f)

        output = "unito.pdf"
        merger.write(output)
        merger.close()

        with open(output, "rb") as f:
            st.download_button("Scarica PDF Unito", f, file_name="unito.pdf")
