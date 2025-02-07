-- Type: role

-- DROP TYPE IF EXISTS public.role;

CREATE TYPE public.role AS ENUM
    ('student', 'instructor', 'admin');

ALTER TYPE public.role
    OWNER TO "teaching-assistant";
