import EntityRefine from '../../business-logic/entity/EntityRefine';
import DefaultLayout from '../../business-logic/layout/DefaultLayout';

export default function EntityPage() {
    return (
        <DefaultLayout>
            <EntityRefine />
        </DefaultLayout>
    );
}
