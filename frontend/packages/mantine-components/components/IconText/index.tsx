import { BackgroundImage, Group } from '@mantine/core';
import Image from 'next/image';
import './style.css';

interface IconTextProps {
    icon: string
    altText?: string
    placeholder?: string
    children: any
}

export default function IconText({ icon, altText, placeholder, children }: IconTextProps) {
    return (
        <Group noWrap spacing={0}>
            <BackgroundImage w={32} src={placeholder || ''}>
                <Image
                    width={24}
                    height={24}
                    src={icon}
                    alt={altText || ''}
                />
            </BackgroundImage>
            {children}
        </Group>
    );
}
