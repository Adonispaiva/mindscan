from fastapi import FastAPI

app = FastAPI(title="MindScan Backend")

@app.get("/health")
def health():
    return {"status": "ok", "service": "MindScan"}
