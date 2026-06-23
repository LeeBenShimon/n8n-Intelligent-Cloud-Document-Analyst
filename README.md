# Intelligent Cloud Document Analyst

This project implements an automated n8n workflow that processes business documents from Google Drive, extracts text from PDF/DOCX/TXT files, analyzes the content using an LLM, enriches the result through a FastAPI metadata service, stores the results in Google Sheets, and sends an email notification via Gmail.

## Scenario
Business documents: invoices, contracts, purchase orders, and vendor agreements.

## Workflow Steps
1. Google Drive Trigger detects new files.
2. File is downloaded from Google Drive.
3. Switch routes files by type: PDF, DOCX, TXT.
4. FastAPI extracts text from the document.
5. LLM analyzes the document and returns structured JSON.
6. Metadata API enriches the output.
7. Results are appended to Google Sheets.
8. Gmail sends a notification email.

## Technologies
- n8n self-hosted with Docker
- Google Drive
- Python FastAPI
- PyMuPDF
- python-docx
- OpenAI / Gemini-compatible LLM
- Google Sheets
- Gmail
