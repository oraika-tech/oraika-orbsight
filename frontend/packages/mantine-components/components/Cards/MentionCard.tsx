import { Box, Button, Image, Stack, Title } from '@mantine/core';
import { IconArrowRight } from '@tabler/icons-react';
import Link from 'next/link';

export interface MentionCardProps {
    logoUrl: string
    logoSize: string
    alt: string
    title?: string
    link?: string
}

export default function MentionCard({ logoUrl, logoSize, alt, title, link }: MentionCardProps) {
    return (
        <Stack align="center" gap={0}>
            <Box style={{ height: '100px' }}>
                <Image w={logoSize} src={logoUrl} alt={alt} />
            </Box>
            {title &&
                <Title order={3} c="dimmed">{title}</Title>
            }
            {link &&
                <Link href={link} target="_blank">
                    <Button variant="subtle" rightSection={<IconArrowRight size="1.2rem" />}>
                        READ MORE
                    </Button>
                </Link>
            }
        </Stack>
    );
}
