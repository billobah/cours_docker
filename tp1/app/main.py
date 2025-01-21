import requests
from fastapi import FastAPI


app = FastAPI()

file_path = "data/database.csv"


@app.get("/")
async def home():
    return {"home":"hello world"}

@app.get("/file")
async def home():
    url = "https://raw.githubusercontent.com/france-connect/data-provider-example/refs/heads/master/database.csv"
    
    #request
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            with open(file_path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            return {"file" : str(e)}
        
        return {"file" : file_path}
    else:
        return{"file" : "il y a un problème", "status" : response.status_code}
