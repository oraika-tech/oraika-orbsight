import { Center, Image, Stack, Text } from '@mantine/core';
import { StaticImageData } from 'next/image';

export interface IconTextVerticalProps {
    icon: StaticImageData
    label: string
}

export default function IconTextVertical({ icon, label }: IconTextVerticalProps) {
    return (
        <Stack>
            <Center>
                <Image src={icon.src} w={50} />
            </Center>
            <Center>
                <Text>{label}</Text>
            </Center>
        </Stack>
    );
}
