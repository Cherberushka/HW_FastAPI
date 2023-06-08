python -m venv env
env\Scripts\activate
pip install fastapi
pip install uvicorn
uvicorn main:app --reload
http://127.0.0.1:8000/docs#