import os 
from pathlib import Path
project_name = "crypto-price-prediction"

structure = {
    ".github/workflows": ["ci-cd.yml"],
    "dags": [".gitkeep"],
    "data/raw": [".gitkeep"],
    "data/model": [".gitkeep"],
    "data/processed": [".gitkeep"],
    "notebook/EDA": ["eda.ipynb"],
    "src/{project_name}/web/api/static/css": [".gitkeep"],
    "src/{project_name}/web/api/static/js": [".gitkeep"],
    "src/{project_name}/web/api/templates": [".gitkeep"],
    "src/{project_name}/web/api": [
        "app.py",
        "route.py",
        "__init__.py"
    ],
    "src/{project_name}/web/services": [
        "__init__.py"
    ],
    "src/{project_name}/config": [
        "__init__.py",
        "loop_config.py",
        "config.py"
    ],
    "src/{project_name}/ml_components": [
        "__init__.py"
    ],
    "src/{project_name}/monitoring": [
        "__init__.py"
    ],
    "src/{project_name}/utils": [
        "__init__.py"
    ],
    "logs": [".gitkeep"],
    "test": [".gitkeep"],
    ".": [
        ".env",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
        "requirements.txt",
        "pyproject.Toml"
    ]
}

# Create folders
def create_folders(base_path, structure):
    print("Creating folders")
    for folder_path in structure.keys():
        full_path = os.path.join(base_path, folder_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"Folder created: {full_path}")

# Create files
def create_files(base_path, structure): 
    print("Create files")
    for folder_path, files in structure.items():
        for file_name in files:
            full_file_path = os.path.join(base_path, folder_path, file_name)
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            if not os.path.exists(full_file_path):
                with open(full_file_path, "w") as f:
                    if file_name == ".gitkeep":
                        pass
                    else:
                        f.write(f"# {file_name}")
                print(f"File created: {full_file_path}")
            else:
                print(f"File already exists: {full_file_path}")

# Runner
def create_project_structure():
    base_path = Path(__file__).resolve().parent
    create_folders(base_path, structure) 
    create_files(base_path, structure)
    print(f" Project structure created successfully at: {base_path}")  

if __name__ == "__main__":
    create_project_structure()

