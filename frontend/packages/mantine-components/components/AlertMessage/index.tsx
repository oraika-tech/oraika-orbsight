import { Alert, Collapse } from '@mantine/core';
import { useEffect, useState } from 'react';

interface AlertMessageProps {
    message: string;
    autoHideDuration: number;
}

export default function AlertMessage({ message, autoHideDuration }: AlertMessageProps) {
    const isOpen = Boolean(message);
    const [open, setOpen] = useState(isOpen);

    let localTimeout;
    const handleClose = () => {
        // const reason = event.currentTarget.getAttribute('data-reason');
        // if (reason !== 'clickaway') {
        setOpen(false);
        localTimeout = undefined;
        // }
    };

    if (isOpen) {
        if (localTimeout) {
            clearTimeout(localTimeout);
        }
        localTimeout = setTimeout(handleClose, autoHideDuration);
    }

    useEffect(() => {
        if (isOpen) {
            setOpen(isOpen);
        }
    }, [isOpen]);

    // const action = (
    //     <ActionIcon
    //         size="sm"
    //         aria-label="close"
    //         color="gray"
    //         onClick={handleClose}
    //         data-reason="clickaway"
    //     >
    //         <IconX />
    //     </ActionIcon>
    // );

    return (
        <Collapse in={open}>
            <Alert color="red" withCloseButton closeButtonLabel="Close alert">
                {message}
            </Alert>
        </Collapse>
    );
}
