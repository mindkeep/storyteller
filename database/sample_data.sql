-- Sample data for StoryTeller database
-- This file demonstrates the schema with realistic test data

-- Sample users
INSERT INTO users (username, email, display_name, preferences) VALUES
('alice_dm', 'alice@example.com', 'Alice the DM', '{"theme": "dark", "notifications": true}'),
('bob_player', 'bob@example.com', 'Bob', '{"theme": "light", "auto_save": true}'),
('charlie_rogue', 'charlie@example.com', 'Charlie', '{"theme": "dark", "dice_animation": false}');

-- Sample scenarios
INSERT INTO scenarios (name, description, setting, initial_location, world_rules, is_public, created_by) VALUES
(
    'Tavern Tales',
    'Classic fantasy adventure starting in a roadside tavern',
    'Our adventure begins in a lonely tavern. The barkeep leans in and says, "I mean no offense, but you look like you could use some work. I have a job for you if you''re interested."',
    'Dusty''s Tavern lays along the road between the small towns of Oakwood and Riverton. It''s a popular stop for travelers, merchants, and those in search of odd jobs.',
    '{"magic_level": "high", "technology_level": "medieval", "danger_level": "moderate"}',
    true,
    (SELECT id FROM users WHERE username = 'alice_dm')
),
(
    'Cyberpunk Streets',
    'Near-future urban adventure in a corporate dystopia',
    'The neon lights flicker against the rain-soaked streets of Neo Tokyo. Corporate towers pierce the smoggy sky while the underground buzzes with rebellion.',
    'You''re in a dimly lit bar in the Shibuya Underground, where data thieves and corporate refugees gather to trade information and plan their next moves.',
    '{"magic_level": "none", "technology_level": "cyberpunk", "danger_level": "high", "corporations": ["Arasaka", "Militech", "NetWatch"]}',
    true,
    (SELECT id FROM users WHERE username = 'alice_dm')
);

-- Sample personas
INSERT INTO personas (name, description, personality, behavior_traits, is_public, created_by) VALUES
(
    'Classic DM',
    'Traditional fantasy dungeon master with a fair but challenging approach',
    'You are a dungeon master responding to player actions. You create immersive fantasy experiences while maintaining game balance. You reward clever thinking and roleplaying.',
    '{"humor_level": "moderate", "difficulty": "balanced", "description_style": "detailed", "npc_voices": true}',
    true,
    (SELECT id FROM users WHERE username = 'alice_dm')
),
(
    'Noir Detective',
    'Gritty urban storyteller focused on mystery and investigation',
    'You are a noir-style game master. Everything is tinged with shadows and moral ambiguity. You excel at weaving mysteries and creating atmospheric tension.',
    '{"humor_level": "dark", "difficulty": "hard", "description_style": "atmospheric", "mystery_focus": true}',
    true,
    (SELECT id FROM users WHERE username = 'alice_dm')
);

-- Sample game
INSERT INTO games (name, description, scenario_id, persona_id, owner_id, current_location, game_time, world_state, max_players, is_multiplayer) VALUES
(
    'The Dusty Crown Adventure',
    'A classic fantasy adventure where our heroes seek the lost crown of the ancient king',
    (SELECT id FROM scenarios WHERE name = 'Tavern Tales'),
    (SELECT id FROM personas WHERE name = 'Classic DM'),
    (SELECT id FROM users WHERE username = 'alice_dm'),
    'Dusty''s Tavern',
    '{"year": 1247, "month": 3, "day": 15, "hour": 18, "minute": 30}',
    '{"weather": "light_rain", "tavern_crowd": "moderate", "barkeep_mood": "friendly", "rumor_level": "high"}',
    4,
    true
);

-- Game participants
INSERT INTO game_participants (game_id, user_id, role) VALUES
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM users WHERE username = 'alice_dm'), 'owner'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM users WHERE username = 'bob_player'), 'player'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM users WHERE username = 'charlie_rogue'), 'player');

-- Sample characters
INSERT INTO characters (game_id, user_id, name, description, background, current_location, level, health_current, health_max, stats) VALUES
(
    (SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'),
    (SELECT id FROM users WHERE username = 'bob_player'),
    'Thorin Ironforge',
    'A stout dwarf with a magnificent braided beard and keen eyes that miss nothing',
    'Former royal guard seeking redemption after failing to protect the old king',
    'Dusty''s Tavern',
    3,
    45,
    50,
    '{"strength": 16, "dexterity": 12, "constitution": 15, "intelligence": 10, "wisdom": 14, "charisma": 8}'
),
(
    (SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'),
    (SELECT id FROM users WHERE username = 'charlie_rogue'),
    'Whisper',
    'A hooded figure whose face is always in shadow, moving with cat-like grace',
    'Street thief turned adventurer, haunted by a mysterious past',
    'Dusty''s Tavern',
    3,
    32,
    35,
    '{"strength": 10, "dexterity": 18, "constitution": 12, "intelligence": 14, "wisdom": 13, "charisma": 15}'
);

-- Sample inventory
INSERT INTO character_inventory (character_id, item_name, item_type, description, quantity, properties, is_equipped) VALUES
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Dwarven Warhammer', 'weapon', 'A masterwork hammer with runes of protection', 1, '{"damage": "1d10+3", "enchantment": "+1", "weight": 5}', true),
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Chain Mail', 'armor', 'Well-maintained chain mail armor', 1, '{"armor_class": 16, "weight": 20}', true),
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Healing Potion', 'consumable', 'Restores 2d4+2 hit points', 3, '{"healing": "2d4+2", "weight": 0.5}', false),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Thieves'' Tools', 'tool', 'Professional lockpicking kit', 1, '{"bonus": "+2", "weight": 1}', false),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Shortsword', 'weapon', 'A balanced blade perfect for quick strikes', 1, '{"damage": "1d6+4", "finesse": true, "weight": 2}', true),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Leather Armor', 'armor', 'Supple leather that doesn''t restrict movement', 1, '{"armor_class": 13, "stealth": "no_disadvantage", "weight": 10}', true);

-- Sample skills
INSERT INTO character_skills (character_id, skill_name, skill_level, skill_type, description) VALUES
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Weapon Mastery: Hammers', 8, 'combat', 'Expert with hammer-type weapons'),
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Shield Wall', 6, 'combat', 'Defensive formation fighting'),
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Royal Protocol', 4, 'social', 'Knowledge of noble customs and court etiquette'),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Stealth', 9, 'social', 'Moving unseen and unheard'),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Lockpicking', 7, 'crafting', 'Opening locks without keys'),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Sleight of Hand', 6, 'social', 'Pickpocketing and misdirection');

-- Sample relationships
INSERT INTO character_relationships (character_id, target_name, target_type, relationship_type, relationship_strength, notes) VALUES
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'King Aldric the Lost', 'npc', 'loyalty', 80, 'Former liege lord, feels responsible for his disappearance'),
((SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'Whisper', 'player', 'friend', 40, 'Cautious trust, appreciates their skills despite different backgrounds'),
((SELECT id FROM characters WHERE name = 'Whisper'), 'The Shadow Guild', 'organization', 'enemy', -70, 'Former thieves guild that betrayed them'),
((SELECT id FROM characters WHERE name = 'Whisper'), 'Thorin Ironforge', 'player', 'friend', 35, 'Respects the dwarf''s honor, though finds them a bit rigid');

-- Sample chat history
INSERT INTO chat_messages (game_id, user_id, character_id, message_type, content, metadata) VALUES
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), NULL, NULL, 'system', 'Welcome to The Dusty Crown Adventure! The rain patters against the windows of Dusty''s Tavern as you both sit at a corner table, nursing your drinks and watching the other patrons.', '{"scene_setting": true}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM users WHERE username = 'bob_player'), (SELECT id FROM characters WHERE name = 'Thorin Ironforge'), 'user', 'I look around the tavern, searching for anyone who might have information about the lost crown.', '{"action_type": "perception", "target": "tavern_patrons"}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), NULL, NULL, 'assistant', 'Your keen dwarven eyes scan the room. Most of the patrons seem to be ordinary travelers, but you notice an old man in the corner wearing a faded royal seal on his cloak. He catches your gaze and nods slightly.', '{"npc_introduced": "old_man_royal_seal", "perception_success": true}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM users WHERE username = 'charlie_rogue'), (SELECT id FROM characters WHERE name = 'Whisper'), 'user', 'I casually move closer to the bar, trying to overhear conversations without drawing attention.', '{"action_type": "stealth", "target": "information_gathering"}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), NULL, NULL, 'assistant', 'You glide silently through the crowd like a shadow. From your position near the bar, you overhear two merchants discussing strange lights seen near the old ruins of Thornwick Castle - the same castle where the crown was last seen.', '{"stealth_success": true, "information_gained": "thornwick_castle_lights", "plot_advancement": true}');

-- Sample world locations
INSERT INTO world_locations (game_id, name, description, location_type, coordinates, connections, properties) VALUES
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), 'Dusty''s Tavern', 'A weathered roadside inn with creaking floors and a warm hearth', 'building', '{"x": 0, "y": 0}', '[{"location": "Oakwood Road", "travel_time": "immediate", "difficulty": "easy"}]', '{"has_barkeep": true, "room_cost": "2sp", "meal_cost": "5cp", "rumor_source": true}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), 'Oakwood Road', 'A well-traveled dirt road connecting Oakwood and Riverton', 'road', '{"x": 0, "y": -1}', '[{"location": "Dusty''s Tavern", "travel_time": "immediate"}, {"location": "Oakwood", "travel_time": "2 hours"}, {"location": "Riverton", "travel_time": "3 hours"}]', '{"random_encounters": true, "merchant_traffic": "moderate"}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), 'Thornwick Castle Ruins', 'Ancient stone ruins shrouded in mystery and strange lights', 'ruins', '{"x": -5, "y": 3}', '[{"location": "Thornwick Forest", "travel_time": "1 hour", "difficulty": "moderate"}]', '{"danger_level": "high", "treasure_likely": true, "magical_aura": true, "last_seen_crown": true}');

-- Sample NPCs
INSERT INTO npcs (game_id, location_id, name, description, personality, role, stats, inventory, dialogue_state) VALUES
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM world_locations WHERE name = 'Dusty''s Tavern'), 'Dusty Pete', 'The tavern owner, a portly man with a permanently flour-dusted apron', 'Friendly but cautious, knows more than he lets on', 'tavern_keeper', '{"health": 25, "armor_class": 10}', '["tavern_keys", "cash_box", "hidden_dagger"]', '{"met_players": true, "trust_level": "neutral", "knows_crown_rumors": true}'),
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), (SELECT id FROM world_locations WHERE name = 'Dusty''s Tavern'), 'Sir Marcus the Exile', 'An old man in faded royal colors, nursing a mug of ale with shaking hands', 'Bitter about past failures, desperate for redemption', 'quest_giver', '{"health": 30, "armor_class": 12}', '["royal_seal", "old_sword", "letter_of_marque"]', '{"met_players": false, "quest_available": true, "emotional_state": "melancholy"}');

-- Sample game summary
INSERT INTO game_summaries (game_id, summary_type, content, covers_messages_from, covers_messages_to) VALUES
((SELECT id FROM games WHERE name = 'The Dusty Crown Adventure'), 'session', 'The adventure began in Dusty''s Tavern where Thorin Ironforge and Whisper met. Thorin spotted a mysterious old man with royal insignia, while Whisper overheard merchants discussing strange lights at Thornwick Castle ruins - potentially connected to the lost crown they seek. The party is positioned to make contact with potential allies and gather more information about their quest.', NOW() - INTERVAL '2 hours', NOW());