import DefaultLayout from '../../business-logic/layout/DefaultLayout';
import DynamicDashboard from '../../components/DynamicDashboard';

export default function KeyPhrasesPage() {
    const dashboard_id = 'a02b099c-784b-472c-a1aa-3f3ab2f21d8f';
    return (
        <DefaultLayout>
            <DynamicDashboard dashboard_id={dashboard_id} />
        </DefaultLayout>
    );
}
