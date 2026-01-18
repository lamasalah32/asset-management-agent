from langchain.tools import tool
from database import SessionLocal
import crud

@tool
def query_assets(query: str) -> str:
    """
    Query assets from the database using natural language intent.
    """
    db = SessionLocal()
    assets = crud.get_assets(db)

    if not assets:
        return "No assets found."

    summary = []
    for a in assets:
        summary.append(f"{a.name} (${a.value})")

    return "Assets: " + ", ".join(summary)

