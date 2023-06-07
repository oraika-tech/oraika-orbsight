import { HeaderMegaMenu } from './HeaderMegaMenu';
import { HeaderLink } from './HeaderMenu';

export function LandingPageHeader({ opened, setOpened, dashboardLinks }) {
    const links: HeaderLink[] = [];
    return (
        <HeaderMegaMenu
            links={links}
            opened={opened}
            setOpened={setOpened}
            dashboardLinks={dashboardLinks}
        />
    );
}
