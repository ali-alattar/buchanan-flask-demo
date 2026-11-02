from pathlib import Path

from flask import Flask, send_from_directory

from opportunity_data import AS_OF, OPPORTUNITIES
from scoring import dashboard_opportunities

app = Flask(__name__, static_folder=None)
FRONTEND_DIST = Path(__file__).resolve().parent / "frontend" / "dist"


@app.get("/")
def dashboard():
    if not (FRONTEND_DIST / "index.html").is_file():
        return (
            "<h1>Frontend build needed</h1><p>From the project folder, run "
            "<code>npm --prefix frontend run build</code>, then reload.</p>",
            503,
        )
    response = send_from_directory(FRONTEND_DIST, "index.html", max_age=0)
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/assets/<path:filename>")
def frontend_asset(filename):
    return send_from_directory(FRONTEND_DIST / "assets", filename, max_age=31536000)


@app.get("/api/opportunities")
def opportunities():
    return {"as_of": AS_OF, "opportunities": dashboard_opportunities(OPPORTUNITIES)}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/roles")
def get_roles():
    roles = [
        {
            "id": 1,
            "title": "Corporate Associate",
            "location": "London"
        },
        {
            "id": 2,
            "title": "Legal Counsel",
            "location": "Miami"
        }
    ]

    return {
        "roles": roles,
        "count": len(roles)
    }
