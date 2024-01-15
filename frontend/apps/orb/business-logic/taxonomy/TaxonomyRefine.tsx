import { EntityField, FieldType, SpecialField } from '../../components/Refine/Common/CommonModels';
import DataPage, { ViewMode } from '../../components/Refine/DataPage/DataPage';

export default function TaxonomyRefine() {
    const fields: EntityField[] = [
        {
            label: 'ID',
            objectKey: 'identifier',
            type: FieldType.String,
            special: SpecialField.Id,
            isHide: true
        },
        {
            label: 'Keyword',
            objectKey: 'keyword',
            type: FieldType.String,
            isCreatable: true
        },
        {
            label: 'Term',
            objectKey: 'term',
            type: FieldType.String,
            isCreatable: true,
            special: SpecialField.Title
        },
        {
            label: 'Description',
            objectKey: 'description',
            type: FieldType.String,
            isCreatable: true
        },
        {
            label: 'Tags',
            objectKey: 'tags',
            type: FieldType.Array,
            isCreatable: true,
            isSummary: true
        }
    ];
    return (
        <DataPage
            title="Terms"
            resource="taxonomies"
            cardOptions={{ fields }}
            allowedViewModes={[ViewMode.TableMode]}
        />
    );
}
