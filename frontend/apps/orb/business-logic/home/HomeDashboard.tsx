import { Loader, Text } from '@mantine/core';
import { useEffect, useState } from 'react';
import DynamicDashboard from '../../components/DynamicDashboard';
import { getDashboards } from '../../lib/service/dashboard-service';

export default function HomeDashboard() {
    const [dashboards, setDashboards] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getDashboards('home')
            .then(response => {
                setDashboards(response);
                setLoading(false);
            })
            .catch(() => {
                setLoading(false);
                // console.log('API call error: ', onrejected);
            });
    }, []);

    const dashboard_id = dashboards && dashboards.length ? dashboards[0].identifier : undefined;

    if (loading) {
        return <Loader />;
    }

    if (!dashboard_id) {
        return <Text>No Data</Text>;
    }

    return <DynamicDashboard dashboard_id={dashboard_id} />;
}
