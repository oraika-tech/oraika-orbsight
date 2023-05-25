import { HeaderMegaMenu } from './HeaderMegaMenu';
import { HeaderLink } from './HeaderMenu';

export function LandingPageHeader() {
    const links: HeaderLink[] = [];
    return <HeaderMegaMenu links={links} />;
}
