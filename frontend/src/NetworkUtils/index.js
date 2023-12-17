// async function login(body) {
//     let myHeaders = new Headers();
//     myHeaders.append("Content-Type", "application/json");

//     let requestOptions = {
//         mode: 'cors',
//         method: "POST",
//         headers: myHeaders,
//         body: body
//     };

//     let response = await fetch('http://localhost:8000/users/token/', requestOptions);
//     if (response.status !== 200) {
//         throw new Error(JSON.stringify({ status: 401 }))
//     }

//     let responseJson = await response.json();
//     localStorage.setItem("refreshToken", responseJson.refresh);
//     localStorage.setItem("authToken", responseJson.access);
//     return responseJson;
// }

// async function logout() {
//     let myHeaders = new Headers();
//     myHeaders.append("Content-Type", "application/json");

//     let jsonData = JSON.stringify({
//         refresh: localStorage.getItem("refreshToken")
//     });

//     let requestOptions = {
//         mode: 'cors',
//         method: "POST",
//         headers: myHeaders,
//         body: jsonData
//     };

//     try {
//         let response = await fetch('http://localhost:8000/users/token/logout/', requestOptions);
//     } catch (error) {
//         console.log(error);
//     }
// }

// async function register(body) {
//     let myHeaders = new Headers();

//     let requestOptions = {
//         mode: 'cors',
//         method: "POST",
//         headers: myHeaders,
//         body: body
//     };

//     let response = await fetch('http://localhost:8000/users/register/', requestOptions);
//     let responseJson = await response.json();
//     if (response.status !== 201) {
//         throw new Error(JSON.stringify({ status: response.status, response: responseJson }))
//     }

//     return responseJson;
// }

// async function sendRequest(url, method, body) {
//     let myHeaders = new Headers();
//     myHeaders.append("Authorization", "Bearer " + localStorage.getItem("authToken"));

//     let requestOptions = {
//         mode: "cors",
//         method: method,
//         headers: myHeaders,
//     };

//     if (body !== undefined)
//         requestOptions['body'] = body;

//     let attempts = 0;
//     while (true) {
//         let response = await fetch(url, requestOptions);
//         if (response.status >= 200 && response.status < 300) {
//             if (response.status === 204) {
//                 return JSON.stringify({ status: 204 })
//             }
//             const responseJson = await response.json();
//             return responseJson;
//         } else if (response.status === 401) {
//             let res = await refresh();
//             if (res === "") {
//                 throw new Error(JSON.stringify({ status: 401 }));
//             } else {
//                 myHeaders.set("Authorization", "Bearer " + res);
//                 requestOptions.headers = myHeaders;
//                 attempts++;
//                 if (attempts >= 2) {  // should never happen unless internet fails
//                     throw new Error(JSON.stringify({ status: 401 }));
//                 }
//             }
//         } else if (response.status >= 401 && response.status < 500) {
//             throw new Error(JSON.stringify({ status: response.status }));
//         } else if (response.status === 400) {
//             let responseJson = await response.json();
//             throw new Error(JSON.stringify({ status: response.status, response: responseJson }));
//         } else {
//             console.log(response);
//             throw new Error(JSON.stringify({ status: 500 }));
//         }
//     }
// }

// async function refresh() {
//     let newTokenResponse = await fetch("http://localhost:8000/users/token/refresh/", {
//         mode: "cors",
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//             refresh: localStorage.getItem('refreshToken')
//         })
//     })

//     if (newTokenResponse.status !== 200) {
//         return "";
//     } else {
//         let newTokens = await newTokenResponse.json();
//         localStorage.setItem("refreshToken", newTokens.refresh);
//         localStorage.setItem("authToken", newTokens.access);
//         return newTokens.access;
//     }
// }

async function sendRequestWithoutAuth(url) {
    let myHeaders = new Headers();

    let requestOptions = {
        mode: "cors",
        method: "GET",
        headers: myHeaders,
    };

    let response = await fetch(url, requestOptions);
    if (response.status >= 200 && response.status < 300) {
        const responseJson = await response.json();
        return responseJson;
    } else if (response.status >= 400 && response.status < 500) {
        let responseJson = await response.json();
        throw new Error(JSON.stringify({ status: response.status, response: responseJson }));
    } else {
        console.log(response);
        throw new Error(JSON.stringify({ status: 500 }));
    }
}

export { sendRequestWithoutAuth };