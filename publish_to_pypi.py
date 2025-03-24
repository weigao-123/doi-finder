#!/usr/bin/env python
"""
Script to build and publish doi-finder to PyPI.
Run with: python publish_to_pypi.py
"""
import os
import sys
import subprocess
import shutil


def run_command(command):
    """Run a shell command and print the output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    print(f"Command completed with exit code: {result.returncode}")
    return result


def clean_build_dirs():
    """Remove old build directories."""
    dirs_to_remove = ['build', 'dist', '*.egg-info']
    for dir_name in dirs_to_remove:
        try:
            if '*' in dir_name:
                # Use glob for wildcard patterns
                import glob
                for path in glob.glob(dir_name):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                        print(f"Removed directory: {path}")
            elif os.path.exists(dir_name):
                if os.path.isdir(dir_name):
                    shutil.rmtree(dir_name)
                else:
                    os.remove(dir_name)
                print(f"Removed: {dir_name}")
        except Exception as e:
            print(f"Error removing {dir_name}: {e}")


def build_package():
    """Build the package."""
    try:
        run_command("python -m pip install --upgrade pip")
        run_command("pip install --upgrade build twine")
        run_command("python -m build")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building package: {e}")
        return False


def validate_package():
    """Validate the package with twine check."""
    try:
        run_command("twine check dist/*")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error validating package: {e}")
        return False


def upload_to_test_pypi():
    """Upload to Test PyPI."""
    try:
        run_command("twine upload --repository testpypi dist/*")
        print("\nPackage uploaded to Test PyPI successfully!")
        print("You can install it with:")
        print("pip install --index-url https://test.pypi.org/simple/ doi-finder")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error uploading to Test PyPI: {e}")
        return False


def upload_to_pypi():
    """Upload to PyPI."""
    try:
        run_command("twine upload dist/*")
        print("\nPackage uploaded to PyPI successfully!")
        print("You can install it with:")
        print("pip install doi-finder")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error uploading to PyPI: {e}")
        return False


def main():
    """Main function to build and publish package."""
    print("Starting package publication process...\n")
    
    # Clean build directories
    print("Cleaning build directories...")
    clean_build_dirs()
    
    # Build the package
    print("\nBuilding package...")
    if not build_package():
        print("Failed to build package. Exiting.")
        return 1
    
    # Validate the package
    print("\nValidating package...")
    if not validate_package():
        print("Package validation failed. Exiting.")
        return 1
    
    # Ask if user wants to upload to test PyPI first
    upload_test = input("\nDo you want to upload to Test PyPI first? (y/n): ").strip().lower() == 'y'
    if upload_test:
        if not upload_to_test_pypi():
            print("Failed to upload to Test PyPI. Exiting.")
            return 1
    
    # Ask if user wants to upload to PyPI
    upload_prod = input("\nDo you want to upload to PyPI? (y/n): ").strip().lower() == 'y'
    if upload_prod:
        if not upload_to_pypi():
            print("Failed to upload to PyPI. Exiting.")
            return 1
    
    print("\nPublication process completed!")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 