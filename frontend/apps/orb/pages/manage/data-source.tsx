import DataSource from '../../business-logic/data-source';
import DefaultLayout from '../../business-logic/layout/DefaultLayout';

export default function DataSourcePage() {
    return (
        <DefaultLayout>
            <DataSource />
        </DefaultLayout>
    );
}
