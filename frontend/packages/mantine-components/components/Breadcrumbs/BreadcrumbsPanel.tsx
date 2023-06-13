import { ActionIcon, Group, Loader, Paper, Tooltip, createStyles } from '@mantine/core';
import { useViewportSize } from '@mantine/hooks';
import {
    IconDownload,
    IconLogout,
    IconReload
} from '@tabler/icons-react';
import { UserInfo } from 'common-utils/service/auth-service';
import UrlBreadcrumbs from 'mantine-components/components/Breadcrumbs/UrlBreadcrumbs';
import CollapseToggleButton from 'mantine-components/components/Buttons/CollapseToggleButton';
import { SubLinkData } from '../Navbars/NestedNavbar';
import { TenantSwitcher } from '../Tenant/TenantSwitcher';

const useStyles = createStyles(() => ({
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

interface BreadcrumbsPanelProps {
    breakpoint: number;
    condition: 'lte' | 'gt';
    opened: boolean;
    setOpened: (opened: (o: boolean) => boolean) => void;
    dashboardLinks: SubLinkData[];
    logout: () => void;
    userInfo: UserInfo;
    setPreferredTenantId: (tenantId: string) => void;
    refreshPage: () => void;
    downloadPdf: () => void;
    downloading: boolean;
}

export default function BreadcrumbsPanel({
    breakpoint, condition, opened, setOpened, dashboardLinks, logout,
    userInfo, setPreferredTenantId, refreshPage, downloadPdf, downloading }: BreadcrumbsPanelProps) {
    const { classes } = useStyles();
    const { width } = useViewportSize();

    const panelGroup = (
        <Group w="100%" h="100%" mt={4} position="apart">
            <Group noWrap>
                <CollapseToggleButton
                    opened={opened}
                    toggle={() => setOpened((o) => !o)}
                />
                <UrlBreadcrumbs dashboardLinks={dashboardLinks} />
            </Group>
            <Group>
                {process.env.NEXT_PUBLIC_DEMO_MODE !== 'true' && (
                    downloading ? (
                        <Tooltip openDelay={2000} label="Downloading..." position="left">
                            <Loader size="sm" />
                        </Tooltip>
                    ) : (
                        <Tooltip openDelay={2000} label="Download PDF" position="left">
                            <ActionIcon size="sm" onClick={downloadPdf}>
                                <IconDownload />
                            </ActionIcon>
                        </Tooltip>
                    )
                )}
                <Tooltip label="Reload" position="left">
                    <ActionIcon size="sm" onClick={refreshPage}>
                        <IconReload />
                    </ActionIcon>
                </Tooltip>
                <TenantSwitcher
                    tenants={userInfo.tenants}
                    refreshPage={refreshPage}
                    preferredTenantId={userInfo.preferredTenantId}
                    setPreferredTenantId={setPreferredTenantId}
                />
                <ActionIcon onClick={logout}>
                    <IconLogout size={20} />
                </ActionIcon>
            </Group>
        </Group>
    );

    if (condition === 'gt' && width > breakpoint) {
        return <>{panelGroup}</>;
    } else if (condition === 'lte' && width <= breakpoint) {
        return <Paper className={classes.breadcrumbsCard}> {panelGroup} </Paper>;
    } else {
        return <></>;
    }
}
