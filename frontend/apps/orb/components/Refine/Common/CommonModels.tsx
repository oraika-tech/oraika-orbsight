import { IModel } from '../models';

export type DataObject = { [key: string]: any; };

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

export interface LinkData {
    fieldKey?: string;
    valueKey?: string;
}

export enum FieldType {
    String = 'string',
    Json = 'json',
    Number = 'number',
    Boolean = 'boolean',
    Date = 'date',
    Array = 'array',
    DropDown = 'dropdown'
}

export interface EntityField {
    // Field Meta
    label: string;
    objectKey: string;
    type: FieldType;
    // Flags
    isHide?: boolean;
    isReadOnly?: boolean;
    isSummary?: boolean;
    isCreatable?: boolean;
    // Data
    foreign?: ForeignField;
    data?: DropDownField[];
    // Special Behaviour
    special?: SpecialField;
    linkData?: LinkData;
}

export enum SpecialField {
    Id = 'id',
    Title = 'title',
    Enabled = 'enabled',
    Time = 'time',
    Link = 'link',
    SourceType = 'sourceType'
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

export interface FieldData {
    rowData: IModel;
    fieldMeta: EntityField;
    foreignData: ForeignData;
}
