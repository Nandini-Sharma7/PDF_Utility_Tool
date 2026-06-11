import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import pdfplumber

st.set_page_config(
    page_title="Smart PDF Utility Tool",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Smart PDF Utility Tool")
st.markdown("### PDF Management Application using Python & Streamlit")

st.sidebar.title("PDF Utility Tool")

st.sidebar.info("""
Features:
✅ Merge PDFs
✅ Split PDF
✅ Extract Text
✅ Protect PDF
✅ View Metadata
""")

operation = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Merge PDFs",
        "Split PDF",
        "Extract Text",
        "Protect PDF",
        "View Metadata"
    ]
)
if operation == "Merge PDFs":

    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Merge PDFs"):

        merger = PdfMerger()

        for pdf in uploaded_files:
            merger.append(pdf)

        output_file = "merged.pdf"

        merger.write(output_file)
        merger.close()

        with open(output_file, "rb") as file:
            st.download_button(
                label="Download Merged PDF",
                data=file,
                file_name="merged.pdf",
                mime="application/pdf"
            )

        st.success("✅ PDFs Merged Successfully!")

elif operation == "Split PDF":

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_pdf:

        reader = PdfReader(uploaded_pdf)

        total_pages = len(reader.pages)

        st.info(f"Total Pages: {total_pages}")

        page_number = st.number_input(
            "Split After Page",
            min_value=1,
            max_value=total_pages - 1,
            value=1
        )

        if st.button("Split PDF"):

            pdf1 = PdfWriter()
            pdf2 = PdfWriter()

            for i in range(page_number):
                pdf1.add_page(reader.pages[i])

            for i in range(page_number, total_pages):
                pdf2.add_page(reader.pages[i])

            with open("part1.pdf", "wb") as f:
                pdf1.write(f)

            with open("part2.pdf", "wb") as f:
                pdf2.write(f)

            st.success("✅ PDFs Split Successfully!")

            with open("part1.pdf", "rb") as f:
                st.download_button(
                    "Download Part 1",
                    f,
                    file_name="part1.pdf"
                )

            with open("part2.pdf", "rb") as f:
                st.download_button(
                    "Download Part 2",
                    f,
                    file_name="part2.pdf"
                )

elif operation == "Extract Text":

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_pdf:

        text = ""

        with pdfplumber.open(uploaded_pdf) as pdf:

            for page in pdf.pages:
                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        st.text_area(
            "Extracted Text",
            text,
            height=300
        )

elif operation == "Protect PDF":

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if uploaded_pdf and password and st.button("Protect PDF"):

        reader = PdfReader(uploaded_pdf)

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open("protected.pdf", "wb") as f:
            writer.write(f)

        st.success("✅ PDF Protected Successfully!")

        with open("protected.pdf", "rb") as f:
            st.download_button(
                "📥 Download Protected PDF",
                f,
                file_name="protected.pdf",
                mime="application/pdf"
            )

elif operation == "View Metadata":

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_pdf:

        reader = PdfReader(uploaded_pdf)

        metadata = reader.metadata

        st.subheader("📋 PDF Metadata")

        if metadata:
            for key, value in metadata.items():
                st.write(f"**{key}** : {value}")

        st.write(f"**Number of Pages:** {len(reader.pages)}")

        uploaded_pdf.seek(0)

        file_size = len(uploaded_pdf.read()) / 1024

        st.write(f"**File Size:** {file_size:.2f} KB")

st.markdown("---")
st.caption(
    "Developed by Nandini Sharma | Smart PDF Utility Tool | Python • Streamlit • PyPDF2"
)