# serve to load model class
from web_app.base.model_loader import ModelLoader

model_loader = ModelLoader()
model_configs = model_loader.load_model_config()