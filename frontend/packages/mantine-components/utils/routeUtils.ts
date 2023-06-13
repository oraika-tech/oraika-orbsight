import { DashboardLink } from '../components/Breadcrumbs/types';

export function getDesktopLabelForId(links: DashboardLink[]): Map<string, string> {
    return new Map(links.map((link) => {
        const id = link.link.split('/').pop() || '';
        return [id, link.label];
    }));
}
