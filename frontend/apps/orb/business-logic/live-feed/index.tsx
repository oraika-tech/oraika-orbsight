import { Card, Loader, Text } from '@mantine/core';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import { useEffect, useState } from 'react';
import DynamicDashboard from '../../components/DynamicDashboard';
import { getDashboards } from '../../lib/service/dashboard-service';

export default function LiveFeedDashboard() {
    const [dashboards, setDashboards] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getDashboards('live-feed')
            .then(response => {
                setDashboards(response);
                setLoading(false);
            })
            .catch(onrejected => {
                setLoading(false);
                // eslint-disable-next-line no-console
                console.log('API call error: ', onrejected);
            });
    }, []);

    const dashboard_id = dashboards && dashboards.length ? dashboards[0].identifier : undefined;

    return (
        loading
            ? <Loader />
            : dashboard_id
                ? (
                    <div>
                        <DynamicDashboard dashboard_id={dashboard_id} />
                        <Card style={{ marginTop: '0.5rem', padding: '0.6rem' }}>
                            <Text>Note: Upto top 100 results only.</Text>
                        </Card>
                    </div>
                )
                : <EmptyData />
    );
}
