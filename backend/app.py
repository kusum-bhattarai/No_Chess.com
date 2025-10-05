from fastapi import FastAPI

app = FastAPI(title="NoChess API", description="Terminal Chess to Web", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "OK", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)