import { Box, Center, Group, Image, Menu } from '@mantine/core';
import { IconChevronDown } from '@tabler/icons-react';
import LOGO from 'assets/images/oraika-logo.png';
import cx from 'clsx';
import { ColorSchemeToggle } from 'mantine-components/components/ColorSchemeToggle';
import { SubLinkData } from 'mantine-components/components/Navbars/NestedNavbar';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState } from 'react';
import LayoutPanel from '../../layout/LayoutPanel';
import classes from './HeaderMegaMenu.module.css';

export interface HeaderLink {
    link: string;
    label: string;
    links?: HeaderLink[];
}

interface HeaderSearchProps {
    links: HeaderLink[];
    opened: boolean;
    setOpened: (opened: (o: boolean) => boolean) => void
    dashboardLinks: SubLinkData[];
    downloadPdf: () => void;
    downloading: boolean;
}

export function HeaderMegaMenu({ links, opened, setOpened, dashboardLinks,
    downloadPdf, downloading }: HeaderSearchProps) {
    const { asPath } = useRouter();
    const [active, setActive] = useState(asPath);

    const items = links.map((link) => {
        const menuItems = link.links?.map((item) => (
            <Menu.Item key={item.link}>
                <Link
                    key={item.label}
                    href={item.link}
                    rel="noreferrer"
                    target={item.link.startsWith('http') ? '_blank' : '_self'}
                    className={cx(classes.link, { [classes.linkActive]: active.endsWith(item.link) })}
                >
                    {item.label}
                </Link>
            </Menu.Item>
        ));

        if (menuItems) {
            return (
                <Menu key={link.label} trigger="hover" transitionProps={{ exitDuration: 0 }}>
                    <Menu.Target>
                        <Link
                            href={link.link}
                            className={cx(classes.link, {
                                [classes.linkActive]: active.endsWith(link.link)
                            })}
                        >
                            <Center>
                                <span className={classes.linkLabel}>{link.label}</span>
                                <IconChevronDown size={12} stroke={1.5} />
                            </Center>
                        </Link>
                    </Menu.Target>
                    <Menu.Dropdown>{menuItems}</Menu.Dropdown>
                </Menu>
            );
        }

        return (
            <Link
                key={link.label}
                href={link.link}
                className={cx(classes.link, { [classes.linkActive]: active.endsWith(link.link) })}
                onClick={() => {
                    setActive(link.link);
                }}
            >
                {link.label}
            </Link>
        );
    });

    return (
        <Box>
            <header className={classes.header}>
                <Group justify="space-between" gap="md" wrap="nowrap" style={{ height: '100%' }}>

                    <Link href={process.env.NEXT_PUBLIC_HOME_URL} target="_blank">
                        <Image height={40} src={LOGO.src} alt="Oraika" />
                    </Link>

                    {items.length > 0 && (
                        <Group style={{ height: '100%' }} gap={10} hiddenFrom="sm">
                            {items}
                        </Group>
                    )}

                    <Box style={{ flex: 1 }}>
                        <LayoutPanel
                            breakpoint={992}
                            condition="gt"
                            opened={opened}
                            setOpened={setOpened}
                            dashboardLinks={dashboardLinks}
                            downloadPdf={downloadPdf}
                            downloading={downloading}
                        />
                    </Box>

                    <ColorSchemeToggle />
                </Group>
            </header>
        </Box>
    );
}
