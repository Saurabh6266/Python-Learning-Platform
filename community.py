import streamlit as st
import json
import os
from datetime import datetime
import utils

# Page configuration
st.set_page_config(
    page_title="Python Learning Community",
    page_icon="💬",
    layout="wide"
)

# Initialize discussion data
DISCUSSIONS_FILE = "data/discussions.json"
os.makedirs("data", exist_ok=True)

# Helper functions for discussions
def load_discussions():
    if not os.path.exists(DISCUSSIONS_FILE):
        with open(DISCUSSIONS_FILE, 'w') as f:
            json.dump({"topics": []}, f)
    try:
        with open(DISCUSSIONS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading discussions: {e}")
        return {"topics": []}

def save_discussions(discussions):
    try:
        with open(DISCUSSIONS_FILE, 'w') as f:
            json.dump(discussions, f, indent=4)
    except Exception as e:
        st.error(f"Error saving discussions: {e}")

def add_topic(title, content, author, category):
    discussions = load_discussions()
    topic_id = len(discussions["topics"]) + 1
    
    new_topic = {
        "id": topic_id,
        "title": title,
        "content": content,
        "author": author,
        "category": category,
        "created_at": datetime.now().isoformat(),
        "replies": []
    }
    
    discussions["topics"].append(new_topic)
    save_discussions(discussions)
    return topic_id

def add_reply(topic_id, content, author):
    discussions = load_discussions()
    topic = next((t for t in discussions["topics"] if t["id"] == topic_id), None)
    
    if topic:
        reply_id = len(topic["replies"]) + 1
        new_reply = {
            "id": reply_id,
            "content": content,
            "author": author,
            "created_at": datetime.now().isoformat()
        }
        topic["replies"].append(new_reply)
        save_discussions(discussions)
        return True
    return False

# Page header
st.title("💬 Python Learning Community")
st.write("""
Connect with fellow Python learners, ask questions, share your projects, and discuss Python topics.
This community forum is a place to enhance your learning through collaboration and knowledge sharing.
""")

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to participate in the community.")
    
    # Show read-only view of discussions
    st.header("Recent Discussions")
    st.info("You can browse discussions, but you need to log in to participate.")
    
    discussions = load_discussions()
    if discussions["topics"]:
        for topic in sorted(discussions["topics"], key=lambda t: t["created_at"], reverse=True)[:5]:
            with st.expander(f"{topic['title']} (by {topic['author']})"):
                st.write(f"**Category**: {topic['category']}")
                st.write(topic['content'])
                st.write(f"Posted on: {datetime.fromisoformat(topic['created_at']).strftime('%Y-%m-%d %H:%M')}")
                
                if topic["replies"]:
                    st.write(f"**Replies ({len(topic['replies'])}):**")
                    for reply in topic["replies"]:
                        st.markdown(f"**{reply['author']}** - {datetime.fromisoformat(reply['created_at']).strftime('%Y-%m-%d %H:%M')}")
                        st.markdown(f"> {reply['content']}")
                        st.markdown("---")
    else:
        st.info("No discussions yet. Be the first to start a topic!")
    
    st.stop()

# Main community features
username = st.session_state.username

# Sidebar with options
st.sidebar.header("Community Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Discussion Forum", "Study Groups", "Project Showcase", "Learning Resources", "Community Guidelines"]
)

# Load discussions
discussions = load_discussions()

if page == "Discussion Forum":
    st.header("Discussion Forum")
    
    # Topic creation form in an expander
    with st.expander("Create a New Topic"):
        topic_title = st.text_input("Topic Title")
        topic_category = st.selectbox(
            "Category",
            ["General Python", "Beginner Questions", "Intermediate Concepts", 
             "Advanced Topics", "Project Help", "Career Advice", "Learning Resources"]
        )
        topic_content = st.text_area("Content", height=150)
        
        if st.button("Post Topic"):
            if topic_title and topic_content:
                add_topic(topic_title, topic_content, username, topic_category)
                st.success("Topic posted successfully!")
                st.rerun()
            else:
                st.error("Please provide both a title and content.")
    
    # Filter topics
    st.subheader("Browse Discussions")
    
    # Get all categories
    all_categories = sorted(list(set([t["category"] for t in discussions["topics"]])))
    selected_category = st.selectbox("Filter by Category", ["All Categories"] + all_categories)
    
    # Apply filter
    filtered_topics = discussions["topics"]
    if selected_category != "All Categories":
        filtered_topics = [t for t in filtered_topics if t["category"] == selected_category]
    
    # Sort by latest
    filtered_topics = sorted(filtered_topics, key=lambda t: t["created_at"], reverse=True)
    
    # Display topics
    if filtered_topics:
        for topic in filtered_topics:
            with st.expander(f"{topic['title']} (by {topic['author']})"):
                st.write(f"**Category**: {topic['category']}")
                st.write(topic['content'])
                st.write(f"Posted on: {datetime.fromisoformat(topic['created_at']).strftime('%Y-%m-%d %H:%M')}")
                
                # Display replies
                if topic["replies"]:
                    st.write(f"**Replies ({len(topic['replies'])}):**")
                    for reply in topic["replies"]:
                        st.markdown(f"**{reply['author']}** - {datetime.fromisoformat(reply['created_at']).strftime('%Y-%m-%d %H:%M')}")
                        st.markdown(f"> {reply['content']}")
                        st.markdown("---")
                
                # Reply form
                reply_content = st.text_area("Your Reply", key=f"reply_{topic['id']}", height=100)
                if st.button("Post Reply", key=f"reply_button_{topic['id']}"):
                    if reply_content:
                        if add_reply(topic['id'], reply_content, username):
                            st.success("Reply posted successfully!")
                            st.rerun()
                    else:
                        st.error("Please provide a reply.")
    else:
        st.info("No topics found in this category. Be the first to create one!")

elif page == "Study Groups":
    st.header("Python Study Groups")
    
    st.write("""
    Join or create study groups to learn Python together with others at your level.
    Study groups are a great way to stay motivated and learn collaboratively.
    """)
    
    # Display available study groups
    st.subheader("Available Study Groups")
    
    study_groups = [
        {
            "name": "Beginner Python Basics",
            "description": "A group for absolute beginners to learn Python fundamentals together",
            "level": "beginner",
            "meeting_time": "Saturdays, 10:00 AM UTC",
            "members": 15
        },
        {
            "name": "Data Science with Python",
            "description": "Working through data science projects and learning pandas, numpy, and matplotlib",
            "level": "intermediate",
            "meeting_time": "Wednesdays, 6:00 PM UTC",
            "members": 12
        },
        {
            "name": "Advanced Python Concepts",
            "description": "Deep dive into advanced Python features, design patterns, and optimization",
            "level": "advanced",
            "meeting_time": "Tuesdays, 8:00 PM UTC",
            "members": 8
        },
        {
            "name": "Web Development with Flask",
            "description": "Building web applications using Flask framework",
            "level": "intermediate",
            "meeting_time": "Mondays, 7:00 PM UTC",
            "members": 10
        }
    ]
    
    # Filter by level
    user_level = st.session_state.current_level
    st.write(f"Showing study groups relevant to your level: **{user_level.capitalize()}**")
    
    # Display groups
    for group in study_groups:
        if group["level"] == user_level or st.checkbox("Show all levels", value=False):
            with st.expander(f"{group['name']} ({group['level'].capitalize()})"):
                st.write(f"**Description**: {group['description']}")
                st.write(f"**Meeting Time**: {group['meeting_time']}")
                st.write(f"**Members**: {group['members']}")
                
                if st.button("Join Group", key=f"join_{group['name']}"):
                    st.success(f"You've joined the {group['name']} study group! Check your email for meeting details.")
    
    # Create new study group
    st.subheader("Create a New Study Group")
    st.write("Want to start your own study group? Fill out the form below:")
    
    col1, col2 = st.columns(2)
    with col1:
        group_name = st.text_input("Group Name")
        group_level = st.selectbox("Group Level", ["beginner", "intermediate", "advanced"])
    with col2:
        group_desc = st.text_input("Description")
        group_time = st.text_input("Meeting Time (e.g., Mondays, 7:00 PM UTC)")
    
    if st.button("Create Study Group"):
        if group_name and group_desc and group_time:
            st.success(f"Study group '{group_name}' created! Others can now join your group.")
        else:
            st.error("Please fill out all fields.")
    
    # Study group tips
    st.subheader("Study Group Tips")
    st.markdown("""
    ### Effective Study Group Practices:
    
    1. **Set Clear Goals**: Define what you want to achieve in each session
    2. **Prepare Materials**: Share resources, code examples, or exercises before meeting
    3. **Take Turns Leading**: Let different members lead discussions on topics they're comfortable with
    4. **Code Together**: Use pair programming or collaborative coding platforms
    5. **Document Your Progress**: Keep notes of what you've learned and questions for next time
    6. **Be Consistent**: Regular meetings help build momentum in learning
    7. **Welcome All Questions**: Create a supportive environment where no question is too basic
    8. **Share Challenges**: Discuss problems you've encountered and solve them together
    """)

elif page == "Project Showcase":
    st.header("Project Showcase")
    
    st.write("""
    Share your Python projects with the community and get feedback from other learners.
    You can also explore projects created by others for inspiration.
    """)
    
    # Project submission form
    with st.expander("Submit Your Project"):
        project_title = st.text_input("Project Title")
        project_desc = st.text_area("Project Description", height=100)
        project_code = st.text_area("Code Sample (optional)", height=200)
        project_link = st.text_input("GitHub/Project Link (optional)")
        project_level = st.selectbox("Project Level", ["beginner", "intermediate", "advanced"])
        
        if st.button("Submit Project"):
            if project_title and project_desc:
                st.success("Project submitted successfully! It will appear in the showcase after review.")
            else:
                st.error("Please provide at least a title and description.")
    
    # Display featured projects
    st.subheader("Featured Projects")
    
    featured_projects = [
        {
            "title": "Weather Data Dashboard",
            "author": "PythonLearner123",
            "description": "A web application that fetches weather data from an API and displays it in an interactive dashboard using Streamlit.",
            "level": "intermediate",
            "link": "https://github.com/example/weather-dashboard",
            "likes": 24
        },
        {
            "title": "Beginner's Text Adventure Game",
            "author": "CodeNewbie",
            "description": "A text-based adventure game with multiple endings, implemented using Python's basic control structures.",
            "level": "beginner",
            "link": "https://github.com/example/text-adventure",
            "likes": 15
        },
        {
            "title": "Advanced NLP Sentiment Analyzer",
            "author": "AIEnthusiast",
            "description": "A sentiment analysis tool using advanced NLP techniques with spaCy and transformer models.",
            "level": "advanced",
            "link": "https://github.com/example/sentiment-analyzer",
            "likes": 42
        }
    ]
    
    for project in featured_projects:
        with st.expander(f"{project['title']} by {project['author']} ({project['level'].capitalize()})"):
            st.write(f"**Description**: {project['description']}")
            if project["link"]:
                st.write(f"**Project Link**: [{project['link']}]({project['link']})")
            st.write(f"**Likes**: {project['likes']}")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("❤️", key=f"like_{project['title']}"):
                    st.success("You liked this project!")
            with col2:
                if st.button("Leave feedback", key=f"feedback_{project['title']}"):
                    feedback = st.text_area("Your feedback", key=f"feedback_text_{project['title']}")
                    if st.button("Submit Feedback", key=f"submit_feedback_{project['title']}"):
                        if feedback:
                            st.success("Feedback submitted!")
                        else:
                            st.error("Please write your feedback.")
    
    # Community project ideas
    st.subheader("Looking for Project Ideas?")
    st.markdown("""
    Here are some project ideas you can work on:
    
    ### Beginner Level:
    - **Todo List Application**: Create a simple command-line or GUI todo list app
    - **Password Generator**: Build a program that generates strong passwords
    - **Quiz Game**: Develop a multiple-choice quiz on a topic you're interested in
    
    ### Intermediate Level:
    - **Personal Blog**: Create a blog website using Flask or Django
    - **Data Visualization Dashboard**: Build an interactive dashboard for analyzing datasets
    - **Web Scraper**: Develop a tool to extract information from websites
    
    ### Advanced Level:
    - **Machine Learning Recommendation System**: Build a system that recommends content based on user preferences
    - **Real-time Chat Application**: Create a chat app with websockets and encryption
    - **Automated Trading Bot**: Develop a bot that analyzes market data and simulates trading decisions
    """)

elif page == "Learning Resources":
    st.header("Community Learning Resources")
    
    st.write("""
    Discover community-curated resources and learning materials that complement our main learning paths.
    Members can share useful links, tutorials, videos, and other resources they've found helpful.
    """)
    
    # Add a resource form
    with st.expander("Share a Resource"):
        resource_title = st.text_input("Resource Title")
        resource_url = st.text_input("URL")
        resource_desc = st.text_area("Description", height=100)
        resource_type = st.selectbox("Resource Type", 
                                    ["Tutorial", "Video", "Article", "Book", "Tool", "Cheat Sheet", "Documentation", "Course", "Other"])
        resource_level = st.selectbox("Level", ["beginner", "intermediate", "advanced", "all levels"])
        
        if st.button("Share Resource"):
            if resource_title and resource_url and resource_desc:
                st.success("Resource shared successfully! It will be available after review.")
            else:
                st.error("Please fill out all required fields.")
    
    # Filter options
    st.subheader("Browse Community Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox("Filter by Type", ["All Types", "Tutorial", "Video", "Article", "Book", "Tool", "Cheat Sheet", "Documentation", "Course", "Other"])
    with col2:
        filter_level = st.selectbox("Filter by Level", ["All Levels", "beginner", "intermediate", "advanced"])
    
    # Community shared resources
    community_resources = [
        {
            "title": "Real Python - Python's Conditional Expressions",
            "url": "https://realpython.com/python-conditional-statements/",
            "description": "A comprehensive guide to conditional statements in Python with practical examples.",
            "type": "Tutorial",
            "level": "beginner",
            "shared_by": "PythonFan42",
            "upvotes": 18
        },
        {
            "title": "Corey Schafer's Python OOP Tutorials",
            "url": "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc",
            "description": "Excellent video series explaining object-oriented programming in Python from basics to advanced concepts.",
            "type": "Video",
            "level": "intermediate",
            "shared_by": "CodeMaster",
            "upvotes": 32
        },
        {
            "title": "Python Concurrency: The Tricky Bits",
            "url": "https://python.hamel.dev/concurrency/",
            "description": "In-depth article about Python's concurrency models with threading, multiprocessing, and asyncio.",
            "type": "Article",
            "level": "advanced",
            "shared_by": "AsyncDev",
            "upvotes": 24
        },
        {
            "title": "Python Testing with pytest",
            "url": "https://pragprog.com/titles/bopytest/python-testing-with-pytest/",
            "description": "Comprehensive guide to testing Python applications with pytest framework.",
            "type": "Book",
            "level": "intermediate",
            "shared_by": "TestEngineer",
            "upvotes": 15
        },
        {
            "title": "Python Cheat Sheet for Beginners",
            "url": "https://www.pythoncheatsheet.org/",
            "description": "Handy reference for Python syntax and common operations - perfect for beginners!",
            "type": "Cheat Sheet",
            "level": "beginner",
            "shared_by": "HelpfulCoder",
            "upvotes": 45
        }
    ]
    
    # Apply filters
    filtered_resources = community_resources
    if filter_type != "All Types":
        filtered_resources = [r for r in filtered_resources if r["type"] == filter_type]
    if filter_level != "All Levels":
        filtered_resources = [r for r in filtered_resources if r["level"] == filter_level]
    
    # Sort by upvotes
    filtered_resources = sorted(filtered_resources, key=lambda r: r["upvotes"], reverse=True)
    
    # Display resources
    if filtered_resources:
        for resource in filtered_resources:
            with st.expander(f"{resource['title']} ({resource['type']})"):
                st.write(f"**Description**: {resource['description']}")
                st.write(f"**Level**: {resource['level'].capitalize()}")
                st.write(f"**Shared by**: {resource['shared_by']}")
                st.write(f"**Link**: [{resource['url']}]({resource['url']})")
                st.write(f"**Upvotes**: {resource['upvotes']}")
                
                if st.button("Upvote", key=f"upvote_{resource['title']}"):
                    st.success("Upvoted!")
    else:
        st.info("No resources match your filter criteria. Try different filters or share a resource!")
    
    # Weekly resource highlights
    st.subheader("Weekly Resource Highlights")
    st.markdown("""
    ### This Week's Top Picks:
    
    1. **[Python 3.10 New Features](https://docs.python.org/3/whatsnew/3.10.html)** - Explore the newest features in Python 3.10 including structural pattern matching
    
    2. **[Effective Python Testing with Pytest](https://realpython.com/pytest-python-testing/)** - Learn how to test your Python code effectively
    
    3. **[Python Design Patterns](https://refactoring.guru/design-patterns/python)** - Practical implementation of design patterns in Python
    
    *These resources are curated by our community moderators based on quality and relevance.*
    """)

elif page == "Community Guidelines":
    st.header("Community Guidelines")
    
    st.write("""
    Welcome to our Python Learning Community! To ensure this remains a helpful, 
    supportive environment for everyone, please follow these guidelines.
    """)
    
    st.subheader("Our Community Values")
    st.markdown("""
    - **Inclusivity**: We welcome learners of all backgrounds and skill levels
    - **Respect**: Treat others with kindness and respect
    - **Helpfulness**: Share knowledge and support other learners
    - **Quality**: Strive for accuracy and clarity in discussions and shared resources
    - **Growth**: Embrace the learning process and be open to new ideas
    """)
    
    st.subheader("Participation Guidelines")
    st.markdown("""
    ### DO:
    - Ask specific, well-formatted questions
    - Share relevant resources and knowledge
    - Provide constructive feedback
    - Be patient with beginners
    - Give credit when sharing others' content
    - Report inappropriate content to moderators
    
    ### DON'T:
    - Post off-topic or promotional content
    - Share complete homework solutions (guide instead)
    - Use disrespectful or discriminatory language
    - Share pirated resources or materials
    - Spam the forums with repetitive content
    """)
    
    st.subheader("Code of Conduct")
    st.markdown("""
    Our community follows a code of conduct based on respect, inclusivity, and collaboration:
    
    1. **Be Respectful**: Treat others as you would like to be treated
    2. **Be Inclusive**: Welcome everyone regardless of background or experience level
    3. **Be Helpful**: Aim to contribute positively to discussions
    4. **Be Patient**: Everyone learns at different paces
    5. **Be Constructive**: Offer feedback that helps others improve
    
    Violations of these guidelines may result in warnings or account restrictions.
    
    For any questions or concerns, please contact the community moderators.
    """)
    
    if st.button("I Agree to Follow These Guidelines"):
        st.success("Thank you for being a valued member of our community!")

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Home"):
        st.switch_page("app.py")
with cols[1]:
    if st.button("My Progress 📊"):
        st.switch_page("pages/progress.py")
with cols[2]:
    if st.button("Go to Projects 🛠️"):
        st.switch_page("pages/projects.py")
