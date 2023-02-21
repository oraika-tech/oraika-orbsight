import {
    Card,
    Center,
    createStyles,
    Group,
    Image,
    List,
    MantineColor,
    Stack,
    Text,
    ThemeIcon,
    Title
} from '@mantine/core';
import { IconCheck } from '@tabler/icons-react';
import { StaticImageData } from 'next/image';

interface PricingCardProps {
    icon: StaticImageData
    bgColor?: MantineColor
    title: string
    subtitle: string
    priceTitle: string
    priceSubtitle: string
    featureList: string[]
}

const useStyles = createStyles(() => ({
    cardWrapper: {
        height: '100%',
        display: 'flex',
        justifyContent: 'center'
    },
    card: {
        width: '100%',
        maxWidth: '450px'
    }
}));

export default function PricingCard(
    { icon, bgColor, title, subtitle, priceTitle, priceSubtitle, featureList }: PricingCardProps) {
    const featureItems = featureList.map((feature) => <List.Item key={feature}>{feature}</List.Item>);
    const { classes, theme } = useStyles();

    return (
        <div className={classes.cardWrapper}>
            <Card className={classes.card} shadow="xl" radius="lg" withBorder bg={bgColor}>
                <Stack spacing={10}>
                    <Center>
                        <Image width={90} src={icon.src} alt="" />
                    </Center>
                    <Center>
                        <Title>{title}</Title>
                    </Center>
                    <Center>
                        <Group>
                            <Title order={1}>{priceTitle}</Title>
                            <Title order={6}>{priceSubtitle}</Title>
                        </Group>
                    </Center>
                    <Center>
                        <Text fz="sm">{subtitle}</Text>
                    </Center>
                    <Center>
                        <List
                            spacing="xs"
                            center
                            size="sm"
                            icon={
                                <ThemeIcon variant="light" color="teal" size={24} radius="xl">
                                    <IconCheck size={16} />
                                </ThemeIcon>
                            }
                        >
                            {featureItems}
                        </List>
                    </Center>
                </Stack>
            </Card>
        </div>
    );
}
