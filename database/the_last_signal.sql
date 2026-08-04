--
-- PostgreSQL database dump
--

\restrict 3tHZykRDpmz8i9guPOPkgtnz2XqvRRKjuoRIcA0icFvclVd6shuSBzwEihexlgD

-- Dumped from database version 17.10 (Debian 17.10-1.pgdg13+1)
-- Dumped by pg_dump version 17.10 (Debian 17.10-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _sqlx_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public._sqlx_migrations (
    version bigint NOT NULL,
    description text NOT NULL,
    installed_on timestamp with time zone DEFAULT now() NOT NULL,
    success boolean NOT NULL,
    checksum bytea NOT NULL,
    execution_time bigint NOT NULL
);


ALTER TABLE public._sqlx_migrations OWNER TO postgres;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    account_id bigint NOT NULL,
    user_id uuid NOT NULL,
    account_name text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_account_id_seq OWNER TO postgres;

--
-- Name: accounts_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_id_seq OWNED BY public.accounts.account_id;


--
-- Name: bansferme; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bansferme (
    user_id uuid NOT NULL,
    auteur text,
    raison text,
    date_ban timestamp without time zone DEFAULT now() NOT NULL,
    date_deban timestamp without time zone NOT NULL
);


ALTER TABLE public.bansferme OWNER TO postgres;

--
-- Name: bansperm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bansperm (
    user_id uuid NOT NULL,
    auteur text NOT NULL,
    raison text NOT NULL,
    date_ban timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.bansperm OWNER TO postgres;

--
-- Name: banssursis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.banssursis (
    user_id uuid NOT NULL,
    auteur text,
    raison text,
    date_ban timestamp without time zone DEFAULT now() NOT NULL,
    sursis timestamp without time zone NOT NULL
);


ALTER TABLE public.banssursis OWNER TO postgres;

--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    client_id bigint NOT NULL,
    user_id uuid NOT NULL,
    platform text,
    game_version text,
    os text,
    cpu text,
    gpu text,
    first_seen timestamp without time zone DEFAULT now() NOT NULL,
    last_seen timestamp without time zone
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_client_id_seq OWNER TO postgres;

--
-- Name: clients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;


--
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    log_id bigint NOT NULL,
    session_id uuid NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    level character varying(16) NOT NULL,
    module text NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- Name: logs_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_log_id_seq OWNER TO postgres;

--
-- Name: logs_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_log_id_seq OWNED BY public.logs.log_id;


--
-- Name: perms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.perms (
    id integer NOT NULL,
    name text NOT NULL,
    perm text NOT NULL
);


ALTER TABLE public.perms OWNER TO postgres;

--
-- Name: perms_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.perms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.perms_id_seq OWNER TO postgres;

--
-- Name: perms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.perms_id_seq OWNED BY public.perms.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    session_id uuid NOT NULL,
    account_id bigint,
    started_at timestamp without time zone DEFAULT now() NOT NULL,
    ended_at timestamp without time zone,
    disconnect_reason text
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id uuid NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    last_login timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: accounts account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN account_id SET DEFAULT nextval('public.accounts_account_id_seq'::regclass);


--
-- Name: clients client_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);


--
-- Name: logs log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs ALTER COLUMN log_id SET DEFAULT nextval('public.logs_log_id_seq'::regclass);


--
-- Name: perms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perms ALTER COLUMN id SET DEFAULT nextval('public.perms_id_seq'::regclass);


--
-- Data for Name: _sqlx_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public._sqlx_migrations (version, description, installed_on, success, checksum, execution_time) FROM stdin;
1	create users	2026-08-04 06:55:21.309074+00	t	\\x2c7ab8d5924ec60b7cb247a01b374f45699c9fb8db026b45d94cce7eff5577f766ea4ae5659dc6f520e04b885e2ce101	2577350
2	create accounts	2026-08-04 06:55:21.312275+00	t	\\x84731522b8eaf5a9e4ccea6c0142340057f9fa4198dc7b2f32df27670b991c124dc00dad279a64363566a36b2ee061ac	3007965
3	create sessions	2026-08-04 06:55:21.315655+00	t	\\x804d661db30dfad76831084f778ddb004c0416b29392e600fbf9d4d8112fa7c9696c425680f2c8be5e0368edd6f54ce7	1877615
4	create logs	2026-08-04 06:55:21.317891+00	t	\\x06fcc11355d3758399a8f8e705b1c60f74efc99177d7b4400c37726fb25df01762eb4a561328ca42d446cd4d642178be	2218881
5	create clients	2026-08-04 06:55:21.320491+00	t	\\x17b5337a6a1864092ad58992a19977b82e5171b44fb244189c77980f8310d4e6c074f252cb55e5435d027bd273612c7e	2183936
6	create bans perm	2026-08-04 06:55:21.323042+00	t	\\x24564135ab44c0e141d9ff33890d7aaa66c9ffe49301b39eb107f3caaf3e2cc6de74691f1d3dc31bba5777f51ce81beb	1855243
7	create ban ferme	2026-08-04 06:55:21.325241+00	t	\\xf62a4c961dc9e3d7ddd53432e757f8fefeba491dbc105ee03f131dc185bdac0084e6013c62edf1c970deafcc9b51f050	2016855
8	create ban sursis	2026-08-04 06:55:21.327616+00	t	\\x37b78821ce7dfb4dbb231b41c8ef7dcc8bc0e9892577cdc8697f14b49959a0d81304e3b93c832d117aa8fd8ecd02dbca	1895167
9	create perms	2026-08-04 06:55:21.329904+00	t	\\x1ed7840eea70d58da460e0b5677fa8439dec9f712f0bf2f39c527c07393f999aa90266576675b90fc486fb27412d0ea6	2197261
\.


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (account_id, user_id, account_name, created_at) FROM stdin;
\.


--
-- Data for Name: bansferme; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bansferme (user_id, auteur, raison, date_ban, date_deban) FROM stdin;
\.


--
-- Data for Name: bansperm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bansperm (user_id, auteur, raison, date_ban) FROM stdin;
\.


--
-- Data for Name: banssursis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.banssursis (user_id, auteur, raison, date_ban, sursis) FROM stdin;
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients (client_id, user_id, platform, game_version, os, cpu, gpu, first_seen, last_seen) FROM stdin;
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs (log_id, session_id, "timestamp", level, module, message) FROM stdin;
\.


--
-- Data for Name: perms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perms (id, name, perm) FROM stdin;
1	Cyril	admin
2	Morgan	Super admin
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (session_id, account_id, started_at, ended_at, disconnect_reason) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, email, password_hash, created_at, last_login) FROM stdin;
\.


--
-- Name: accounts_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_id_seq', 1, false);


--
-- Name: clients_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_client_id_seq', 1, false);


--
-- Name: logs_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_log_id_seq', 1, false);


--
-- Name: perms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.perms_id_seq', 2, true);


--
-- Name: _sqlx_migrations _sqlx_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public._sqlx_migrations
    ADD CONSTRAINT _sqlx_migrations_pkey PRIMARY KEY (version);


--
-- Name: accounts accounts_account_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_account_name_key UNIQUE (account_name);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (account_id);


--
-- Name: bansferme bansferme_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bansferme
    ADD CONSTRAINT bansferme_pkey PRIMARY KEY (user_id);


--
-- Name: bansperm bansperm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bansperm
    ADD CONSTRAINT bansperm_pkey PRIMARY KEY (user_id);


--
-- Name: banssursis banssursis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banssursis
    ADD CONSTRAINT banssursis_pkey PRIMARY KEY (user_id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (user_id);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (log_id);


--
-- Name: perms perms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perms
    ADD CONSTRAINT perms_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (session_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: accounts accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: bansferme bansferme_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bansferme
    ADD CONSTRAINT bansferme_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: bansperm bansperm_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bansperm
    ADD CONSTRAINT bansperm_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: banssursis banssursis_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banssursis
    ADD CONSTRAINT banssursis_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: clients clients_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: logs logs_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(session_id) ON DELETE CASCADE;


--
-- Name: sessions sessions_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(account_id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict 3tHZykRDpmz8i9guPOPkgtnz2XqvRRKjuoRIcA0icFvclVd6shuSBzwEihexlgD

