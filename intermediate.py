import streamlit as st
import json
import utils
import os

# Page configuration
st.set_page_config(
    page_title="Intermediate Python Resources",
    page_icon="🚀",
    layout="wide"
)

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to track your progress.")
    st.stop()

# Load resources
resources = utils.load_resources()
intermediate_resources = [r for r in resources if r['level'] == 'intermediate']

# Header
st.title("🚀 Intermediate Python Resources")
st.write("""
Ready to take your Python skills to the next level? This section contains carefully selected free resources 
for intermediate Python developers who already understand the basics and want to deepen their knowledge.
""")

# Intermediate learning path
st.header("Learning Path for Intermediate Python")
st.write("""
Follow this learning path to enhance your Python programming skills:

1. **Advanced Data Structures** - Dive deeper into lists, dictionaries, sets, and tuples
2. **Object-Oriented Programming** - Master classes, inheritance, and encapsulation
3. **Functional Programming** - Learn about lambda functions, map, filter, and reduce
4. **Decorators & Generators** - Understand these powerful Python features
5. **File Handling & Context Managers** - Work with files efficiently
6. **Regular Expressions** - Parse and manipulate text with regex
7. **Working with APIs** - Connect to web services and parse JSON data
8. **Testing & Debugging** - Write tests and debug code effectively
9. **Virtual Environments & Package Management** - Manage dependencies properly
10. **Intermediate Projects** - Apply your skills to more complex challenges
""")

# Filter options
st.sidebar.header("Filter Resources")
resource_types = ["All Types"] + sorted(list(set([r['type'] for r in intermediate_resources])))
selected_type = st.sidebar.selectbox("Resource Type", resource_types)

if selected_type != "All Types":
    filtered_resources = [r for r in intermediate_resources if r['type'] == selected_type]
else:
    filtered_resources = intermediate_resources

# Tags filter
all_tags = []
for resource in intermediate_resources:
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
                    utils.save_user_progress(st.session_state.username, 
                                         st.session_state.resources_completed,
                                         st.session_state.current_level)
                    st.rerun()
            else:
                if st.button("Mark as Completed", key=f"complete_{resource['id']}"):
                    st.session_state.resources_completed.append(resource['id'])
                    utils.save_user_progress(st.session_state.username, 
                                         st.session_state.resources_completed,
                                         st.session_state.current_level)
                    st.rerun()
else:
    st.info("No resources match your filter criteria. Try adjusting your filters.")

# Level progression
st.header("Ready to Level Up?")
completed_resources = [r for r in intermediate_resources if r['id'] in st.session_state.resources_completed]
total_resources = len(intermediate_resources)
completion_percentage = len(completed_resources) / total_resources * 100 if total_resources > 0 else 0

st.write(f"You've completed {len(completed_resources)} out of {total_resources} intermediate resources ({completion_percentage:.1f}%).")

progress_bar = st.progress(completion_percentage / 100)

if completion_percentage >= 70:
    st.success("Congratulations! You've mastered intermediate Python concepts. You're ready to move on to advanced topics!")
    if st.session_state.current_level == "intermediate" and st.button("Move to Advanced Level"):
        st.session_state.current_level = "advanced"
        utils.save_user_progress(st.session_state.username, 
                             st.session_state.resources_completed,
                             st.session_state.current_level)
        st.success("Level updated! You are now at the advanced level.")
        st.balloons()
else:
    st.info(f"Complete at least 70% of intermediate resources to unlock the advanced level. You're at {completion_percentage:.1f}% now.")

# Code examples section
st.header("Intermediate Python Code Examples")

code_examples = {
    "List Comprehensions & Generator Expressions": """# List comprehension vs. generator expression
import sys

# List comprehension - creates full list in memory
list_comp = [x**2 for x in range(1000)]
print(f"List size in memory: {sys.getsizeof(list_comp)} bytes")
print(f"First 5 elements: {list_comp[:5]}")

# Generator expression - values generated on-demand
gen_exp = (x**2 for x in range(1000))
print(f"Generator size in memory: {sys.getsizeof(gen_exp)} bytes")
print(f"First 5 elements: {[next(gen_exp) for _ in range(5)]}")

# Multi-level comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened matrix: {flattened}")
""",
    "Object-Oriented Programming": """# Object-Oriented Programming in Python
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        
    def make_sound(self):
        print("Some generic animal sound")
        
    def __str__(self):
        return f"{self.name} is a {self.species}"

# Inheritance
class Dog(Animal):
    def __init__(self, name, breed):
        # Call the parent class's __init__ method
        super().__init__(name, species="Dog")
        self.breed = breed
        
    def make_sound(self):
        print("Woof!")
        
    def fetch(self, item):
        print(f"{self.name} fetched the {item}!")

# Create instances
generic_animal = Animal("Generic", "Animal")
print(generic_animal)
generic_animal.make_sound()

dog = Dog("Buddy", "Golden Retriever")
print(dog)
print(f"Breed: {dog.breed}")
dog.make_sound()
dog.fetch("ball")

# Check instance relationships
print(f"Is dog an Animal? {isinstance(dog, Animal)}")
print(f"Is dog a Dog? {isinstance(dog, Dog)}")
""",
    "Decorators": """# Python Decorators

# A simple decorator
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Call the decorated function
say_hello()

# Decorator with parameters
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
    return name

# Call the decorated function with parameters
greet("Alice")

# Class as a decorator
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
        
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hi():
    print("Hi!")

# Call the function several times
say_hi()
say_hi()
say_hi()
""",
    "Context Managers": """# Context Managers in Python

# Using a file with a context manager
with open("example.txt", "w") as f:
    f.write("Hello, World!")
    # File is automatically closed after the block

# Creating a custom context manager using a class
class MyContext:
    def __init__(self, name):
        self.name = name
        
    def __enter__(self):
        print(f"Entering context: {self.name}")
        return self  # Returns the context object
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting context: {self.name}")
        # Return True to suppress exceptions
        # Return False or None to let exceptions propagate
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
        return False

# Using the custom context manager
with MyContext("test") as ctx:
    print(f"Inside context: {ctx.name}")
    
# Context manager using contextlib
from contextlib import contextmanager

@contextmanager
def my_context(name):
    print(f"Entering context: {name}")
    try:
        yield name  # Yield value is what's assigned to the 'as' variable
        print(f"Exiting context normally: {name}")
    except Exception as e:
        print(f"Exiting context with error: {name}, {e}")
        # Re-raise the exception
        raise

# Using the function-based context manager
with my_context("function-based") as name:
    print(f"Inside context: {name}")
""",
    "Working with APIs": """# Working with APIs in Python
import requests
import json

# Making a GET request
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(f"Status code: {response.status_code}")

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    print("JSON Response:")
    print(f"Title: {data['title']}")
    print(f"Body: {data['body']}")
else:
    print(f"Request failed with status code {response.status_code}")

# Making a POST request
new_post = {
    "title": "New Post",
    "body": "This is the content of the new post.",
    "userId": 1
}

post_response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post  # Automatically converts dict to JSON
)

print(f"POST Status code: {post_response.status_code}")
if post_response.status_code in (200, 201):
    created_post = post_response.json()
    print(f"Created post with ID: {created_post['id']}")

# Using query parameters
params = {
    "userId": 1
}

filtered_response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params=params
)

if filtered_response.status_code == 200:
    posts = filtered_response.json()
    print(f"Found {len(posts)} posts by user 1")
""",
    "Functional Programming": """# Functional Programming in Python

# Lambda functions (anonymous functions)
square = lambda x: x**2
print(f"Square of 5: {square(5)}")

# Using map() to apply a function to all items in a list
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(f"Squared numbers: {squared}")

# Using filter() to filter items based on a condition
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")

# Using reduce() to apply a function to all items and get a single result
from functools import reduce
product = reduce(lambda x, y: x * y, numbers)
print(f"Product of all numbers: {product}")

# Higher-order functions (functions that take or return functions)
def create_adder(x):
    return lambda y: x + y

add_5 = create_adder(5)
print(f"5 + 3 = {add_5(3)}")

# Partial application
from functools import partial

def multiply(x, y):
    return x * y

double = partial(multiply, 2)  # Fix first parameter to 2
triple = partial(multiply, 3)  # Fix first parameter to 3

print(f"Double 7: {double(7)}")
print(f"Triple 7: {triple(7)}")
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
st.header("Intermediate Python Tips")
st.markdown("""
### Tips for Intermediate Python Developers:

1. **Read Open Source Code**: Study how experienced developers structure their code
2. **Explore the Standard Library**: Python's standard library is vast and powerful
3. **Learn Design Patterns**: Understand common design patterns and their Python implementations
4. **Write Documentation**: Document your code with docstrings and comments
5. **Explore Different Programming Paradigms**: Try functional programming alongside OOP
6. **Contribute to Open Source**: Start contributing to projects you use
7. **Profile Your Code**: Learn to use profiling tools to identify bottlenecks
8. **Learn Testing Frameworks**: Master pytest or unittest for effective testing
9. **Focus on Pythonic Code**: Learn Python idioms to write cleaner, more efficient code
10. **Build Real Projects**: Apply your knowledge to solve real-world problems

### Recommended Free Tools:
- [PyCharm Community Edition](https://www.jetbrains.com/pycharm/) - Professional Python IDE
- [Visual Studio Code](https://code.visualstudio.com/) - Lightweight, extensible editor
- [Python Tutor](http://pythontutor.com/) - Visualize code execution
- [GitHub](https://github.com/) - Host your projects and collaborate
- [Travis CI](https://travis-ci.org/) - Continuous integration for your projects
""")

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Beginner"):
        st.switch_page("pages/beginner.py")
with cols[1]:
    if st.button("Next: Advanced ➡️"):
        st.switch_page("pages/advanced.py")
with cols[2]:
    if st.button("Go to Projects 🛠️"):
        st.switch_page("pages/projects.py")
