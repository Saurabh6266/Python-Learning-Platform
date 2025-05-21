import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import json

# Create engine and base
db_path = os.path.join('data', 'python_learning.db')
os.makedirs('data', exist_ok=True)
engine = create_engine(f'sqlite:///{db_path}')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define association tables for many-to-many relationships
resource_tag_association = Table(
    'resource_tag_association', 
    Base.metadata,
    Column('resource_id', String, ForeignKey('resources.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

project_skill_association = Table(
    'project_skill_association',
    Base.metadata,
    Column('project_id', String, ForeignKey('projects.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

# Define models
class User(Base):
    __tablename__ = 'users'
    
    username = Column(String, primary_key=True)
    current_level = Column(String, default='beginner')
    last_active = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    completed_resources = relationship("CompletedResource", back_populates="user")
    
    def __repr__(self):
        return f"<User(username='{self.username}', level='{self.current_level}')>"
        
    def update_last_active(self):
        """Update the last_active timestamp"""
        self.last_active = datetime.datetime.now()

class CompletedResource(Base):
    __tablename__ = 'completed_resources'
    
    id = Column(Integer, primary_key=True)
    user_username = Column(String, ForeignKey('users.username'))
    resource_id = Column(String, ForeignKey('resources.id'))
    completed_at = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="completed_resources")
    resource = relationship("Resource")
    
    def __repr__(self):
        return f"<CompletedResource(user='{self.user_username}', resource='{self.resource_id}')>"

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    def __repr__(self):
        return f"<Tag(name='{self.name}')>"

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    def __repr__(self):
        return f"<Skill(name='{self.name}')>"

class Resource(Base):
    __tablename__ = 'resources'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    type = Column(String)
    description = Column(Text)
    url = Column(String)
    level = Column(String)
    
    # Relationships
    tags = relationship("Tag", secondary=resource_tag_association)
    
    def __repr__(self):
        return f"<Resource(id='{self.id}', title='{self.title}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'url': self.url,
            'level': self.level,
            'tags': [tag.name for tag in self.tags]
        }

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    level = Column(String)
    difficulty = Column(Integer)
    details = Column(Text)
    starter_code = Column(Text)
    
    # Relationships
    skills = relationship("Skill", secondary=project_skill_association)
    
    def __repr__(self):
        return f"<Project(id='{self.id}', title='{self.title}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'level': self.level,
            'difficulty': self.difficulty,
            'details': self.details,
            'starter_code': self.starter_code,
            'skills': [skill.name for skill in self.skills]
        }

class Discussion(Base):
    __tablename__ = 'discussions'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    author = Column(String, ForeignKey('users.username'))
    category = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    replies = relationship("Reply", back_populates="discussion")
    
    def __repr__(self):
        return f"<Discussion(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'replies': [reply.to_dict() for reply in self.replies]
        }

class Reply(Base):
    __tablename__ = 'replies'
    
    id = Column(Integer, primary_key=True)
    discussion_id = Column(Integer, ForeignKey('discussions.id'))
    content = Column(Text)
    author = Column(String, ForeignKey('users.username'))
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    discussion = relationship("Discussion", back_populates="replies")
    
    def __repr__(self):
        return f"<Reply(id={self.id}, discussion_id={self.discussion_id})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat()
        }

# Initialize the database
def init_db():
    Base.metadata.create_all(engine)

# Migration: Move data from JSON files to SQLite
def migrate_from_json():
    from utils import load_resources, load_projects
    
    session = Session()
    
    # Migrate resources
    try:
        resources = load_resources()
        for resource in resources:
            # First check if resource already exists
            existing = session.query(Resource).filter_by(id=resource['id']).first()
            if existing:
                continue
                
            db_resource = Resource(
                id=resource['id'],
                title=resource['title'],
                type=resource['type'],
                description=resource['description'],
                url=resource['url'],
                level=resource['level']
            )
            
            # Add tags
            for tag_name in resource.get('tags', []):
                # Get or create tag
                tag = session.query(Tag).filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    session.add(tag)
                db_resource.tags.append(tag)
            
            session.add(db_resource)
        
        # Migrate projects
        projects = load_projects()
        for project in projects:
            # First check if project already exists
            existing = session.query(Project).filter_by(id=project['id']).first()
            if existing:
                continue
                
            db_project = Project(
                id=project['id'],
                title=project['title'],
                description=project['description'],
                level=project['level'],
                difficulty=project['difficulty'],
                details=project['details'],
                starter_code=project.get('starter_code', '')
            )
            
            # Add skills
            for skill_name in project.get('skills', []):
                # Get or create skill
                skill = session.query(Skill).filter_by(name=skill_name).first()
                if not skill:
                    skill = Skill(name=skill_name)
                    session.add(skill)
                db_project.skills.append(skill)
            
            session.add(db_project)
        
        # Migrate user progress
        user_progress_file = os.path.join('data', 'user_progress.json')
        if os.path.exists(user_progress_file):
            with open(user_progress_file, 'r') as f:
                user_progress = json.load(f)
                
            for username, data in user_progress.items():
                # Create or update user
                user = session.query(User).filter_by(username=username).first()
                if not user:
                    user = User(username=username)
                
                user.current_level = data.get('current_level', 'beginner')
                
                # Add completed resources
                for resource_id in data.get('completed_resources', []):
                    # Check if this completion already exists
                    existing = session.query(CompletedResource).filter_by(
                        user_username=username, 
                        resource_id=resource_id
                    ).first()
                    
                    if not existing:
                        completed = CompletedResource(
                            user_username=username,
                            resource_id=resource_id
                        )
                        session.add(completed)
                
                session.add(user)
        
        # Migrate discussions
        discussions_file = os.path.join('data', 'discussions.json')
        if os.path.exists(discussions_file):
            with open(discussions_file, 'r') as f:
                discussions_data = json.load(f)
                
            for topic in discussions_data.get('topics', []):
                # Check if this user exists, create if not
                user = session.query(User).filter_by(username=topic['author']).first()
                if not user:
                    user = User(username=topic['author'])
                    session.add(user)
                
                # Create discussion
                discussion = Discussion(
                    id=topic['id'],
                    title=topic['title'],
                    content=topic['content'],
                    author=topic['author'],
                    category=topic['category'],
                    created_at=datetime.datetime.fromisoformat(topic['created_at'])
                )
                
                # Add replies
                for reply_data in topic.get('replies', []):
                    # Check if this user exists, create if not
                    reply_user = session.query(User).filter_by(username=reply_data['author']).first()
                    if not reply_user:
                        reply_user = User(username=reply_data['author'])
                        session.add(reply_user)
                    
                    reply = Reply(
                        content=reply_data['content'],
                        author=reply_data['author'],
                        created_at=datetime.datetime.fromisoformat(reply_data['created_at'])
                    )
                    discussion.replies.append(reply)
                
                session.add(discussion)
        
        session.commit()
        print("Data migration completed successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {e}")
    finally:
        session.close()

# Initialize database and migrate data
if __name__ == '__main__':
    init_db()
    migrate_from_json()