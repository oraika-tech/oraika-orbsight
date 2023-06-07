import { doLogout } from 'common-utils/service/auth-service';
import { UserContext } from 'mantine-components/components/Auth/AuthProvider';
import BreadcrumbsPanel from 'mantine-components/components/Breadcrumbs/BreadcrumbsPanel';
import { SubLinkData } from 'mantine-components/components/Navbars/NestedNavbar';
import { useContext } from 'react';

interface LayoutPanelProps {
    breakpoint: number;
    condition: 'lte' | 'gt';
    opened: boolean
    setOpened: (opened: (o: boolean) => boolean) => void
    dashboardLinks: SubLinkData[]
}

export default function LayoutPanel({ breakpoint, condition, opened, setOpened, dashboardLinks }: LayoutPanelProps) {
    const { userInfo, refreshPage, clearUserInfo, setPreferredTenantId } = useContext(UserContext);

    const logout = () => {
        doLogout()
            .then(() => { clearUserInfo(); })
            .finally(() => { refreshPage(); });
    };

    return (
        <BreadcrumbsPanel
            breakpoint={breakpoint}
            condition={condition}
            opened={opened}
            setOpened={setOpened}
            dashboardLinks={dashboardLinks}
            logout={logout}
            userInfo={userInfo}
            setPreferredTenantId={setPreferredTenantId}
            refreshPage={refreshPage}
        />
    );
}
