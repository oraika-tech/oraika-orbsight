import { EntityField, FieldType, SpecialField } from '../../components/Refine/Common/CommonModels';
import DataPage from '../../components/Refine/DataPage/DataPage';

export default function DataSourceRefine() {
    const fields: EntityField[] = [
        {
            label: 'ID',
            objectKey: 'identifier',
            type: FieldType.String,
            special: SpecialField.Id,
            isHide: true
        },
        {
            label: 'Name',
            objectKey: 'name',
            type: FieldType.String,
            isSummary: false,
            isCreatable: true,
            special: SpecialField.Title,
            linkData: {
                fieldKey: 'config_data',
                valueKey: 'url'
            },
        },
        {
            label: 'Entity',
            objectKey: 'entity_id',
            foreign: {
                resource: 'entities',
                labelKey: 'name'
            },
            type: FieldType.DropDown,
            isCreatable: true,
            isSummary: true
        },
        {
            label: 'Source Type',
            objectKey: 'type',
            data: [
                { value: 1, label: 'Twitter' },
                { value: 2, label: 'Android' },
                { value: 3, label: 'iOS' },
                { value: 4, label: 'GoogleMaps' },
                { value: 5, label: 'Facebook' },
                { value: 6, label: 'Reddit' },
                { value: 7, label: 'GoogleNews' },
                { value: 8, label: 'GoogleSearch' }
            ],
            linkData: {
                fieldKey: 'config_data'
            },
            type: FieldType.DropDown,
            special: SpecialField.SourceType,
            isCreatable: true,
            isSummary: true
        },
        {
            label: 'Data',
            objectKey: 'config_data',
            type: FieldType.Json,
            isHide: true,
            special: SpecialField.Link,
            linkData: {
                valueKey: 'url'
            }
        },
        {
            label: 'Enabled',
            objectKey: 'is_enabled',
            type: FieldType.Boolean,
            isSummary: false,
            special: SpecialField.Enabled
        },
        {
            label: 'Created At',
            objectKey: 'created_at',
            type: FieldType.Date,
            isReadOnly: true
        },
        {
            label: 'Updated At',
            objectKey: 'updated_at',
            type: FieldType.Date,
            isReadOnly: true,
            special: SpecialField.Time
        }
    ];
    return (
        <DataPage
            title="Observers"
            resource="observers"
            cardOptions={{ fields }}
        />
    );
}
