import os
from typing import List

from google.oauth2 import service_account
from googleapiclient.discovery import build

from chatbot.schema import ChatState


def _get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json"),
        scopes=[
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/documents.readonly",
        ],
    )
    drive = build("drive", "v3", credentials=creds)
    docs = build("docs", "v1", credentials=creds)
    return drive, docs


def _find_file_by_name(drive, name_substring: str) -> str | None:
    results = drive.files().list(
        q=f"name contains '{name_substring}' and mimeType='application/vnd.google-apps.document'",
        fields="files(id, name)",
        pageSize=10,
    ).execute()
    files: List[dict] = results.get("files", [])
    if not files:
        return None
    return files[0]["id"]


def _get_doc_text(docs, doc_id: str) -> str:
    doc = docs.documents().get(documentId=doc_id).execute()
    content = doc.get("body", {}).get("content", [])
    parts: List[str] = []
    for c in content:
        p = c.get("paragraph")
        if not p:
            continue
        for el in p.get("elements", []):
            text_run = el.get("textRun")
            if text_run and "content" in text_run:
                parts.append(text_run["content"])
    return "".join(parts).strip()


def node_google_drive_expert(state: ChatState) -> ChatState:
    last = state["messages"][-1]["content"]
    drive, docs = _get_drive_service()

    # aici folosim un nume generic; tu poți schimba după nevoile tale
    target_name = "info_suplim_sapt_01_ziua01"

    file_id = _find_file_by_name(drive, target_name)
    if not file_id:
        state["messages"].append({
            "role": "assistant",
            "content": f"Nu am găsit niciun document Google Docs care să conțină în nume: {target_name}."
        })
        return state

    text = _get_doc_text(docs, file_id)

    # adăugăm contextul din document ca mesaj de sistem
    state["messages"].insert(0, {
        "role": "system",
        "content": f"Acesta este conținutul documentului Google Docs '{target_name}':\n\n{text}"
    })

    return state
