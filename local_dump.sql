--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: lora; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA lora;


ALTER SCHEMA lora OWNER TO postgres;

--
-- Name: prompt; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA prompt;


ALTER SCHEMA prompt OWNER TO postgres;

--
-- Name: structure_prompt; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA structure_prompt;


ALTER SCHEMA structure_prompt OWNER TO postgres;

--
-- Name: team; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA team;


ALTER SCHEMA team OWNER TO postgres;

--
-- Name: user; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "user";


ALTER SCHEMA "user" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: loras; Type: TABLE; Schema: lora; Owner: postgres
--

CREATE TABLE lora.loras (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    trigger_words character varying(255),
    clip_skip integer,
    base_strength double precision,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE lora.loras OWNER TO postgres;

--
-- Name: loras_id_seq; Type: SEQUENCE; Schema: lora; Owner: postgres
--

CREATE SEQUENCE lora.loras_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE lora.loras_id_seq OWNER TO postgres;

--
-- Name: loras_id_seq; Type: SEQUENCE OWNED BY; Schema: lora; Owner: postgres
--

ALTER SEQUENCE lora.loras_id_seq OWNED BY lora.loras.id;


--
-- Name: prompts; Type: TABLE; Schema: prompt; Owner: postgres
--

CREATE TABLE prompt.prompts (
    id integer NOT NULL,
    prompt_name character varying(255) NOT NULL,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE prompt.prompts OWNER TO postgres;

--
-- Name: prompts_id_seq; Type: SEQUENCE; Schema: prompt; Owner: postgres
--

CREATE SEQUENCE prompt.prompts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE prompt.prompts_id_seq OWNER TO postgres;

--
-- Name: prompts_id_seq; Type: SEQUENCE OWNED BY; Schema: prompt; Owner: postgres
--

ALTER SEQUENCE prompt.prompts_id_seq OWNED BY prompt.prompts.id;


--
-- Name: structure_prompts; Type: TABLE; Schema: structure_prompt; Owner: postgres
--

CREATE TABLE structure_prompt.structure_prompts (
    id integer NOT NULL,
    prompt_name character varying(255) NOT NULL,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE structure_prompt.structure_prompts OWNER TO postgres;

--
-- Name: structure_prompts_id_seq; Type: SEQUENCE; Schema: structure_prompt; Owner: postgres
--

CREATE SEQUENCE structure_prompt.structure_prompts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE structure_prompt.structure_prompts_id_seq OWNER TO postgres;

--
-- Name: structure_prompts_id_seq; Type: SEQUENCE OWNED BY; Schema: structure_prompt; Owner: postgres
--

ALTER SEQUENCE structure_prompt.structure_prompts_id_seq OWNED BY structure_prompt.structure_prompts.id;


--
-- Name: team; Type: TABLE; Schema: team; Owner: postgres
--

CREATE TABLE team.team (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE team.team OWNER TO postgres;

--
-- Name: team_id_seq; Type: SEQUENCE; Schema: team; Owner: postgres
--

CREATE SEQUENCE team.team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE team.team_id_seq OWNER TO postgres;

--
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: team; Owner: postgres
--

ALTER SEQUENCE team.team_id_seq OWNED BY team.team.id;


--
-- Name: team_members; Type: TABLE; Schema: team; Owner: postgres
--

CREATE TABLE team.team_members (
    id integer NOT NULL,
    team_id integer NOT NULL,
    user_id integer NOT NULL,
    role character varying(50) DEFAULT 'member'::character varying NOT NULL,
    joined_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE team.team_members OWNER TO postgres;

--
-- Name: team_members_id_seq; Type: SEQUENCE; Schema: team; Owner: postgres
--

CREATE SEQUENCE team.team_members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE team.team_members_id_seq OWNER TO postgres;

--
-- Name: team_members_id_seq; Type: SEQUENCE OWNED BY; Schema: team; Owner: postgres
--

ALTER SEQUENCE team.team_members_id_seq OWNED BY team.team_members.id;


--
-- Name: users; Type: TABLE; Schema: user; Owner: postgres
--

CREATE TABLE "user".users (
    id integer NOT NULL,
    user_id character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    full_name character varying(255),
    is_active boolean DEFAULT true,
    is_superuser boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone
);


ALTER TABLE "user".users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: user; Owner: postgres
--

CREATE SEQUENCE "user".users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "user".users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: user; Owner: postgres
--

ALTER SEQUENCE "user".users_id_seq OWNED BY "user".users.id;


--
-- Name: loras id; Type: DEFAULT; Schema: lora; Owner: postgres
--

ALTER TABLE ONLY lora.loras ALTER COLUMN id SET DEFAULT nextval('lora.loras_id_seq'::regclass);


--
-- Name: prompts id; Type: DEFAULT; Schema: prompt; Owner: postgres
--

ALTER TABLE ONLY prompt.prompts ALTER COLUMN id SET DEFAULT nextval('prompt.prompts_id_seq'::regclass);


--
-- Name: structure_prompts id; Type: DEFAULT; Schema: structure_prompt; Owner: postgres
--

ALTER TABLE ONLY structure_prompt.structure_prompts ALTER COLUMN id SET DEFAULT nextval('structure_prompt.structure_prompts_id_seq'::regclass);


--
-- Name: team id; Type: DEFAULT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team ALTER COLUMN id SET DEFAULT nextval('team.team_id_seq'::regclass);


--
-- Name: team_members id; Type: DEFAULT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team_members ALTER COLUMN id SET DEFAULT nextval('team.team_members_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user".users ALTER COLUMN id SET DEFAULT nextval('"user".users_id_seq'::regclass);


--
-- Data for Name: loras; Type: TABLE DATA; Schema: lora; Owner: postgres
--

COPY lora.loras (id, name, trigger_words, clip_skip, base_strength, description, created_at) FROM stdin;
\.


--
-- Data for Name: prompts; Type: TABLE DATA; Schema: prompt; Owner: postgres
--

COPY prompt.prompts (id, prompt_name, content, created_at) FROM stdin;
2	string	string	2025-04-10 18:01:45.800848
3	string	string	2025-04-11 13:10:43.037925
4	string	string	2025-04-11 13:56:04.546065
1	string	rrrrr	2025-04-10 17:58:57.440683
5	string	string	2025-04-21 12:00:39.330488
\.


--
-- Data for Name: structure_prompts; Type: TABLE DATA; Schema: structure_prompt; Owner: postgres
--

COPY structure_prompt.structure_prompts (id, prompt_name, content, created_at) FROM stdin;
\.


--
-- Data for Name: team; Type: TABLE DATA; Schema: team; Owner: postgres
--

COPY team.team (id, name, description, created_at) FROM stdin;
42	Victor's Test Team	Test team for victor	2025-04-14 14:44:22.171127+08
\.


--
-- Data for Name: team_members; Type: TABLE DATA; Schema: team; Owner: postgres
--

COPY team.team_members (id, team_id, user_id, role, joined_at) FROM stdin;
8	42	3	admin	2025-04-14 14:44:22.171127+08
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: user; Owner: postgres
--

COPY "user".users (id, user_id, email, username, hashed_password, full_name, is_active, is_superuser, created_at, updated_at) FROM stdin;
1	5a72d84d-739c-49f1-85b5-ed21718e3f1b	user@example.com	johndoe	$pbkdf2-sha256$29000$5XzPufd.T0lJiRHiPOc8Bw$6j1B87Er.5BtSYtrxcjCrg3GKGHcBCPVuGiKvIRxOVc	John Doe	t	f	2025-04-10 17:50:03.096738+08	\N
3	24744d6b-1485-45e2-b1aa-008a8f3873e1	victor@xfire.com	victor	$pbkdf2-sha256$29000$UwphLIXwnrP23jtHqFVKyQ$s4yWXtl793yBCpL8sxnGQG2t.m4CYGJnOfX4Gs4Ra8M	victor	t	t	2025-04-11 16:39:04.619084+08	\N
5	9a28786c-983a-46de-a0e2-657f1efb5851	user@example1.com	johndoe2	$pbkdf2-sha256$29000$8Z6TUuq9t7ZWijHmnBOCsA$iyeUAD3c4fBRddX7eGg8LHTbUKIPyfT6OqhK27x/j2U	John Doe2	t	f	2025-04-14 12:08:05.80024+08	\N
\.


--
-- Name: loras_id_seq; Type: SEQUENCE SET; Schema: lora; Owner: postgres
--

SELECT pg_catalog.setval('lora.loras_id_seq', 1, true);


--
-- Name: prompts_id_seq; Type: SEQUENCE SET; Schema: prompt; Owner: postgres
--

SELECT pg_catalog.setval('prompt.prompts_id_seq', 5, true);


--
-- Name: structure_prompts_id_seq; Type: SEQUENCE SET; Schema: structure_prompt; Owner: postgres
--

SELECT pg_catalog.setval('structure_prompt.structure_prompts_id_seq', 1, false);


--
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: team; Owner: postgres
--

SELECT pg_catalog.setval('team.team_id_seq', 42, true);


--
-- Name: team_members_id_seq; Type: SEQUENCE SET; Schema: team; Owner: postgres
--

SELECT pg_catalog.setval('team.team_members_id_seq', 8, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: user; Owner: postgres
--

SELECT pg_catalog.setval('"user".users_id_seq', 5, true);


--
-- Name: loras loras_name_key; Type: CONSTRAINT; Schema: lora; Owner: postgres
--

ALTER TABLE ONLY lora.loras
    ADD CONSTRAINT loras_name_key UNIQUE (name);


--
-- Name: loras loras_pkey; Type: CONSTRAINT; Schema: lora; Owner: postgres
--

ALTER TABLE ONLY lora.loras
    ADD CONSTRAINT loras_pkey PRIMARY KEY (id);


--
-- Name: prompts prompts_pkey; Type: CONSTRAINT; Schema: prompt; Owner: postgres
--

ALTER TABLE ONLY prompt.prompts
    ADD CONSTRAINT prompts_pkey PRIMARY KEY (id);


--
-- Name: structure_prompts structure_prompts_pkey; Type: CONSTRAINT; Schema: structure_prompt; Owner: postgres
--

ALTER TABLE ONLY structure_prompt.structure_prompts
    ADD CONSTRAINT structure_prompts_pkey PRIMARY KEY (id);


--
-- Name: team_members team_members_pkey; Type: CONSTRAINT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team_members
    ADD CONSTRAINT team_members_pkey PRIMARY KEY (id);


--
-- Name: team team_name_key; Type: CONSTRAINT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team
    ADD CONSTRAINT team_name_key UNIQUE (name);


--
-- Name: team team_pkey; Type: CONSTRAINT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- Name: team_members uq_team_member; Type: CONSTRAINT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team_members
    ADD CONSTRAINT uq_team_member UNIQUE (team_id, user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user".users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user".users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_user_id_key; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user".users
    ADD CONSTRAINT users_user_id_key UNIQUE (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user".users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: team_members team_members_team_id_fkey; Type: FK CONSTRAINT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team_members
    ADD CONSTRAINT team_members_team_id_fkey FOREIGN KEY (team_id) REFERENCES team.team(id) ON DELETE CASCADE;


--
-- Name: team_members team_members_user_id_fkey; Type: FK CONSTRAINT; Schema: team; Owner: postgres
--

ALTER TABLE ONLY team.team_members
    ADD CONSTRAINT team_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user".users(id);


--
-- PostgreSQL database dump complete
--

