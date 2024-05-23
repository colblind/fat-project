import uvicorn

from config.app.instance import get_app_instance

app = get_app_instance()

if __name__ == "__main__":
    uvicorn.run(app=app, reload=True, host='0.0.0.0', port=8000)
