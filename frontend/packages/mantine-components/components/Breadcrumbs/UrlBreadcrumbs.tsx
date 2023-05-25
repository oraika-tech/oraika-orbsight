import { Breadcrumbs, Text } from '@mantine/core';
import { IconHome } from '@tabler/icons-react';
import Link from 'next/link';
import { NextRouter, useRouter } from 'next/router';

function formatTitle(title: string): string {
    return title
        .split('-')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function getDesktopLabelForId(links: DashboardLink[]): Map<string, string> {
    return new Map(links.map((link) => {
        const id = link.link.split('/').pop() || '';
        return [id, link.label];
    }));
}

interface DashboardLink {
    label: string
    link: string
}

interface UrlBreadcrumbsProps {
    dashboardLinks: DashboardLink[]
}

export default function UrlBreadcrumbs({ dashboardLinks }: UrlBreadcrumbsProps) {
    const router: NextRouter = useRouter();
    const pathnames: string[] = router.asPath.split('/').filter((x) => x);

    const dashboardMap = getDesktopLabelForId(dashboardLinks);

    const items = pathnames.map((path: string, index: number) => {
        const title: string = dashboardMap.get(path) || formatTitle(path);
        return <Text key={index}>{title}</Text>;
    });

    if (items.length === 0) {
        items.unshift(<Text>Home</Text>);
    }
    items.unshift(<Link key="home" href="/"><IconHome style={{ marginTop: '3px' }} size={16} /></Link>);

    return <Breadcrumbs>{items}</Breadcrumbs>;
}
