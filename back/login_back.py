import fastapi as fs
import httpx
from fastapi.staticfiles import StaticFiles

log_app=fs.FastAPI()

@log_app.get("/")
def redirect_from_github(code: str=""):
    #example code=4d11b545c16e378ad2bb
    if code!="":
        response=httpx.post("https://github.com/login/oauth/access_token", params={
            'client_id': 'Iv23liDMCg3eeIfAIYy1',
            'client_secret': 'acd0e734f8cd0e64db104c4f210d71b63b7214db',
            'code': code,
            'redirect_uri': 'http://localhost:5173/'
        })
        token=response.content.decode().split("&")[0].split("=")[-1]
        if token=="bad_verification_code":
            return {"error": token}
        else:
            return {"token": response.content.decode().split("&")[0].split("=")[-1]}
    else:
        return {'greetings': "hello from MDLIV"}