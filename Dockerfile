FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501


CMD ["streamlit","run","new_app.py", "--server.address=0.0.0.0"]
