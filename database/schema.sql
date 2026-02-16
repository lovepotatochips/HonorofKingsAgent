CREATE DATABASE IF NOT EXISTS honor_of_kings DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE honor_of_kings;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY,
    nickname VARCHAR(50),
    avatar VARCHAR(200),
    rank VARCHAR(50),
    stars INT DEFAULT 0,
    favorite_heroes JSON,
    preferences JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS heroes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(100),
    position VARCHAR(20),
    difficulty VARCHAR(20),
    description TEXT,
    skills JSON,
    passive_skill JSON,
    win_rate FLOAT DEFAULT 0.0,
    ban_rate FLOAT DEFAULT 0.0,
    pick_rate FLOAT DEFAULT 0.0,
    counter_heroes JSON,
    countered_by_heroes JSON,
    version VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_position (position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS hero_equipments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hero_id INT NOT NULL,
    rank VARCHAR(20),
    position VARCHAR(20),
    equipment_list JSON,
    win_rate FLOAT,
    pick_rate FLOAT,
    version VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hero_id) REFERENCES heroes(id) ON DELETE CASCADE,
    INDEX idx_hero_id (hero_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS hero_inscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hero_id INT NOT NULL,
    rank VARCHAR(20),
    inscription_name VARCHAR(50),
    inscription_config JSON,
    description TEXT,
    win_rate FLOAT,
    version VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hero_id) REFERENCES heroes(id) ON DELETE CASCADE,
    INDEX idx_hero_id (hero_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS equipments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(20),
    price INT,
    stats JSON,
    passive TEXT,
    active TEXT,
    build_from JSON,
    build_into JSON,
    version VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50) NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT,
    intent VARCHAR(50),
    context JSON,
    hero_id INT,
    match_id VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (hero_id) REFERENCES heroes(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS matches (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    hero_id INT,
    hero_name VARCHAR(50),
    position VARCHAR(20),
    result VARCHAR(10),
    duration INT,
    kills INT DEFAULT 0,
    deaths INT DEFAULT 0,
    assists INT DEFAULT 0,
    gold INT DEFAULT 0,
    damage INT DEFAULT 0,
    damage_taken INT DEFAULT 0,
    healing INT DEFAULT 0,
    participation_rate FLOAT DEFAULT 0.0,
    kda FLOAT DEFAULT 0.0,
    equipment_list JSON,
    inscription JSON,
    rank VARCHAR(50),
    screenshot_url VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (hero_id) REFERENCES heroes(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS analyses (
    id VARCHAR(50) PRIMARY KEY,
    match_id VARCHAR(50) NOT NULL,
    overall_rating VARCHAR(20),
    highlights JSON,
    mistakes JSON,
    suggestions JSON,
    report TEXT,
    improvements JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    INDEX idx_match_id (match_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
