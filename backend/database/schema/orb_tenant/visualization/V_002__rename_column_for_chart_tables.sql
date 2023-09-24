--liquibase formatted sql

--changeset girish:viz_ddl_002

ALTER TABLE public.viz_chart RENAME COLUMN data_field_mapping TO data_transformer_meta;
ALTER TABLE public.viz_chart ALTER COLUMN data_transformer_meta DROP NOT NULL;

--rollback ALTER TABLE public.viz_chart ALTER COLUMN data_transformer_meta SET NOT NULL;
--rollback ALTER TABLE public.viz_chart RENAME COLUMN data_transformer_meta TO data_field_mapping ;
