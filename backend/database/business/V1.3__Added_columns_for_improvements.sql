/* Changes to add regulated type field in entity and observer */

ALTER TABLE entity RENAME COLUMN type TO regulated_type;

ALTER TABLE entity
ALTER COLUMN regulated_type TYPE varchar[]
USING array[regulated_type]::varchar[];

ALTER TABLE entity ADD COLUMN is_deleted boolean DEFAULT FALSE;

ALTER TABLE observer
ADD COLUMN regulated_entity_type varchar[],
ADD COLUMN is_deleted boolean DEFAULT FALSE;
