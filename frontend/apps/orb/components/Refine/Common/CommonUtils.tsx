import { JsonInput, Select, Switch, TagsInput, Text, TextInput } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { DateField } from '@refinedev/mantine';
import ChipArray from 'mantine-components/components/Chip/ChipArray';
import { ReactNode, createContext } from 'react';
import { IModel } from '../models';

export type DataObject = { [key: string]: any; };

export enum FieldType {
    String = 'string',
    Json = 'json',
    Number = 'number',
    Boolean = 'boolean',
    Date = 'date',
    Array = 'array',
    DropDown = 'dropdown'
}

export interface DropDownField {
    value: string | number;
    label: string;
}

export interface ForeignField {
    resource: string;
    labelKey: string;
}

export interface ForeignData {
    [key: string]: DropDownField[];
}

export interface EntityField {
    label: string;
    objectKey: string;
    type: FieldType;
    isHide?: boolean;
    isReadOnly?: boolean;
    isSummary?: boolean;
    isCreatable?: boolean;
    foreign?: ForeignField;
    data?: DropDownField[];
    special?: SpecialField;
}

export enum SpecialField {
    Id = 'id',
    Title = 'title',
    Enabled = 'enabled',
    Time = 'time'
}

export interface EntityOptions {
    fields: EntityField[];
}

export interface ModelButtonProps {
    resource: string;
    hideText?: boolean;
    variant?: string;
    children?: React.ReactNode;
}

export interface ExistingDataModelButtonProps extends ModelButtonProps {
    id?: string | number;
    foreignData: ForeignData;
}

export function snakeToCamel(s: string): string {
    return s.replace(/(_\w)/g, (m) => m[1].toUpperCase());
}

export function camelToSnake(s: string): string {
    return s.replace(/[\w]([A-Z])/g, (m) => `${m[0]}_${m[1]}`).toLowerCase();
}

// ------------------------------------------------------------------------------------------------

export const EntityMetaContext = createContext<EntityOptions>({ fields: [] });

// ------------------------------------------------------------------------------------------------

export function get_field_view(value: any, fieldMeta: EntityField, foriegnData): ReactNode {
    let data;
    switch (fieldMeta.type) {
        case FieldType.Date:
            return <DateField format="lll" value={value} />;

        case FieldType.Array:
            return <ChipArray chipList={value} bgColor="teal" />;

        case FieldType.Boolean:
            return <Switch checked={value} disabled />;

        case FieldType.DropDown:
            data = fieldMeta.foreign
                ? foriegnData[fieldMeta.foreign.resource]
                : fieldMeta.data;
            return <Text>{data.find((d) => d.value === value)?.label}</Text>;

        case FieldType.Json:
            if (typeof value === 'object') {
                value = JSON.stringify(value, null, 2);
            }
            return (
                <JsonInput
                    validationError="Invalid JSON"
                    formatOnBlur
                    autosize
                    disabled
                    value={value}
                />
            );

        default:
            return <Text>{value.toString()}</Text>;
    }
}

export function get_field_editable(value: any, fieldMeta: EntityField, fieldProps, foriegnData): ReactNode {
    if (fieldMeta.isReadOnly) {
        return get_field_view(value, fieldMeta, foriegnData);
    }
    switch (fieldMeta.type) {
        case FieldType.Date:
            return <DateInput {...fieldProps} />;
        case FieldType.Boolean:
            fieldProps.checked = value;
            return <Switch {...fieldProps} disabled />;
        case FieldType.Array:
            return <TagsInput placeholder="Press Enter or Comma to add" {...fieldProps} />;
        case FieldType.DropDown:
            if (fieldMeta.foreign) {
                fieldProps.data = foriegnData[fieldMeta.foreign.resource];
            } else {
                fieldProps.data = fieldMeta.data;
            }
            return <Select placeholder={`Select ${fieldMeta.label}`} {...fieldProps} />;
        case FieldType.Json:
            if (typeof fieldProps.value === 'object') {
                fieldProps.value = JSON.stringify(fieldProps.value, null, 2);
            }
            return (
                <JsonInput
                    validationError="Invalid JSON"
                    formatOnBlur
                    autosize
                    {...fieldProps}
                />
            );
        default:
            fieldProps.placeholder = fieldMeta.label;
            return <TextInput {...fieldProps} />;
    }
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
            acc[objectKey] = '{}';
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
