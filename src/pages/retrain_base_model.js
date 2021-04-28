import React, { useState } from "react";
import { store } from "react-notifications-component";
import { Button, Progress } from "shards-react";
import Pusher from "pusher-js";
import { useHistory } from "react-router-dom";
import { authFetch, useAuth } from "../auth";
import NavigationBar from "../components/navbar";

export default function Retrain() {
  const [logged] = useAuth();
  const history = useHistory();
  const [progress, setProgress] = useState(1);
  const [isInProgress, setIsInProgress] = useState(false);

  const retrainLM = (event) => {
    setIsInProgress(true);
    authFetch(`/api/retrain`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.status === 400 || response.status === 404) {
          history.push(`/`);
          return null;
        }
        return response.json();
      })
      .then((response) => {});

    const pusher = new Pusher("33b4f28f7e51e14cc56f", {
      cluster: "ap1",
      encrypted: true,
    });

    const channel = pusher.subscribe("upload");
    channel.bind("progress-lm", (data) => {
      console.log(data)
      if (data.percentage < 100) {
        setIsInProgress(true);
        setProgress(data.percentage);
      }

      if (data.percentage === 100) {
        setIsInProgress(false);
        setProgress(100);

        store.addNotification({
          title: "Congratulations !!!",
          message: "Retraining the LM is completed",
          type: "success",
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

  return (
    <>
      {logged ? (
        <>
          <NavigationBar />
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              height: "100vh",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <h4 className="mb-4" style={{ fontWeight: "600" }}>
              Retrain Base Language Model !!!
            </h4>
            <p className="mt-3 mb-5 ml-4" style={{ fontWeight: "400" }}>
              This process will take several minutes based on the data corpus
              currently available via lifelong learning
            </p>

            <Button
              onClick={retrainLM}
              style={{ width: "20rem" }}
              className="mt-5"
              disabled={isInProgress ? true : false}
            >
              Retrain &rarr;
            </Button>

            {isInProgress && progress < 100 ? (
              <Progress
                className="mt-5"
                style={{ width: "60vw" }}
                theme={isInProgress ? "primary" : "success"}
                value={progress}
                animated
              >
                {progress}
              </Progress>
            ) : null}
          </div>
        </>
      ) : null}
    </>
  );
}
