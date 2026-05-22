"""
Database connection and models for StoryTeller
Production-ready PostgreSQL integration with SQLAlchemy
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import create_engine, Column, String, Text, Integer, Boolean, DateTime, JSON, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, field_validator
from contextlib import contextmanager

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    avatar_url = Column(Text)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    owned_games = relationship("Game", back_populates="owner")
    participations = relationship("GameParticipant", back_populates="user")
    characters = relationship("Character", back_populates="user")

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    setting = Column(Text, nullable=False)
    initial_location = Column(Text, nullable=False)
    world_rules = Column(JSON, default={})
    is_public = Column(Boolean, default=False)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    games = relationship("Game", back_populates="scenario")

class Persona(Base):
    __tablename__ = "personas"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    personality = Column(Text, nullable=False)
    behavior_traits = Column(JSON, default={})
    prompt_template = Column(Text)
    is_public = Column(Boolean, default=False)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    games = relationship("Game", back_populates="persona")

class Game(Base):
    __tablename__ = "games"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    scenario_id = Column(PGUUID(as_uuid=True), ForeignKey("scenarios.id", ondelete="RESTRICT"))
    persona_id = Column(PGUUID(as_uuid=True), ForeignKey("personas.id", ondelete="RESTRICT"))
    owner_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    current_location = Column(Text)
    game_time = Column(JSON, default={"year": 1, "month": 1, "day": 1, "hour": 12, "minute": 0})
    world_state = Column(JSON, default={})
    status = Column(String(20), default="active")
    max_players = Column(Integer, default=1)
    is_multiplayer = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_played = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="owned_games")
    scenario = relationship("Scenario", back_populates="games")
    persona = relationship("Persona", back_populates="games")
    participants = relationship("GameParticipant", back_populates="game")
    characters = relationship("Character", back_populates="game")
    messages = relationship("ChatMessage", back_populates="game")
    summaries = relationship("GameSummary", back_populates="game")

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(PGUUID(as_uuid=True), ForeignKey("games.id", ondelete="CASCADE"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    background = Column(Text)
    current_location = Column(Text)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    health_current = Column(Integer, default=100)
    health_max = Column(Integer, default=100)
    stats = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    game = relationship("Game", back_populates="characters")
    user = relationship("User", back_populates="characters")
    inventory = relationship("CharacterInventory", back_populates="character")
    skills = relationship("CharacterSkill", back_populates="character")
    relationships = relationship("CharacterRelationship", back_populates="character")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(PGUUID(as_uuid=True), ForeignKey("games.id", ondelete="CASCADE"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    character_id = Column(PGUUID(as_uuid=True), ForeignKey("characters.id", ondelete="SET NULL"))
    message_type = Column(String(20), default="user")
    content = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True))
    is_deleted = Column(Boolean, default=False)
    
    # Relationships
    game = relationship("Game", back_populates="messages")

class GameParticipant(Base):
    __tablename__ = "game_participants"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    game_id = Column(PGUUID(as_uuid=True), ForeignKey("games.id", ondelete="CASCADE"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(String(20), default="player")
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    game = relationship("Game", back_populates="participants")
    user = relationship("User", back_populates="participations")

# Additional models would go here (CharacterInventory, CharacterSkill, etc.)

# Pydantic models for API
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    display_name: Optional[str] = None
    
    @field_validator('username')
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class GameCreate(BaseModel):
    name: str
    description: Optional[str] = None
    scenario_id: UUID
    persona_id: UUID
    max_players: int = 1
    is_multiplayer: bool = False

class CharacterCreate(BaseModel):
    name: str
    description: Optional[str] = None
    background: Optional[str] = None
    stats: Dict[str, Any] = {}

class MessageCreate(BaseModel):
    content: str
    message_type: str = "user"
    character_id: Optional[UUID] = None

# Database utility functions
@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class DatabaseManager:
    """High-level database operations"""
    
    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        with get_db_session() as session:
            user = User(**user_data.dict())
            session.add(user)
            session.flush()
            return user
    
    @staticmethod
    def get_user_games(user_id: UUID) -> List[Game]:
        """Get all games for a user"""
        with get_db_session() as session:
            return session.query(Game).filter(
                Game.participants.any(user_id=user_id)
            ).all()
    
    @staticmethod
    def create_game(game_data: GameCreate, owner_id: UUID) -> Game:
        """Create a new game"""
        with get_db_session() as session:
            game = Game(**game_data.dict(), owner_id=owner_id)
            session.add(game)
            session.flush()
            
            # Add owner as participant
            participant = GameParticipant(
                game_id=game.id,
                user_id=owner_id,
                role="owner"
            )
            session.add(participant)
            return game
    
    @staticmethod
    def add_message(game_id: UUID, message_data: MessageCreate, user_id: Optional[UUID] = None) -> ChatMessage:
        """Add a message to a game"""
        with get_db_session() as session:
            message = ChatMessage(
                game_id=game_id,
                user_id=user_id,
                **message_data.dict()
            )
            session.add(message)
            session.flush()
            return message
    
    @staticmethod
    def get_game_history(game_id: UUID, limit: int = 50) -> List[ChatMessage]:
        """Get recent chat history for a game"""
        with get_db_session() as session:
            return session.query(ChatMessage).filter(
                ChatMessage.game_id == game_id,
                ChatMessage.is_deleted == False
            ).order_by(ChatMessage.created_at.desc()).limit(limit).all()

# Connection test function
def test_connection():
    """Test database connection"""
    try:
        with get_db_session() as session:
            result = session.execute(text("SELECT 1")).scalar()
            return result == 1
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")