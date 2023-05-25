import Home from '../business-logic/home';
import DefaultLayout from '../business-logic/layout/DefaultLayout';
import WithRoute from '../components/next/WithRoute/WithRoute';

export default function HomePage() {
    return (
        <WithRoute>
            <DefaultLayout>
                <Home />
            </DefaultLayout>
        </WithRoute>
    );
}
