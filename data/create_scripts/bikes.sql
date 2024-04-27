-- Table: vapaus.bikes

-- DROP TABLE IF EXISTS vapaus.bikes;

CREATE TABLE IF NOT EXISTS bikes
(
    id integer NOT NULL,
    organisation_id integer,
    brand text COLLATE pg_catalog."default",
    model text COLLATE pg_catalog."default",
    price double precision,
    serial_number text COLLATE pg_catalog."default",
    CONSTRAINT bikes_pkey PRIMARY KEY (id),
    CONSTRAINT bikes_organisation_id_fkey FOREIGN KEY (organisation_id)
        REFERENCES organisations (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bikes
    OWNER to postgres;
-- Index: covering_index

-- DROP INDEX IF EXISTS vapaus.covering_index;

CREATE INDEX IF NOT EXISTS covering_index
    ON bikes USING btree
    (organisation_id ASC NULLS LAST)
    TABLESPACE pg_default;