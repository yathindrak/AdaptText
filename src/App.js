import React, { useEffect, useState } from "react";
import ReactNotification from "react-notifications-component";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  Link,
} from "react-router-dom";
import { FilePond } from "react-filepond";
import "filepond/dist/filepond.min.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "shards-ui/dist/css/shards.min.css";
import "react-notifications-component/dist/theme.css";
import { login, authFetch, useAuth, logout } from "./auth";
import Login from "./pages/login";
import Home from "./pages/home";
import Tasks from "./pages/tasks";
import "./App.css";
import Task from "./pages/task";

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

const LoginRoute = ({ component: Component, ...rest }) => {
  const [logged] = useAuth();

  return (
    <Route
      {...rest}
      render={(props) =>
        !logged ? <Component {...props} /> : <Redirect to="/" />
      }
    />
  );
};

export default function App() {
  return (
    <Router>
      <div>
        {/* <nav>
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
        </nav> */}

        <ReactNotification />

        <Switch>
          <LoginRoute path="/login" component={Login} />
          <Route path="/login123">
            <Login123 />
          </Route>
          <PrivateRoute path="/secret" component={Secret} />
          <Route path="/123">
            <Home123 />
          </Route>
          <PrivateRoute path="/tasks" component={Tasks} />
          <PrivateRoute path="/task/:id" component={Task} />


          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home123() {
  return <h2>Home</h2>;
}

function Login123() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [files, setFiles] = useState([]);
  const [pond, setPond] = useState();
  const [task_id, setTask_id] = useState();

  // this.state = {
  //   // Set initial files, type 'local' means this is a file
  //   // that has already been uploaded to the server (see docs)
  //   files: [{
  //       source: 'index.html',
  //       options: {
  //           type: 'local'
  //       }
  //   }]
  // };

  const [logged] = useAuth();

  useEffect(() => {
    setTask_id(1);
    // FilePond.registerPlugin(
    //   FilePondPluginImagePreview,
    //   FilePondPluginImageExifOrientation,
    //   FilePondPluginFileValidateSize,
    //   FilePondPluginImageEdit
    // );
    // Select the file input and use
    // create() to turn it into a pond
    // FilePond.create(
    //   document.querySelector('input')
    // );
  }, []);

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

  const handleInit = () => {
    console.log("FilePond instance has initialised", pond);
  };

  return (
    <div>
      <h2>Login</h2>

      {/* <input
        type="file"
        class="filepond"
        name="filepond"
        data-allow-reorder="true"
        data-max-file-size="50MB"
        data-max-files="1"
      /> */}

      <FilePond
        ref={(ref) => setPond(ref)}
        files={files}
        allowMultiple={false}
        server={{
          url: "/api/task/upload/" + task_id,
        }}
        oninit={() => handleInit()}
        onupdatefiles={(fileItems) => {
          // Set current file objects to this.state
          setFiles(fileItems.map((fileItem) => fileItem.file));

          console.log("File Items : ");
          console.log(fileItems);
        }}
      ></FilePond>

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

    // FilePond.registerPlugin(
    //   FilePondPluginImagePreview,
    //   FilePondPluginImageExifOrientation,
    //   FilePondPluginFileValidateSize,
    //   FilePondPluginImageEdit
    // );

    // Select the file input and use
    // create() to turn it into a pond
    // FilePond.create(
    //   document.querySelector('input')
    // );
  }, []);
  return (
    <div>
      <h2>Secret: {message}</h2>
      {/* <input
        type="file"
        class="filepond"
        name="filepond"
        multiple
        data-allow-reorder="true"
        data-max-file-size="3MB"
        data-max-files="3"
      /> */}
    </div>
  );
}
