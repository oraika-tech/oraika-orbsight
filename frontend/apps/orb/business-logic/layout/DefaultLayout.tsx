import { ActionIcon, Box, Group, Paper, Space, Stack, createStyles } from '@mantine/core';
import {
    IconAdjustments,
    IconAlignBoxLeftMiddle,
    IconArrowsJoin,
    IconCloud,
    IconDeviceDesktopAnalytics,
    IconGauge,
    IconHome,
    IconLogout,
    IconPresentationAnalytics,
    IconReload,
    IconRocket,
    IconTextCaption,
    IconTopologyStar2
} from '@tabler/icons-react';
import { doLogout } from 'common-utils/service/auth-service';
import { UserContext } from 'mantine-components/components/Auth/AuthProvider';
import UrlBreadcrumbs from 'mantine-components/components/Breadcrumbs/UrlBreadcrumbs';
import CollapseToggleButton from 'mantine-components/components/Buttons/CollapseToggleButton';
import NavbarNested, { LinkData } from 'mantine-components/components/Navbars/NestedNavbar';
import { useRouter } from 'next/router';
import { ReactNode, useContext, useEffect, useState } from 'react';
import { getDashboards } from '../../lib/service/dashboard-service';
import { LandingPageHeader } from '../LandingPage/Header/Header';
import { RefreshContext } from '../utils/RefreshProvider';
import { TenantSwitcher } from './TenantSwitcher';

interface DefaultLayoutProps {
    children: ReactNode
}

const useStyles = createStyles((theme) => ({
    container: {
        borderRadius: 10,
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[1],
        height: '100%'
    },
    navbar: {
        position: 'sticky',
        top: '70px',
        zIndex: 1
    },
    breadcrumbsCard: {
        position: 'sticky',
        top: '70px',
        zIndex: 1,
        opacity: 0.8,
        padding: '10px',
        borderRadius: 5,
        paddingTop: 5,
        paddingBottom: 5
    }
}));

function routeExist(path: string, data: LinkData[]): boolean {
    for (const link of data) {
        if (link.link === path) {
            return true;
        }

        if (link.links) {
            for (const subLink of link.links) {
                if (subLink.link === path) {
                    return true;
                }
            }
        }
    }

    return false;
}

export default function DefaultLayout({ children }: DefaultLayoutProps) {
    const router = useRouter();
    const { classes } = useStyles();
    const [opened, setOpened] = useState(true);
    const [dashboardLinks, setDashboardLinks] = useState([]);
    const { userInfo, refreshPage, clearUserInfo, setPreferredTenantId } = useContext(UserContext);

    const linkData: LinkData[] = [
        { label: 'Home', icon: IconHome, link: '/' },
        { label: 'Live Feed', icon: IconRocket, link: '/live-feed' },
        { label: 'Dashboard', icon: IconGauge, initiallyOpened: true, links: dashboardLinks },
        {
            label: 'Text Analysis',
            icon: IconPresentationAnalytics,
            initiallyOpened: true,
            links: [
                { label: 'Key Phrases', icon: IconTextCaption, link: '/text-analysis/key-phrases' },
                { label: 'Word Cloud', icon: IconCloud, link: '/text-analysis/word-cloud' }
            ]
        }
    ];

    if (process.env.NEXT_PUBLIC_DEMO_MODE !== 'true') {
        linkData.push({
            label: 'Manage',
            icon: IconAdjustments,
            initiallyOpened: true,
            links: [
                { label: 'Entity', icon: IconTopologyStar2, link: '/manage/entity' },
                { label: 'Data Source', icon: IconArrowsJoin, link: '/manage/data-source' },
                { label: 'Taxonomy', icon: IconAlignBoxLeftMiddle, link: '/manage/taxonomy' }
            ]
        });
    }

    const path = router.asPath;
    if (path !== '/' && !path.startsWith('/dashboards') && !routeExist(path, linkData)) {
        router.replace('/');
        return <></>;
    }

    useEffect(() => {
        getDashboards('dashboard-list')
            .then((dashboards) => {
                const dashboardData = dashboards.map((dashboard) => ({
                    label: dashboard.title,
                    icon: IconDeviceDesktopAnalytics,
                    link: `/dashboards/${dashboard.identifier}`
                }));
                setDashboardLinks(dashboardData);
            })
            .catch(() => {

            });
    }, []);

    const logout = () => {
        doLogout()
            .then(() => { clearUserInfo(); })
            .finally(() => { refreshPage(); });
    };

    return (
        <Stack className={classes.container} spacing={5}>
            <LandingPageHeader />
            <Space h={50} />
            <Group spacing={4} align="flex-start" m={5} noWrap>
                {opened
                    ? (
                        <Box className={classes.navbar}>
                            <NavbarNested
                                links={linkData}
                                opened={opened}
                                name={userInfo.name}
                                email={userInfo.email}
                            />
                        </Box>
                    )
                    : <></>
                }
                <Stack align="stretch" w="100%" m={5} spacing={10}>
                    <Paper className={classes.breadcrumbsCard}>
                        <Group position="apart">
                            <Group noWrap>
                                <CollapseToggleButton
                                    opened={opened}
                                    toggle={() => setOpened((o) => !o)}
                                />
                                <UrlBreadcrumbs dashboardLinks={dashboardLinks} />
                            </Group>
                            <Group>
                                <ActionIcon size="sm" onClick={refreshPage}>
                                    <IconReload />
                                </ActionIcon>
                                <RefreshContext.Provider value={{ refreshPage }}>
                                    <TenantSwitcher
                                        tenants={userInfo.tenants}
                                        preferredTenantId={userInfo.preferredTenantId}
                                        setPreferredTenantId={setPreferredTenantId}
                                    />
                                </RefreshContext.Provider>
                                <ActionIcon onClick={logout}>
                                    <IconLogout size={20} />
                                </ActionIcon>
                            </Group>
                        </Group>
                    </Paper>
                    {children}
                </Stack>
            </Group>
        </Stack>
    );
}
