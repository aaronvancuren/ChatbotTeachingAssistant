-- Type: role

CREATE TYPE public.role AS ENUM
    ('student', 'instructor', 'admin');

ALTER TYPE public.role
    OWNER TO "teaching-assistant";
