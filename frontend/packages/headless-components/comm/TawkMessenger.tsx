import TawkMessengerReact from '@tawk.to/tawk-messenger-react';
import { useRef } from 'react';

// Tawk Doc: https://help.tawk.to/article/react-js
// https://github.com/tawk/tawk-messenger-react/blob/main/docs/api-reference.md

interface TawkMessengerProps {
    propertyId: string
    widgetId: string
}

export function TawkMessenger({ propertyId, widgetId }: TawkMessengerProps) {
    const tawkMessengerRef = useRef();

    return <TawkMessengerReact
        ref={tawkMessengerRef}
        propertyId={propertyId}
        widgetId={widgetId}
    />;
}
