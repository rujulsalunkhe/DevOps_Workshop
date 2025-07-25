import os
import zipfile
import shutil
import subprocess
import sys

def create_lambda_package():
    print("🚀 Starting Lambda package creation...")
    
    package_dir = "lambda_package"
    zip_filename = "lambda-deployment.zip"
    
    # Clean up existing files
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
        print("🧹 Cleaned up existing package directory")
    
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print("🧹 Removed existing zip file")
    
    # Create package directory
    os.makedirs(package_dir)
    print(f"📁 Created package directory: {package_dir}")
    
    # Copy Python files
    python_files = ["app.py", "lambda_handler.py"]
    
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"📄 Added {file} to package")
        else:
            print(f"⚠️  Warning: {file} not found")
    
    # Install Flask if requirements.txt exists, otherwise install Flask directly
    print("📦 Installing Flask...")
    try:
        if os.path.exists("requirements.txt"):
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "-r", "requirements.txt", 
                "-t", package_dir,
                "--no-user"
            ], check=True)
        else:
            # Install Flask directly
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "flask", 
                "-t", package_dir,
                "--no-user"
            ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to install dependencies: {e}")
    
    # Create the zip file
    print(f"🗜️  Creating {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    # Clean up package directory
    shutil.rmtree(package_dir)
    print("🧹 Cleaned up temporary package directory")
    
    size_mb = os.path.getsize(zip_filename) / 1024 / 1024
    print(f"✅ Successfully created {zip_filename}")
    print(f"📦 Package size: {size_mb:.2f} MB")
    
    return True

if __name__ == "__main__":
    try:
        success = create_lambda_package()
        if success:
            print("\n🎉 Package creation completed!")
            print("Now you can run: terraform apply")
        else:
            print("\n❌ Package creation failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error creating package: {e}")
        sys.exit(1)
