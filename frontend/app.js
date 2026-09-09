/* =====================================================
   CONFIG
===================================================== */

// const API_URL = "http://127.0.0.1:8000";
const API_URL = "https://app-text-post.onrender.com";


/* =====================================================
   STATE
===================================================== */

let accessToken = localStorage.getItem("access_token");
let currentUsername = localStorage.getItem("username");


/* =====================================================
   DOM
===================================================== */

const loginPage = document.getElementById("login-page");
const signupPage = document.getElementById("signup-page");
const appPage = document.getElementById("app-page");

const homeContent = document.getElementById("home-content");
const exploreContent = document.getElementById("explore-content");
const newPostContent = document.getElementById("new-post-content");
const postDetailContent = document.getElementById("post-detail-content");


/* =====================================================
   AUTH UI
===================================================== */

document
    .getElementById("show-signup")
    .addEventListener("click", () => {

        loginPage.classList.add("hidden");
        signupPage.classList.remove("hidden");

    });


document
    .getElementById("show-login")
    .addEventListener("click", () => {

        signupPage.classList.add("hidden");
        loginPage.classList.remove("hidden");

    });


/* =====================================================
   LOGIN
===================================================== */

document
    .getElementById("login-form")
    .addEventListener("submit", async (event) => {

        event.preventDefault();

        const username =
            document.getElementById("login-username").value.trim();

        const password =
            document.getElementById("login-password").value;

        const errorElement =
            document.getElementById("login-error");

        errorElement.textContent = "";

        const formData = new URLSearchParams();

        formData.append("username", username);
        formData.append("password", password);


        try {

            const response = await fetch(
                `${API_URL}/user/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },

                    body: formData
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail || "Login failed"
                );

            }


            accessToken = data.access_token;

            currentUsername = username;


            localStorage.setItem(
                "access_token",
                accessToken
            );

            localStorage.setItem(
                "username",
                currentUsername
            );


            showApp();

            loadHomePosts();

        } catch (error) {

            errorElement.textContent = error.message;

        }

    });


/* =====================================================
   SIGN UP
===================================================== */

document
    .getElementById("signup-form")
    .addEventListener("submit", async (event) => {

        event.preventDefault();

        const username =
            document.getElementById("signup-username").value.trim();

        const password =
            document.getElementById("signup-password").value;

        const errorElement =
            document.getElementById("signup-error");

        errorElement.textContent = "";


        try {

            const response = await fetch(
                `${API_URL}/user/sign_up`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail || "Signup failed"
                );

            }


            showToast("Account created. You can login now.");

            document
                .getElementById("signup-form")
                .reset();

            signupPage.classList.add("hidden");
            loginPage.classList.remove("hidden");


        } catch (error) {

            errorElement.textContent = error.message;

        }

    });


/* =====================================================
   APP
===================================================== */

function showApp() {

    loginPage.classList.add("hidden");
    signupPage.classList.add("hidden");

    appPage.classList.remove("hidden");

    document
        .getElementById("current-username")
        .textContent =
        currentUsername
            ? currentUsername.charAt(0).toUpperCase()
            : "U";
}


/* =====================================================
   LOGOUT
===================================================== */

document
    .getElementById("logout-button")
    .addEventListener("click", () => {

        localStorage.removeItem("access_token");
        localStorage.removeItem("username");

        accessToken = null;
        currentUsername = null;

        appPage.classList.add("hidden");
        loginPage.classList.remove("hidden");

    });


/* =====================================================
   NAVIGATION
===================================================== */

document
    .querySelectorAll(".nav-item")
    .forEach(button => {

        button.addEventListener("click", () => {

            const page = button.dataset.page;

            setActiveNav(button);

            hideAllContent();

            if (page === "home") {

                homeContent.classList.remove("hidden");

                loadHomePosts();

            }

            if (page === "explore") {

                exploreContent.classList.remove("hidden");

                loadExplorePosts();

            }

        });

    });


function setActiveNav(activeButton) {

    document
        .querySelectorAll(".nav-item")
        .forEach(button => {

            button.classList.remove("active");

        });

    activeButton.classList.add("active");
}


function hideAllContent() {

    homeContent.classList.add("hidden");
    exploreContent.classList.add("hidden");
    newPostContent.classList.add("hidden");
    postDetailContent.classList.add("hidden");

}


/* =====================================================
   NEW POST PAGE
===================================================== */

document
    .getElementById("new-post-button")
    .addEventListener("click", () => {

        hideAllContent();

        newPostContent.classList.remove("hidden");

    });


document
    .getElementById("cancel-post")
    .addEventListener("click", () => {

        hideAllContent();

        homeContent.classList.remove("hidden");

    });


/* =====================================================
   CREATE POST
===================================================== */

document
    .getElementById("new-post-form")
    .addEventListener("submit", async (event) => {

        event.preventDefault();

        const title =
            document.getElementById("post-title").value.trim();

        const description =
            document.getElementById("post-description").value.trim();

        const errorElement =
            document.getElementById("new-post-error");

        errorElement.textContent = "";


        try {

            const response = await fetch(
                `${API_URL}/posts/new`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "Authorization":
                            `Bearer ${accessToken}`
                    },

                    body: JSON.stringify({
                        title,
                        description
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail || "Could not create post"
                );

            }


            document
                .getElementById("new-post-form")
                .reset();


            showToast("Post created successfully.");

            hideAllContent();

            homeContent.classList.remove("hidden");

            loadHomePosts();


        } catch (error) {

            errorElement.textContent = error.message;

        }

    });


/* =====================================================
   HOME POSTS
===================================================== */

async function loadHomePosts() {

    const container =
        document.getElementById("home-posts");

    container.innerHTML =
        `<div class="loading">Loading posts...</div>`;


    try {

        const response = await fetch(
            `${API_URL}/posts/`,
            {
                headers: {
                    "Authorization":
                        `Bearer ${accessToken}`
                }
            }
        );


        const data = await response.json();


        if (!response.ok) {

            if (response.status === 401) {

                logout();

                return;
            }

            throw new Error(
                data.detail || "Could not load posts"
            );

        }


        renderPosts(container, data);

    } catch (error) {

        container.innerHTML =
            `<div class="empty-state">
                ${error.message}
            </div>`;

    }

}


/* =====================================================
   EXPLORE POSTS
===================================================== */

async function loadExplorePosts() {

    const container =
        document.getElementById("explore-posts");

    container.innerHTML =
        `<div class="loading">Loading posts...</div>`;


    try {

        const response = await fetch(
            `${API_URL}/posts/explore`
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Could not load posts"
            );

        }


        renderPosts(container, data);

    } catch (error) {

        container.innerHTML =
            `<div class="empty-state">
                ${error.message}
            </div>`;

    }

}


/* =====================================================
   RENDER POSTS
===================================================== */

function renderPosts(container, posts) {

    if (!posts || posts.length === 0) {

        container.innerHTML =
            `<div class="empty-state">
                No posts found.
            </div>`;

        return;
    }


    container.innerHTML = "";


    posts.forEach(post => {

        const card =
            document.createElement("article");

        card.className = "post-card";


        const ownerId =
            post.owner_id
                ? String(post.owner_id).slice(0, 6)
                : "U";


        card.innerHTML = `

            <div class="post-header">

                <div class="post-user">

                    <div class="post-avatar">
                        ${ownerId.charAt(0).toUpperCase()}
                    </div>

                    <div>

                        <div class="post-author">
                            User ${ownerId}
                        </div>

                        <div class="post-date">
                            ${formatDate(post.created_at)}
                        </div>

                    </div>

                </div>

                <button class="post-menu">
                    ···
                </button>

            </div>


            <h2 class="post-title">
                ${escapeHTML(post.title)}
            </h2>


            <p class="post-description">
                ${escapeHTML(post.description)}
            </p>


            <div class="post-actions">

                <button
                    class="post-action"
                    onclick="openPost('${encodeURIComponent(post.title)}')"
                >
                    View
                </button>

                ${
                    currentUsername
                        ? `
                        <button
                            class="post-action"
                            onclick="openEditPost('${encodeURIComponent(post.title)}')"
                        >
                            Edit
                        </button>

                        <button
                            class="post-action delete"
                            onclick="deletePost('${encodeURIComponent(post.title)}')"
                        >
                            Delete
                        </button>
                        `
                        : ""
                }

            </div>

        `;


        container.appendChild(card);

    });

}


/* =====================================================
   GET SINGLE POST
===================================================== */

async function openPost(encodedTitle) {

    const title =
        decodeURIComponent(encodedTitle);

    hideAllContent();

    postDetailContent.classList.remove("hidden");

    const container =
        document.getElementById("post-detail");

    container.innerHTML =
        `<div class="loading">Loading post...</div>`;


    try {

        const response = await fetch(
            `${API_URL}/posts/${encodeURIComponent(title)}`,
            {
                headers: {
                    "Authorization":
                        `Bearer ${accessToken}`
                }
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Post not found"
            );

        }


        renderPostDetail(container, data);

    } catch (error) {

        container.innerHTML =
            `<div class="empty-state">
                ${error.message}
            </div>`;

    }

}


/* =====================================================
   EDIT POST
===================================================== */

async function openEditPost(encodedTitle) {

    const title =
        decodeURIComponent(encodedTitle);

    try {

        const response = await fetch(
            `${API_URL}/posts/${encodeURIComponent(title)}`,
            {
                headers: {
                    "Authorization":
                        `Bearer ${accessToken}`
                }
            }
        );


        const post = await response.json();


        if (!response.ok) {

            throw new Error(
                post.detail || "Post not found"
            );

        }


        hideAllContent();

        newPostContent.classList.remove("hidden");


        document.querySelector(
            "#new-post-content h1"
        ).textContent = "Edit Post";


        document.querySelector(
            "#new-post-content .page-heading p"
        ).textContent = "Update your post.";


        document.getElementById("post-title").value =
            post.title;

        document.getElementById("post-description").value =
            post.description;


        const form =
            document.getElementById("new-post-form");


        form.onsubmit = async function(event) {

            event.preventDefault();

            await updatePost(title);

        };


    } catch (error) {

        showToast(error.message);

    }

}


/* =====================================================
   UPDATE POST
===================================================== */

async function updatePost(oldTitle) {

    const title =
        document.getElementById("post-title").value.trim();

    const description =
        document.getElementById("post-description").value.trim();


    try {

        const response = await fetch(
            `${API_URL}/posts/${encodeURIComponent(oldTitle)}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",

                    "Authorization":
                        `Bearer ${accessToken}`
                },

                body: JSON.stringify({
                    title,
                    description
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Update failed"
            );

        }


        showToast("Post updated.");

        document
            .getElementById("new-post-form")
            .reset();

        resetCreateForm();

        hideAllContent();

        homeContent.classList.remove("hidden");

        loadHomePosts();


    } catch (error) {

        document.getElementById(
            "new-post-error"
        ).textContent = error.message;

    }

}


/* =====================================================
   DELETE POST
===================================================== */

async function deletePost(encodedTitle) {

    const title =
        decodeURIComponent(encodedTitle);


    const confirmed =
        confirm(
            `Delete "${title}"?`
        );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/posts/${encodeURIComponent(title)}`,
            {
                method: "DELETE",

                headers: {
                    "Authorization":
                        `Bearer ${accessToken}`
                }
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Delete failed"
            );

        }


        showToast("Post deleted.");

        loadHomePosts();


    } catch (error) {

        showToast(error.message);

    }

}


/* =====================================================
   POST DETAIL UI
===================================================== */

function renderPostDetail(container, post) {

    container.innerHTML = `

        <article class="detail-card">

            <div class="post-user">

                <div class="post-avatar">
                    U
                </div>

                <div>

                    <div class="post-author">
                        User
                    </div>

                    <div class="post-date">
                        ${formatDate(post.created_at)}
                    </div>

                </div>

            </div>


            <h1 class="detail-title">
                ${escapeHTML(post.title)}
            </h1>


            <p class="detail-description">
                ${escapeHTML(post.description)}
            </p>


            <div class="post-actions">

                <button
                    class="post-action"
                    onclick="openEditPost('${encodeURIComponent(post.title)}')"
                >
                    Edit
                </button>

                <button
                    class="post-action delete"
                    onclick="deletePost('${encodeURIComponent(post.title)}')"
                >
                    Delete
                </button>

            </div>

        </article>

    `;

}


/* =====================================================
   BACK
===================================================== */

document
    .getElementById("back-button")
    .addEventListener("click", () => {

        hideAllContent();

        homeContent.classList.remove("hidden");

        loadHomePosts();

    });


/* =====================================================
   REFRESH
===================================================== */

document
    .getElementById("refresh-home")
    .addEventListener(
        "click",
        loadHomePosts
    );


document
    .getElementById("refresh-explore")
    .addEventListener(
        "click",
        loadExplorePosts
    );


/* =====================================================
   HELPERS
===================================================== */

function formatDate(date) {

    if (!date) {
        return "";
    }

    return new Date(date).toLocaleDateString(
        "en-US",
        {
            year: "numeric",
            month: "short",
            day: "numeric"
        }
    );

}


function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;

}


function showToast(message) {

    const toast =
        document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");


    setTimeout(() => {

        toast.classList.remove("show");

    }, 2500);

}


function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("username");

    accessToken = null;
    currentUsername = null;

    appPage.classList.add("hidden");

    loginPage.classList.remove("hidden");

}


function resetCreateForm() {

    const form =
        document.getElementById("new-post-form");

    form.onsubmit = null;

    document.querySelector(
        "#new-post-content h1"
    ).textContent = "Create Post";

    document.querySelector(
        "#new-post-content .page-heading p"
    ).textContent =
        "Share something with the community.";

}


/* =====================================================
   INITIAL STATE
===================================================== */

if (accessToken) {

    showApp();

    loadHomePosts();

} else {

    loginPage.classList.remove("hidden");

}