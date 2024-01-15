import { Tooltip } from '@mantine/core';
import { getLogoFromObserverType } from 'common-utils/utils/common';
import Image from 'next/image';

export default function ObserverTypeCell({ observerType }) {
    const logo = getLogoFromObserverType(observerType);
    return (
        <Tooltip label={observerType}>
            <Image
                width={24}
                height={24}
                src={logo}
                alt={observerType}
            />
        </Tooltip>
    );
}
