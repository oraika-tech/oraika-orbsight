--liquibase formatted sql

--changeset girish:insight_ddl_101 runOnChange:true

CREATE SCHEMA IF NOT EXISTS data_view;

DROP VIEW IF EXISTS data_view.processed_data_view_v1;
CREATE OR REPLACE VIEW data_view.processed_data_view_v1 AS
SELECT
	event_time,
	-- ids ---------
	rd.identifier as raw_data_id,
    pd.identifier as processed_data_id,
    reference_id,
    unstructured_data ->>'conversation_id' as conversation_id,
    -- observer and entity info -------
    obs.name as observer_name,
    (CASE
        WHEN obs.type = 1 THEN 'Twitter'
        WHEN obs.type = 2 THEN 'Android'
        WHEN obs.type = 3 THEN 'iOS'
        WHEN obs.type = 4 THEN 'GoogleMaps'
        WHEN obs.type = 5 THEN 'Facebook'
        WHEN obs.type = 6 THEN 'Reddit'
        WHEN obs.type = 7 THEN 'GoogleNews'
        WHEN obs.type = 8 THEN 'GoogleSearch'
    END) as observer_type,
    entity.name as entity_name,
    -- message info ------
    (CASE
        WHEN obs.type = 1 THEN (unstructured_data ->>'author_info')::json->>'username'
        WHEN obs.type = 2 THEN unstructured_data ->>'userName'
        WHEN obs.type = 3 THEN unstructured_data ->>'author_name'
        WHEN obs.type = 4 THEN unstructured_data ->>'author_title'
        WHEN obs.type = 7 THEN unstructured_data ->>'publisher_title'
    END) as author_name,
    (CASE
        WHEN obs.type = 2 THEN unstructured_data ->>'score'
        WHEN obs.type = 3 THEN unstructured_data ->>'rating'
        WHEN obs.type = 4 THEN unstructured_data ->>'review_rating'
    END) as rating,
    emotion,
    raw_text,
    -- Text meta
    md5(raw_text) as text_hash,
    text_lang,
    text_length,
    (CASE
        WHEN obs.type = 1 THEN unstructured_data ->>'tweet_url'
        WHEN obs.type = 2 THEN config_data ->>'url'
        WHEN obs.type = 3 THEN config_data ->>'url'
        WHEN obs.type = 4 THEN unstructured_data ->>'review_link'
        WHEN obs.type = 7 THEN unstructured_data ->>'link'
        WHEN obs.type = 8 THEN unstructured_data ->>'link'
    END) as url,
    -- analysis data --------
    taxonomy_tags,
    taxonomy_terms,
    categories,
    COALESCE(people, ARRAY[]::varchar[]) as people
FROM insight_raw_data rd
LEFT JOIN insight_processed_data pd ON rd.identifier = pd.raw_data_id
INNER JOIN config_observer obs ON obs.identifier = rd.observer_id
INNER JOIN config_entity entity ON entity.identifier = obs.entity_id
WHERE rd.is_deleted = FALSE AND pd.emotion IS NOT NULL
ORDER BY event_time DESC
;

GRANT USAGE ON SCHEMA data_view TO ${ORBSIGHT_TENANT_USER};
GRANT SELECT ON data_view.processed_data_view_v1 TO ${ORBSIGHT_TENANT_USER};

--rollback DROP SCHEMA IF EXISTS data_view;

