import { Refine } from '@refinedev/core';
import { notificationProvider } from '@refinedev/mantine';
import { DocumentTitleHandler, UnsavedChangesNotifier } from '@refinedev/nextjs-router';
import dataProvider from '@refinedev/simple-rest';
import axios from 'axios';
import { getUrlRoot } from 'common-utils/utils/common';
import { useTranslation } from 'next-i18next';

interface WithRefineProps {
    children: React.ReactNode;
}

export default function WithRefine({ children }: WithRefineProps) {
    const { t, i18n } = useTranslation();
    const i18nProvider = {
        translate: (key: string, params: object) => t(key, { defaultValue: '', ...params }),
        changeLocale: (lang: string) => i18n.changeLanguage(lang),
        getLocale: () => i18n.language
    };
    const axiosInstance = axios.create({
        withCredentials: true
    });
    return (
        <Refine
            dataProvider={dataProvider(`${getUrlRoot()}/generic`, axiosInstance)}
            notificationProvider={notificationProvider}
            i18nProvider={i18nProvider}
            options={{
                syncWithLocation: true,
                warnWhenUnsavedChanges: true,
                projectId: 'FkM2Th-Y5j5cz-OQ6aIO'
            }}
            resources={[
                { name: 'entities' },
                { name: 'observers' }
            ]}
        >
            {children}
            <UnsavedChangesNotifier />
            <DocumentTitleHandler />
        </Refine>
    );
}
