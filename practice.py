import streamlit as st
import db_utils
import json
import os
import random

# Page configuration
st.set_page_config(
    page_title="Coding Practice Problems",
    page_icon="💻",
    layout="wide"
)

# Check if user is logged in
if "username" not in st.session_state or not st.session_state.username:
    st.warning("Please log in on the home page to track your progress.")
    st.stop()

# Header
st.title("💻 Coding Practice Problems")
st.write("""
✨ Sharpen your Python skills with curated practice problems from platforms like LeetCode, 
HackerRank, and more. These problems are organized by difficulty to match your current level.
""")

# Load user's current level
current_level = st.session_state.current_level

# Define mapping between our levels and platform difficulty levels
difficulty_mapping = {
    "beginner": ["Easy", "Basic"],
    "intermediate": ["Medium", "Intermediate"],
    "advanced": ["Hard", "Advanced", "Expert"]
}

# Load or initialize practice problems
def load_practice_problems():
    # Create the file if it doesn't exist
    problems_file = "data/practice_problems.json"
    if not os.path.exists(problems_file):
        # Define initial set of practice problems
        default_problems = {
            "leetcode": [
                {
                    "id": "lc1",
                    "title": "Two Sum",
                    "difficulty": "Easy",
                    "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                    "url": "https://leetcode.com/problems/two-sum/",
                    "platform": "LeetCode",
                    "tags": ["Array", "Hash Table"]
                },
                {
                    "id": "lc2",
                    "title": "Add Two Numbers",
                    "difficulty": "Medium",
                    "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
                    "url": "https://leetcode.com/problems/add-two-numbers/",
                    "platform": "LeetCode",
                    "tags": ["Linked List", "Math", "Recursion"]
                },
                {
                    "id": "lc3",
                    "title": "Longest Substring Without Repeating Characters",
                    "difficulty": "Medium",
                    "description": "Given a string s, find the length of the longest substring without repeating characters.",
                    "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
                    "platform": "LeetCode",
                    "tags": ["Hash Table", "String", "Sliding Window"]
                },
                {
                    "id": "lc4",
                    "title": "Median of Two Sorted Arrays",
                    "difficulty": "Hard",
                    "description": "Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.",
                    "url": "https://leetcode.com/problems/median-of-two-sorted-arrays/",
                    "platform": "LeetCode",
                    "tags": ["Array", "Binary Search", "Divide and Conquer"]
                },
                {
                    "id": "lc5",
                    "title": "Longest Palindromic Substring",
                    "difficulty": "Medium",
                    "description": "Given a string s, return the longest palindromic substring in s.",
                    "url": "https://leetcode.com/problems/longest-palindromic-substring/",
                    "platform": "LeetCode",
                    "tags": ["String", "Dynamic Programming"]
                },
                {
                    "id": "lc6",
                    "title": "Valid Parentheses",
                    "difficulty": "Easy",
                    "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                    "url": "https://leetcode.com/problems/valid-parentheses/",
                    "platform": "LeetCode",
                    "tags": ["String", "Stack"]
                },
                {
                    "id": "lc7",
                    "title": "Remove Duplicates from Sorted Array",
                    "difficulty": "Easy",
                    "description": "Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once.",
                    "url": "https://leetcode.com/problems/remove-duplicates-from-sorted-array/",
                    "platform": "LeetCode",
                    "tags": ["Array", "Two Pointers"]
                },
                {
                    "id": "lc8",
                    "title": "Merge Two Sorted Lists",
                    "difficulty": "Easy",
                    "description": "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists in a one sorted list.",
                    "url": "https://leetcode.com/problems/merge-two-sorted-lists/",
                    "platform": "LeetCode",
                    "tags": ["Linked List", "Recursion"]
                },
                {
                    "id": "lc9",
                    "title": "Binary Tree Level Order Traversal",
                    "difficulty": "Medium",
                    "description": "Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
                    "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
                    "platform": "LeetCode",
                    "tags": ["Tree", "BFS", "Binary Tree"]
                },
                {
                    "id": "lc10",
                    "title": "Word Search",
                    "difficulty": "Medium",
                    "description": "Given an m x n grid of characters board and a string word, return true if word exists in the grid.",
                    "url": "https://leetcode.com/problems/word-search/",
                    "platform": "LeetCode",
                    "tags": ["Array", "Backtracking", "Matrix"]
                },
                {
                    "id": "lc11",
                    "title": "Trapping Rain Water",
                    "difficulty": "Hard",
                    "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
                    "url": "https://leetcode.com/problems/trapping-rain-water/",
                    "platform": "LeetCode",
                    "tags": ["Array", "Two Pointers", "Dynamic Programming", "Stack"]
                },
                {
                    "id": "lc12",
                    "title": "Merge k Sorted Lists",
                    "difficulty": "Hard",
                    "description": "You are given an array of k linked-lists lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.",
                    "url": "https://leetcode.com/problems/merge-k-sorted-lists/",
                    "platform": "LeetCode",
                    "tags": ["Linked List", "Divide and Conquer", "Heap"]
                }
            ],
            "hackerrank": [
                {
                    "id": "hr1",
                    "title": "Solve Me First",
                    "difficulty": "Easy",
                    "description": "Complete the function solveMeFirst to compute the sum of two integers.",
                    "url": "https://www.hackerrank.com/challenges/solve-me-first/problem",
                    "platform": "HackerRank",
                    "tags": ["Introduction"]
                },
                {
                    "id": "hr2",
                    "title": "Simple Array Sum",
                    "difficulty": "Easy",
                    "description": "Given an array of integers, find the sum of its elements.",
                    "url": "https://www.hackerrank.com/challenges/simple-array-sum/problem",
                    "platform": "HackerRank",
                    "tags": ["Arrays"]
                },
                {
                    "id": "hr3",
                    "title": "Compare the Triplets",
                    "difficulty": "Easy",
                    "description": "Alice and Bob each created one problem for HackerRank. A reviewer rates the two challenges, awarding points on a scale from 1 to 100 for three categories: problem clarity, originality, and difficulty.",
                    "url": "https://www.hackerrank.com/challenges/compare-the-triplets/problem",
                    "platform": "HackerRank",
                    "tags": ["Implementation"]
                },
                {
                    "id": "hr4",
                    "title": "A Very Big Sum",
                    "difficulty": "Easy", 
                    "description": "Calculate and print the sum of the elements in an array, keeping in mind that some of those integers may be quite large.",
                    "url": "https://www.hackerrank.com/challenges/a-very-big-sum/problem",
                    "platform": "HackerRank",
                    "tags": ["Arrays", "Math"]
                },
                {
                    "id": "hr5",
                    "title": "Diagonal Difference",
                    "difficulty": "Easy",
                    "description": "Given a square matrix, calculate the absolute difference between the sums of its diagonals.",
                    "url": "https://www.hackerrank.com/challenges/diagonal-difference/problem",
                    "platform": "HackerRank",
                    "tags": ["Arrays", "Math"]
                },
                {
                    "id": "hr6",
                    "title": "Birthday Cake Candles",
                    "difficulty": "Easy",
                    "description": "You are in charge of the cake for a child's birthday. You have decided the cake will have one candle for each year of their total age. They will only be able to blow out the tallest of the candles. Count how many candles are tallest.",
                    "url": "https://www.hackerrank.com/challenges/birthday-cake-candles/problem",
                    "platform": "HackerRank",
                    "tags": ["Arrays", "Math"]
                },
                {
                    "id": "hr7",
                    "title": "Matrix Layer Rotation",
                    "difficulty": "Hard",
                    "description": "You are given a 2D matrix of dimension MxN and a positive integer R. You have to rotate the matrix R times and print the resultant matrix.",
                    "url": "https://www.hackerrank.com/challenges/matrix-rotation-algo/problem",
                    "platform": "HackerRank",
                    "tags": ["Implementation", "Arrays"]
                },
                {
                    "id": "hr8",
                    "title": "The Time in Words",
                    "difficulty": "Medium",
                    "description": "Given the time in numerals we may convert it into words.",
                    "url": "https://www.hackerrank.com/challenges/the-time-in-words/problem",
                    "platform": "HackerRank",
                    "tags": ["Implementation", "Strings"]
                },
                {
                    "id": "hr9",
                    "title": "Forming a Magic Square",
                    "difficulty": "Medium",
                    "description": "We define a magic square to be an n×n matrix of distinct positive integers from 1 to n^2 where the sum of any row, column, or diagonal is always equal to the same number.",
                    "url": "https://www.hackerrank.com/challenges/magic-square-forming/problem",
                    "platform": "HackerRank",
                    "tags": ["Implementation", "Backtracking"]
                },
                {
                    "id": "hr10",
                    "title": "Journey to the Moon",
                    "difficulty": "Medium",
                    "description": "The member states of the UN are planning to send people to the moon. They want them to be from different countries. You will be given a list of pairs of astronaut ID's. Each pair is made of astronauts from the same country. Determine how many pairs of astronauts from different countries they can choose from.",
                    "url": "https://www.hackerrank.com/challenges/journey-to-the-moon/problem",
                    "platform": "HackerRank",
                    "tags": ["Graph Theory", "DFS"]
                },
                {
                    "id": "hr11",
                    "title": "Sherlock and the Valid String",
                    "difficulty": "Medium",
                    "description": "Sherlock considers a string to be valid if all characters of the string appear the same number of times. It is also valid if he can remove just 1 character at 1 index in the string, and the remaining characters will occur the same number of times.",
                    "url": "https://www.hackerrank.com/challenges/sherlock-and-valid-string/problem",
                    "platform": "HackerRank",
                    "tags": ["String", "Hash Tables"]
                },
                {
                    "id": "hr12",
                    "title": "The Bomberman Game",
                    "difficulty": "Medium",
                    "description": "Bomberman lives in a rectangular grid. Each cell in the grid either contains a bomb or nothing at all. Each bomb can be planted in any cell of the grid but once planted, it will detonate after exactly 3 seconds. Once a bomb detonates, it destroys all adjacent cells.",
                    "url": "https://www.hackerrank.com/challenges/bomber-man/problem",
                    "platform": "HackerRank",
                    "tags": ["Implementation", "Simulation"]
                }
            ],
            "completed_problems": {}
        }
        
        with open(problems_file, 'w') as f:
            json.dump(default_problems, f, indent=4)
        
        return default_problems
    
    # Load the problems file
    try:
        with open(problems_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading practice problems: {e}")
        return {"leetcode": [], "hackerrank": [], "completed_problems": {}}

# Save completed problems
def save_completed_problem(username, problem_id):
    problems = load_practice_problems()
    
    # Initialize user's completed problems if needed
    if username not in problems["completed_problems"]:
        problems["completed_problems"][username] = []
    
    # Add problem to completed list if not already there
    if problem_id not in problems["completed_problems"][username]:
        problems["completed_problems"][username].append(problem_id)
    
    # Save updated problems
    with open("data/practice_problems.json", 'w') as f:
        json.dump(problems, f, indent=4)

# Remove from completed problems
def remove_completed_problem(username, problem_id):
    problems = load_practice_problems()
    
    # Remove problem from completed list if it's there
    if username in problems["completed_problems"] and problem_id in problems["completed_problems"][username]:
        problems["completed_problems"][username].remove(problem_id)
    
    # Save updated problems
    with open("data/practice_problems.json", 'w') as f:
        json.dump(problems, f, indent=4)

# Load problems
all_problems = load_practice_problems()
leetcode_problems = all_problems["leetcode"]
hackerrank_problems = all_problems["hackerrank"]
completed_problems = all_problems["completed_problems"].get(st.session_state.username, [])

# Combine all problems into one list
all_platform_problems = leetcode_problems + hackerrank_problems

# Platform selection
st.sidebar.header("🔍 Filter Problems")
selected_platform = st.sidebar.selectbox(
    "Platform",
    ["All Platforms", "LeetCode", "HackerRank"]
)

# Filter by platform
if selected_platform == "LeetCode":
    filtered_problems = leetcode_problems
elif selected_platform == "HackerRank":
    filtered_problems = hackerrank_problems
else:
    filtered_problems = all_platform_problems

# Filter by difficulty level
level_difficulties = difficulty_mapping.get(current_level, ["Easy", "Medium", "Hard"])
selected_difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["All Difficulties"] + level_difficulties
)

if selected_difficulty != "All Difficulties":
    filtered_problems = [p for p in filtered_problems if p["difficulty"] == selected_difficulty]

# Filter by tag
all_tags = []
for problem in all_platform_problems:
    all_tags.extend(problem.get("tags", []))
unique_tags = sorted(list(set(all_tags)))

selected_tag = st.sidebar.selectbox(
    "Topic/Tag",
    ["All Topics"] + unique_tags
)

if selected_tag != "All Topics":
    filtered_problems = [p for p in filtered_problems if "tags" in p and selected_tag in p["tags"]]

# Show completed problems toggle
show_completed = st.sidebar.checkbox("Show Completed Problems", True)

# Apply completed filter if needed
if not show_completed:
    filtered_problems = [p for p in filtered_problems if p["id"] not in completed_problems]

# Display user's current level
st.write(f"### Your Current Level: {current_level.capitalize()}")
st.write(f"We're showing problems that match your current skill level. You can use the sidebar to filter by platform, difficulty, and topic.")

# Display recommended problems for the user's level
st.header(f"🎯 Recommended Problems for {current_level.capitalize()} Level")

# Filter to show problems matching the user's level
level_problems = [p for p in all_platform_problems 
                 if p["difficulty"] in difficulty_mapping.get(current_level, [])]

# Get 3 random problems to recommend (that aren't completed)
uncompleted_level_problems = [p for p in level_problems if p["id"] not in completed_problems]
recommendations = random.sample(uncompleted_level_problems, min(3, len(uncompleted_level_problems)))

if recommendations:
    for problem in recommendations:
        with st.expander(f"✨ {problem['title']} ({problem['difficulty']}) - {problem['platform']}"):
            st.write(f"**📝 Description**: {problem['description']}")
            st.write(f"**🔖 Tags**: {', '.join(problem.get('tags', []))}")
            st.markdown(f"[🔗 Solve on {problem['platform']}]({problem['url']})")
            
            # Mark as completed/uncompleted button
            if problem["id"] in completed_problems:
                if st.button("❌ Mark as Incomplete", key=f"incomplete_{problem['id']}"):
                    remove_completed_problem(st.session_state.username, problem["id"])
                    st.success("Problem marked as incomplete!")
                    st.rerun()
            else:
                if st.button("✅ Mark as Completed", key=f"complete_{problem['id']}"):
                    save_completed_problem(st.session_state.username, problem["id"])
                    st.success("Problem marked as completed! Great job!")
                    st.rerun()
else:
    st.info("You've completed all the recommended problems at your level! Try adjusting the filters to find more challenges.")

# Display all filtered problems
st.header("🧩 All Coding Problems")

if filtered_problems:
    # Group problems by difficulty
    easy_problems = [p for p in filtered_problems if p["difficulty"] == "Easy" or p["difficulty"] == "Basic"]
    medium_problems = [p for p in filtered_problems if p["difficulty"] == "Medium" or p["difficulty"] == "Intermediate"]
    hard_problems = [p for p in filtered_problems if p["difficulty"] == "Hard" or p["difficulty"] == "Advanced" or p["difficulty"] == "Expert"]
    
    # Only show sections that have problems after filtering
    if easy_problems and (current_level == "beginner" or selected_difficulty == "Easy" or selected_difficulty == "All Difficulties"):
        st.subheader("🟢 Easy Problems")
        for problem in easy_problems:
            problem_key = f"{problem['platform']}-{problem['id']}"
            with st.expander(f"{problem['title']} ({problem['platform']})"):
                st.write(f"**📝 Description**: {problem['description']}")
                st.write(f"**🔖 Tags**: {', '.join(problem.get('tags', []))}")
                st.markdown(f"[🔗 Solve on {problem['platform']}]({problem['url']})")
                
                # Mark as completed/uncompleted button
                if problem["id"] in completed_problems:
                    st.success("✅ You've completed this problem!")
                    if st.button("❌ Mark as Incomplete", key=f"incomplete_{problem_key}"):
                        remove_completed_problem(st.session_state.username, problem["id"])
                        st.success("Problem marked as incomplete!")
                        st.rerun()
                else:
                    if st.button("✅ Mark as Completed", key=f"complete_{problem_key}"):
                        save_completed_problem(st.session_state.username, problem["id"])
                        st.success("Problem marked as completed! Great job!")
                        st.rerun()
    
    if medium_problems and (current_level == "intermediate" or selected_difficulty == "Medium" or selected_difficulty == "All Difficulties"):
        st.subheader("🟠 Medium Problems")
        for problem in medium_problems:
            problem_key = f"{problem['platform']}-{problem['id']}"
            with st.expander(f"{problem['title']} ({problem['platform']})"):
                st.write(f"**📝 Description**: {problem['description']}")
                st.write(f"**🔖 Tags**: {', '.join(problem.get('tags', []))}")
                st.markdown(f"[🔗 Solve on {problem['platform']}]({problem['url']})")
                
                # Mark as completed/uncompleted button
                if problem["id"] in completed_problems:
                    st.success("✅ You've completed this problem!")
                    if st.button("❌ Mark as Incomplete", key=f"incomplete_{problem_key}"):
                        remove_completed_problem(st.session_state.username, problem["id"])
                        st.success("Problem marked as incomplete!")
                        st.rerun()
                else:
                    if st.button("✅ Mark as Completed", key=f"complete_{problem_key}"):
                        save_completed_problem(st.session_state.username, problem["id"])
                        st.success("Problem marked as completed! Great job!")
                        st.rerun()
    
    if hard_problems and (current_level == "advanced" or selected_difficulty == "Hard" or selected_difficulty == "All Difficulties"):
        st.subheader("🔴 Hard Problems")
        for problem in hard_problems:
            problem_key = f"{problem['platform']}-{problem['id']}"
            with st.expander(f"{problem['title']} ({problem['platform']})"):
                st.write(f"**📝 Description**: {problem['description']}")
                st.write(f"**🔖 Tags**: {', '.join(problem.get('tags', []))}")
                st.markdown(f"[🔗 Solve on {problem['platform']}]({problem['url']})")
                
                # Mark as completed/uncompleted button
                if problem["id"] in completed_problems:
                    st.success("✅ You've completed this problem!")
                    if st.button("❌ Mark as Incomplete", key=f"incomplete_{problem_key}"):
                        remove_completed_problem(st.session_state.username, problem["id"])
                        st.success("Problem marked as incomplete!")
                        st.rerun()
                else:
                    if st.button("✅ Mark as Completed", key=f"complete_{problem_key}"):
                        save_completed_problem(st.session_state.username, problem["id"])
                        st.success("Problem marked as completed! Great job!")
                        st.rerun()
    
    # Show message if no problems match the filtered difficulty level
    if not any([easy_problems and (current_level == "beginner" or selected_difficulty == "Easy" or selected_difficulty == "All Difficulties"),
                medium_problems and (current_level == "intermediate" or selected_difficulty == "Medium" or selected_difficulty == "All Difficulties"),
                hard_problems and (current_level == "advanced" or selected_difficulty == "Hard" or selected_difficulty == "All Difficulties")]):
        st.info("No problems found matching your difficulty level filter. Try adjusting your filters.")
        
else:
    st.info("No problems found matching your criteria. Try adjusting your filters.")

# Tips section
st.header("💡 Coding Problem Tips")
st.markdown("""
### Tips for Solving Coding Problems:

1. **Understand the Problem**: Read the problem statement carefully and make sure you understand what's being asked
2. **Think about Edge Cases**: Consider input/output edge cases like empty arrays, zero values, etc.
3. **Solve by Hand First**: Work through a simple example manually before coding
4. **Start with Brute Force**: Get a working solution first, then optimize later
5. **Watch for Time/Space Complexity**: Consider the efficiency of your solution
6. **Test Your Code**: Double-check your solution with multiple test cases

### Common Patterns in Coding Problems:
- **Two Pointers**: Useful for array problems
- **Sliding Window**: Great for substring/subarray problems
- **Binary Search**: For searching in sorted arrays
- **DFS/BFS**: For tree and graph traversals
- **Dynamic Programming**: For optimization problems
""")

# Track progress
st.header("📊 Your Progress")

# Calculate statistics
total_solved = len(completed_problems)
platform_stats = {
    "LeetCode": len([p for p in completed_problems if p.startswith("lc")]),
    "HackerRank": len([p for p in completed_problems if p.startswith("hr")])
}

# Display stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Problems Solved", total_solved)
with col2:
    st.metric("LeetCode Problems", platform_stats["LeetCode"])
with col3:
    st.metric("HackerRank Problems", platform_stats["HackerRank"])

# Display difficulty breakdown
easy_solved = len([p for p in completed_problems if any(prob["id"] == p and (prob["difficulty"] == "Easy" or prob["difficulty"] == "Basic") for prob in all_platform_problems)])
medium_solved = len([p for p in completed_problems if any(prob["id"] == p and (prob["difficulty"] == "Medium" or prob["difficulty"] == "Intermediate") for prob in all_platform_problems)])
hard_solved = len([p for p in completed_problems if any(prob["id"] == p and (prob["difficulty"] == "Hard" or prob["difficulty"] == "Advanced" or prob["difficulty"] == "Expert") for prob in all_platform_problems)])

st.subheader("Difficulty Breakdown")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Easy Problems", easy_solved)
with col2:
    st.metric("Medium Problems", medium_solved)
with col3:
    st.metric("Hard Problems", hard_solved)

# Navigation buttons at the bottom
st.markdown("---")
cols = st.columns([1, 1, 1])
with cols[0]:
    if st.button("⬅️ Home"):
        st.switch_page("app_updated.py")
with cols[1]:
    if st.button("📚 Learning Resources"):
        level_page_map = {
            "beginner": "pages/beginner_updated.py",
            "intermediate": "pages/intermediate.py",
            "advanced": "pages/advanced.py"
        }
        st.switch_page(level_page_map.get(current_level, "pages/beginner_updated.py"))
with cols[2]:
    if st.button("🛠️ Projects"):
        st.switch_page("pages/projects.py")