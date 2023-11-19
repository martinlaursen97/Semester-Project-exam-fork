async function sendRequest(
    resource: string,
    method: string = "get",
    payload: any = null,
) {
    const accessToken = useCookie('access_token');
    const url = `http://localhost:7070/api${resource}`

    const requestOptions: any = {
        method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken.value}`,
        },
    };

    if (payload !== null) {
        requestOptions.body = JSON.stringify(payload);
    }

    const { data, error, execute, refresh } = await useFetch(url, requestOptions);

    return { data, error, execute, refresh }
}

export async function post(resource: string, payload: any) {
    return await sendRequest(resource, "POST", payload);
}

export async function get(resource: string) {
    return await sendRequest(resource, "GET");
}

export async function update(resource: string, payload: any) {
    return await sendRequest(resource, "PATCH", payload);
}
