import os
import shutil
import json

# Load file type mappings from config.json
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Function to create directories for file categories
def create_directories(base_path, categories):
    for category in categories:
        folder_path = os.path.join(base_path, category)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

# Function to move files to categorized folders
def organize_files(source_path, config):
    for file_name in os.listdir(source_path):
        file_path = os.path.join(source_path, file_name)

        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue

        # Get file extension and determine its category
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        category = None

        for cat, extensions in config.items():
            if ext in extensions:
                category = cat
                break

        # If no matching category is found, classify as "Others"
        if category is None:
            category = "Others"

        # Move file to the appropriate folder
        dest_folder = os.path.join(source_path, "organized_files", category)
        dest_path = os.path.join(dest_folder, file_name)

        # Handle duplicate file names
        base_name, ext = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{base_name}_{counter}{ext}")
            counter += 1

        shutil.move(file_path, dest_path)
        print(f"Moved: {file_name} --> {category}")

def main():
    # Define source directory and load configuration
    source_path = input("Enter the path of the directory to organize: ").strip()
    if not os.path.exists(source_path):
        print("Invalid path. Please try again.")
        return

    config = load_config()

    # Create directories for categories
    base_output_path = os.path.join(source_path, "organized_files")
    create_directories(base_output_path, list(config.keys()) + ["Others"])

    # Organize files
    organize_files(source_path, config)
    print("\nFile organization complete!")

if __name__ == "__main__":
    main()
