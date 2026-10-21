from flask import Flask

app = Flask(__name__)


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