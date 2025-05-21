import streamlit as st
import utils
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Python Projects",
    page_icon="🛠️",
    layout="wide"
)

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to track your progress.")
    st.stop()

# Load projects
projects = utils.load_projects()

# Header
st.title("🛠️ Python Projects")
st.write("""
Apply your Python knowledge by working on real-world projects. We've curated a collection of 
practical Python projects across different difficulty levels to help you build your portfolio and
gain hands-on experience.
""")

# Filter sidebar
st.sidebar.header("Filter Projects")

# Level filter
levels = ["All Levels"] + sorted(list(set([p["level"] for p in projects])))
selected_level = st.sidebar.selectbox("Skill Level", levels)

# Difficulty filter
difficulties = ["All Difficulties"] + sorted(list(set([str(p["difficulty"]) for p in projects])))
selected_difficulty = st.sidebar.selectbox("Difficulty", difficulties)

# Skills filter
all_skills = []
for project in projects:
    all_skills.extend(project.get("skills", []))
unique_skills = ["All Skills"] + sorted(list(set(all_skills)))
selected_skill = st.sidebar.selectbox("Required Skill", unique_skills)

# Apply filters
filtered_projects = projects
if selected_level != "All Levels":
    filtered_projects = [p for p in filtered_projects if p["level"] == selected_level]
if selected_difficulty != "All Difficulties":
    filtered_projects = [p for p in filtered_projects if str(p["difficulty"]) == selected_difficulty]
if selected_skill != "All Skills":
    filtered_projects = [p for p in filtered_projects if selected_skill in p.get("skills", [])]

# Display projects
if not filtered_projects:
    st.info("No projects match your filter criteria. Try adjusting your filters.")
else:
    # Group projects by level for display
    beginner_projects = [p for p in filtered_projects if p["level"] == "beginner"]
    intermediate_projects = [p for p in filtered_projects if p["level"] == "intermediate"]
    advanced_projects = [p for p in filtered_projects if p["level"] == "advanced"]
    
    # Show project counts
    st.write(f"Showing {len(filtered_projects)} projects: {len(beginner_projects)} beginner, {len(intermediate_projects)} intermediate, {len(advanced_projects)} advanced")
    
    # Display projects by level if not filtering by a specific level
    if selected_level == "All Levels":
        # Display beginner projects
        if beginner_projects:
            st.header("🐣 Beginner Projects")
            for project in beginner_projects:
                with st.expander(f"{project['title']} (Difficulty: {project['difficulty']}/5)"):
                    st.write(f"**Description**: {project['description']}")
                    st.write(f"**Skills**: {', '.join(project['skills'])}")
                    st.write(f"**Details**: {project['details']}")
                    if "starter_code" in project and project["starter_code"]:
                        st.subheader("Starter Code")
                        st.code(project["starter_code"], language="python")
                    
                    # Add a "Try it yourself" button
                    if st.button("Work on this project", key=f"work_{project['id']}"):
                        st.session_state.current_project = project
                        st.rerun()
        
        # Display intermediate projects
        if intermediate_projects:
            st.header("🚀 Intermediate Projects")
            for project in intermediate_projects:
                with st.expander(f"{project['title']} (Difficulty: {project['difficulty']}/5)"):
                    st.write(f"**Description**: {project['description']}")
                    st.write(f"**Skills**: {', '.join(project['skills'])}")
                    st.write(f"**Details**: {project['details']}")
                    if "starter_code" in project and project["starter_code"]:
                        st.subheader("Starter Code")
                        st.code(project["starter_code"], language="python")
                    
                    # Add a "Try it yourself" button
                    if st.button("Work on this project", key=f"work_{project['id']}"):
                        st.session_state.current_project = project
                        st.rerun()
        
        # Display advanced projects
        if advanced_projects:
            st.header("🔥 Advanced Projects")
            for project in advanced_projects:
                with st.expander(f"{project['title']} (Difficulty: {project['difficulty']}/5)"):
                    st.write(f"**Description**: {project['description']}")
                    st.write(f"**Skills**: {', '.join(project['skills'])}")
                    st.write(f"**Details**: {project['details']}")
                    if "starter_code" in project and project["starter_code"]:
                        st.subheader("Starter Code")
                        st.code(project["starter_code"], language="python")
                    
                    # Add a "Try it yourself" button
                    if st.button("Work on this project", key=f"work_{project['id']}"):
                        st.session_state.current_project = project
                        st.rerun()
    else:
        # Just show filtered projects without level headers
        for project in filtered_projects:
            with st.expander(f"{project['title']} (Difficulty: {project['difficulty']}/5)"):
                st.write(f"**Description**: {project['description']}")
                st.write(f"**Skills**: {', '.join(project['skills'])}")
                st.write(f"**Details**: {project['details']}")
                if "starter_code" in project and project["starter_code"]:
                    st.subheader("Starter Code")
                    st.code(project["starter_code"], language="python")
                
                # Add a "Try it yourself" button
                if st.button("Work on this project", key=f"work_{project['id']}"):
                    st.session_state.current_project = project
                    st.rerun()

# Project workspace
if "current_project" in st.session_state:
    project = st.session_state.current_project
    
    st.header(f"Project Workspace: {project['title']}")
    st.write(f"**Level**: {project['level'].capitalize()}, **Difficulty**: {project['difficulty']}/5")
    
    # Create tabs for different parts of the workspace
    tab1, tab2, tab3 = st.tabs(["Requirements", "Code Editor", "Resources"])
    
    with tab1:
        st.subheader("Project Requirements")
        st.write(project['details'])
        st.write("**Skills needed**:")
        for skill in project['skills']:
            st.write(f"- {skill}")
    
    with tab2:
        st.subheader("Code Editor")
        # Get starter code or provide default
        starter_code = project.get('starter_code', '# Your code here\n\n')
        
        # Check if we have saved code for this project
        user_code_key = f"code_{project['id']}_{st.session_state.username}"
        if user_code_key in st.session_state:
            starter_code = st.session_state[user_code_key]
        
        # Code editor
        user_code = st.text_area("Edit your code here:", value=starter_code, height=400)
        
        # Save the code in session state
        st.session_state[user_code_key] = user_code
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Run Code"):
                try:
                    # Create a file
                    with open("temp_project_code.py", "w") as f:
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
                    if os.path.exists("temp_project_code.py"):
                        os.remove("temp_project_code.py")
        
        with col2:
            if st.button("Clear Code"):
                st.session_state[user_code_key] = project.get('starter_code', '# Your code here\n\n')
                st.rerun()
    
    with tab3:
        st.subheader("Helpful Resources")
        st.write("Here are some resources that might help you with this project:")
        
        # Get resources related to the skills needed for this project
        resources = utils.load_resources()
        relevant_resources = []
        
        for skill in project['skills']:
            # Look for resources with matching tags
            for resource in resources:
                if 'tags' in resource and any(tag.lower() in skill.lower() for tag in resource['tags']):
                    if resource not in relevant_resources:
                        relevant_resources.append(resource)
        
        if relevant_resources:
            for i, resource in enumerate(relevant_resources[:5]):  # Limit to 5 resources
                st.markdown(f"{i+1}. [{resource['title']}]({resource['url']}) - {resource['description']}")
        else:
            st.write("No specific resources found. Try looking at the general resources for your level.")
            
            # Recommend general resources based on project level
            level_resources = [r for r in resources if r['level'] == project['level']]
            for i, resource in enumerate(level_resources[:3]):
                st.markdown(f"{i+1}. [{resource['title']}]({resource['url']}) - {resource['description']}")
    
    # Exit workspace button
    if st.button("Exit Workspace"):
        del st.session_state.current_project
        st.rerun()

# Project suggestions based on completed resources
if "current_project" not in st.session_state:
    st.header("Recommended Projects for You")
    
    # Get user's current level and completed resources
    current_level = st.session_state.current_level
    completed_resources = st.session_state.resources_completed
    
    # Load resources to check which skills the user might have
    resources = utils.load_resources()
    completed_resource_objects = [r for r in resources if r['id'] in completed_resources]
    
    # Extract tags from completed resources (these represent skills the user has)
    user_skills = []
    for r in completed_resource_objects:
        if 'tags' in r:
            user_skills.extend(r['tags'])
    
    # Find projects that match the user's skills and level
    matching_projects = []
    for project in projects:
        if project['level'] == current_level:
            # Check if any of the project's required skills match user's skills
            if any(skill.lower() in [s.lower() for s in user_skills] for skill in project['skills']):
                matching_projects.append(project)
    
    # If no matching projects, recommend based on level only
    if not matching_projects:
        matching_projects = [p for p in projects if p['level'] == current_level]
    
    # Display recommended projects
    if matching_projects:
        # Sort by difficulty
        matching_projects.sort(key=lambda x: x['difficulty'])
        
        # Show top 3 recommendations
        st.write("Based on your progress, here are some projects you might want to try:")
        for i, project in enumerate(matching_projects[:3]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"{i+1}. {project['title']}")
                st.write(f"**Difficulty**: {project['difficulty']}/5")
                st.write(f"**Description**: {project['description']}")
                st.write(f"**Skills**: {', '.join(project['skills'])}")
            with col2:
                if st.button("Start Project", key=f"start_{project['id']}"):
                    st.session_state.current_project = project
                    st.rerun()
    else:
        st.info("Complete more resources to get personalized project recommendations.")

# Tips for completing projects
st.header("Tips for Successful Project Completion")
st.markdown("""
### Steps to Complete a Project Successfully:

1. **Understand the Requirements**: Make sure you understand what the project is asking you to build
2. **Plan Your Approach**: Break down the project into smaller tasks and plan your implementation
3. **Start Simple**: Begin with a simplified version that covers the basic functionality
4. **Iterative Development**: Add features incrementally and test as you go
5. **Debug Effectively**: When you encounter errors, read the error messages carefully and use print statements
6. **Research When Stuck**: If you get stuck, search for solutions online or look at documentation
7. **Refactor Your Code**: Once it works, improve your code's structure and readability
8. **Test Thoroughly**: Test your project with different inputs to ensure it works correctly
9. **Document Your Code**: Add comments to explain complex sections and how to use your program
10. **Share and Get Feedback**: Share your project with others to get feedback and suggestions

### Project Completion Checklist:
- [ ] Program runs without errors
- [ ] All requirements are implemented
- [ ] Code is well-structured and follows Python conventions
- [ ] Edge cases are handled appropriately
- [ ] Comments explain complex logic
- [ ] User experience is considered (clear instructions, error messages, etc.)
""")

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Home"):
        st.switch_page("app.py")
with cols[1]:
    level_page_map = {
        "beginner": "pages/beginner.py",
        "intermediate": "pages/intermediate.py",
        "advanced": "pages/advanced.py"
    }
    if st.button(f"Go to {st.session_state.current_level.capitalize()} Resources"):
        st.switch_page(level_page_map[st.session_state.current_level])
with cols[2]:
    if st.button("Community Forum 💬"):
        st.switch_page("pages/community.py")
