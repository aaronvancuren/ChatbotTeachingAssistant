-- Type: model

-- DROP TYPE IF EXISTS public.model;

CREATE TYPE public.model AS ENUM
    ('gpt-4o', 'chatgpt-4o-latest', 'gpt-4o-mini', 'o1', 'o1-mini', 'o1-preview');

ALTER TYPE public.model
    OWNER TO "teaching-assistant";
