import { Box, Group, Modal, Space, Stack, createStyles } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import {
    IconAdjustments,
    IconAlignBoxLeftMiddle,
    IconArrowsJoin,
    IconCloud,
    IconDeviceDesktopAnalytics,
    IconGauge,
    IconHome,
    IconPresentationAnalytics,
    IconRocket,
    IconTextCaption,
    IconTopologyStar2
} from '@tabler/icons-react';
import oraikaLogo from 'assets/images/oraika-logo.png';
import playarenaLogo from 'assets/images/play-arena-logo.png';
import shohozLogo from 'assets/images/shohoz-logo.png';
import { PdfMode, handleDownloadPdf } from 'common-utils/service/pdf-service';
import { capitalizeFirstLetter, getCurrentDateTimeFormatted } from 'common-utils/utils/common';
import { UserContext } from 'mantine-components/components/Auth/AuthProvider';
import NavbarNested, { LinkData } from 'mantine-components/components/Navbars/NestedNavbar';
import { getDesktopLabelForId } from 'mantine-components/utils/routeUtils';
import { StaticImageData } from 'next/image';
import { useRouter } from 'next/router';
import { ReactNode, useContext, useEffect, useRef, useState } from 'react';
import PdfDialog from '../../components/PdfDialog/PdfDialog';
import { getDashboards } from '../../lib/service/dashboard-service';
import { LandingPageHeader } from '../LandingPage/Header/Header';
import LayoutPanel from './LayoutPanel';

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
    const childRef = useRef();
    const { classes } = useStyles();
    const [opened, setOpened] = useState(true);
    const [dashboardLinks, setDashboardLinks] = useState([]);
    const { userInfo } = useContext(UserContext);
    const [downloading, setDownloading] = useState<boolean>(false);
    const [isOpened, { open, close }] = useDisclosure(false);

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

    const dashboardMap = getDesktopLabelForId(dashboardLinks);
    const urlEndPart = path.replace(/\/$/, '').split('/').pop() || 'home';
    const fileBaseName = capitalizeFirstLetter(dashboardMap.get(urlEndPart) || urlEndPart);
    const nowDate = getCurrentDateTimeFormatted().replaceAll(' ', '_').replaceAll(':', '.');
    const defaultFileName = `${fileBaseName}_${nowDate}.pdf`.replaceAll(' ', '-');
    const defaultTitle = fileBaseName;

    const logoSrcMap: Record<string, StaticImageData> = {
        '02ddd60c-2d58-47cc-a445-275d8e621252': playarenaLogo,
        '8f0cbfcd-da2c-42b9-b554-d67e7617e86d': shohozLogo
    };

    // function to return name of tenant based on user.preferredTenantId from user.tenents list
    const getTenantName = (tenantId: string) => {
        const tenant = userInfo.tenants.find((t) => t.identifier === tenantId);
        return tenant ? tenant.name : '';
    };

    const generatePdf = (fileName: string, pdfMode: PdfMode, title?: string) => {
        close();
        setDownloading(true);
        const pdfPages: HTMLElement[] = Array.from(document.querySelectorAll('.pdf-page'));
        const rootGrid: HTMLElement[] = Array.from(document.querySelectorAll('.mantine-Grid-root'));
        const pages = pdfPages.length > 0 ? pdfPages : (rootGrid.length > 0 ? [rootGrid[0]] : [childRef.current]);
        const logoSrc = logoSrcMap[userInfo.preferredTenantId] || getTenantName(userInfo.preferredTenantId);
        // loader is not working on direct call, hence delayed call
        setTimeout(() => {
            handleDownloadPdf(
                pages,
                fileName,
                pdfMode,
                title,
                oraikaLogo.src,
                logoSrc,
                () => {
                    setDownloading(false);
                }
            );
        }, 100);
    };

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

    return (
        <Stack className={classes.container} spacing={5}>
            <Modal opened={isOpened} onClose={close} title="PDF Download">
                <PdfDialog fileName={defaultFileName} title={defaultTitle} close={close} generatePdf={generatePdf} />
            </Modal>
            <LandingPageHeader
                opened={opened}
                setOpened={setOpened}
                dashboardLinks={dashboardLinks}
                downloadPdf={open}
                downloading={downloading}
            />
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
                    <LayoutPanel
                        breakpoint={992}
                        condition="lte"
                        opened={opened}
                        setOpened={setOpened}
                        dashboardLinks={dashboardLinks}
                        downloadPdf={open}
                        downloading={downloading}
                    />
                    <Box ref={childRef}>
                        {children}
                    </Box>
                </Stack>
            </Group>
        </Stack>
    );
}
