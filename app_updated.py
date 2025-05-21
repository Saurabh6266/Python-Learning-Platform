import streamlit as st
import json
import os
from datetime import datetime
import db_utils

# Page configuration
st.set_page_config(page_title="Python Learning Path",
                   page_icon="🐍",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Initialize session state for user progress if not exists
if 'username' not in st.session_state:
    st.session_state.username = None
if 'resources_completed' not in st.session_state:
    st.session_state.resources_completed = []
if 'current_level' not in st.session_state:
    st.session_state.current_level = "beginner"

# Main header
st.title("🐍 Python Learning Path 🚀")
st.subheader(
    "✨ A comprehensive resource for learning Python from beginner to advanced ✨"
)

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
                db_utils.load_user_progress(username)
                st.rerun()
            else:
                st.error("⚠️ Please enter a username")

    st.divider()
    st.write("### 🧭 Navigation")
    st.write(
        "📚 Use the pages in the sidebar to navigate through different sections of the learning path."
    )

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
    st.write(
        f"👋 Welcome back, **{st.session_state.username}**! Let's continue your Python learning journey. 🚀"
    )

    # Display current progress
    current_level = st.session_state.current_level
    level_emoji = {"beginner": "🐣", "intermediate": "🚀", "advanced": "🔥"}

    st.write(
        f"### 📊 Your Current Level: {level_emoji[current_level]} {current_level.capitalize()}"
    )

    # Calculate progress percentage
    resources = db_utils.load_resources()
    level_resources = [r for r in resources if r['level'] == current_level]
    completed = [
        r for r in level_resources
        if r['id'] in st.session_state.resources_completed
    ]

    if level_resources:
        progress_percentage = len(completed) / len(level_resources) * 100
        st.progress(progress_percentage / 100)
        st.write(
            f"🎯 You've completed **{len(completed)}** out of **{len(level_resources)}** resources (**{progress_percentage:.1f}%**)"
        )

    # Quick navigation cards
    st.write("### 🚀 Continue Learning")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        #### 🐣 Beginner Path
        Fundamentals of Python programming for newcomers.
        """)
        if st.button("📚 Go to Beginner Resources", key="goto_beginner"):
            st.switch_page("pages/beginner.py")

    with col2:
        st.markdown("""
        #### 🚀 Intermediate Path
        Advanced concepts and practical applications.
        """)
        if st.button("📘 Go to Intermediate Resources",
                     key="goto_intermediate"):
            st.switch_page("pages/intermediate.py")

    with col3:
        st.markdown("""
        #### 🔥 Advanced Path
        Expert techniques and specialized domains.
        """)
        if st.button("📕 Go to Advanced Resources", key="goto_advanced"):
            st.switch_page("pages/advanced.py")

    with col4:
        st.markdown("""
        #### 💻 Practice Problems
        LeetCode and HackerRank coding challenges.
        """)
        if st.button("🏆 Go to Practice Problems", key="goto_practice"):
            st.switch_page("pages/practice.py")

    # Recommended next resources
    st.write("### 🧠 Recommended Next Steps")

    # Get recommendations based on user progress
    recommendations = db_utils.get_recommendations(
        current_level, st.session_state.resources_completed)

    if recommendations:
        for i, resource in enumerate(recommendations[:3]):
            with st.expander(f"{i+1}. ✨ {resource['title']}"):
                st.write(f"**📋 Type**: {resource['type']}")
                st.write(f"**📝 Description**: {resource['description']}")
                st.markdown(f"[🔗 Open Resource]({resource['url']})")

                # Mark as completed button
                if resource['id'] not in st.session_state.resources_completed:
                    if st.button("✅ Mark as Completed",
                                 key=f"complete_{resource['id']}"):
                        st.session_state.resources_completed.append(
                            resource['id'])
                        db_utils.save_user_progress(
                            st.session_state.username,
                            st.session_state.resources_completed,
                            st.session_state.current_level)
                        st.rerun()
                else:
                    st.success("✅ Completed!")
    else:
        st.info(
            "🎉 Great job! You've completed all resources at your current level. Consider moving to the next level!"
        )

    # Project suggestions
    st.write("### 💻 Suggested Projects")
    projects = db_utils.load_projects()
    level_projects = [p for p in projects if p['level'] == current_level]

    if level_projects:
        selected_project = st.selectbox(
            "🔍 Select a project to work on:",
            options=[p['title'] for p in level_projects],
            index=0)

        project = next(
            (p for p in level_projects if p['title'] == selected_project),
            None)

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
st.markdown("✨ Created with ❤️ using Streamlit and SQLite Database ✨")
