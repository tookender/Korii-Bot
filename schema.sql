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