# Python Learning Platform

A comprehensive learning platform for Python programming, from beginner to advanced levels.

## Features

- 🐍 Structured learning paths for all skill levels
- 📚 Curated free resources and tutorials
- 💻 Coding problems from LeetCode and HackerRank
- 🧪 Interactive code examples with live execution
- 📊 Progress tracking and personalized recommendations
- 🛠️ Project ideas with starter code
- 👥 Community forum for discussions

## Deployment Instructions

### Option 1: Deploy on Streamlit Cloud (Recommended)

1. **Create a GitHub repository**
   - Create a new repository and upload all these files
   - Make sure to include all .py files, the data folder, and all configuration files

2. **Sign up for Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account

3. **Deploy your app**
   - Click "New app"
   - Select your repository, branch, and main file (app_updated.py)
   - Set the Python version to 3.9 or higher
   - Deploy!

### Option 2: Deploy Locally

1. **Install dependencies**
   - Rename `requirements_deploy.txt` to `requirements.txt`
   - Run `pip install -r requirements.txt`

2. **Initialize the database**
   - Run `python init_db.py`

3. **Start the application**
   - Run `streamlit run app_updated.py`

## Directory Structure

- `app_updated.py`: Main application file
- `database.py`: Database schema and migrations
- `db_utils.py`: Database utilities
- `init_db.py`: Database initialization
- `pages/`: Directory containing page modules
  - `beginner_updated.py`: Beginner resources
  - `intermediate.py`: Intermediate resources
  - `advanced.py`: Advanced resources
  - `practice.py`: Coding problems from LeetCode and HackerRank
  - `projects.py`: Project ideas
  - `progress.py`: Progress tracking
  - `community.py`: Community forum

## Usage

1. Create an account by entering a username
2. Browse resources by your skill level
3. Mark resources as completed to track progress
4. Practice coding problems from LeetCode and HackerRank
5. Work on suggested projects
6. Track your progress and level up as you learn more

## Data

All data is stored in a SQLite database (`data/python_learning.db`). This includes:
- User accounts and progress
- Learning resources
- Projects
- Coding problems
- Community discussions

## Credits

This platform curates free resources from across the web to help you learn Python programming from beginner to advanced levels. All content is organized to provide a structured learning path.