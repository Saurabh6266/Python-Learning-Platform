import streamlit as st
import json
import utils
import os

# Page configuration
st.set_page_config(
    page_title="Advanced Python Resources",
    page_icon="🔥",
    layout="wide"
)

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to track your progress.")
    st.stop()

# Load resources
resources = utils.load_resources()
advanced_resources = [r for r in resources if r['level'] == 'advanced']

# Header
st.title("🔥 Advanced Python Resources")
st.write("""
Take your Python mastery to expert level with these carefully selected free resources.
These materials cover advanced topics and specialized domains for experienced Python developers.
""")

# Advanced learning path
st.header("Learning Path for Advanced Python")
st.write("""
Follow this learning path to reach expert-level Python proficiency:

1. **Advanced Object-Oriented Programming** - Metaclasses, descriptors, and deep inheritance
2. **Metaprogramming** - Code that writes code
3. **Advanced Concurrency** - Threading, multiprocessing, async/await, and GIL management
4. **Performance Optimization** - Profiling, caching, and optimizing Python code
5. **C Extensions** - Interfacing Python with C/C++
6. **Design Patterns & Architecture** - Advanced software design patterns in Python
7. **Python Internals** - Understanding CPython implementation details
8. **Advanced Web Frameworks** - Deep dive into Flask, Django, or FastAPI
9. **Machine Learning & Data Science** - Specialized Python applications
10. **Advanced Projects** - Build complex, production-ready applications
""")

# Filter options
st.sidebar.header("Filter Resources")
resource_types = ["All Types"] + sorted(list(set([r['type'] for r in advanced_resources])))
selected_type = st.sidebar.selectbox("Resource Type", resource_types)

if selected_type != "All Types":
    filtered_resources = [r for r in advanced_resources if r['type'] == selected_type]
else:
    filtered_resources = advanced_resources

# Tags filter
all_tags = []
for resource in advanced_resources:
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
st.header("Python Mastery")
completed_resources = [r for r in advanced_resources if r['id'] in st.session_state.resources_completed]
total_resources = len(advanced_resources)
completion_percentage = len(completed_resources) / total_resources * 100 if total_resources > 0 else 0

st.write(f"You've completed {len(completed_resources)} out of {total_resources} advanced resources ({completion_percentage:.1f}%).")

progress_bar = st.progress(completion_percentage / 100)

if completion_percentage >= 70:
    st.success("Congratulations! You've reached Python mastery! Continue exploring specialized areas or share your knowledge with others.")
    st.balloons()
else:
    st.info(f"Complete at least 70% of advanced resources to achieve Python mastery. You're at {completion_percentage:.1f}% now.")

# Code examples section
st.header("Advanced Python Code Examples")

code_examples = {
    "Metaclasses": """# Metaclasses in Python
class Meta(type):
    def __new__(cls, name, bases, attrs):
        # Add a new attribute to the class
        attrs['added_by_meta'] = 'This attribute was added by the metaclass'
        
        # Print all methods being defined
        print(f"Creating class: {name}")
        for key, value in attrs.items():
            if callable(value) and not key.startswith('__'):
                print(f"Method defined: {key}")
        
        # Create and return the new class
        return super().__new__(cls, name, bases, attrs)
    
    def __init__(cls, name, bases, attrs):
        print(f"Initializing class: {name}")
        super().__init__(name, bases, attrs)

class MyClass(metaclass=Meta):
    def method1(self):
        return "This is method1"
    
    def method2(self):
        return "This is method2"

# Create an instance of MyClass
obj = MyClass()
print(f"Does obj have the attribute added by Meta? {'added_by_meta' in dir(obj)}")
print(f"Value of the attribute: {obj.added_by_meta}")

# Demonstrate practical use: Registry pattern
class PluginRegistry(type):
    plugins = {}
    
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        if name != 'Plugin':  # Don't register the base Plugin class
            cls.plugins[name] = new_cls
        return new_cls

class Plugin(metaclass=PluginRegistry):
    def process(self, data):
        raise NotImplementedError("All plugins must implement process method")

class TextPlugin(Plugin):
    def process(self, data):
        return f"Processing text: {data.upper()}"

class NumberPlugin(Plugin):
    def process(self, data):
        return f"Processing number: {data * 2}"

# Access the plugin registry
print(f"Available plugins: {list(PluginRegistry.plugins.keys())}")
text_processor = PluginRegistry.plugins['TextPlugin']()
print(text_processor.process("hello world"))
""",
    "Descriptors": """# Descriptors in Python
class Validator:
    def __init__(self, name, min_value=None, max_value=None):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
    
    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be at least {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be at most {self.max_value}")
        instance.__dict__[self.name] = value
        
    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Person:
    age = Validator('age', min_value=0, max_value=120)
    height = Validator('height', min_value=0)
    weight = Validator('weight', min_value=0)
    
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
    
    def __str__(self):
        return f"{self.name}, Age: {self.age}, Height: {self.height}cm, Weight: {self.weight}kg"

# Create a person
try:
    person = Person("John", 30, 180, 75)
    print(person)
    
    # Try to set an invalid age
    print("Trying to set age to -5...")
    person.age = -5
except ValueError as e:
    print(f"Error: {e}")

# Create another person with invalid parameters
try:
    print("Creating person with age 150...")
    invalid_person = Person("Invalid", 150, 180, 75)
except ValueError as e:
    print(f"Error: {e}")

# Property-based implementation of a descriptor
class Temperature:
    def __init__(self):
        self._celsius = 0
        
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# Test the Temperature class
temp = Temperature()
print(f"Default temperature: {temp.celsius}°C, {temp.fahrenheit}°F")

temp.celsius = 25
print(f"After setting to 25°C: {temp.celsius}°C, {temp.fahrenheit}°F")

temp.fahrenheit = 68
print(f"After setting to 68°F: {temp.celsius}°C, {temp.fahrenheit}°F")

try:
    temp.celsius = -300
except ValueError as e:
    print(f"Error: {e}")
""",
    "Async Programming": """# Asynchronous Programming in Python
import asyncio
import time

async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message)
    return message

async def main():
    print(f"Started at {time.strftime('%X')}")
    
    # Sequential execution
    print("Running sequentially:")
    start = time.time()
    
    result1 = await say_after(1, "Hello")
    result2 = await say_after(2, "World")
    
    print(f"Sequential results: {result1} {result2}")
    print(f"Sequential execution took {time.time() - start:.2f} seconds")
    
    # Concurrent execution
    print("\\nRunning concurrently:")
    start = time.time()
    
    task1 = asyncio.create_task(say_after(1, "Hello"))
    task2 = asyncio.create_task(say_after(2, "World"))
    
    # Wait for both tasks to complete
    await asyncio.gather(task1, task2)
    
    print(f"Concurrent execution took {time.time() - start:.2f} seconds")
    
    # Waiting for multiple tasks with timeout
    print("\\nRunning with timeout:")
    start = time.time()
    
    task3 = asyncio.create_task(say_after(1, "Quick task"))
    task4 = asyncio.create_task(say_after(5, "Slow task"))
    
    try:
        await asyncio.wait_for(asyncio.gather(task3, task4), timeout=3)
        print("Both tasks completed within timeout")
    except asyncio.TimeoutError:
        print("Timeout occurred before all tasks completed")
        # The slow task is still running, we can cancel it
        task4.cancel()
        try:
            await task4
        except asyncio.CancelledError:
            print("Slow task was cancelled")
    
    print(f"Execution with timeout took {time.time() - start:.2f} seconds")
    
    # Demonstrating asyncio.gather with different return modes
    print("\\nUsing asyncio.gather with error handling:")
    
    async def successful_task():
        await asyncio.sleep(1)
        return "Success"
    
    async def failing_task():
        await asyncio.sleep(0.5)
        raise ValueError("Task failed deliberately")
    
    # With return_exceptions=True, exceptions are returned rather than raised
    results = await asyncio.gather(
        successful_task(),
        failing_task(),
        return_exceptions=True
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1} failed with: {result}")
        else:
            print(f"Task {i+1} succeeded with: {result}")
    
    print(f"Finished at {time.strftime('%X')}")

# Run the main coroutine
asyncio.run(main())
""",
    "Context Variables": """# Context Variables in Python (Python 3.7+)
import contextvars
import asyncio

# Create a context variable with a default value
request_id = contextvars.ContextVar('request_id', default='unknown')

# Function that accesses the context variable
def get_request_info():
    return f"Processing request: {request_id.get()}"

# Asynchronous function that uses context variables
async def process_request(request_number):
    # Set context variable for this specific request
    token = request_id.set(f"request-{request_number}")
    try:
        print(f"Starting {get_request_info()}")
        # Simulate some async work
        await asyncio.sleep(0.5)
        print(f"Finishing {get_request_info()}")
        return get_request_info()
    finally:
        # Reset the context variable to its previous value
        request_id.reset(token)

async def main():
    # Show the default value
    print(f"Default request ID: {request_id.get()}")
    
    # Process multiple requests concurrently
    # Each will have its own context
    tasks = [process_request(i) for i in range(1, 4)]
    results = await asyncio.gather(*tasks)
    
    # The context variable should be back to its default value
    print(f"After processing, request ID: {request_id.get()}")
    
    # Show results
    print("Results:")
    for result in results:
        print(f"  {result}")
    
    # Demonstrate contextvars.copy_context()
    print("\\nDemonstrating context copying:")
    
    # Create a new context with a specific value
    request_id.set("special-request")
    ctx = contextvars.copy_context()
    
    # Change the current context
    request_id.set("changed-after-copy")
    
    # Original context is preserved in ctx
    print(f"Current context: {request_id.get()}")
    print(f"Copied context: {ctx.get(request_id)}")
    
    # Run a function in the copied context
    def show_id():
        print(f"Inside function: {request_id.get()}")
    
    ctx.run(show_id)

asyncio.run(main())
""",
    "Advanced Generators": """# Advanced Generators in Python

# Generator function with send() and yield from
def echo_generator():
    print("Starting echo generator")
    received = yield "Generator ready"
    while True:
        value_to_yield = f"Echo: {received}"
        try:
            received = yield value_to_yield
        except GeneratorExit:
            print("Generator received exit signal")
            break
        except Exception as e:
            print(f"Generator caught exception: {e}")
            received = f"Error occurred: {e}"

# Using the generator
print("Basic generator usage:")
gen = echo_generator()
initial = next(gen)  # Prime the generator
print(f"Initial value: {initial}")

echo1 = gen.send("Hello")
print(f"First echo: {echo1}")

echo2 = gen.send("World")
print(f"Second echo: {echo2}")

# Throwing an exception into the generator
try:
    echo3 = gen.throw(ValueError("Custom error"))
    print(f"After throw: {echo3}")
except Exception as e:
    print(f"Exception propagated: {e}")

# Closing the generator
gen.close()

# Generator expression with filtering
print("\nGenerator expression with filtering:")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = (x**2 for x in numbers if x % 2 == 0)

print("Even squares:", end=" ")
for square in even_squares:
    print(square, end=" ")
print()

# Subgenerator with yield from
def subgen():
    yield "Subgenerator value 1"
    yield "Subgenerator value 2"
    return "Subgenerator return value"

def delegating_gen():
    print("Delegating generator started")
    # yield from delegates to the subgenerator
    result = yield from subgen()
    print(f"Subgenerator returned: {result}")
    yield "Delegating generator value"

print("\nDemonstrating yield from:")
for item in delegating_gen():
    print(f"Main loop received: {item}")

# Pipeline of generators
def producer():
    for i in range(5):
        yield i

def square(numbers):
    for number in numbers:
        yield number ** 2

def negative(numbers):
    for number in numbers:
        yield -number

print("\nGenerator pipeline:")
# Create a pipeline of generator functions
pipeline = negative(square(producer()))
for result in pipeline:
    print(result)
""",
    "Python Internals": """# Python Internals: Exploring Python's internals

import sys
import dis
import inspect
import types

# Examine Python's compilation process
def show_bytecode(func):
    print(f"Disassembly of {func.__name__}:")
    dis.dis(func)
    print()

# Example function to disassemble
def example_function(x, y):
    result = x + y
    for i in range(result):
        if i % 2 == 0:
            print(f"{i} is even")
    return result

# Show bytecode
show_bytecode(example_function)

# Examining function attributes
print(f"Function name: {example_function.__name__}")
print(f"Function docstring: {example_function.__doc__}")
print(f"Function module: {example_function.__module__}")
print(f"Function annotations: {example_function.__annotations__}")
print(f"Function defaults: {example_function.__defaults__}")

# Inspect function signature
sig = inspect.signature(example_function)
print(f"Function signature: {sig}")
print(f"Parameters: {list(sig.parameters.items())}")

# Create a function dynamically
print("\nCreating a function dynamically:")

# Create function code
code = compile("result = a + b", "<string>", "exec")

# Create a function object from code
def create_dynamic_function(code_obj, params):
    # We need to create a new code object with the appropriate parameters
    # This is a simplified version; in a real case, you'd use the code object's
    # attributes to create a new code object with different parameters
    
    # For simplicity, create a function with eval instead
    func_def = f"def dynamic_func({', '.join(params)}):\n    result = {' + '.join(params)}\n    return result"
    namespace = {}
    exec(func_def, namespace)
    return namespace["dynamic_func"]

# Create and test our dynamic function
dynamic_add = create_dynamic_function(code, ["a", "b"])
print(f"Result of dynamic_add(5, 3): {dynamic_add(5, 3)}")
show_bytecode(dynamic_add)

# Examining the call stack
def level3():
    frame = sys._getframe()
    print("Call stack (innermost last):")
    depth = 0
    while frame:
        func_name = frame.f_code.co_name
        line_num = frame.f_lineno
        file_name = frame.f_code.co_filename
        print(f"  Depth {depth}: {func_name} at line {line_num} in {file_name}")
        frame = frame.f_back
        depth += 1

def level2():
    level3()

def level1():
    level2()

# Call the nested functions to show the stack
level1()

# Understanding memory management and object lifecycle
import gc

# Track object creation and destruction
class TrackingObject:
    def __init__(self, name):
        self.name = name
        print(f"Created {self.name}")
    
    def __del__(self):
        print(f"Destroyed {self.name}")

# Create objects with circular references
print("\nDemonstrating garbage collection:")
a = TrackingObject("Object A")
b = TrackingObject("Object B")

# Create circular reference
a.ref = b
b.ref = a

# Remove original references
print("Removing references...")
a = None
b = None

# Force garbage collection
print("Running garbage collection...")
gc.collect()

# Show number of tracked objects
print(f"Objects tracked by GC: {gc.get_count()}")
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
st.header("Advanced Python Developer Tips")
st.markdown("""
### Tips for Advanced Python Developers:

1. **Master the Python C API**: Understand how to extend Python with C/C++
2. **Explore Python's Design Decisions**: Read PEPs to understand why Python works the way it does
3. **Contribute to Core Python**: Consider contributing to CPython or other implementations
4. **Learn Multiple Python Implementations**: Try PyPy, Jython, or IronPython to understand differences
5. **Benchmark and Profile**: Become an expert at optimizing Python performance
6. **Share Your Knowledge**: Write blogs, create tutorials, and mentor others
7. **Focus on Maintainability**: Write code that others (including future you) can understand
8. **Stay Current**: Follow Python's development and new features
9. **Explore Language Internals**: Study and understand Python's object model and evaluation model
10. **Build Advanced Frameworks**: Design your own tools and frameworks for others to use

### Recommended Free Tools for Advanced Developers:
- [PyPI](https://pypi.org/) - Share your packages with the Python community
- [ReadTheDocs](https://readthedocs.org/) - Host comprehensive documentation
- [Coverage.py](https://coverage.readthedocs.io/) - Track code coverage for testing
- [Sphinx](https://www.sphinx-doc.org/) - Create professional documentation
- [Black](https://black.readthedocs.io/) - Uncompromising Python code formatter
""")

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Intermediate"):
        st.switch_page("pages/intermediate.py")
with cols[1]:
    if st.button("View Progress 📊"):
        st.switch_page("pages/progress.py")
with cols[2]:
    if st.button("Go to Projects 🛠️"):
        st.switch_page("pages/projects.py")
