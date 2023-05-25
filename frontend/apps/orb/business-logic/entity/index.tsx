import { Grid } from '@mantine/core';

import { useEffect, useState } from 'react';
// import { getEntities, updateEntityEnabled } from 'service/entity-service';
import { getEntities, updateEntityEnabled } from '../../lib/service/entity-service';
import EntityTable, { EntityState } from './EntityTable';

interface ResponseEntity {
    identifier: string
    name: string
    tags: string[]
    is_enabled: boolean
}

export default function Entity() {
    const [entities, setEntities] = useState<EntityState[]>([]);
    const [showLoader, setShowLoader] = useState<boolean>(true);

    const convertData = (entity: ResponseEntity) => {
        const tags: string[] = (entity.tags && entity.tags.length > 0) ? entity.tags : [];
        return {
            id: entity.identifier,
            name: entity.name,
            entityType: tags,
            isEnabled: {
                id: entity.identifier,
                isEnabled: entity.is_enabled
            }
        };
    };

    useEffect(() => {
        setShowLoader(true);
        const syncEntities = () => getEntities()
            .then(response => {
                setEntities(response.map(convertData));
                setShowLoader(false);
            })
            .catch(error => {
                console.error('There has been a problem with your operation:', error);
                setShowLoader(false);
            });

        syncEntities();

        return () => setEntities([]);
    }, []);

    const handleEnableToggle = (id: string, isEnabled: boolean, handlerDone: (isSuccess: boolean) => void) => {
        updateEntityEnabled(id, isEnabled)
            .then(() => {
                handlerDone(true);
                setEntities((entityList) => entityList.map(entity => {
                    if (entity.id === id) {
                        // eslint-disable-next-line no-param-reassign
                        entity.isEnabled.isEnabled = isEnabled;
                    }
                    return entity;
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
                <EntityTable rows={entities} handleEnableToggle={handleEnableToggle} showLoader={showLoader} />
            </Grid.Col>
        </Grid>
    );
}
