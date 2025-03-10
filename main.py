from fastapi import FastAPI
from wifi_scanner import scan_wifi

app = FastAPI()

@app.get("/wifi")
def get_wifi_networks():
    return {"networks": scan_wifi()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
