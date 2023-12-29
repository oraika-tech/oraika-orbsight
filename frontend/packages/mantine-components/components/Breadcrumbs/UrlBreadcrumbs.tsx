import { Breadcrumbs, Loader, Text } from '@mantine/core';
import { IconHome } from '@tabler/icons-react';
import Link from 'next/link';
import { NextRouter, useRouter } from 'next/router';
import { getDesktopLabelForId } from '../../utils/routeUtils';
import { DashboardLink } from './types';

function formatTitle(title: string): string {
    return title
        .split('-')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

export interface UrlBreadcrumbsProps {
    dashboardLinks: DashboardLink[]
}

export default function UrlBreadcrumbs({ dashboardLinks }: UrlBreadcrumbsProps) {
    const router: NextRouter = useRouter();
    const pathnames: string[] = router.asPath.split('/').filter((x) => x);

    const dashboardMap = getDesktopLabelForId(dashboardLinks);

    const items = pathnames.map((rawPath: string, index: number) => {
        const [path] = rawPath.split('?');
        if (dashboardMap.has(path)) {
            return <Text key={index}>{dashboardMap.get(path)}</Text>;
        } else if (path.replaceAll('-', '').match(/^[0-9a-f]{32}$/i)) {
            return <Loader variant="bars" size="xs" />;
        } else {
            return <Text key={index}>{formatTitle(path)}</Text>;
        }
    });

    if (items.length === 0) {
        items.unshift(<Text key="home_text">Home</Text>);
    }
    items.unshift(<Link key="home_icon" href="/"><IconHome style={{ marginTop: '3px' }} size={16} /></Link>);

    return <Breadcrumbs>{items}</Breadcrumbs>;
}
