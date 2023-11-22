import {
    Avatar,
    Blockquote,
    Card,
    Grid,
    Highlight,
    Image,
    Rating,
    Space,
    Stack,
    Text,
    Title,
    useMantineColorScheme
} from '@mantine/core';
import { useMediaQuery } from '@mantine/hooks';
import { ReactNode } from 'react';
import classes from './TestimonialCard.module.css';

export interface TestimonialCardProps {
    reviewerPictureUrl?: string
    reviewerName: string
    reviewerTitle: string
    companyName: string
    companyLogoUrl: string
    rating?: number
    highlightedTexts: string[]
    reviewText: string
    reviewTime?: Date
    reviewSourceIcon?: ReactNode
}

export default function TestimonialCard({
    reviewerName,
    reviewerPictureUrl,
    reviewerTitle,
    companyName,
    companyLogoUrl,
    rating,
    highlightedTexts,
    reviewText,
    reviewTime,
    reviewSourceIcon }: TestimonialCardProps) {
    const mobileScreen = useMediaQuery('(max-width: 350px)');
    const { colorScheme } = useMantineColorScheme();
    const avatarBg = colorScheme === 'light' ? 'var(--mantine-color-gray-2)' : 'var(--mantine-color-gray-3)';
    return (
        <Card shadow="xl" p="lg" radius={15} className={classes.card}>
            <Grid>
                {rating &&
                    <Grid.Col span={3}>
                        <Rating value={rating} size="md" fractions={5} readOnly />
                    </Grid.Col>
                }
                <Grid.Col>
                    <Blockquote cite={reviewTime && reviewTime.toDateString()} color="teal">
                        <Highlight ta={mobileScreen ? 'left' : 'justify'} highlight={highlightedTexts}>
                            {reviewText}
                        </Highlight>
                    </Blockquote>
                </Grid.Col>
                {reviewSourceIcon &&
                    <Grid.Col>
                        {reviewSourceIcon}
                    </Grid.Col>
                }

                {reviewerPictureUrl
                    ? (
                        <Grid.Col span={1.7}>
                            <Avatar
                                className={classes.picImage}
                                radius="xl"
                                size="lg"
                                alt=""
                                src={reviewerPictureUrl}
                            />
                        </Grid.Col>
                    ) : (
                        <Grid.Col span={1.5}>
                            <Avatar
                                className={classes.picImage}
                                variant="filled"
                                bg={avatarBg}
                                size="lg"
                                radius={40}
                                p="0.4rem"
                                src={companyLogoUrl}
                            />
                            {/* <Image span={{ base:50, height:20 }} src={companyLogoUrl} /> */}
                        </Grid.Col>
                    )
                }
                <Grid.Col span={7}>
                    <Stack gap={0} h="100%" justify="center" align="flex-start">
                        <Title order={5}>
                            {reviewerName}
                        </Title>
                        <Text>
                            {reviewerTitle} at {companyName}
                        </Text>
                    </Stack>
                </Grid.Col>
                <Grid.Col span={1.7}>
                    <Space />
                </Grid.Col>
                {reviewerPictureUrl &&
                    <Grid.Col span={1}>
                        <Image w={50} height={50} src={companyLogoUrl} />
                    </Grid.Col>
                }

            </Grid>
        </Card>
    );
}
