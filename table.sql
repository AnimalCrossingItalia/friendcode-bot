-- Table: public.data

-- DROP TABLE public.data;

CREATE TABLE public.data
(
    "ID" bigint NOT NULL DEFAULT nextval('"data_ID_seq"'::regclass),
    "user" text COLLATE pg_catalog."default" NOT NULL,
    key text COLLATE pg_catalog."default" NOT NULL,
    code text COLLATE pg_catalog."default" NOT NULL,
    chat bigint NOT NULL,
    CONSTRAINT data_pkey PRIMARY KEY ("ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.data
    OWNER to zrenwfngnsyfll;