import streamlit as st
import json
import db_utils
import os

# Page configuration
st.set_page_config(
    page_title="Beginner Python Resources",
    page_icon="🐣",
    layout="wide"
)

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to track your progress.")
    st.stop()

# Load resources
resources = db_utils.load_resources()
beginner_resources = [r for r in resources if r['level'] == 'beginner']

# Header
st.title("🐣 Beginner Python Resources")
st.write("""
This section contains carefully curated free resources for beginners learning Python. 
These materials will help you build a solid foundation in Python programming.
""")

# Beginner learning path
st.header("Learning Path for Beginners")
st.write("""
Follow this learning path to systematically build your Python knowledge from scratch:

1. **Python Installation & Setup** - Get Python running on your computer
2. **Basic Syntax & Data Types** - Learn the building blocks of Python
3. **Control Flow** - Master if statements, loops, and program flow
4. **Functions & Modules** - Organize your code efficiently
5. **File Operations** - Read and write files
6. **Error Handling** - Deal with errors gracefully
7. **Basic Data Structures** - Lists, dictionaries, sets, and tuples
8. **Simple Projects** - Apply your knowledge to real problems
""")

# Filter options
st.sidebar.header("Filter Resources")
resource_types = ["All Types"] + sorted(list(set([r['type'] for r in beginner_resources])))
selected_type = st.sidebar.selectbox("Resource Type", resource_types)

if selected_type != "All Types":
    filtered_resources = [r for r in beginner_resources if r['type'] == selected_type]
else:
    filtered_resources = beginner_resources

# Tags filter
all_tags = []
for resource in beginner_resources:
    all_tags.extend(resource.get('tags', []))
unique_tags = ["All Tags"] + sorted(list(set(all_tags)))
selected_tag = st.sidebar.selectbox("Filter by Tag", unique_tags)

if selected_tag != "All Tags":
    filtered_resources = [r for r in filtered_resources if 'tags' in r and selected_tag in r['tags']]

# Display resources
if filtered_resources:
    for resource in filtered_resources:
        with st.expander(f"{resource['title']} ({resource['type']})"):
            st.write(f"**Description**: {resource['description']}")
            
            # Display tags if they exist
            if 'tags' in resource and resource['tags']:
                st.write("**Tags**: " + ", ".join(resource['tags']))
            
            st.markdown(f"**Link**: [{resource['url']}]({resource['url']})")
            
            # Progress tracking
            if resource['id'] in st.session_state.resources_completed:
                st.success("✅ You've completed this resource")
                if st.button("Mark as Incomplete", key=f"incomplete_{resource['id']}"):
                    st.session_state.resources_completed.remove(resource['id'])
                    db_utils.save_user_progress(st.session_state.username, 
                                         st.session_state.resources_completed,
                                         st.session_state.current_level)
                    st.rerun()
            else:
                if st.button("Mark as Completed", key=f"complete_{resource['id']}"):
                    st.session_state.resources_completed.append(resource['id'])
                    db_utils.save_user_progress(st.session_state.username, 
                                         st.session_state.resources_completed,
                                         st.session_state.current_level)
                    st.rerun()
else:
    st.info("No resources match your filter criteria. Try adjusting your filters.")

# Level progression
st.header("Ready to Level Up?")
completed_resources = [r for r in beginner_resources if r['id'] in st.session_state.resources_completed]
total_resources = len(beginner_resources)
completion_percentage = len(completed_resources) / total_resources * 100 if total_resources > 0 else 0

st.write(f"You've completed {len(completed_resources)} out of {total_resources} beginner resources ({completion_percentage:.1f}%).")

progress_bar = st.progress(completion_percentage / 100)

if completion_percentage >= 70:
    st.success("Congratulations! You've mastered the basics of Python. You're ready to move on to intermediate concepts!")
    if st.session_state.current_level == "beginner" and st.button("Move to Intermediate Level"):
        st.session_state.current_level = "intermediate"
        db_utils.save_user_progress(st.session_state.username, 
                             st.session_state.resources_completed,
                             st.session_state.current_level)
        st.success("Level updated! You are now at the intermediate level.")
        st.balloons()
else:
    st.info(f"Complete at least 70% of beginner resources to unlock the intermediate level. You're at {completion_percentage:.1f}% now.")

# Code examples section
st.header("Basic Python Code Examples")

code_examples = {
    "Hello World": """# Your first Python program
print("Hello, World!")
""",
    "Variables & Data Types": """# Variables and data types
name = "John"  # String
age = 30       # Integer
height = 5.9   # Float
is_student = True  # Boolean

print(f"Name: {name}, Age: {age}, Height: {height}, Student: {is_student}")
print("Type of name variable:", type(name))
""",
    "Lists": """# Working with lists
fruits = ["apple", "banana", "cherry"]
print("Original list:", fruits)

# Add an item
fruits.append("orange")
print("After append:", fruits)

# Access items
print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])

# Slice a list
print("First two fruits:", fruits[0:2])

# List comprehension
squared_numbers = [x**2 for x in range(1, 6)]
print("Squared numbers from 1-5:", squared_numbers)
""",
    "Conditionals": """# Conditional statements
age = 18

if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
else:
    print("Adult")

# Ternary operator (conditional expression)
message = "Can vote" if age >= 18 else "Cannot vote"
print(message)
""",
    "Loops": """# Loops in Python
# For loop
print("Counting with for loop:")
for i in range(1, 6):
    print(i, end=" ")
print()

# Looping through a list
fruits = ["apple", "banana", "cherry"]
print("Fruits with for loop:")
for fruit in fruits:
    print(fruit, end=" ")
print()

# While loop
print("Counting with while loop:")
count = 1
while count <= 5:
    print(count, end=" ")
    count += 1
print()
""",
    "Functions": """# Functions in Python
def greet(name):
    return f"Hello, {name}!"

# Function with default parameter
def greet_with_time(name, time_of_day="day"):
    return f"Good {time_of_day}, {name}!"

print(greet("Alice"))
print(greet_with_time("Bob", "morning"))
print(greet_with_time("Charlie"))  # Uses default parameter

# Function with multiple return values
def get_person_details():
    name = "Dave"
    age = 30
    country = "USA"
    return name, age, country

person_name, person_age, person_country = get_person_details()
print(f"{person_name} is {person_age} years old and from {person_country}")
"""
}

selected_example = st.selectbox("Select an example", list(code_examples.keys()))
st.code(code_examples[selected_example], language="python")

# Add a "Try it yourself" section with editable code
st.subheader("Try It Yourself")
st.write("Edit the code below and run it to see the results.")

user_code = st.text_area("Code Editor", value=code_examples[selected_example], height=200)

if st.button("Run Code"):
    try:
        # Create a file
        with open("temp_code.py", "w") as f:
            f.write(user_code)
        
        # Capture stdout
        import io
        import sys
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            exec(user_code)
        output = f.getvalue()
        
        # Display output
        st.subheader("Output:")
        st.code(output)
        
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        # Clean up
        if os.path.exists("temp_code.py"):
            os.remove("temp_code.py")

# Further resources
st.header("Additional Learning Tips")
st.markdown("""
### Tips for Beginners:

1. **Practice Regularly**: Coding is like a muscle - it needs regular exercise
2. **Follow the Learning Path**: Work through the resources in the recommended order
3. **Type the Code Yourself**: Don't just copy-paste; typing code helps you learn
4. **Experiment with Examples**: Try modifying code examples to see what happens
5. **Solve Coding Challenges**: Sites like LeetCode, HackerRank, and Codewars offer beginner-friendly problems
6. **Read Others' Code**: Look at open-source projects to learn best practices
7. **Join Communities**: Python has a friendly community on forums like Reddit's r/learnpython
8. **Build Small Projects**: Apply what you learn to simple, practical applications
9. **Be Patient**: Everyone struggles at first; programming takes time to master
10. **Have Fun**: Choose projects that interest you to stay motivated

### Free Online Practice Environments:
- [Python Tutor](http://pythontutor.com/) - Visualize code execution
- [Replit](https://replit.com/) - Write and run code in your browser
- [Google Colab](https://colab.research.google.com/) - Free Python notebook environment
""")

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Home"):
        st.switch_page("app_updated.py")
with cols[1]:
    if st.button("Next: Intermediate ➡️"):
        st.switch_page("pages/intermediate.py")
with cols[2]:
    if st.button("Go to Projects 🛠️"):
        st.switch_page("pages/projects.py")