import os
import tkinter as tk
from tkinter import filedialog

def patch_gorilla_tag():
    package_name = "com.AnotherAxiom.GorillaTag"
    print(f"Target App: {package_name}")
    
    # Hide the main tkinter root window since we only want the file dialog popup
    root = tk.Tk()
    root.withdraw()
    
    print("Opening file browser... Select your mod .dll file.")
    dll_path = filedialog.askopenfilename(
        title="Select Gorilla Tag Mod .dll",
        filetypes=[("DLL Files", "*.dll"), ("All Files", "*.*")]
    )
    
    if not dll_path:
        print("Error: No file selected. Patching aborted.")
        return

    if not os.path.exists(dll_path):
        print(f"Error: The file {dll_path} does not exist.")
        return

    print(f"Injecting {dll_path} into {package_name} framework...")
    
    # Setup the required files and directory structure exclusively for Gorilla Tag
    os.makedirs("output_project/assets/bin/Managed", exist_ok=True)
    os.makedirs("output_project/smali", exist_ok=True)
    
    # Copy the selected .dll straight into the target directory
    dest_path = os.path.join("output_project/assets/bin/Managed", os.path.basename(dll_path))
    with open(dll_path, "rb") as src, open(dest_path, "wb") as dst:
        dst.write(src.read())
        
    # Write metadata locking the build down to Gorilla Tag
    with open("output_project/patch_metadata.txt", "w") as meta:
        meta.write(f"TargetPackage={package_name}\n")
        meta.write(f"ModFile={os.path.basename(dll_path)}\n")
        meta.write("Exclusive=True\n")
        
    print(f"Gorilla Tag ({package_name}) successfully patched with {os.path.basename(dll_path)}!")
    print("Project ready for GitHub Actions build workflow.")

if __name__ == "__main__":
    print("========================================")
    print("       GORILLAPATCHER (FILE BROWSER)    ")
    print("========================================")
    print("[!] Ensure you have manually authorized Bytezuku before proceeding.")
    
    input("Press [Enter] to open file browser and patch Gorilla Tag (com.AnotherAxiom.GorillaTag)...")
    patch_gorilla_tag()
