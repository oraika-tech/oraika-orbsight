import { EntityField, FieldType, SpecialField } from '../../components/Refine/Common/CommonUtils';
import DataPage from '../../components/Refine/DataPage/DataPage';

export default function DataSourceRefine() {
    const fields: EntityField[] = [
        {
            label: 'ID',
            objectKey: 'identifier',
            type: FieldType.String,
            special: SpecialField.Id,
            isReadOnly: true
        },
        {
            label: 'Name',
            objectKey: 'name',
            type: FieldType.String,
            isSummary: false,
            isCreatable: true,
            special: SpecialField.Title
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
                { value: '1', label: 'Twitter' },
                { value: '2', label: 'Android' },
                { value: '3', label: 'iOS' },
                { value: '4', label: 'GoogleMaps' },
                { value: '5', label: 'Facebook' },
                { value: '6', label: 'Reddit' },
                { value: '7', label: 'GoogleNews' }
            ],
            type: FieldType.DropDown,
            isCreatable: true,
            isSummary: true
        },
        {
            label: 'Data',
            objectKey: 'config_data',
            type: FieldType.Json,
            isCreatable: true
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
