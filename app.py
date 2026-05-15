
from pathlib import Path
from visa.utils.main_utile import read_yaml


file_name = Path("config\schema.yaml")

data = read_yaml(file_name)

print(data.all_columns.values())

