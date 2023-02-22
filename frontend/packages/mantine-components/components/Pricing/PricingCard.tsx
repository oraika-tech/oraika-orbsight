import {
    ActionIcon,
    Badge,
    Card,
    Center,
    createStyles,
    Group,
    Image,
    List,
    MantineColor, Space, Stack, Text, Title
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
    showTrialBadge?: boolean
}

const useStyles = createStyles((theme) => ({
    cardWrapper: {
        height: '100%',
        display: 'flex',
        justifyContent: 'center'
    },
    card: {
        width: '100%',
        maxWidth: '450px'
    },
    badge: {
        backgroundColor: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 3 : 3]
    },
    text: {
        color: theme.colorScheme === 'dark' ? theme.colors.gray[4] : theme.colors.gray[0]
    },
    actionButton: {
        '&:hover': {
            cursor: 'default'
        }
    }
}));

export default function PricingCard({ icon, bgColor, title, subtitle, priceTitle,
    priceSubtitle, featureList, showTrialBadge }: PricingCardProps) {
    const featureItems = featureList.map((feature) => <List.Item key={feature}>{feature}</List.Item>);
    const { classes } = useStyles();

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
                                <ActionIcon
                                    className={classes.actionButton}
                                    variant="transparent"
                                    color="dark"
                                    size={24}
                                    radius="xl"
                                >
                                    <IconCheck size={16} />
                                </ActionIcon>
                            }
                        >
                            {featureItems}
                        </List>
                    </Center>
                    <Space h={20} />
                    {showTrialBadge &&
                        <Center>
                            <Badge className={classes.badge} sx={{ padding: 15 }}>
                                <Text className={classes.text} size="sm">
                                    Start with one month free trial
                                </Text>
                            </Badge>
                        </Center>
                    }
                </Stack>
            </Card>
        </div>
    );
}

PricingCard.defaultProps = {
    showTrialBadge: false
};
