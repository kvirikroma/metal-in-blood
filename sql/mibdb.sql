--
-- PostgreSQL database dump
--

-- Dumped from database version 11.8 (Ubuntu 11.8-1.pgdg18.04+1)
-- Dumped by pg_dump version 11.8 (Ubuntu 11.8-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid(); Type: FUNCTION; Schema: public; Owner: api
--

CREATE FUNCTION public.uuid() RETURNS uuid
    LANGUAGE sql
    AS $$SELECT uuid_in(md5(random()::text)::cstring)$$;


ALTER FUNCTION public.uuid() OWNER TO api;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: albums; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.albums (
    id uuid NOT NULL,
    author text NOT NULL,
    album_name text NOT NULL,
    picture text NOT NULL
);


ALTER TABLE public.albums OWNER TO api;

--
-- Name: forum_messages; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.forum_messages (
    id uuid NOT NULL,
    author uuid NOT NULL,
    body text NOT NULL,
    date timestamp without time zone NOT NULL,
    related_to uuid NOT NULL
);


ALTER TABLE public.forum_messages OWNER TO api;

--
-- Name: forum_threads; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.forum_threads (
    id uuid NOT NULL,
    author uuid NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    date timestamp without time zone NOT NULL
);


ALTER TABLE public.forum_threads OWNER TO api;

--
-- Name: news; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.news (
    id uuid NOT NULL,
    author uuid NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    date timestamp without time zone NOT NULL,
    picture text
);


ALTER TABLE public.news OWNER TO api;

--
-- Name: tips; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.tips (
    id uuid NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    picture text
);


ALTER TABLE public.tips OWNER TO api;

--
-- Name: users; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.users (
    id uuid DEFAULT public.uuid() NOT NULL,
    login text NOT NULL,
    password_hash text NOT NULL
);


ALTER TABLE public.users OWNER TO api;

--
-- Name: yt_compilations; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.yt_compilations (
    id uuid NOT NULL,
    link text NOT NULL,
    channel text NOT NULL,
    video_name text NOT NULL
);


ALTER TABLE public.yt_compilations OWNER TO api;

--
-- Name: albums albums_author_album_name_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_author_album_name_key UNIQUE (author, album_name);


--
-- Name: albums albums_picture_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_picture_key UNIQUE (picture);


--
-- Name: albums albums_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_pkey PRIMARY KEY (id);


--
-- Name: forum_messages forum_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.forum_messages
    ADD CONSTRAINT forum_messages_pkey PRIMARY KEY (id);


--
-- Name: forum_threads forum_threads_author_title_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.forum_threads
    ADD CONSTRAINT forum_threads_author_title_key UNIQUE (author, title);


--
-- Name: forum_threads forum_threads_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.forum_threads
    ADD CONSTRAINT forum_threads_pkey PRIMARY KEY (id);


--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (id);


--
-- Name: tips tips_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.tips
    ADD CONSTRAINT tips_pkey PRIMARY KEY (id);


--
-- Name: tips tips_title_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.tips
    ADD CONSTRAINT tips_title_key UNIQUE (title);


--
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: yt_compilations yt_compilations_channel_video_name_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.yt_compilations
    ADD CONSTRAINT yt_compilations_channel_video_name_key UNIQUE (channel, video_name);


--
-- Name: yt_compilations yt_compilations_link_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.yt_compilations
    ADD CONSTRAINT yt_compilations_link_key UNIQUE (link);


--
-- Name: yt_compilations yt_compilations_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.yt_compilations
    ADD CONSTRAINT yt_compilations_pkey PRIMARY KEY (id);


--
-- Name: forum_messages_related_to_idx; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX forum_messages_related_to_idx ON public.forum_messages USING btree (related_to);


--
-- Name: forum_threads_title_body_idx; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX forum_threads_title_body_idx ON public.forum_threads USING btree (title, body);


--
-- Name: news_title_date_author_body_idx; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX news_title_date_author_body_idx ON public.news USING btree (title, date, author, body);


--
-- Name: tips_title_body_idx; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX tips_title_body_idx ON public.tips USING btree (title, body);


--
-- Name: forum_messages forum_messages_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.forum_messages
    ADD CONSTRAINT forum_messages_author_fkey FOREIGN KEY (author) REFERENCES public.users(id);


--
-- Name: forum_messages forum_messages_related_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.forum_messages
    ADD CONSTRAINT forum_messages_related_to_fkey FOREIGN KEY (related_to) REFERENCES public.forum_threads(id) ON DELETE CASCADE;


--
-- Name: forum_threads forum_threads_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.forum_threads
    ADD CONSTRAINT forum_threads_author_fkey FOREIGN KEY (author) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: news news_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_author_fkey FOREIGN KEY (author) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

