import { Button, Switch } from '@mantine/core';
import { useState } from 'react';
import ConfirmPanel from '../ConfirmPanel';

enum ButtonState {
    Initial = 1,
    Confirmation,
    Loading,
}

interface ToggleButtonProps {
    value: any;
    handleToggle: (id: string, isEnabled: boolean, handlerDone: (isSuccess: boolean) => void) => void;
}

export default function ToggleButton({ value, handleToggle }: ToggleButtonProps) {
    const [isEnabled, setIsEnabled] = useState(value.isEnabled);
    const [buttonState, setButtonState] = useState(ButtonState.Initial);

    const handleToggleInternal = () => {
        setButtonState(ButtonState.Confirmation);
    };

    const cancelHandler = () => {
        setButtonState(ButtonState.Initial);
    };

    const handlerDone = (isSuccess: boolean) => {
        setButtonState(ButtonState.Initial);
        if (isSuccess) {
            setIsEnabled(!isEnabled);
        }
    };

    const confirmHandler = () => {
        setButtonState(ButtonState.Loading);
        handleToggle(value.id, !isEnabled, handlerDone);
    };

    switch (buttonState) {
        case ButtonState.Confirmation:
            return <ConfirmPanel onConfirm={confirmHandler} onCancel={cancelHandler} />;
        case ButtonState.Loading:
            return (
                <Button
                    size="sm"
                    loading
                    variant="outline"
                    disabled
                />
            );
        default:
            return <Switch checked={isEnabled} onChange={handleToggleInternal} />;
    }
}
