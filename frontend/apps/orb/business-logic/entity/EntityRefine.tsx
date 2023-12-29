import { EntityField, FieldType, SpecialField } from '../../components/Refine/Common/CommonUtils';
import DataPage from '../../components/Refine/DataPage/DataPage';

export default function EntityRefine() {
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
            label: 'Tags',
            objectKey: 'tags',
            type: FieldType.Array,
            isCreatable: true,
            isSummary: true
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
            title="Entities"
            resource="entities"
            cardOptions={{ fields }}
        />
    );
}
