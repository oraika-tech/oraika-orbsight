import { Box, Button, Image, Stack, Title } from '@mantine/core';
import { IconArrowRight } from '@tabler/icons-react';
import { StaticImageData } from 'next/image';
import Link from 'next/link';

interface MentionCardProps {
    logo: StaticImageData
    logoSize: string
    alt: string
    title: string
    link: string
}

export default function MentionCard({ logo, logoSize, alt, title, link }: MentionCardProps) {
    return (
        <Stack align="center" spacing={0}>
            <Box sx={{ height: '100px' }}>
                <Image width={logoSize} src={logo.src} alt={alt} />
            </Box>
            <Title order={3} color="dimmed">{title}</Title>
            <Link href={link} target="_blank">
                <Button variant="subtle" uppercase rightIcon={<IconArrowRight size="1.2rem" />}>
                    Read More
                </Button>
            </Link>
        </Stack>
    );
}
