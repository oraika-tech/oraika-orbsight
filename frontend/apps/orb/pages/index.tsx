import HomeDashboard from '../business-logic/home/HomeDashboard';
import DefaultLayout from '../business-logic/layout/DefaultLayout';
import WithRoute from '../components/next/WithRoute/WithRoute';

export default function HomePage() {
    return (
        <WithRoute>
            <DefaultLayout>
                <HomeDashboard />
            </DefaultLayout>
        </WithRoute>
    );
}
