import { Box, Overlay } from '@mantine/core';
import Image from 'next/image';
import DATA_ERROR from '../../../assets/images/data-fetch-error.png';

interface ErrorPanelProps {
    isError: boolean;
    children: React.ReactNode;
}

export default function ErrorPanel({ isError, children }: ErrorPanelProps) {
    return (
        <Box>
            {children}
            {isError && <Overlay><Image src={DATA_ERROR} alt="Something went wrong!" /></Overlay>}
        </Box>
    );
}
