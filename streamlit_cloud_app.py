import streamlit as st
import json
import os
from datetime import datetime

# File paths
RESOURCES_FILE = "data/resources.json"
PROJECTS_FILE = "data/projects.json"
USER_PROGRESS_FILE = "data/user_progress.json"
DISCUSSIONS_FILE = "data/discussions.json"
PRACTICE_PROBLEMS_FILE = "data/practice_problems.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Utility functions
def load_resources():
    if not os.path.exists(RESOURCES_FILE):
        resources = generate_default_resources()
        save_resources(resources)
    
    try:
        with open(RESOURCES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading resources: {e}")
        return []

def save_resources(resources):
    try:
        with open(RESOURCES_FILE, 'w') as f:
            json.dump(resources, f, indent=4)
    except Exception as e:
        st.error(f"Error saving resources: {e}")

def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        projects = generate_default_projects()
        save_projects(projects)
    
    try:
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading projects: {e}")
        return []

def save_projects(projects):
    try:
        with open(PROJECTS_FILE, 'w') as f:
            json.dump(projects, f, indent=4)
    except Exception as e:
        st.error(f"Error saving projects: {e}")

def load_user_progress(username):
    if not os.path.exists(USER_PROGRESS_FILE):
        with open(USER_PROGRESS_FILE, 'w') as f:
            json.dump({}, f, indent=4)
    
    try:
        with open(USER_PROGRESS_FILE, 'r') as f:
            progress_data = json.load(f)
            
        if username in progress_data:
            user_data = progress_data[username]
            st.session_state.resources_completed = user_data.get('completed_resources', [])
            st.session_state.current_level = user_data.get('current_level', 'beginner')
    except Exception as e:
        st.error(f"Error loading user progress: {e}")

def save_user_progress(username, completed_resources, current_level):
    try:
        if os.path.exists(USER_PROGRESS_FILE):
            with open(USER_PROGRESS_FILE, 'r') as f:
                progress_data = json.load(f)
        else:
            progress_data = {}
        
        progress_data[username] = {
            'completed_resources': completed_resources,
            'current_level': current_level,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(USER_PROGRESS_FILE, 'w') as f:
            json.dump(progress_data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving user progress: {e}")

def load_practice_problems():
    if not os.path.exists(PRACTICE_PROBLEMS_FILE):
        practice_problems = generate_default_practice_problems()
        with open(PRACTICE_PROBLEMS_FILE, 'w') as f:
            json.dump(practice_problems, f, indent=4)
    
    try:
        with open(PRACTICE_PROBLEMS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading practice problems: {e}")
        return []

def load_discussions():
    if not os.path.exists(DISCUSSIONS_FILE):
        with open(DISCUSSIONS_FILE, 'w') as f:
            json.dump([], f, indent=4)
    
    try:
        with open(DISCUSSIONS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading discussions: {e}")
        return []

def save_discussions(discussions):
    try:
        with open(DISCUSSIONS_FILE, 'w') as f:
            json.dump(discussions, f, indent=4)
    except Exception as e:
        st.error(f"Error saving discussions: {e}")

def add_topic(title, content, author, category):
    discussions = load_discussions()
    
    new_topic = {
        'id': len(discussions) + 1,
        'title': title,
        'content': content,
        'author': author,
        'category': category,
        'created_at': datetime.now().isoformat(),
        'replies': []
    }
    
    discussions.append(new_topic)
    save_discussions(discussions)
    return new_topic

def add_reply(topic_id, content, author):
    discussions = load_discussions()
    
    for topic in discussions:
        if topic['id'] == int(topic_id):
            new_reply = {
                'id': len(topic['replies']) + 1,
                'content': content,
                'author': author,
                'created_at': datetime.now().isoformat()
            }
            topic['replies'].append(new_reply)
            save_discussions(discussions)
            return new_reply
    return None

def get_recommendations(level, completed_resources):
    resources = load_resources()
    
    # Filter resources by level and not completed
    available_resources = [r for r in resources if r['level'] == level and r['id'] not in completed_resources]
    
    # If user has completed more than 80% of current level, suggest some from next level
    if level != "advanced":
        completed_level_resources = [r for r in resources if r['level'] == level and r['id'] in completed_resources]
        all_level_resources = [r for r in resources if r['level'] == level]
        
        if len(all_level_resources) > 0 and len(completed_level_resources) / len(all_level_resources) >= 0.8:
            next_level = "intermediate" if level == "beginner" else "advanced"
            next_level_resources = [r for r in resources if r['level'] == next_level and r['id'] not in completed_resources]
            available_resources.extend(next_level_resources[:2])
    
    # Randomize a bit to provide variety
    import random
    random.shuffle(available_resources)
    
    return available_resources

def generate_default_resources():
    """Generate default resource dataset"""
    return [
        # Beginner resources
        {
            "id": "b1",
            "title": "Official Python Documentation - Getting Started",
            "type": "Documentation",
            "description": "The official Python documentation's beginner guide",
            "url": "https://docs.python.org/3/tutorial/index.html",
            "level": "beginner",
            "tags": ["syntax", "basics", "installation"]
        },
        {
            "id": "b2",
            "title": "Python for Everybody (py4e)",
            "type": "Free Course",
            "description": "A complete beginner-friendly Python course by Dr. Charles Severance",
            "url": "https://www.py4e.com/",
            "level": "beginner",
            "tags": ["basics", "programming", "fundamentals"]
        },
        {
            "id": "b3",
            "title": "W3Schools Python Tutorial",
            "type": "Tutorial",
            "description": "Interactive Python tutorial with exercises and examples",
            "url": "https://www.w3schools.com/python/",
            "level": "beginner",
            "tags": ["syntax", "examples", "interactive"]
        },
        {
            "id": "b4",
            "title": "Automate the Boring Stuff with Python",
            "type": "Free Book",
            "description": "Practical programming for total beginners by Al Sweigart",
            "url": "https://automatetheboringstuff.com/",
            "level": "beginner",
            "tags": ["automation", "practical", "scripts"]
        },
        {
            "id": "b5",
            "title": "Real Python - Python Basics",
            "type": "Tutorial",
            "description": "Python basics with practical examples and explanations",
            "url": "https://realpython.com/python-basics/",
            "level": "beginner",
            "tags": ["basics", "examples", "fundamentals"]
        },
        {
            "id": "b6",
            "title": "Codecademy - Learn Python",
            "type": "Interactive Course",
            "description": "Interactive Python course with coding exercises",
            "url": "https://www.codecademy.com/learn/learn-python-3",
            "level": "beginner",
            "tags": ["interactive", "basics", "syntax"]
        },
        {
            "id": "b7",
            "title": "freeCodeCamp - Python Beginner Course",
            "type": "Video Course",
            "description": "Full Python course for beginners on YouTube",
            "url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "level": "beginner",
            "tags": ["video", "comprehensive", "tutorial"]
        },
        {
            "id": "b8",
            "title": "Programiz Python Tutorial",
            "type": "Tutorial",
            "description": "Step by step Python tutorial with examples",
            "url": "https://www.programiz.com/python-programming",
            "level": "beginner",
            "tags": ["tutorial", "examples", "basics"]
        },
        
        # Intermediate resources
        {
            "id": "i1",
            "title": "Python Design Patterns",
            "type": "Tutorial",
            "description": "Implementation of design patterns in Python",
            "url": "https://refactoring.guru/design-patterns/python",
            "level": "intermediate",
            "tags": ["design patterns", "OOP", "architecture"]
        },
        {
            "id": "i2",
            "title": "Intermediate Python",
            "type": "Free Book",
            "description": "A free book for intermediate Python programmers",
            "url": "https://book.pythontips.com/en/latest/",
            "level": "intermediate",
            "tags": ["advanced concepts", "tips", "tricks"]
        },
        {
            "id": "i3",
            "title": "Fluent Python",
            "type": "Book Excerpts",
            "description": "Clear, concise, and effective programming with Python",
            "url": "https://github.com/fluentpython",
            "level": "intermediate",
            "tags": ["idiomatic", "effective", "pythonic"]
        },
        {
            "id": "i4",
            "title": "Real Python - Intermediate Topics",
            "type": "Tutorial Collection",
            "description": "A collection of intermediate-level Python tutorials",
            "url": "https://realpython.com/tutorials/intermediate/",
            "level": "intermediate",
            "tags": ["diverse topics", "practical", "tutorials"]
        },
        {
            "id": "i5",
            "title": "Python Testing with pytest",
            "type": "Tutorial",
            "description": "Learn about testing Python applications with pytest",
            "url": "https://realpython.com/pytest-python-testing/",
            "level": "intermediate",
            "tags": ["testing", "pytest", "quality"]
        },
        {
            "id": "i6",
            "title": "Python Tricks: The Book",
            "type": "Book Samples",
            "description": "A buffet of awesome Python features and tricks",
            "url": "https://realpython.com/products/python-tricks-book/",
            "level": "intermediate",
            "tags": ["tricks", "features", "techniques"]
        },
        {
            "id": "i7",
            "title": "Python Data Science Handbook",
            "type": "Free Book",
            "description": "Python data science libraries and techniques",
            "url": "https://jakevdp.github.io/PythonDataScienceHandbook/",
            "level": "intermediate",
            "tags": ["data science", "numpy", "pandas", "matplotlib"]
        },
        {
            "id": "i8",
            "title": "Python Concurrency",
            "type": "Tutorial",
            "description": "Understanding concurrency in Python with threading, multiprocessing, and asyncio",
            "url": "https://realpython.com/python-concurrency/",
            "level": "intermediate",
            "tags": ["concurrency", "threading", "asyncio"]
        },
        
        # Advanced resources
        {
            "id": "a1",
            "title": "Python 3 Module of the Week",
            "type": "Documentation",
            "description": "Deep dive into Python's standard library modules",
            "url": "https://pymotw.com/3/",
            "level": "advanced",
            "tags": ["standard library", "modules", "reference"]
        },
        {
            "id": "a2",
            "title": "Python Cookbook",
            "type": "Book Excerpts",
            "description": "Recipes for mastering Python 3",
            "url": "https://github.com/dabeaz/python-cookbook",
            "level": "advanced",
            "tags": ["recipes", "techniques", "advanced patterns"]
        },
        {
            "id": "a3",
            "title": "CPython Internals",
            "type": "Tutorial",
            "description": "Understanding the internals of CPython",
            "url": "https://realpython.com/cpython-source-code-guide/",
            "level": "advanced",
            "tags": ["cpython", "internals", "c-api"]
        },
        {
            "id": "a4",
            "title": "Full Stack Python",
            "type": "Documentation",
            "description": "Full stack Python web development",
            "url": "https://www.fullstackpython.com/",
            "level": "advanced",
            "tags": ["web development", "deployment", "frameworks"]
        },
        {
            "id": "a5",
            "title": "Python Decorators",
            "type": "Tutorial",
            "description": "Deep dive into Python decorators",
            "url": "https://realpython.com/primer-on-python-decorators/",
            "level": "advanced",
            "tags": ["decorators", "metaprogramming", "functions"]
        },
        {
            "id": "a6",
            "title": "Building Machine Learning Systems with Python",
            "type": "Tutorial Series",
            "description": "Advanced machine learning with Python",
            "url": "https://github.com/luispedro/BuildingMachineLearningSystemsWithPython",
            "level": "advanced",
            "tags": ["machine learning", "algorithms", "data science"]
        },
        {
            "id": "a7",
            "title": "Python Performance Optimization",
            "type": "Tutorial",
            "description": "Advanced techniques for optimizing Python code",
            "url": "https://pythonspeed.com/",
            "level": "advanced",
            "tags": ["performance", "optimization", "profiling"]
        },
        {
            "id": "a8",
            "title": "Making Python Programs Blazingly Fast",
            "type": "Video",
            "description": "Advanced techniques for high-performance Python",
            "url": "https://www.youtube.com/watch?v=o9wePFI0XkE",
            "level": "advanced",
            "tags": ["optimization", "performance", "cython"]
        }
    ]

def generate_default_projects():
    """Generate default projects dataset"""
    return [
        # Beginner projects
        {
            "id": "pb1",
            "title": "Number Guessing Game",
            "description": "Create a simple number guessing game where the computer generates a random number and the user tries to guess it.",
            "level": "beginner",
            "difficulty": 1,
            "skills": ["Basic syntax", "Input/Output", "Random module", "Conditionals"],
            "details": "Build a console-based number guessing game where the program generates a random number between 1 and 100. The player gets feedback after each guess whether their guess was too high or too low, until they correctly guess the number.",
            "starter_code": """import random

# Generate a random number between 1 and 100
target_number = random.randint(1, 100)
attempts = 0

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

# Your code here
# Hint: Use a while loop to keep asking for guesses
# Use input() to get the user's guess
# Convert the input to an integer using int()
# Compare the guess with target_number
# Provide appropriate feedback
"""
        },
        {
            "id": "pb2",
            "title": "To-Do List Application",
            "description": "Build a simple command-line to-do list where users can add, view, and delete tasks.",
            "level": "beginner",
            "difficulty": 2,
            "skills": ["Lists", "Functions", "File I/O", "User input"],
            "details": "Create a command-line application that allows users to manage their to-do list. Implement functions to add tasks, view all tasks, mark tasks as completed, delete tasks, and save the tasks to a file for persistence.",
            "starter_code": """# To-Do List Application

todos = []

def show_menu():
    print("\\n==== TO-DO LIST MENU ====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Save and exit")
    
    choice = input("Enter your choice (1-5): ")
    return choice

def add_task():
    # Your code here
    pass

def view_tasks():
    # Your code here
    pass

def complete_task():
    # Your code here
    pass

def delete_task():
    # Your code here
    pass

def save_tasks():
    # Your code here
    pass

def load_tasks():
    # Your code here
    pass

# Main program
load_tasks()  # Load any existing tasks
while True:
    user_choice = show_menu()
    
    # Implement the menu logic
    # Your code here
"""
        },
        # Add more projects as needed
    ]

def generate_default_practice_problems():
    """Generate default practice problems dataset"""
    return [
        # LeetCode problems
        {
            "id": "lc1",
            "title": "Two Sum",
            "source": "LeetCode",
            "difficulty": "Easy",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "url": "https://leetcode.com/problems/two-sum/",
            "example": """
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
            """
        },
        {
            "id": "lc2",
            "title": "Valid Parentheses",
            "source": "LeetCode",
            "difficulty": "Easy",
            "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "url": "https://leetcode.com/problems/valid-parentheses/",
            "example": """
Input: s = "()[]{}"
Output: true

Input: s = "(]"
Output: false
            """
        },
        {
            "id": "lc3",
            "title": "Add Two Numbers",
            "source": "LeetCode",
            "difficulty": "Medium",
            "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
            "url": "https://leetcode.com/problems/add-two-numbers/",
            "example": """
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
            """
        },
        
        # HackerRank problems
        {
            "id": "hr1",
            "title": "Solve Me First",
            "source": "HackerRank",
            "difficulty": "Easy",
            "description": "Complete the function sum_of_two_numbers to solve a simple addition problem.",
            "url": "https://www.hackerrank.com/challenges/solve-me-first/problem",
            "example": """
Input: a = 2, b = 3
Output: 5
            """
        },
        {
            "id": "hr2",
            "title": "Simple Array Sum",
            "source": "HackerRank",
            "difficulty": "Easy",
            "description": "Given an array of integers, find the sum of its elements.",
            "url": "https://www.hackerrank.com/challenges/simple-array-sum/problem",
            "example": """
Input: ar = [1, 2, 3, 4, 10, 11]
Output: 31
            """
        },
        {
            "id": "hr3",
            "title": "Compare the Triplets",
            "source": "HackerRank",
            "difficulty": "Medium",
            "description": "Alice and Bob each created one problem for HackerRank. A reviewer rates the two challenges, awarding points on a scale from 1 to 100 for three categories: problem clarity, originality, and difficulty.",
            "url": "https://www.hackerrank.com/challenges/compare-the-triplets/problem",
            "example": """
Input: a = [5, 6, 7], b = [3, 6, 10]
Output: [1, 1]
Explanation: Alice receives 1 point (for a[0] > b[0]), and Bob receives 1 point (for a[2] < b[2]).
            """
        }
    ]

# Page configuration
st.set_page_config(
    page_title="Python Learning Path",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user progress if not exists
if 'username' not in st.session_state:
    st.session_state.username = None
if 'resources_completed' not in st.session_state:
    st.session_state.resources_completed = []
if 'current_level' not in st.session_state:
    st.session_state.current_level = "beginner"

# Main header
st.title("🐍 Python Learning Path 🚀")
st.subheader("✨ A comprehensive resource for learning Python from beginner to advanced ✨")

# User login/profile section in sidebar
with st.sidebar:
    st.header("👤 User Profile")
    
    if st.session_state.username:
        st.success(f"👋 Logged in as: {st.session_state.username}")
        if st.button("🚪 Log Out"):
            st.session_state.username = None
            st.session_state.resources_completed = []
            st.rerun()
    else:
        username = st.text_input("👉 Enter your username")
        if st.button("🔑 Log In/Register"):
            if username:
                st.session_state.username = username
                # Load user progress if exists
                load_user_progress(username)
                st.rerun()
            else:
                st.error("⚠️ Please enter a username")
    
    st.divider()
    st.write("### 🧭 Navigation")
    st.write("📚 Use the pages in the sidebar to navigate through different sections of the learning path.")

# Main content
if not st.session_state.username:
    # Welcome section for non-logged in users
    st.info("🔐 Please log in to track your progress and access all features!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## 🤔 Why Learn Python?
        
        Python is one of the most popular programming languages worldwide because:
        
        - **🔍 Easy to learn**: Simple syntax and readability
        - **🛠️ Versatile**: Used in web development, data science, AI, automation, and more
        - **💼 High demand**: Consistently ranked among top skills employers seek
        - **👥 Strong community**: Rich ecosystem of libraries and frameworks
        - **🆓 Free and open-source**: Accessible to everyone
        """)
    
    with col2:
        st.markdown("""
        ## 🚀 How to Use This Platform
        
        1. **👤 Register/Login**: Create an account to track your progress
        2. **🎯 Choose your level**: Start from beginner or jump to your current skill level
        3. **📚 Follow the learning path**: Work through curated resources
        4. **💻 Practice with projects**: Apply your knowledge with hands-on coding
        5. **📊 Track progress**: Mark completed resources and monitor your journey
        """)
else:
    # Dashboard for logged-in users
    st.write(f"👋 Welcome back, **{st.session_state.username}**! Let's continue your Python learning journey. 🚀")
    
    # Display current progress
    current_level = st.session_state.current_level
    level_emoji = {"beginner": "🐣", "intermediate": "🚀", "advanced": "🔥"}
    
    st.write(f"### 📊 Your Current Level: {level_emoji[current_level]} {current_level.capitalize()}")
    
    # Calculate progress percentage
    resources = load_resources()
    level_resources = [r for r in resources if r['level'] == current_level]
    completed = [r for r in level_resources if r['id'] in st.session_state.resources_completed]
    
    if level_resources:
        progress_percentage = len(completed) / len(level_resources) * 100
        st.progress(progress_percentage / 100)
        st.write(f"🎯 You've completed **{len(completed)}** out of **{len(level_resources)}** resources (**{progress_percentage:.1f}%**)")
    
    # Quick navigation cards
    st.write("### 🚀 Continue Learning")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        #### 🐣 Beginner Path
        Fundamentals of Python programming for newcomers.
        """)
        st.button("📚 Go to Beginner Resources", key="goto_beginner")
    
    with col2:
        st.markdown("""
        #### 🚀 Intermediate Path
        Advanced concepts and practical applications.
        """)
        st.button("📘 Go to Intermediate Resources", key="goto_intermediate")
    
    with col3:
        st.markdown("""
        #### 🔥 Advanced Path
        Expert techniques and specialized domains.
        """)
        st.button("📕 Go to Advanced Resources", key="goto_advanced")
        
    with col4:
        st.markdown("""
        #### 💻 Practice Problems
        LeetCode and HackerRank coding challenges.
        """)
        st.button("🏆 Go to Practice Problems", key="goto_practice")
    
    # Recommended next resources
    st.write("### 🧠 Recommended Next Steps")
    
    # Get recommendations based on user progress
    recommendations = get_recommendations(current_level, st.session_state.resources_completed)
    
    if recommendations:
        for i, resource in enumerate(recommendations[:3]):
            with st.expander(f"{i+1}. ✨ {resource['title']}"):
                st.write(f"**📋 Type**: {resource['type']}")
                st.write(f"**📝 Description**: {resource['description']}")
                st.markdown(f"[🔗 Open Resource]({resource['url']})")
                
                # Mark as completed button
                if resource['id'] not in st.session_state.resources_completed:
                    if st.button("✅ Mark as Completed", key=f"complete_{resource['id']}"):
                        st.session_state.resources_completed.append(resource['id'])
                        save_user_progress(st.session_state.username, 
                                        st.session_state.resources_completed, 
                                        st.session_state.current_level)
                        st.rerun()
                else:
                    st.success("✅ Completed!")
    else:
        st.info("🎉 Great job! You've completed all resources at your current level. Consider moving to the next level!")
        
    # Project suggestions
    st.write("### 💻 Suggested Projects")
    projects = load_projects()
    level_projects = [p for p in projects if p['level'] == current_level]
    
    if level_projects:
        selected_project = st.selectbox(
            "🔍 Select a project to work on:",
            options=[p['title'] for p in level_projects],
            index=0
        )
        
        project = next((p for p in level_projects if p['title'] == selected_project), None)
        
        if project:
            st.write(f"**📝 Description**: {project['description']}")
            st.write(f"**🌡️ Difficulty**: {project['difficulty']}/5")
            st.write("**🔑 Key Skills**:")
            for skill in project['skills']:
                st.write(f"- ✨ {skill}")
            
            with st.expander("📋 View Project Details"):
                st.write(project['details'])
                if 'starter_code' in project and project['starter_code']:
                    st.code(project['starter_code'], language="python")
    else:
        st.info("🔍 No projects available at your current level.")

# Footer
st.markdown("---")
st.markdown("### 📌 About This Platform")
st.markdown(
    "🌟 This free Python learning platform curates high-quality resources "
    "from across the web to help you learn Python programming from beginner "
    "to advanced levels. All content is organized to provide a structured learning path. 🚀"
)
st.markdown("✨ Created with ❤️ using Streamlit ✨")