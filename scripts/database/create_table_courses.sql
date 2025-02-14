-- Table: public.courses

CREATE TABLE IF NOT EXISTS public.courses
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    instructor_id uuid NOT NULL,
    display_name text COLLATE pg_catalog."default" NOT NULL,
    subject course_subject NOT NULL,
    course_number numeric(5,0) NOT NULL,
    section_number numeric(2,0) NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    model text COLLATE pg_catalog."default" NOT NULL,
    prompt text COLLATE pg_catalog."default",
    documents_path text COLLATE pg_catalog."default" NOT NULL,
    image_path text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    archived boolean NOT NULL DEFAULT false,
    archived_by uuid,
    archived_at timestamp with time zone,
    CONSTRAINT courses_pkey PRIMARY KEY (id),
    CONSTRAINT courses_instructor_id_fkey FOREIGN KEY (instructor_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT,
    CONSTRAINT courses_archived_by_fkey FOREIGN KEY (archived_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.courses
    OWNER to "teaching-assistant";

COMMENT ON TABLE public.courses
    IS 'List of courses';

COMMENT ON COLUMN public.courses.display_name
    IS 'Displays [subject][course_number]-[section_number]:[title]';

COMMENT ON COLUMN public.courses.subject
    IS 'Course subject as defined by the institution';

COMMENT ON COLUMN public.courses.course_number
    IS 'Five digit identifier';

COMMENT ON COLUMN public.courses.section_number
    IS 'Two digit identifier';

COMMENT ON COLUMN public.courses.title
    IS 'Title of the course';

COMMENT ON COLUMN public.courses.model
    IS 'Most expensive model available (less expensive models will be available)';

COMMENT ON COLUMN public.courses.prompt
    IS 'Instructor-defined prompt for the course';

COMMENT ON COLUMN public.courses.documents_path
    IS 'Path to Chroma collection storing course documents';

COMMENT ON COLUMN public.courses.image_path
    IS 'Path to course display image';

-- Index: course_codes

CREATE UNIQUE INDEX IF NOT EXISTS course_codes
    ON public.courses USING btree
    (subject ASC NULLS LAST, course_number ASC NULLS LAST, section_number ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: fki_courses_archived_by_fkey

CREATE INDEX IF NOT EXISTS fki_courses_archived_by_fkey
    ON public.courses USING btree
    (archived_by ASC NULLS LAST)
    TABLESPACE pg_default;