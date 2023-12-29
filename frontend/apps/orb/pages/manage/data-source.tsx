import DataSourceRefine from '../../business-logic/data-source/DataSourceRefine';
import DefaultLayout from '../../business-logic/layout/DefaultLayout';

export default function DataSourcePage() {
    return (
        <DefaultLayout>
            <DataSourceRefine />
        </DefaultLayout>
    );
}
