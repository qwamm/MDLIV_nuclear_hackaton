import random

import fastapi as fs
import httpx
from fastapi.staticfiles import StaticFiles

log_app=fs.FastAPI()

#Btw useful code to get tokens for testing
@log_app.get("/")
def redirect_from_github(code: str=""):
    #example code=4d11b545c16e378ad2bb
    if code!="":
        if len(code)==20:
            response=httpx.post("https://github.com/login/oauth/access_token", params={
                'client_id': 'Iv23liDMCg3eeIfAIYy1',
                'client_secret': 'acd0e734f8cd0e64db104c4f210d71b63b7214db',
                'code': code,
                'redirect_uri': 'http://localhost:5173/'
            })
            token=response.content.decode().split("&")[0].split("=")[-1]
            if token=="bad_verification_code":
                return {"github_error": token}
            else:
                return {"github_token": token}
        else:
            response = httpx.post("https://auth.atlassian.com/oauth/token", headers={'Content-Type': 'application/json'}, json={
                    "grant_type": "authorization_code",
                    "client_id": "kpZForY3FmJ5SerZaGZnKf3Kz5I6qF4s",
                    "client_secret": "ATOATNDEGnmgm2oRwRDIJPpWgUA_ghPro4Ho2GTADYbW6BgQJsYIG75cm0bzdEZ9VdaD3FDCC732",
                    "code": code,
                    "redirect_uri": "http://localhost:5173/"
            })
            print(response.json()['access_token'])
            return response.json()
    else:
        return {'greetings': "hello from MDLIV"}
