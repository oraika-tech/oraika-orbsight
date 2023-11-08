--liquibase formatted sql

--changeset girish:insight_ddl_006

ALTER TABLE public.insight_processed_data ADD people VARCHAR[] DEFAULT NULL;

--rollback ALTER TABLE public.insight_processed_data DROP COLUMN people;
