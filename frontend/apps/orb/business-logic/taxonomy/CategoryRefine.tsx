import { EntityField, FieldType, SpecialField } from '../../components/Refine/Common/CommonUtils';
import DataPage, { ViewMode } from '../../components/Refine/DataPage/DataPage';

export default function CategoryRefine() {
    const fields: EntityField[] = [
        {
            label: 'ID',
            objectKey: 'identifier',
            type: FieldType.String,
            special: SpecialField.Id,
            isReadOnly: true,
            isSummary: false
        },
        {
            label: 'Name',
            objectKey: 'name',
            type: FieldType.String,
            isCreatable: true,
            special: SpecialField.Title
        }
    ];
    return (
        <DataPage
            title="Categories"
            resource="categories"
            cardOptions={{ fields }}
            allowedViewModes={[ViewMode.TableMode]}
        />
    );
}
