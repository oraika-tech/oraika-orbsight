import { useInterval } from '@mantine/hooks';
import { useEffect, useState } from 'react';

interface TransMessageData {
    index: number;
    messages: string[];
    message: string;
}

interface RunningTextProps {
    messages: string[];
    charPeriodMs: number;
    wordPeriodMs: number;
}

export function RunningText({ messages, charPeriodMs, wordPeriodMs }: RunningTextProps) {
    const [transMessageData, setTransMessageData] = useState<TransMessageData>({
        index: 0,
        messages,
        message: ''
    });

    const wordRotationInterval = useInterval(() => {
        setTransMessageData((value) => {
            let newValue = value.index + 1;
            if (newValue >= value.messages.length) {
                // rotate index
                newValue = 0;
            }
            return { ...value, index: newValue, message: '' };
        });
    }, wordPeriodMs);

    useEffect(() => {
        wordRotationInterval.start();
        return wordRotationInterval.stop;
    }, []);

    const charTypingInterval = useInterval(() => {
        setTransMessageData((msgData) => {
            const selectedMessage = msgData.messages[msgData.index];
            const currentMessage = msgData.message;
            let newMessage = currentMessage;
            if (currentMessage.length < selectedMessage.length) {
                newMessage = currentMessage + selectedMessage[currentMessage.length];
            }
            return { ...msgData, message: newMessage };
        });
    }, charPeriodMs);

    useEffect(() => {
        charTypingInterval.start();
        return charTypingInterval.stop();
    }, []);

    return <> {transMessageData.message} </>;
}
