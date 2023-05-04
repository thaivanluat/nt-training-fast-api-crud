from fastapi import FastAPI
from routers import company, user, task, auth

app = FastAPI()
app.include_router(company.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)

@app.get("/")
async def health_check():
    return "API Service is running"