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
const profileContent = document.getElementById("profile-content");


/* =====================================================

=====================================================*/ 

function showLoginPage() {
    if (accessToken) {
        showApp();
        return;
    }

    appPage.classList.add("hidden");
    signupPage.classList.add("hidden");
    loginPage.classList.remove("hidden");
}


function showSignupPage() {
    if (accessToken) {
        showApp();
        return;
    }

    appPage.classList.add("hidden");
    loginPage.classList.add("hidden");
    signupPage.classList.remove("hidden");
}


/* =====================================================
   AUTH UI
===================================================== */

document
    .getElementById("show-signup")
    .addEventListener("click", showSignupPage);


document
    .getElementById("show-login")
    .addEventListener("click", showLoginPage);


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

            navigateTo("home");

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

    const isLoggedIn = Boolean(accessToken);

    document.getElementById("new-post-button")
        .classList.toggle("hidden", !isLoggedIn);

    document.getElementById("logout-button")
        .classList.toggle("hidden", !isLoggedIn);

    document.getElementById("guest-actions")
        .classList.toggle("hidden", isLoggedIn);

    document.getElementById("current-username").textContent =
    currentUsername
            ? currentUsername.charAt(0).toUpperCase()
            : "G";
}

function showLoginPage() {
    appPage.classList.add("hidden");
    signupPage.classList.add("hidden");
    loginPage.classList.remove("hidden");
}

function showSignupPage() {
    appPage.classList.add("hidden");
    loginPage.classList.add("hidden");
    signupPage.classList.remove("hidden");
}

document.getElementById("guest-login-button")
    .addEventListener("click", showLoginPage);

document.getElementById("guest-signup-button")
    .addEventListener("click", showSignupPage);

/* =====================================================
   LOGOUT
===================================================== */

document
    .getElementById("logout-button")
    .addEventListener(
        "click",
        logout
    );


/* =====================================================
   NAVIGATION
===================================================== */

let currentPage = "explore";

function navigateTo(page) {
    if (page === "home" && !accessToken) {
        showToast("Please login to view your home page.");
        showLoginPage();
        return;
    }

    currentPage = page;

    hideAllContent();

    document.querySelectorAll(".nav-item").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.page === page
        );
    });

    if (page === "home") {

        homeContent.classList.remove("hidden");

        loadHomePage();

    }

    if (page === "explore") {

        exploreContent.classList.remove("hidden");

        loadExplorePosts();

    }
}

document.querySelectorAll(".nav-item").forEach(button => {
    button.addEventListener("click", () => {
        navigateTo(button.dataset.page);

    });
});

function hideAllContent() {

    homeContent.classList.add("hidden");
    exploreContent.classList.add("hidden");
    newPostContent.classList.add("hidden");
    postDetailContent.classList.add("hidden");

    // Support existing code if the old profile section remains.
    if (profileContent) {
        profileContent.classList.add("hidden");

    }
}


/* =====================================================
   TEXTPOST LOGO NAVIGATION
===================================================== */

function openExplore() {

    loginPage.classList.add("hidden");
    signupPage.classList.add("hidden");
    appPage.classList.remove("hidden");

    // Update buttons for guests and logged-in users.
    showApp();

    currentPage = "explore";

    hideAllContent();
    exploreContent.classList.remove("hidden");

    document.querySelectorAll(".nav-item").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.page === "explore"
        );
    });

    loadExplorePosts();
}

// Handle mouse clicks and keyboard activation.
document.querySelectorAll(".app-logo").forEach(logo => {

    logo.style.cursor = "pointer";

    logo.addEventListener("click", openExplore);

    logo.addEventListener("keydown", event => {

        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openExplore();
        }

    });

});

/* =====================================================
   PROFILE
===================================================== */

async function loadProfile() {


    const usernameInput =
        document.getElementById("profile-username");

    const avatar =
        document.getElementById("profile-avatar-letter");

    const errorElement =
        document.getElementById("profile-error");

    errorElement.textContent = "";

    try {

        const response = await fetch(
            `${API_URL}/user/profile`,
            {
                method: "GET",

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
                data.detail ||
                "Could not load profile"
            );
        }

        usernameInput.value = data.username;

        avatar.textContent =
            data.username
                ? data.username
                    .charAt(0)
                    .toUpperCase()
                : "U";

    } catch (error) {

        errorElement.textContent =
            error.message;

    }
}


async function updateUsername() {

    const usernameInput =
        document.getElementById("profile-username");

    const errorElement =
        document.getElementById("profile-error");

    const newUsername =
        usernameInput.value.trim();

    errorElement.textContent = "";

    if (!newUsername) {

        errorElement.textContent =
            "Username cannot be empty.";

        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/user/profile`,
            {
                method: "PUT",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${accessToken}`
                },

                body: JSON.stringify({
                    username: newUsername
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not update username"
            );
        }

        /*
         * Username changed successfully.
         *
         * The current JWT contains the old username,
         * so we logout and ask the user to login again.
         */

        await logout();

    } catch (error) {

        errorElement.textContent =
            error.message;

    }
}

document
    .getElementById("save-profile-button")
    .addEventListener("click", updateUsername);

    
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

            navigateTo("home");


        } catch (error) {

            errorElement.textContent = error.message;

        }

    });


/* =====================================================
   HOME PAGE
===================================================== */

async function loadHomePage() {
    if (!accessToken) {
        showLoginPage();
        return;
    }

    const container = document.getElementById("home-posts");

    container.innerHTML =
        '<div class="loading">Loading your profile...</div>';

    try {
        const response = await fetch(`${API_URL}/user/home`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
                await logout();
                return;
            }

            throw new Error(
                data.detail || "Could not load your home page."
            );
        }

        // Check the profile data before using it.
        if (!data.profile || !data.profile.username) {
            throw new Error(
                "The server returned invalid profile data."
            );
        }

        const profile = data.profile;
        const posts = Array.isArray(data.posts)
            ? data.posts
            : [];

        // Display the profile.
        const username = profile.username;

        document.getElementById("home-username").textContent =
            username;

        document.getElementById("home-username-handle").textContent =
            `@${username}`;

        document.getElementById("home-avatar").textContent =
            username.charAt(0).toUpperCase();

        document.getElementById("home-post-count").textContent =
            posts.length;

        // These counts are placeholders.
        document.getElementById("home-following-count").textContent =
            "0";

        document.getElementById("home-followers-count").textContent =
            "0";

        // Keep the local username in sync with the server.
        currentUsername = username;

        localStorage.setItem("username", username);

        document.getElementById("current-username").textContent =
            username.charAt(0).toUpperCase();

        // Render the posts, even when the list is empty.
        await refreshLikedPostIds();

        renderPosts(container, posts);

    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                ${escapeHTML(error.message)}
            </div>
        `;
    }
}


/* =====================================================
   EXPLORE POSTS
===================================================== */

async function loadExplorePosts(search = null) {

    const container =
        document.getElementById("explore-posts");

    container.innerHTML =
        `<div class="loading">Loading posts...</div>`;

    try {

        let url = `${API_URL}/posts/explore`;

        if (search) {
            url += `?search=${encodeURIComponent(search)}`;
        }

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Could not load posts"
            );
        }
        await refreshLikedPostIds();
        renderPosts(container, data);

    } catch (error) {

        container.innerHTML =
            `<div class="empty-state">
                ${error.message}
            </div>`;
    }
}


/* =====================================================
   SEARCH
===================================================== */

const searchInput =
    document.getElementById("search-input");


searchInput.addEventListener("keydown", function(event) {

    if (event.key !== "Enter") {
        return;
    }

    const search =
        searchInput.value.trim();

    if (currentPage === "explore") {

        loadExplorePosts(search || null);

    }

});


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


        const username =
            post.owner?.username || "User";
        const avatarLetter =
            username.charAt(0).toUpperCase();
        
        const isOwner =
            Boolean(
                currentUsername &&
                post.owner?.username === currentUsername
            );

        const isLiked =
            getLikedPostIds().includes(String(post.id));

        const likeCount =
            Number(post.number_of_post_likes) || 0;


        card.innerHTML = `

            <div class="post-header">

                <div class="post-user">
                    <div class="post-avatar">
                        ${escapeHTML(avatarLetter)}
                    </div>

                    <div>
                        <div class="post-author">
                            ${escapeHTML(username)}
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
                    class="post-action like-action ${isLiked ? "liked" : ""}"
                    aria-label="${isLiked ? "Unlike post" : "Like post"}"
                    aria-pressed="${isLiked}"
                    onclick="toggleLike('${String(post.id)}', this)"
                >
                    <span class="like-icon">${isLiked ? "♥" : "♡"}</span>
                    <span class="like-count">${likeCount}</span>
                </button>

                ${
                    isOwner
                        ? `
                        <button
                            class="post-action"
                            onclick="openPost('${encodeURIComponent(post.title)}')"
                        >
                            View
                        </button>

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
   POST LIKES
===================================================== */

function getLikedPostIds() {
    const storageKey = `liked_post_ids_${currentUsername || "guest"}`;

    try {
        const savedIds = JSON.parse(
            localStorage.getItem(storageKey) || "[]"
        );

        return Array.isArray(savedIds)
            ? savedIds.map(String)
            : [];
    } catch {
        return [];
    }
}

async function refreshLikedPostIds() {
    if (!accessToken || !currentUsername) {
        return;
    }

    const response = await fetch(`${API_URL}/likes/mine`, {
        headers: {
            "Authorization": `Bearer ${accessToken}`
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Could not load liked posts."
        );
    }

    const storageKey = `liked_post_ids_${currentUsername}`;

    localStorage.setItem(
        storageKey,
        JSON.stringify(data.map(String))
    );
}

function saveLikedPostState(postId, isLiked) {
    const storageKey = `liked_post_ids_${currentUsername || "guest"}`;
    const likedIds = new Set(getLikedPostIds());

    if (isLiked) {
        likedIds.add(String(postId));
    } else {
        likedIds.delete(String(postId));
    }

    localStorage.setItem(
        storageKey,
        JSON.stringify([...likedIds])
    );
}


async function sendLikeRequest(action, postId) {
    return fetch(`${API_URL}/likes/${action}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            post_id: postId
        })
    });
}


async function toggleLike(postId, button) {
    if (!accessToken) {
    loginPage.classList.remove("hidden");
    signupPage.classList.add("hidden");
    appPage.classList.add("hidden");
    return;
}

    if (button.disabled) {
        return;
    }

    button.disabled = true;

    const countElement = button.querySelector(".like-count");
    const currentlyLiked = button.classList.contains("liked");

    let nextLikedState = !currentlyLiked;
    let countDelta = nextLikedState ? 1 : -1;

    try {
        let response = await sendLikeRequest(
            nextLikedState ? "like" : "unlike",
            postId
        );

        let data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const detail = String(data.detail || "").toLowerCase();

            // The post was already liked, but local state was outdated.
            if (
                nextLikedState &&
                response.status === 400 &&
                detail.includes("already liked")
            ) {
                nextLikedState = true;
                countDelta = 0;
            } else if (
                !nextLikedState &&
                response.status === 400 &&
                detail.includes("have not liked")
            ) {
                // The saved local state was outdated.
                response = await sendLikeRequest("like", postId);
                data = await response.json().catch(() => ({}));

                if (!response.ok) {
                    throw new Error(
                        data.detail || "Could not like this post."
                    );
                }

                nextLikedState = true;
                countDelta = 1;
            } else {
                if (response.status === 401) {
                    logout();
                    return;
                }

                throw new Error(
                    data.detail || "Could not update like."
                );
            }
        }

        button.classList.toggle("liked", nextLikedState);

        button.setAttribute(
            "aria-pressed",
            String(nextLikedState)
        );

        button.setAttribute(
            "aria-label",
            nextLikedState ? "Unlike post" : "Like post"
        );

        const icon = button.querySelector(".like-icon");

        if (icon) {
            icon.textContent = nextLikedState ? "♥" : "♡";
        }

        if (countElement) {
            const currentCount =
                Number(countElement.textContent) || 0;

            countElement.textContent = String(
                Math.max(0, currentCount + countDelta)
            );
        }

        saveLikedPostState(postId, nextLikedState);

    } catch (error) {
        showToast(error.message || "Could not update like.");
    } finally {
        button.disabled = false;
    }
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

        navigateTo("home");


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

        navigateTo("home");


    } catch (error) {

        showToast(error.message);

    }

}


/* =====================================================
   POST DETAIL UI
===================================================== */

function renderPostDetail(container, post) {

    const username =
        post.owner?.username || "User";
    const avatarLetter =
        username.charAt(0).toUpperCase();


    container.innerHTML = `

        <article class="detail-card">

            <div class="post-header">

                <div class="post-user">
                    <div class="post-avatar">
                        ${escapeHTML(avatarLetter)}
                    </div>

                    <div>
                        <div class="post-author">
                            ${escapeHTML(username)}
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

        navigateTo("home");

    });


/* =====================================================
   REFRESH
===================================================== */

document
    .getElementById("refresh-home")
    .addEventListener("click", () => {
        loadHomePage();
    });

document
    .getElementById("refresh-explore")
    .addEventListener("click", () => {
        loadExplorePosts();
    });

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


async function logout() {
    const tokenToRevoke = accessToken;
    let serverLogoutSucceeded = !tokenToRevoke;

    try {
        if (tokenToRevoke) {
            const response = await fetch(
                `${API_URL}/user/logout`,
                {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${tokenToRevoke}`
                    }
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Server logout failed: ${response.status}`
                );
            }

            serverLogoutSucceeded = true;
        }
    } catch (error) {
        console.error("Logout request failed:", error);
    } finally {
        // پاک کردن اطلاعات ورود از مرورگر
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");

        accessToken = null;
        currentUsername = null;

        // نمایش صفحه ورود
        appPage.classList.add("hidden");
        signupPage.classList.add("hidden");
        loginPage.classList.remove("hidden");

        document.getElementById("login-form").reset();
    }

    if (!serverLogoutSucceeded) {
        showToast(
            "Logged out locally, but server logout could not be confirmed."
        );
    }
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
    navigateTo("home");

} else {

    openExplore();

}