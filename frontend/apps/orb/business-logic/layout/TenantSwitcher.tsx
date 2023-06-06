// import Select, { SelectChangeEvent } from '@mui/material/Select'
import { Select } from '@mantine/core';
import { setPreferredTenant } from 'common-utils/service/auth-service';
import { useContext } from 'react';
import { RefreshContext } from '../utils/RefreshProvider';

interface TenantInfo {
    identifier: string
    name: string
}

interface TenantSwitcherProps {
    tenants: TenantInfo[]
    preferredTenantId: string
    setPreferredTenantId: (tenantId: string) => void
}

export function TenantSwitcher({ tenants, preferredTenantId, setPreferredTenantId }: TenantSwitcherProps) {
    const { refreshPage } = useContext(RefreshContext);

    const handleChange = (value: string) => {
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
