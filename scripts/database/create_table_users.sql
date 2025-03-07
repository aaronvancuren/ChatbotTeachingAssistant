-- Table: public.users

CREATE TABLE IF NOT EXISTS public.users
(
    id uuid,
    display_name text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    role role NOT NULL DEFAULT 'student'::role,
    create_at timestamp with time zone NOT NULL DEFAULT now(),
	archived boolean NOT NULL DEFAULT false,
    archived_by uuid,
    archived_at timestamp with time zone,
    CONSTRAINT users_pkey PRIMARY KEY (email),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_archived_by_fkey FOREIGN KEY (archived_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to "teaching-assistant";

COMMENT ON TABLE public.users
    IS 'Application users';

COMMENT ON COLUMN public.users.id
    IS 'GUID set by the application';

COMMENT ON COLUMN public.users.display_name
    IS 'Display name retrieved from PFW';

COMMENT ON COLUMN public.users.email
    IS 'PFW email';