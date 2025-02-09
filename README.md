# llm_chatbot_example

```console
gunicorn --bind 0.0.0.0:8000 main:app --workers 1 --worker-class uvicorn.workers.UvicornH11Worker --preload
```