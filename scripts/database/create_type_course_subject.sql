-- Type: course_subject

CREATE TYPE public.course_subject AS ENUM
    ('ANTH', 'ACS', 'ARET', 'AD', 'ASTR', 'BIOL', 'BUS', 'CHM', 'CDFS', 'CE', 'CLCS', 'CSD', 'COM', 'CS', 'CRIM', 'ECON', 'EDU', 'ECET', 'ECE', 'ENGR', 'ENGL', 'ETCS', 'FVS', 'HIST', 'HTM', 'HSRV', 'IET', 'IST', 'ITC', 'IDIS', 'LGBT', 'LING', 'MA', 'ME', 'MET', 'MUSC', 'NUTR', 'OLS', 'PACS', 'PHIL', 'PHYS', 'POL', 'PSY', 'REL', 'SOC', 'SPAN', 'STAT', 'THTR', 'WOST');

ALTER TYPE public.course_subject
    OWNER TO "teaching-assistant";
