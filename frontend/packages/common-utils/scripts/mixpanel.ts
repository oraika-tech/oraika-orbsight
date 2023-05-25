import mixpanel from 'mixpanel-browser';
import { getLocalUserEmail } from 'orb/lib/local-storage/user-info';

const enabled = process.env.NEXT_PUBLIC_MIX_PANEL_ENABLED === 'true';

export function mixPanelSetup() {
    const token = process.env.NEXT_PUBLIC_MIX_PANEL_TOKEN;

    if (enabled) {
        mixpanel.init(token);
        mixpanel.track('Oraika Loaded');
    }
}

export function trackFilter(location: string, filters: object) {
    if (!enabled) {
        return;
    }
    const event_properties = { location, email: '', filters: {} };
    const userEmail = getLocalUserEmail();
    if (userEmail) {
        event_properties.email = userEmail;
    }
    event_properties.filters = filters;
    mixpanel.track('filter_changed', event_properties);
}
