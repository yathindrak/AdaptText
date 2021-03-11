import React from "react";
import ReactNotification from "react-notifications-component";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
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
import Metrics from "./pages/metrics";

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
        <ReactNotification />

        <Switch>
          <LoginRoute path="/login" component={Login} />
          <PrivateRoute path="/tasks" component={Tasks} />
          <PrivateRoute path="/task/metrics/:id" component={Metrics} />
          <PrivateRoute path="/task/:id" component={Task} />
          <PrivateRoute path="/" component={Home} />
        </Switch>
      </div>
    </Router>
  );
}