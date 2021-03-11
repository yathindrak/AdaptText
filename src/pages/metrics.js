import React, { useEffect, useState } from "react";
import { store } from "react-notifications-component";
import { Button, Progress } from "shards-react";
import { useRouteMatch } from "react-router-dom";
import Pusher from "pusher-js";
import { useHistory } from "react-router-dom";
import { authFetch, useAuth } from "../auth";
import NavigationBar from "../components/navbar";

export default function Metrics() {
  const [logged] = useAuth();
  const history = useHistory();
  let task_obj = useRouteMatch("/task/:id");
  let task_id = task_obj?.params?.id;
  const [task, setTask] = useState();

  useEffect(() => {
    if (task_id) {
      authFetch(`/api/task/${parseInt(task_id)}`, {
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
        .then((response) => {
          if (response && response?.task) {
            setTask(response?.task);

            // set initial progress from db
            if (response?.task?.progress !== 100) {
              history.push(`/tasks`);
              return;
            }
          }
        });
    } else {
      history.push(`/`);
    }
  }, []);

  // const onDisplayMetrices = (event) => {
  //   if (!isInProgress) {
  //     history.push(`/task/metrics/${parseInt(task_id)}`);
  //   }
  // };

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
              Training CompleteZXd !!!
            </h4>
            <p className="mt-3 mb-5 ml-4" style={{ fontWeight: "400" }}>
              Tkjlkjljlhis process will take several minutes based on the dataset you
              have provided.
            </p>
            {/* <Progress
              className="mb-5"
              style={{ width: "60vw" }}
              theme={isInProgress ? "primary" : "success"}
              value={progress}
              animated
            >
              {progress}
            </Progress> */}
            {/* <Button
              onClick={onDisplayMetrices}
              style={{ width: "20rem" }}
              className="mt-5"
              disabled={isInProgress ? true : false}
            >
              Display Metrics &rarr;
            </Button> */}
          </div>
        </>
      ) : null}
    </>
  );
}
