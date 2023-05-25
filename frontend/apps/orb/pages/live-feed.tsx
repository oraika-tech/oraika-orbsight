import DefaultLayout from '../business-logic/layout/DefaultLayout';
import LiveFeedDashboard from '../business-logic/live-feed';

export default function LiveFeedPage() {
    return (
        <DefaultLayout>
            <LiveFeedDashboard />
        </DefaultLayout>
    );
}
