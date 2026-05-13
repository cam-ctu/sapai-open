"""Streamlit entry point for local development.

Run with:  streamlit run streamlit_app.py

In production (rct-sap-ai/sapai-streamlit), the same UI is invoked via a
3-line shim that does `from sapai_open.app import main; main()`. Keep this
file equivalent to that shim so behaviour is identical in both contexts.
"""

from sapai_open.app import main

main()
