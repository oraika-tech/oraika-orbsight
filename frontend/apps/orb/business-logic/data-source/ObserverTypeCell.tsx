import { Grid, Tooltip } from '@mantine/core';
import { getLogoFromObserverType } from 'common-utils/utils/common';
import Image from 'next/image';

export default function ObserverTypeCell({ observerType }) {
    const logo = getLogoFromObserverType(observerType);
    return (
        <Grid justify="right">
            <Grid.Col
                style={{ minHeight: '1rem', minWidth: '1rem' }}
            >
                <Tooltip label={observerType}>
                    <Image
                        width={24}
                        height={24}
                        src={logo}
                        alt={observerType}
                    />
                </Tooltip>
            </Grid.Col>
        </Grid>
    );
}
