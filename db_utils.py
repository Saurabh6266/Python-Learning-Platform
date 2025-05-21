from database import Session, User, Resource, Tag, Project, Skill, CompletedResource, Discussion, Reply
import streamlit as st
import datetime
import random

def load_resources():
    """Load resources from database"""
    session = Session()
    try:
        resources = session.query(Resource).all()
        return [resource.to_dict() for resource in resources]
    finally:
        session.close()

def load_projects():
    """Load projects from database"""
    session = Session()
    try:
        projects = session.query(Project).all()
        return [project.to_dict() for project in projects]
    finally:
        session.close()

def load_user_progress(username):
    """Load user progress from database"""
    session = Session()
    try:
        # Get or create user
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username=username)
            session.add(user)
            session.commit()
        
        # Update Streamlit session state
        st.session_state.username = username
        
        # Get completed resources
        completed = session.query(CompletedResource).filter_by(user_username=username).all()
        st.session_state.resources_completed = [cr.resource_id for cr in completed]
        st.session_state.current_level = user.current_level
        
        # Update last active
        user.update_last_active()
        session.commit()
        
    finally:
        session.close()

def save_user_progress(username, completed_resources, current_level):
    """Save user progress to database"""
    session = Session()
    try:
        # Get or create user
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username=username)
            session.add(user)
        
        # Update user level
        user.current_level = current_level
        user.update_last_active()
        
        # Get existing completed resources
        existing_completed = set(cr.resource_id for cr in 
                              session.query(CompletedResource).filter_by(user_username=username).all())
        
        # Add new completed resources
        for resource_id in completed_resources:
            if resource_id not in existing_completed:
                completed = CompletedResource(
                    user_username=username,
                    resource_id=resource_id,
                    completed_at=datetime.datetime.now()
                )
                session.add(completed)
        
        # Remove completed resources that are no longer in the list
        for resource_id in existing_completed:
            if resource_id not in completed_resources:
                to_delete = session.query(CompletedResource).filter_by(
                    user_username=username, 
                    resource_id=resource_id
                ).first()
                if to_delete:
                    session.delete(to_delete)
        
        session.commit()
    finally:
        session.close()

def get_recommendations(level, completed_resources):
    """Get personalized recommendations based on user's progress"""
    session = Session()
    try:
        # Get all resources for the current level that haven't been completed
        resources = session.query(Resource).filter(
            Resource.level == level,
            ~Resource.id.in_(completed_resources)
        ).all()
        
        # Convert to dictionary format
        available_resources = [resource.to_dict() for resource in resources]
        
        # If user has completed more than 80% of current level, suggest some from next level
        if level != "advanced":
            # Count completed level resources
            completed_count = session.query(Resource).filter(
                Resource.level == level,
                Resource.id.in_(completed_resources)
            ).count()
            
            # Count all resources at this level
            total_count = session.query(Resource).filter(
                Resource.level == level
            ).count()
            
            if total_count > 0 and completed_count / total_count >= 0.8:
                next_level = "intermediate" if level == "beginner" else "advanced"
                next_level_resources = session.query(Resource).filter(
                    Resource.level == next_level,
                    ~Resource.id.in_(completed_resources)
                ).limit(2).all()
                
                available_resources.extend([r.to_dict() for r in next_level_resources])
        
        # Randomize a bit to provide variety
        random.shuffle(available_resources)
        
        return available_resources
    finally:
        session.close()

def load_discussions():
    """Load discussions from database"""
    session = Session()
    try:
        discussions = session.query(Discussion).all()
        return {"topics": [discussion.to_dict() for discussion in discussions]}
    finally:
        session.close()

def add_topic(title, content, author, category):
    """Add a new discussion topic"""
    session = Session()
    try:
        # Get next ID 
        max_id = session.query(Discussion).order_by(Discussion.id.desc()).first()
        next_id = 1 if max_id is None else max_id.id + 1
        
        # Create discussion
        discussion = Discussion(
            id=next_id,
            title=title,
            content=content,
            author=author,
            category=category
        )
        
        session.add(discussion)
        session.commit()
        return discussion.id
    finally:
        session.close()

def add_reply(topic_id, content, author):
    """Add a reply to a discussion topic"""
    session = Session()
    try:
        # Find discussion
        discussion = session.query(Discussion).filter_by(id=topic_id).first()
        if not discussion:
            return False
        
        # Create reply
        reply = Reply(
            content=content,
            author=author,
            discussion=discussion
        )
        
        session.add(reply)
        session.commit()
        return True
    finally:
        session.close()