async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch("https://appointment-booking-api-2dkv.onrender.com/api/token/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    if (!res.ok) {
        alert("Login failed");
        return;
    }

    const data = await res.json();

    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);

    alert("Login success");
    loadBookings();
}






// ------------------------------------------------------
const API_URL = "https://appointment-booking-api-2dkv.onrender.com/api/appointments/";
let loading = false;
let nextPage = null;
let prevPage = null;

// ----------------------
// Refresh token
// ----------------------
async function refreshAccessToken() {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return null;

    const res = await fetch("https://appointment-booking-api-2dkv.onrender.com/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh })
    });

    if (!res.ok) return null;

    const data = await res.json();
    localStorage.setItem("access", data.access);
    return data.access;
}

// ----------------------
// Authorized fetch WITH retry
// ----------------------
async function authorizedFetch(url, options = {}) {
    let token = localStorage.getItem("access");

    options.headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    };

    let res = await fetch(url, options);

    if (res.status === 401) {
        token = await refreshAccessToken();
        if (!token) throw new Error("Session expired");

        options.headers.Authorization = "Bearer " + token;
        res = await fetch(url, options);
    }

    return res;
}

// ----------------------
// Load bookings
// ----------------------
async function loadBookings(url = API_URL) {
    if (loading) return;
    loading = true;

    const status = document.getElementById("statusFilter").value;
    const date = document.getElementById("dateFilter").value;

    if (url === API_URL) {
        const params = new URLSearchParams();
        if (status) params.append("status", status);
        if (date) params.append("date", date);
        url += "?" + params.toString();
    }

    try {
        const res = await authorizedFetch(url);
        if (!res.ok) throw new Error();

        const data = await res.json();

        nextPage = data.next;
        prevPage = data.previous;

        const table = document.getElementById("bookingTable");
        table.innerHTML = "";

        (data.results || []).forEach(b => {
            table.innerHTML += `
            <tr>
                <td>${b.id}</td>
                <td>${b.patient_name || "-"}</td>
                <td>${b.date}</td>
                <td><span class="status ${b.status}">${b.status}</span></td>
                <td>
                    ${b.status === "pending" ? `
                        <button class="approve" onclick="updateStatus(${b.id}, 'approve')">Approve</button>
                        <button class="reject" onclick="updateStatus(${b.id}, 'reject')">Reject</button>
                    ` : ``}
                    <button class="delete" onclick="deleteBooking(${b.id})">Delete</button>
                </td>
            </tr>`;
        });

    } catch {
        alert("Load failed");
    } finally {
        loading = false;
    }
}

// ----------------------
// Approve / Reject
// ----------------------
async function updateStatus(id, action) {
    const res = await authorizedFetch(`${API_URL}${id}/${action}/`, {
        method: "PATCH"
    });

    if (!res.ok) {
        alert("Action failed");
        return;
    }

    loadBookings();
}

// ----------------------
// Delete
// ----------------------
async function deleteBooking(id) {
    if (!confirm("Delete this appointment?")) return;

    const res = await authorizedFetch(`${API_URL}${id}/delete/`, {
        method: "DELETE"
    });

    if (!res.ok) {
        alert("Delete failed");
        return;
    }

    loadBookings();
}

function loadNext() {
    if (nextPage) loadBookings(nextPage);
}

function loadPrev() {
    if (prevPage) loadBookings(prevPage);
}

loadBookings();
