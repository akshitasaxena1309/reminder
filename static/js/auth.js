/**
 * Wrapper around fetch() that automatically attaches the JWT and
 * redirects to the login page if the token is missing or expired.
 */
async function authFetch(url, options = {}) {
  const token = localStorage.getItem("token");

  if (!token) {
    redirectToLogin();
    return null;
  }

  options.headers = {
    ...(options.headers || {}),
    "Authorization": "Bearer " + token,
  };

  const res = await fetch(url, options);

  if (res.status === 401) {
    redirectToLogin();
    return null;
  }

  return res;
}

function redirectToLogin() {
  localStorage.removeItem("token");
  window.location.href = "/?expired=1";
}