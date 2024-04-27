-- Table: vapaus.organisations

-- DROP TABLE IF EXISTS vapaus.organisations;

CREATE TABLE IF NOT EXISTS organisations
(
    id integer NOT NULL,
    name text COLLATE pg_catalog."default",
    business_id text COLLATE pg_catalog."default",
    CONSTRAINT organisation_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS organisations
    OWNER to postgres;