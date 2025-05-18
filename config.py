# config.py – share config across modules
import yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)