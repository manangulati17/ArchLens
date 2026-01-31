from fastapi import FastAPI

app = FastAPI(title="Archlens")

@app.get("/")
async def health():
    return {"status":"archlens backend is running"}