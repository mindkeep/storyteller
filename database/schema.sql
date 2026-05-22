-- StoryTeller Database Schema

-- Enable UUID extension for better ID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table - authentication and profile data
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true
);

-- Scenarios table - reusable game settings and templates
CREATE TABLE scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    setting TEXT NOT NULL,
    initial_location TEXT NOT NULL,
    world_rules JSONB DEFAULT '{}',
    is_public BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personas table - AI dungeon master personalities
CREATE TABLE personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    personality TEXT NOT NULL,
    behavior_traits JSONB DEFAULT '{}',
    prompt_template TEXT,
    is_public BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Games table - individual game instances
CREATE TABLE games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    scenario_id UUID REFERENCES scenarios(id) ON DELETE RESTRICT,
    persona_id UUID REFERENCES personas(id) ON DELETE RESTRICT,
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    current_location TEXT,
    game_time JSONB DEFAULT '{"year": 1, "month": 1, "day": 1, "hour": 12, "minute": 0}',
    world_state JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'archived')),
    max_players INTEGER DEFAULT 1,
    is_multiplayer BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_played TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Game participants - handles multiplayer games
CREATE TABLE game_participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'player' CHECK (role IN ('owner', 'player', 'observer')),
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    UNIQUE(game_id, user_id)
);

-- Characters table - player characters in games
CREATE TABLE characters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    background TEXT,
    current_location TEXT,
    level INTEGER DEFAULT 1,
    experience_points INTEGER DEFAULT 0,
    health_current INTEGER DEFAULT 100,
    health_max INTEGER DEFAULT 100,
    stats JSONB DEFAULT '{}', -- strength, dexterity, intelligence, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Character inventory - items and equipment
CREATE TABLE character_inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50), -- weapon, armor, consumable, tool, misc
    description TEXT,
    quantity INTEGER DEFAULT 1,
    properties JSONB DEFAULT '{}', -- damage, armor_class, magic_properties, etc.
    is_equipped BOOLEAN DEFAULT false,
    acquired_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Character skills and abilities
CREATE TABLE character_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    skill_level INTEGER DEFAULT 1,
    experience_points INTEGER DEFAULT 0,
    skill_type VARCHAR(50), -- combat, magic, social, crafting, etc.
    description TEXT,
    learned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(character_id, skill_name)
);

-- Character relationships - NPCs, other players, factions
CREATE TABLE character_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    target_name VARCHAR(100) NOT NULL,
    target_type VARCHAR(20) CHECK (target_type IN ('npc', 'player', 'faction', 'organization')),
    relationship_type VARCHAR(20), -- friend, enemy, neutral, romantic, family, etc.
    relationship_strength INTEGER DEFAULT 0, -- -100 to 100
    notes TEXT,
    last_interaction TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat history - conversation messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    character_id UUID REFERENCES characters(id) ON DELETE SET NULL,
    message_type VARCHAR(20) DEFAULT 'user' CHECK (message_type IN ('user', 'assistant', 'system', 'action', 'narration')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}', -- embedding vectors, mood, context flags, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    edited_at TIMESTAMP WITH TIME ZONE,
    is_deleted BOOLEAN DEFAULT false
);

-- Game summaries - periodic state snapshots for context management
CREATE TABLE game_summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    summary_type VARCHAR(20) DEFAULT 'periodic' CHECK (summary_type IN ('periodic', 'chapter', 'session')),
    content TEXT NOT NULL,
    covers_messages_from TIMESTAMP WITH TIME ZONE,
    covers_messages_to TIMESTAMP WITH TIME ZONE,
    embedding_vector VECTOR(1536), -- for semantic search (OpenAI ada-002 dimension)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- World locations - places that can be visited
CREATE TABLE world_locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    location_type VARCHAR(50), -- town, dungeon, wilderness, building, etc.
    coordinates JSONB, -- x, y, z coordinates or map references
    connections JSONB DEFAULT '[]', -- connected location IDs and travel requirements
    properties JSONB DEFAULT '{}', -- shops, NPCs, hazards, resources, etc.
    discovered_by UUID REFERENCES characters(id) ON DELETE SET NULL,
    discovered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- NPCs - non-player characters
CREATE TABLE npcs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    location_id UUID REFERENCES world_locations(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    personality TEXT,
    role VARCHAR(50), -- merchant, guard, quest_giver, enemy, etc.
    stats JSONB DEFAULT '{}',
    inventory JSONB DEFAULT '[]',
    dialogue_state JSONB DEFAULT '{}',
    is_alive BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_games_owner_status ON games(owner_id, status);
CREATE INDEX idx_chat_messages_game_created ON chat_messages(game_id, created_at);
CREATE INDEX idx_characters_game_active ON characters(game_id, is_active);
CREATE INDEX idx_game_participants_user ON game_participants(user_id, is_active);
CREATE INDEX idx_summaries_game_type ON game_summaries(game_id, summary_type);
CREATE INDEX idx_inventory_character ON character_inventory(character_id);
CREATE INDEX idx_skills_character ON character_skills(character_id);
CREATE INDEX idx_relationships_character ON character_relationships(character_id);

-- Update timestamp triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_scenarios_updated_at BEFORE UPDATE ON scenarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_personas_updated_at BEFORE UPDATE ON personas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_games_updated_at BEFORE UPDATE ON games
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_characters_updated_at BEFORE UPDATE ON characters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_npcs_updated_at BEFORE UPDATE ON npcs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();