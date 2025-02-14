-- Database: chatbot
-- OWNER depends on the default local server. Update as necessary.

CREATE DATABASE chatbot
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = default
    LC_CTYPE = default
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;