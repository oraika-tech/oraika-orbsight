import { restApi } from 'common-utils/utils';
import { getUrlRoot } from 'common-utils/utils/common';

const urlBase = `${getUrlRoot()}/auth`;
export const EMAIL_FORMAT_ERROR = 'Wrong email format';

export interface Tenant {
    identifier: string;
    name: string;
    code: string;
}

export interface UserInfo {
    identifier: string;
    preferredTenantId: string;
    tenants: Tenant[];
    name: string;
    email: string;
}

export interface LoginResponse {
    access_token: string
    token_type: string // bearer
}

export async function doLoginWithToken(token: string) {
    const response = await fetch(`${urlBase}/login`, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: `{ "token": "${token}" }`,
        credentials: 'include'
    });

    if (response.ok) {
        return response.ok;
    }
    throw new Error('Fetch failed');
}

export async function doLogout() {
    return restApi(`${urlBase}/logout`, { method: 'POST' });
}

export async function getProfile() {
    return restApi(`${urlBase}/session`);
}

export async function setPreferredTenant(preferred_tenant_id: string) {
    return restApi(
        `${urlBase}/preferred-tenant`,
        {
            method: 'POST',
            body: JSON.stringify({ preferred_tenant_id })
        }
    );
}

export async function doLogin(userName: string, password: string) {
    const credential = JSON.stringify({ username: userName, password });

    const response = await fetch(`${urlBase}/login`, {
        headers: {
            accept: 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: credential,
        credentials: 'include'
    });

    if (response.ok) {
        return response.json();
    }
    throw new Error('Fetch failed');
}

export async function doDemoLogin(email: string) {
    const response = await fetch(`${getUrlRoot()} / demo / auth / demo - login`, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: `{ "email": "${email}" }`,
        credentials: 'include'
    });

    if (response.ok) {
        return response.ok;
    } if (response.status === 422) {
        throw new Error(EMAIL_FORMAT_ERROR);
    } else {
        throw new Error('Fetch failed');
    }
}
