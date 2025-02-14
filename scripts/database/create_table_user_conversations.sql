-- Table: public.user_conversations

CREATE TABLE IF NOT EXISTS public.user_conversations
(
    conversation_id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    course_id uuid NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    archived boolean NOT NULL DEFAULT false,
    archived_by uuid,
    archived_at timestamp with time zone,
    CONSTRAINT user_conversations_pkey PRIMARY KEY (conversation_id),
    CONSTRAINT user_conversations_archive_by_fkey FOREIGN KEY (archived_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT,
    CONSTRAINT user_conversations_course_id_fkey FOREIGN KEY (course_id)
        REFERENCES public.courses (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT,
    CONSTRAINT user_conversations_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_conversations
    OWNER to "teaching-assistant";

COMMENT ON TABLE public.user_conversations
    IS 'Joining table for linking users to conversations';

COMMENT ON COLUMN public.user_conversations.user_id
    IS 'Student user that started the conversation';

COMMENT ON COLUMN public.user_conversations.title
    IS 'Title of the conversation';

-- Index: fki_user_conversations_archive_by_fkey

CREATE INDEX IF NOT EXISTS fki_user_conversations_archive_by_fkey
    ON public.user_conversations USING btree
    (archived_by ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: fki_user_conversations_course_id_fkey

CREATE INDEX IF NOT EXISTS fki_user_conversations_course_id_fkey
    ON public.user_conversations USING btree
    (course_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: fki_user_conversations_user_id_fkey

CREATE INDEX IF NOT EXISTS fki_user_conversations_user_id_fkey
    ON public.user_conversations USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: user_course_conversations

CREATE INDEX IF NOT EXISTS user_course_conversations
    ON public.user_conversations USING btree
    (user_id ASC NULLS LAST, course_id ASC NULLS LAST)
    TABLESPACE pg_default;