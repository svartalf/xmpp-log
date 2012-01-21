--
-- Database scheme for https://github.com/svartalf/xmpp-log
--

CREATE SEQUENCE conference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE conferences (
    id integer DEFAULT nextval('conference_id_seq'::regclass) NOT NULL,
    name character varying(255) NOT NULL
);

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE logs (
    id integer DEFAULT nextval('log_id_seq'::regclass) NOT NULL,
    conference_id integer,
    "user" character varying(255),
    text text,
    type integer,
    date timestamp with time zone
);

ALTER TABLE ONLY logs ADD CONSTRAINT log_pk PRIMARY KEY (id);

ALTER TABLE ONLY conferences ADD CONSTRAINT pk PRIMARY KEY (id);