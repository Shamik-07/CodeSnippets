from fastapi import FastAPI
import uvicorn
 
app = FastAPI()
 
@app.get("/")
def root ():
  return {"message": "Hello World!"}

if __name__ == '__main__':
  host = "127.0.0.1"
  uvicorn.run("hello:app", host=host, port=8000, reload=True) 