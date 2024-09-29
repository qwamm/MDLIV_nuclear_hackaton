import logging.config

import uvicorn

from src import DEBUG, SITE_IP, SITE_PORT

if __name__ == "__main__":
    print("DOCS ARE AVALABLE AT: http://127.0.0.1:8080/api/docs#/")
    uvicorn.run("src.main:app", host=SITE_IP, port=SITE_PORT, reload=DEBUG)
