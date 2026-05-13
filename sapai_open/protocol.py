"""Protocol loader. Reads a clinical-trial protocol PDF or TXT into plain text.

Slim copy of `auto_sap.classes.protocol_classes.Protocol` from sap-kcl,
trimmed to just the upload-path use case (no repo-search helpers).
"""

from __future__ import annotations

import os
from typing import Union

import PyPDF2


class Protocol:
    """Load a clinical trial protocol from a PDF or TXT file."""

    def __init__(self, file_path: str):
        if not file_path:
            raise ValueError("file_path must be provided")

        self.file_path = file_path
        ext = self._check_extension(file_path)
        if ext == ".pdf":
            self._load_pdf()
        elif ext == ".txt":
            self._load_txt()
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def _load_pdf(self) -> None:
        chunks = []
        with open(self.file_path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                text = page.extract_text() or ""
                chunks.append(text.rstrip())
        self.protocol_txt = "\n\n".join(chunks)

    def _load_txt(self) -> None:
        with open(self.file_path, "r", encoding="utf-8", errors="replace") as fh:
            self.protocol_txt = fh.read()

    @staticmethod
    def _check_extension(filename: str) -> str:
        _, ext = os.path.splitext(filename)
        if ext.lower() not in {".txt", ".pdf"}:
            raise ValueError(
                f"Unsupported file extension: {ext}. Must be .txt or .pdf"
            )
        return ext.lower()


def load_protocol_from_upload(uploaded_file) -> str:
    """Read a Streamlit UploadedFile (or any file-like with .read() and .name).

    Returns the extracted protocol text. Writes to a tempfile internally so
    Protocol() (which expects a path) keeps working uniformly across PDF/TXT.

    This mirrors the production fix in sapai-streamlit's open app.
    """
    import tempfile

    suffix = os.path.splitext(getattr(uploaded_file, "name", ""))[1].lower() or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    return Protocol(tmp_path).protocol_txt
