--liquibase formatted sql

--changeset girish:rbi_ddl_003
CREATE INDEX raw_data_event_time_idx ON raw_data USING brin( event_time );
CREATE INDEX raw_data_entity_name_idx ON raw_data USING hash( entity_name );
CREATE INDEX raw_data_observer_type_idx ON raw_data USING hash( observer_type );
CREATE INDEX raw_data_observer_id_idx ON raw_data ( observer_id );
CREATE unique INDEX raw_data_reference_id_idx ON raw_data ( reference_id );


-- processed_data
CREATE INDEX processed_data_event_time_idx ON processed_data USING brin( event_time );
CREATE INDEX processed_data_entity_name_idx ON processed_data USING hash( entity_name );
CREATE INDEX processed_data_observer_type_idx ON processed_data USING hash( observer_type );
CREATE INDEX processed_data_text_lang_idx ON processed_data USING hash( text_lang );
CREATE INDEX processed_data_emotion_idx ON processed_data ( emotion ) where emotion is not null;
create index processed_data_regulated_entity_type_idx on processed_data using gin( regulated_entity_type )
CREATE INDEX processed_data_raw_data_id_idx ON processed_data ( raw_data_id desc );

--rollback drop index raw_data_event_time_idx
--rollback drop index raw_data_entity_name_idx
--rollback drop index raw_data_observer_type_idx
--rollback drop index raw_data_observer_id_idx
--rollback drop index raw_data_reference_id_idx

--rollback drop index processed_data_event_time_idx
--rollback drop index processed_data_raw_data_id_idx
--rollback drop index processed_data_entity_name_idx
--rollback drop index processed_data_observer_type_idx
--rollback drop index processed_data_text_lang_idx
--rollback drop index processed_data_emotion_idx
--rollback drop index processed_data_regulated_entity_type_idx
--rollback drop index processed_data_raw_data_id_idx
