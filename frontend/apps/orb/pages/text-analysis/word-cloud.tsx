import DefaultLayout from '../../business-logic/layout/DefaultLayout';
import DynamicDashboard from '../../components/DynamicDashboard';

export default function WordCloudPage() {
    const dashboard_id = '6689b4f9-31b1-4f78-a468-7c980db8b908';
    return (
        <DefaultLayout>
            <DynamicDashboard dashboard_id={dashboard_id} />
        </DefaultLayout>
    );
}
