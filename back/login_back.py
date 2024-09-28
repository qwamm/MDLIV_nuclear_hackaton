import fastapi as fs
import httpx
from fastapi.staticfiles import StaticFiles

HOST="127.0.0.1"
PORT="5173"
log_app=fs.FastAPI()
log_app.mount("/", StaticFiles(directory="", html=True))

@log_app.get("/")
def redirect_from_github(code: str = ""):
    #example code=4d11b545c16e378ad2bb
    if code!="":
        httpx.post("https://github.com/login/oauth/access_token", data={
            'client_id': 'Iv23liDMCg3eeIfAIYy1',
            'client_secret': 'acd0e734f8cd0e64db104c4f210d71b63b7214db',
            'code': code,
            'redirect_uri': '/'
        })

@log_app.get("/")
def default_greetings():
    return {'greetings':"hello from MDLIV"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(log_app, host=HOST, port=PORT)