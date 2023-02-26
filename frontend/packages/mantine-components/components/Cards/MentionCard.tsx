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
        <Stack align="center" spacing={0}>
            <Box sx={{ height: '100px' }}>
                <Image width={logoSize} src={logoUrl} alt={alt} />
            </Box>
            {title &&
                <Title order={3} color="dimmed">{title}</Title>
            }
            {link &&
                <Link href={link} target="_blank">
                    <Button variant="subtle" uppercase rightIcon={<IconArrowRight size="1.2rem" />}>
                        Read More
                    </Button>
                </Link>
            }
        </Stack>
    );
}
