DO $$

DECLARE studentOne uuid := gen_random_uuid();
DECLARE	studentTwo uuid := gen_random_uuid();
DECLARE	studentThree uuid := gen_random_uuid();
DECLARE	instructorOne uuid := gen_random_uuid();
DECLARE	instructorTwo uuid := gen_random_uuid();

DECLARE	courseOne uuid := gen_random_uuid();
DECLARE	courseTwo uuid := gen_random_uuid();

DECLARE conversationOne uuid := gen_random_uuid();
DECLARE conversationTwo uuid := gen_random_uuid();
DECLARE conversationThree uuid := gen_random_uuid();

BEGIN
	RAISE NOTICE 'studentOne: %', studentOne;
	RAISE NOTICE 'studentTwo: %', studentTwo;
	RAISE NOTICE 'studentThree: %', studentThree;
	RAISE NOTICE 'instructorOne: %', instructorOne;
	RAISE NOTICE 'instructorTwo: %', instructorTwo;
	RAISE NOTICE 'courseOne: %', courseOne;
	RAISE NOTICE 'courseTwo: %', courseTwo;
	RAISE NOTICE 'conversationOne: %', conversationOne;
	RAISE NOTICE 'conversationTwo: %', conversationTwo;
	RAISE NOTICE 'conversationThree: %', conversationThree;

	--
	
	TRUNCATE TABLE public.users CASCADE;
	TRUNCATE TABLE public.courses CASCADE;
	TRUNCATE TABLE public.user_courses CASCADE;
	TRUNCATE TABLE public.user_conversations CASCADE;
	TRUNCATE TABLE public.messages CASCADE;

	--
	
	INSERT INTO public.users (id, display_name, email, "role") VALUES (studentOne, 'Aaron Van Curen', 'vancac03@pfw.edu', 'student');
	INSERT INTO public.users (id, display_name, email, "role") VALUES (studentTwo, 'Neal Birchfield', 'bircng01@pfw.edu', 'student');
	INSERT INTO public.users (id, display_name, email, "role") VALUES (studentThree, 'Wright Ceresa', 'cerews01@pfw.edu', 'student');
	INSERT INTO public.users (id, display_name, email, "role") VALUES (instructorOne, 'Carter Besson', 'bessca01@pfw.edu', 'instructor');
	INSERT INTO public.users (id, display_name, email, "role") VALUES (instructorTwo, 'Zesheng Chen', 'chenz@pfw.edu', 'instructor');
	
	INSERT INTO public.courses (id, instructor_id, display_name, subject, course_number, section_number, title, model, prompt, documents_path, image_path)
		VALUES (courseOne, instructorOne, 'CS23200-01 Intro to C and Unix', 'CS', 23200, 01, 'Intro to C and Unix', 'gpt-4o', '', '', '');
	INSERT INTO public.courses (id, instructor_id, display_name, subject, course_number, section_number, title, model, prompt, documents_path, image_path)
		VALUES (courseTwo, instructorTwo, 'CS45500-01 Computer Security', 'CS', 44500, 01, 'Computer Security', 'gpt-4o', '', '', '');

	INSERT INTO public.user_courses (user_id, course_id) VALUES (studentOne, courseOne);
	INSERT INTO public.user_courses (user_id, course_id) VALUES (studentTwo, courseOne);
	INSERT INTO public.user_courses (user_id, course_id) VALUES (studentThree, courseOne);
	INSERT INTO public.user_courses (user_id, course_id) VALUES (studentOne, courseTwo);
	INSERT INTO public.user_courses (user_id, course_id) VALUES (studentTwo, courseTwo);
	INSERT INTO public.user_courses (user_id, course_id) VALUES (studentThree, courseTwo);
	
	INSERT INTO public.user_conversations (conversation_id, user_id, course_id, title, model) VALUES (conversationOne, studentOne, courseOne, 'Test Conversation', 'gpt-4o');
	INSERT INTO public.user_conversations (conversation_id, user_id, course_id, title, model) VALUES (conversationTwo, studentTwo, courseOne, 'Test Conversation', 'gpt-4o');
	INSERT INTO public.user_conversations (conversation_id, user_id, course_id, title, model) VALUES (conversationThree, studentThree, courseOne, 'Test Conversation', 'gpt-4o');
	
	INSERT INTO public.messages (conversation_id, model, prompt, response) VALUES (conversationOne, 'gpt-4o', 'Echo Hello World', 'Hello World');
	INSERT INTO public.messages (conversation_id, model, prompt, response) VALUES (conversationTwo, 'gpt-4o', 'Echo Hello World', 'Hello World');
	INSERT INTO public.messages (conversation_id, model, prompt, response) VALUES (conversationThree, 'gpt-4o', 'Echo Hello World', 'Hello World');

END $$

-- SELECT * FROM public.users;
-- SELECT * FROM public.courses;
-- SELECT * FROM public.user_courses;
-- SELECT * FROM public.user_conversations;
-- SELECT * FROM public.messages;