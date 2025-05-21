"""
Main entry point for the Python Learning Platform
This file is configured as the main file for Streamlit Cloud deployment
"""
import os
import sys
import database
from app_updated import *

# Initialize the database if it's not already created
if not os.path.exists(os.path.join('data', 'python_learning.db')):
    print("Initializing database...")
    database.init_db()
    database.migrate_from_json()
    print("Database initialization complete!")