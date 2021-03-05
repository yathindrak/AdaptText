import { createAuthProvider } from "react-token-auth";

export const [useAuth, authFetch, login, logout] = createAuthProvider({
  accessTokenKey: "access_token",
  onUpdateToken: (auth_token) =>
    fetch("/api/refresh", {
      method: "POST",
      headers: {
        'Content-Type':'application/json'
      },
      body: auth_token.access_token,
    }).then(res => res.json()),
});
