import { Box, Burger, Button, Center, Group, Image, Menu } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconChevronDown } from '@tabler/icons-react';
import LOGO from 'assets/images/oraika-logo.png';
import cx from 'clsx';
import { ColorSchemeToggle } from 'mantine-components/components/ColorSchemeToggle';
import { useState } from 'react';
import classes from './HeaderMenu.module.css';

export interface HeaderLink {
    link: string;
    label: string;
    links?: HeaderLink[];
}

interface HeaderSearchProps {
    links: HeaderLink[];
}

export function HeaderMenu({ links }: HeaderSearchProps) {
    const [opened, { toggle }] = useDisclosure(false);
    const [active, setActive] = useState(links[0].link);

    const items = links.map((link) => {
        const menuItems = link.links?.map((item) => (
            <Menu.Item key={item.link}>{item.label}</Menu.Item>
        ));

        if (menuItems) {
            return (
                <Menu key={link.label} trigger="hover" transitionProps={{ exitDuration: 0 }}>
                    <Menu.Target>
                        <a href={link.link} className={classes.link}>
                            <Center>
                                <span className={classes.linkLabel}>{link.label}</span>
                                <IconChevronDown size={12} stroke={1.5} />
                            </Center>
                        </a>
                    </Menu.Target>
                    <Menu.Dropdown>{menuItems}</Menu.Dropdown>
                </Menu>
            );
        }

        return (
            <a
                key={link.label}
                href={link.link}
                className={cx(classes.link, { [classes.linkActive]: active === link.link })}
                onClick={(event) => {
                    event.preventDefault();
                    setActive(link.link);
                }}
            >
                {link.label}
            </a>
        );
    });

    return (
        // <Header span={{ base: 60, mb: 20 }}>
        <Group justify="space-between">
            <Box pl="lg">
                <Image height={40} src={LOGO.src} alt="oraika" />
            </Box>
            <Group gap={5} className={classes.links}>
                {items}
            </Group>
            <Group justify="center" grow px="md">
                <Button className={classes.headerButton} variant="default" radius="xl">
                    Sign in
                </Button>
                <Button
                    className={classes.headerButton}
                    color="orange"
                    radius="xl"
                    variant="filled"
                >
                    Apply for free access
                </Button>
            </Group>
            <Box pr="xs">
                <ColorSchemeToggle />
            </Box>
            <Burger opened={opened} onClick={toggle} className={classes.burger} size="sm" />
        </Group>
        // </Header>
    );
}
