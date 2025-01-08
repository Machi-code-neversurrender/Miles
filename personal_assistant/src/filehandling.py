import os
import PyPDF2
from docx import Document
import pandas as pd

class FileHandler:
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def upload_file(self, file_path, description):
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(self.storage_dir, file_name)
        os.rename(file_path, destination_path)

        # Extract content based on file type
        if file_name.endswith(".pdf"):
            with open(destination_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
        elif file_name.endswith(".docx"):
            doc = Document(destination_path)
            content = "\n".join([p.text for p in doc.paragraphs])
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(destination_path)
            content = df.to_string()
        else:
            content = f"Unsupported file type: {file_name}"

        return content