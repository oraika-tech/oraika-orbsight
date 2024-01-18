import { Loader, Text } from '@mantine/core';
import { useEffect, useState } from 'react';
import Home from '.';
import DynamicDashboard from '../../components/DynamicDashboard';
import { getDashboards } from '../../lib/service/dashboard-service';

export default function HomeDashboard() {
    const [isHomeExists, setHomeExists] = useState(true);
    const [dashboards, setDashboards] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (isHomeExists) {
            getDashboards('home')
                .then(response => {
                    if (!response || !response.length) {
                        setHomeExists(false);
                    } else {
                        setDashboards(response);
                    }
                    setLoading(false);
                })
                .catch(() => {
                    setLoading(false);
                    // console.log('API call error: ', onrejected);
                });
        }
    }, []);

    if (!isHomeExists) {
        return <Home />;
    }

    const dashboard_id = dashboards && dashboards.length ? dashboards[0].identifier : undefined;

    if (loading) {
        return <Loader />;
    }

    if (!dashboard_id) {
        return <Text>No Data</Text>;
    }

    return <DynamicDashboard dashboard_id={dashboard_id} />;
}
