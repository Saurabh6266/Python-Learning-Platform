import streamlit as st
import utils
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Learning Progress",
    page_icon="📊",
    layout="wide"
)

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to track your progress.")
    st.stop()

# Load user data
username = st.session_state.username
completed_resources = st.session_state.resources_completed
current_level = st.session_state.current_level

# Load resources
resources = utils.load_resources()

# Header
st.title("📊 Your Python Learning Progress")
st.write(f"Track your journey to Python mastery, {username}!")

# Calculate stats for different levels
beginner_resources = [r for r in resources if r['level'] == 'beginner']
intermediate_resources = [r for r in resources if r['level'] == 'intermediate']
advanced_resources = [r for r in resources if r['level'] == 'advanced']

completed_beginner = [r for r in beginner_resources if r['id'] in completed_resources]
completed_intermediate = [r for r in intermediate_resources if r['id'] in completed_resources]
completed_advanced = [r for r in advanced_resources if r['id'] in completed_resources]

# Calculate percentages
beginner_percentage = len(completed_beginner) / len(beginner_resources) * 100 if beginner_resources else 0
intermediate_percentage = len(completed_intermediate) / len(intermediate_resources) * 100 if intermediate_resources else 0
advanced_percentage = len(completed_advanced) / len(advanced_resources) * 100 if advanced_resources else 0

# Overall progress
total_resources = len(resources)
total_completed = len(completed_resources)
overall_percentage = total_completed / total_resources * 100 if total_resources else 0

# Display overview
st.header("Progress Overview")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Level", current_level.capitalize())
with col2:
    st.metric("Resources Completed", f"{total_completed}/{total_resources}")
with col3:
    st.metric("Overall Progress", f"{overall_percentage:.1f}%")

# Progress bars
st.subheader("Progress by Level")

# Beginner progress
st.write("🐣 **Beginner**")
st.progress(beginner_percentage / 100)
st.write(f"Completed {len(completed_beginner)}/{len(beginner_resources)} resources ({beginner_percentage:.1f}%)")

# Intermediate progress
st.write("🚀 **Intermediate**")
st.progress(intermediate_percentage / 100)
st.write(f"Completed {len(completed_intermediate)}/{len(intermediate_resources)} resources ({intermediate_percentage:.1f}%)")

# Advanced progress
st.write("🔥 **Advanced**")
st.progress(advanced_percentage / 100)
st.write(f"Completed {len(completed_advanced)}/{len(advanced_resources)} resources ({advanced_percentage:.1f}%)")

# Create visual chart of progress
st.subheader("Visual Progress")

# Create chart
fig, ax = plt.subplots(figsize=(10, 5))
levels = ['Beginner', 'Intermediate', 'Advanced']
percentages = [beginner_percentage, intermediate_percentage, advanced_percentage]
colors = ['#FFA07A', '#87CEFA', '#FFD700']  # Light salmon, Light sky blue, Gold

# Create bar chart
bars = ax.bar(levels, percentages, color=colors)

# Add percentage labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

ax.set_ylim(0, 100)
ax.set_ylabel('Completion Percentage')
ax.set_title('Learning Progress by Level')

# Display the chart
st.pyplot(fig)

# Recently completed resources
st.header("Recently Completed Resources")

# Load user progress file to get timestamps
try:
    with open(utils.USER_PROGRESS_FILE, 'r') as f:
        progress_data = json.load(f)
        
    if username in progress_data and 'completed_resources' in progress_data[username]:
        # Get completed resources with timestamps if available
        completed_with_time = []
        
        for r_id in completed_resources:
            # Find the resource object
            resource = next((r for r in resources if r['id'] == r_id), None)
            if resource:
                # Try to get completion time if it exists
                completion_time = progress_data[username].get('completion_times', {}).get(r_id)
                completed_with_time.append({
                    'id': r_id,
                    'title': resource['title'],
                    'level': resource['level'],
                    'type': resource['type'],
                    'completed_at': completion_time if completion_time else 'Unknown'
                })
        
        # Sort by completion time (most recent first)
        # Those without timestamps will be at the end
        completed_with_time.sort(key=lambda x: x['completed_at'] if x['completed_at'] != 'Unknown' else '0', reverse=True)
        
        if completed_with_time:
            # Display recent completions
            df = pd.DataFrame(completed_with_time[:5])  # Show most recent 5
            if 'completed_at' in df.columns:
                df = df.rename(columns={'completed_at': 'Completed At', 'title': 'Title', 'level': 'Level', 'type': 'Type'})
                # Format the timestamp to readable format if not 'Unknown'
                df['Completed At'] = df['Completed At'].apply(
                    lambda x: datetime.fromisoformat(x).strftime('%Y-%m-%d %H:%M') if x != 'Unknown' else x
                )
                st.dataframe(df[['Title', 'Level', 'Type', 'Completed At']], use_container_width=True)
            else:
                df = df.rename(columns={'title': 'Title', 'level': 'Level', 'type': 'Type'})
                st.dataframe(df[['Title', 'Level', 'Type']], use_container_width=True)
        else:
            st.info("You haven't completed any resources yet.")
    else:
        st.info("No completion data found.")
except Exception as e:
    st.error(f"Error loading completion data: {e}")
    st.info("Complete some resources to see your progress here.")

# Learning streaks
st.header("Learning Streak")

# Create or load streak data
streak_file = "data/streaks.json"
if not os.path.exists(streak_file):
    with open(streak_file, 'w') as f:
        json.dump({}, f)

try:
    with open(streak_file, 'r') as f:
        streak_data = json.load(f)
    
    # Initialize user streak data if not exists
    if username not in streak_data:
        streak_data[username] = {
            'current_streak': 0,
            'longest_streak': 0,
            'last_active': None,
            'active_days': []
        }
    
    # Update streak for today
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Update if this is the first visit today
    if today not in streak_data[username]['active_days']:
        streak_data[username]['active_days'].append(today)
        
        # Check if continuing a streak
        if streak_data[username]['last_active']:
            last_date = datetime.strptime(streak_data[username]['last_active'], '%Y-%m-%d')
            today_date = datetime.strptime(today, '%Y-%m-%d')
            days_diff = (today_date - last_date).days
            
            if days_diff == 1:  # Sequential day
                streak_data[username]['current_streak'] += 1
            elif days_diff > 1:  # Streak broken
                streak_data[username]['current_streak'] = 1
            # If same day, no change to streak
        else:
            # First activity ever
            streak_data[username]['current_streak'] = 1
        
        # Update last active day
        streak_data[username]['last_active'] = today
        
        # Update longest streak if current is longer
        if streak_data[username]['current_streak'] > streak_data[username]['longest_streak']:
            streak_data[username]['longest_streak'] = streak_data[username]['current_streak']
        
        # Limit active_days list to last 30 days
        streak_data[username]['active_days'] = sorted(streak_data[username]['active_days'])[-30:]
        
        # Save updated streak data
        with open(streak_file, 'w') as f:
            json.dump(streak_data, f)
    
    # Display streak information
    current_streak = streak_data[username]['current_streak']
    longest_streak = streak_data[username]['longest_streak']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Streak", f"{current_streak} day{'s' if current_streak != 1 else ''}")
    with col2:
        st.metric("Longest Streak", f"{longest_streak} day{'s' if longest_streak != 1 else ''}")
    
    # Create a heatmap-like visualization of active days
    st.subheader("Your Activity (Last 30 Days)")
    
    # Generate last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=29)
    date_range = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    # Create activity data
    active_days = streak_data[username]['active_days']
    activity = [1 if date in active_days else 0 for date in date_range]
    
    # Plot activity
    fig, ax = plt.subplots(figsize=(15, 3))
    ax.bar(date_range, activity, color=['#4B8BBE' if a else '#E6E6E6' for a in activity])
    
    # Customize x-axis labels to show fewer dates for readability
    ax.set_xticks([date_range[i] for i in range(0, 30, 5)])
    ax.set_xticklabels([datetime.strptime(date_range[i], '%Y-%m-%d').strftime('%b %d') for i in range(0, 30, 5)], rotation=45)
    
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_ylim(0, 1.5)  # Set y-axis limits
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add title and caption
    ax.set_title('Daily Activity')
    fig.tight_layout()
    
    st.pyplot(fig)
    
    # Encouragement message
    if current_streak > 0:
        st.success(f"Great job! You've been learning Python for {current_streak} consecutive day{'s' if current_streak != 1 else ''}. Keep it up!")
    else:
        st.info("Start your learning streak today by completing a resource!")
    
except Exception as e:
    st.error(f"Error tracking streak: {e}")
    st.info("We'll start tracking your learning streak from today.")

# Recommendations based on progress
st.header("Next Steps")

# Get recommendations based on user progress
recommendations = utils.get_recommendations(current_level, completed_resources)

if recommendations:
    st.write("Based on your progress, here are some recommended resources:")
    
    for i, resource in enumerate(recommendations[:3]):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"{i+1}. {resource['title']}")
            st.write(f"**Type**: {resource['type']}")
            st.write(f"**Description**: {resource['description']}")
        with col2:
            st.markdown(f"[Open Resource]({resource['url']})")
            
            # Mark as completed button
            if resource['id'] not in completed_resources:
                if st.button("Mark as Completed", key=f"complete_{resource['id']}"):
                    st.session_state.resources_completed.append(resource['id'])
                    utils.save_user_progress(username, completed_resources, current_level)
                    st.rerun()
            else:
                st.success("Completed ✓")
else:
    st.info("You've completed all resources at your current level. Consider moving to the next level!")

# Level up section
st.header("Ready to Level Up?")

level_thresholds = {
    "beginner": {
        "percentage": beginner_percentage,
        "next_level": "intermediate",
        "required": 70
    },
    "intermediate": {
        "percentage": intermediate_percentage,
        "next_level": "advanced",
        "required": 70
    },
    "advanced": {
        "percentage": advanced_percentage,
        "next_level": None,
        "required": 70
    }
}

current = level_thresholds[current_level]

if current["next_level"] is not None:
    st.write(f"You've completed {current['percentage']:.1f}% of {current_level} resources.")
    
    # Progress bar for leveling up
    st.progress(min(current['percentage'] / current['required'], 1.0))
    
    if current['percentage'] >= current['required']:
        st.success(f"Congratulations! You're ready to move up to the {current['next_level']} level!")
        if st.button(f"Move to {current['next_level'].capitalize()} Level"):
            st.session_state.current_level = current['next_level']
            utils.save_user_progress(username, completed_resources, current['next_level'])
            st.success(f"Level updated! You are now at the {current['next_level']} level.")
            st.balloons()
            st.rerun()
    else:
        st.info(f"Complete at least {current['required']}% of {current_level} resources to unlock the {current['next_level']} level.")
else:
    st.success("You've reached the highest level! Continue mastering advanced Python concepts.")

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Home"):
        st.switch_page("app.py")
with cols[1]:
    if st.button("Go to Projects 🛠️"):
        st.switch_page("pages/projects.py")
with cols[2]:
    if st.button("Community Forum 💬"):
        st.switch_page("pages/community.py")
