import { Select } from '@mantine/core';
import { setPreferredTenant } from 'common-utils/service/auth-service';

interface TenantInfo {
    identifier: string
    name: string
}

interface TenantSwitcherProps {
    tenants: TenantInfo[]
    refreshPage: () => void
    preferredTenantId: string
    setPreferredTenantId: (tenantId: string) => void
}

export function TenantSwitcher({ tenants, refreshPage, preferredTenantId, setPreferredTenantId }: TenantSwitcherProps) {
    const handleChange = (value: string | null) => {
        if (!value) {
            return;
        }
        const selectedPreferredTenantId = value;

        setPreferredTenant(selectedPreferredTenantId)
            .then(() => {
                setPreferredTenantId(selectedPreferredTenantId);
                refreshPage();
            });
    };

    const menuItems = [];
    let maxTextSize = 0;
    if (tenants) {
        for (const tenant of tenants) {
            menuItems.push({ value: tenant.identifier, label: tenant.name });
            maxTextSize = Math.max(maxTextSize, tenant.name.length);
        }
    }

    const dropdownTextWidth = 10 * maxTextSize + 20; // actual width on local and prod are different

    if (preferredTenantId && tenants.length > 0) {
        return (
            <Select
                id="tenant-select"
                value={preferredTenantId}
                variant="unstyled"
                onChange={handleChange}
                data={menuItems}
                style={{
                    width: dropdownTextWidth,
                    minWidth: dropdownTextWidth
                }}
            />
        );
    } else {
        return <div />;
    }
}
