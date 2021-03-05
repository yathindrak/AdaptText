import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  Link,
} from "react-router-dom";
import { login, authFetch, useAuth, logout } from "./auth";

const PrivateRoute = ({ component: Component, ...rest }) => {
  const [logged] = useAuth();

  return (
    <Route
      {...rest}
      render={(props) =>
        logged ? <Component {...props} /> : <Redirect to="/login" />
      }
    />
  );
};

export default function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/secret">Secret</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/login">
            <Login />
          </Route>
          <PrivateRoute path="/secret" component={Secret} />
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [logged] = useAuth();

  const onLoginClick = (e) => {
    e.preventDefault();

    let credentials = {
      username: username,
      password: password,
    };

    fetch("/api/login", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    })
      .then((res) => res.json())
      .then((token) => {
        if (token.access_token) {
          login(token);
        } else {
          console.log("Invalid username or password");
        }
      });
  };

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  return (
    <div>
      <h2>Login</h2>
      {!logged ? (
        <form action="#">
          <div>
            <input
              type="text"
              placeholder="Username"
              onChange={handleUsernameChange}
              value={username}
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              onChange={handlePasswordChange}
              value={password}
            />
          </div>
          <button onClick={onLoginClick} type="submit">
            Login Now
          </button>
        </form>
      ) : (
        <button onClick={() => logout()}>Logout</button>
      )}
    </div>
  );
}

function Secret() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    authFetch("/api/protected", {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.status === 401) {
          setMessage("Sorry you aren't authorized!");
          return null;
        }
        return response.json();
      })
      .then((response) => {
        if (response && response.message) {
          setMessage(response.message);
        }
      });
  }, []);
  return <h2>Secret: {message}</h2>;
}
