const defaultHeaders = {
    accept: 'application/json',
    'Content-Type': 'application/json'
};

function setDefaultHeaders(request: RequestInit) {
    const headers = new Headers(request.headers || {});
    Object.entries(defaultHeaders).forEach(header => {
        if (!headers.get(header[0])) {
            headers.set(header[0], header[1]);
        }
    });

    request.headers = headers;
}
export function restPublicApi(url: string, requestArg?: RequestInit) {
    const request = requestArg || {};
    setDefaultHeaders(request);
    request.mode = 'no-cors';
    return fetch(url, request)
        .then(response => {
            if (response.status < 300) {
                if (response.status === 204 || response.status === 0) {
                    return {};
                }
                return response.json();
            }
            throw new Error(`API failed with status: ${response.status}`);
        });
}

export function formSubmit(formUrl: string, formData: FormData) {
    return fetch(formUrl, {
        mode: 'no-cors',
        headers: {
            Accept: 'application/json, application/xml, text/plain, text/html, *.*'
        },
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok || response.status === 0) {
                return response.ok;
            }
            throw new Error(`Fetch failed: ${response.status}`);
        });
}

export function zohoFormSubmit(formName: string, formId: string, formFields: Map<string, string>, formValues: object) {
    const formUrl = `https://forms.zohopublic.in/oraika/form/${formName}/formperma/${formId}/htmlRecords/submit`;

    const formData = new FormData();

    Object.entries(formValues).forEach(fieldValue => {
        const formField = formFields.get(fieldValue[0]);
        const value = fieldValue[1];
        if (formField) {
            formData.append(formField, value);
        }
    });

    return formSubmit(formUrl, formData);
}

export function zohoFormPost(formName: string, formId: string, formValues: object) {
    const formUrl = `https://forms.zohopublic.in/oraika/form/${formName}/formperma/${formId}/records`;

    return restPublicApi(formUrl, {
        method: 'POST',
        body: JSON.stringify(formValues)
    });
}
