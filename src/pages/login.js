import React, { useEffect, useState } from "react";
import { store } from "react-notifications-component";
import {
  Card,
  CardHeader,
  CardTitle,
  CardBody,
  Button,
  FormInput,
} from "shards-react";

import { login, useAuth, logout } from "../auth";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [invalid, setInvalid] = useState(false);

  const [logged] = useAuth();

  useEffect(() => {
    //
  }, []);

  const onLoginBtnCLicked = (e) => {
    e.preventDefault();

    let credentials = {
      username: username,
      password: password,
    };

    if (!(username && password)) {
      setInvalid(true);
      store.addNotification({
        title: "Error",
        message: "Please fill required fields!",
        type: "danger",
        insert: "top",
        container: "top-right",
        animationIn: ["animate__animated", "animate__fadeIn"],
        animationOut: ["animate__animated", "animate__fadeOut"],
        dismiss: {
          duration: 5000,
          onScreen: true,
        },
      });

      return;
    }

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
          setInvalid(true);
          //   NotificationManager.error('Click me!', 5000);
          store.addNotification({
            title: "Error",
            message: "Invalid credentials!",
            type: "danger",
            insert: "top",
            container: "top-right",
            animationIn: ["animate__animated", "animate__fadeIn"],
            animationOut: ["animate__animated", "animate__fadeOut"],
            dismiss: {
              duration: 5000,
              onScreen: true,
            },
          });
        }
      });
  };

  const handleUsernameChange = (event) => {
    if (invalid) {
      setInvalid(false);
    }
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    if (invalid) {
      setInvalid(false);
    }
    setPassword(event.target.value);
  };

  // const handleInit = () => {
  //   console.log("FilePond instance has initialised", pond);
  // };

  return (
    <>
      {!logged ? (
        <div
          style={{
            display: "flex",
            height: "100vh",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Card
            small={false}
            style={{ maxWidth: "500px", textAlign: "center", width: "80%" }}
          >
            <CardHeader
              style={{
                backgroundPosition: "center",
              }}
            >
              <h4
                className="mb-4"
                style={{ color: "white", fontWeight: "600" }}
              >
                Welcome to AdaptText !
              </h4>
              {/* <p style={{ color: "white", fontWeight: "400" }}>
                We are Lorem ipsum dolor sit amet.Lorem ipsum dolor sit
                amet.Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet.
              </p> */}
            </CardHeader>
            <CardBody>
              <CardTitle>Log In</CardTitle>
              <br />
              <FormInput
                invalid={invalid}
                onChange={handleUsernameChange}
                value={username}
                placeholder="Email"
                className="mb-3"
              />
              <FormInput
                invalid={invalid}
                onChange={handlePasswordChange}
                value={password}
                type="password"
                placeholder="Password"
                className="mb-3"
              />
              <Button onClick={onLoginBtnCLicked} type="submit">
                Login &rarr;
              </Button>
            </CardBody>
          </Card>
        </div>
      ) : null
      }
    </>
  );
}
