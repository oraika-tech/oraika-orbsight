import { Group } from '@mantine/core';
import { CanAccess } from '@refinedev/core';
import { DeleteButton } from '@refinedev/mantine';
import { ForeignData } from '../../Common/CommonModels';
import { DataEditModelButton } from './DataEditModelButton';
import { DataShowModelButton } from './DataShowModelButton';

interface ControlButtonsPanelProps {
    resource: string;
    id: string | number;
    foreignData: ForeignData;
}

export default function ControlButtonsPanel({ resource, id, foreignData }: ControlButtonsPanelProps) {
    return (
        <Group justify="space-between" gap={0}>
            <Group gap={10}>
                <DataShowModelButton
                    resource={resource}
                    foreignData={foreignData}
                    id={id}
                    hideText
                    variant="transparent" />
                <DataEditModelButton
                    resource={resource}
                    id={id}
                    hideText
                    variant="transparent"
                    foreignData={foreignData} />
                <CanAccess resource={resource} action="delete">
                    <DeleteButton
                        resource={resource}
                        confirmTitle="Delete"
                        confirmOkText="Confirm"
                        confirmCancelText="Cancel"
                        hideText
                        size="sm"
                        // @ts-ignore
                        variant="transparent"
                        recordItemId={id}
                    >
                        Delete
                    </DeleteButton>
                </CanAccess>
            </Group>
        </Group>
    );
}
