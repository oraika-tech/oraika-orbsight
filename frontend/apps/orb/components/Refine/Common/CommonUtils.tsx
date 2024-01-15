import { IModel } from '../models';
import { DataObject, EntityField, FieldType, SpecialField } from './CommonModels';

export function snakeToCamel(s: string): string {
    return s.replace(/(_\w)/g, (m) => m[1].toUpperCase());
}

export function camelToSnake(s: string): string {
    return s.replace(/[\w]([A-Z])/g, (m) => `${m[0]}_${m[1]}`).toLowerCase();
}

export function convertObjectKeys(obj: DataObject): DataObject {
    if (!obj) {
        return {};
    }
    return Object.fromEntries(Object.entries(obj).map(([key, value]) => {
        // Detect Date field
        if (typeof value === 'string' && key.endsWith('_at') && !Number.isNaN(Date.parse(value))) {
            return [key, new Date(value)];
        } else {
            return [key, value];
        }
    }));
}

export function get_special_field(special: SpecialField, fields: EntityField[]): EntityField {
    const specialFields = fields.filter((f) => f.special === special);
    if (specialFields.length === 0) {
        return null;
    }
    return specialFields[0];
}

export function get_special_field_value(special: SpecialField, fields: EntityField[], data: IModel): any {
    if (!data) {
        return null;
    }
    const specialField = get_special_field(special, fields);
    if (!specialField || !specialField.objectKey) {
        return null;
    }
    return data[specialField.objectKey];
}

export function getDefaultValue(entityFields: EntityField[], fieldData?) {
    if (!fieldData) {
        fieldData = {};
    }
    return entityFields.reduce((acc, obj) => {
        const { objectKey } = obj;
        if (objectKey in fieldData) {
            acc[objectKey] = fieldData[objectKey];
        } else if (obj.type === FieldType.Array) {
            acc[objectKey] = [];
        } else if (obj.type === FieldType.Json) {
            acc[objectKey] = {};
        } else if (obj.type === FieldType.String) {
            acc[objectKey] = '';
        } else {
            acc[objectKey] = null;
        }
        return acc;
    }, {});
}

export function transformValues(values, initialValues, fields) {
    return (Object.fromEntries(Object.entries(values).filter(
        ([key, value]) => (value !== initialValues[key])
    ).map(([key, value]) => {
        const fieldMeta = fields.find((f) => f.objectKey === key);
        if (typeof value === 'string' && fieldMeta.type === FieldType.Json) {
            return [key, JSON.parse(value)];
        } else {
            return [key, value];
        }
    })
    ));
}
