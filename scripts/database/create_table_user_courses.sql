-- Table: public.user_courses

CREATE TABLE IF NOT EXISTS public.user_courses
(
    user_id uuid NOT NULL,
    course_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT user_courses_pkey PRIMARY KEY (user_id, course_id),
    CONSTRAINT user_courses_course_id_fkey FOREIGN KEY (course_id)
        REFERENCES public.courses (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT,
    CONSTRAINT user_courses_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_courses
    OWNER to "teaching-assistant";

COMMENT ON TABLE public.user_courses
    IS 'Joining table for assigning users to courses';

-- Index: fki_user_courses_course_id_fkey

CREATE INDEX IF NOT EXISTS fki_user_courses_course_id_fkey
    ON public.user_courses USING btree
    (course_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: fki_user_courses_user_id_fkey

CREATE INDEX IF NOT EXISTS fki_user_courses_user_id_fkey
    ON public.user_courses USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;