DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'blacklist_type') THEN
        CREATE TYPE blacklist_type AS ENUM ('user', 'guild');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'owo_type') THEN
        CREATE TYPE owo_type AS ENUM ('owo', 'uwu', 'qwq', ':3', '-w-');
    END IF;
END
$$;

DROP TABLE levels;
DROP TABLE guilds;
DROP TABLE role_rewards;

CREATE TABLE IF NOT EXISTS levels (
    guild_id BIGINT PRIMARY KEY,
    user_id  BIGINT NOT NULL,
    level    BIGINT NOT NULL,
    xp       BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS role_rewards (
    guild_id BIGINT NOT NULL,
    role_id  BIGINT PRIMARY KEY,
    level    BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS guilds (
    guild_id          BIGINT  PRIMARY KEY,
    levelling_enabled BOOLEAN DEFAULT NULL
);