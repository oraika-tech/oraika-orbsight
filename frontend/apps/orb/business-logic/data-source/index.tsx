import { Grid } from '@mantine/core';

import { useEffect, useState } from 'react';
import { getDataSources, updateDataSourceEnabled } from '../../lib/service/data-source-service';
import DataSourceTable from './DataSourceTable';

interface ConfigData {
    official_handle?: string;
    queries?: string;
    url?: string;
}

interface ResponseDataSource {
    identifier: string
    name: string
    type: string
    entity_name: string
    config_data: ConfigData
    is_enabled: boolean
}

interface DataSourceState {
    id: string
    nameLink: {
        name: string
        link: string
    }
    dataSourceType: string
    entityName: string
    isEnabled: {
        id: string
        isEnabled: boolean
    }
}

export default function DataSource() {
    const [dataSources, setDataSources] = useState<DataSourceState[]>([]);
    const [showLoading, setShowLoading] = useState<boolean>(true);

    const convertData = (dataSource: ResponseDataSource) => {
        let link: string;
        if (dataSource.type === 'Twitter') {
            link = `https://twitter.com/${dataSource.config_data.official_handle}`;
        } else if (dataSource.type === 'GoogleNews') {
            link = `https://news.google.com/search?q=${dataSource.config_data.queries}`;
        } else {
            link = dataSource.config_data.url;
        }
        return {
            id: dataSource.identifier,
            nameLink: {
                name: dataSource.name,
                link
            },
            dataSourceType: dataSource.type,
            entityName: dataSource.entity_name,
            isEnabled: {
                id: dataSource.identifier,
                isEnabled: dataSource.is_enabled
            }
        };
    };

    useEffect(() => {
        setShowLoading(true);

        const syncDataSources = () => getDataSources()
            .then(response => setDataSources(response.map(convertData)))
            .finally(() => setShowLoading(false));

        syncDataSources();
        return () => setDataSources([]);
    }, []);

    const handleEnableToggle = (id: string, isEnabled: boolean, handlerDone: (isSuccess: boolean) => void) => {
        updateDataSourceEnabled(id, isEnabled)
            .then(() => {
                handlerDone(true);
                setDataSources(dataSources.map(dataSource => {
                    if (dataSource.id === id) {
                        // eslint-disable-next-line no-param-reassign
                        dataSource.isEnabled.isEnabled = isEnabled;
                    }
                    return dataSource;
                }));
            })
            .catch(error => {
                console.error('There has been a problem with your operation:', error);
                handlerDone(false);
            });
    };

    return (
        <Grid gutter={2}>
            <Grid.Col xs={12}>
                <DataSourceTable
                    rows={dataSources}
                    handleEnableToggle={handleEnableToggle}
                    showLoading={showLoading}
                />
            </Grid.Col>
        </Grid>
    );
}
