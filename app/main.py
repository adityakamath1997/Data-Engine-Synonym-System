from fastapi import FastAPI

# Boilerplate code for now lol
app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}

