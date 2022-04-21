/* Migration script to create columns for entity and observer to improve analytics */

ALTER TABLE raw_data
ADD COLUMN observer_name varchar,
ADD COLUMN observer_type varchar,
ADD COLUMN entity_id int,
ADD COLUMN entity_name varchar,
ADD COLUMN regulated_entity_type varchar[],
ADD COLUMN event_time timestamp with time zone;

ALTER TABLE processed_data RENAME COLUMN entity_type TO regulated_entity_type;

ALTER TABLE processed_data
ALTER COLUMN regulated_entity_type TYPE varchar[]
USING array[regulated_entity_type]::varchar[];

ALTER TABLE processed_data ADD COLUMN event_time timestamp with time zone;

ALTER TABLE processed_data ALTER COLUMN fraud DROP DEFAULT;
ALTER TABLE processed_data ALTER COLUMN complaint DROP DEFAULT;
ALTER TABLE processed_data ALTER COLUMN harassment DROP DEFAULT;
ALTER TABLE processed_data ALTER COLUMN "access" DROP DEFAULT;
ALTER TABLE processed_data ALTER COLUMN delay DROP DEFAULT;
ALTER TABLE processed_data ALTER COLUMN interface DROP DEFAULT;
ALTER TABLE processed_data ALTER COLUMN charges DROP DEFAULT;
