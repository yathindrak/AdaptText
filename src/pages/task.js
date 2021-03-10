import React, { useEffect, useState } from "react";
import { store } from "react-notifications-component";
import { Progress } from "shards-react";
import { useRouteMatch } from "react-router-dom";
import Pusher from "pusher-js";
import { useHistory } from "react-router-dom";
import { login, authFetch, useAuth, logout } from "../auth";
import NavigationBar from "../components/navbar";

export default function Task() {
  const [logged] = useAuth();
  const history = useHistory();
  const [tasks, setTasks] = useState([]);
  let task_obj = useRouteMatch("/task/:id");
  let task_id = task_obj?.params?.id;
  const [task, setTask] = useState();
  const [progress, setProgress] = useState(0);
  const [isInProgress, setIsInProgress] = useState(false);

  useEffect(() => {
    if (task_id) {
      authFetch(`/api/task/${parseInt(task_id)}`, {
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status === 401) {
            // setMessage("Sorry you aren't authorized!");
            return null;
          } else if (response.status === 400) {
            history.push(`/`);
            return null;
          }
          return response.json();
        })
        .then((response) => {
          if (response && response?.task) {
            setTask(response?.task);

            // set initial progress from db
            if (response?.task?.progress === 100) {
              setIsInProgress(false);
              setProgress(100);
            } else {
              setIsInProgress(true);
              setProgress(response?.task?.progress);
            }

            // Get updated value from
            if (response?.task.progress === 0) {
              // execute api call
              authFetch(`/api/task/execute/${parseInt(task_id)}`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
              }).then((response) => {
                console.log(response);
              });

              const pusher = new Pusher("33b4f28f7e51e14cc56f", {
                cluster: "ap1",
                encrypted: true,
              });

              const channel = pusher.subscribe("upload");
              channel.bind("progress-" + parseInt(task_id), (data) => {
                if (data.percentage < 100) {
                  isInProgress(true);
                  setProgress(data.percentage);
                }

                if (data.percentage === 100) {
                  isInProgress(false);
                  setProgress(100);
                  
                  store.addNotification({
                    title: "Congratulations !!!",
                    message: "Building the classifier is completed",
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
            } else if (response?.task?.progress < 100) {
              setIsInProgress(true);

              const pusher = new Pusher("33b4f28f7e51e14cc56f", {
                cluster: "ap1",
                encrypted: true,
              });

              const channel = pusher.subscribe("upload");
              channel.bind("progress-" + parseInt(task_id), (data) => {
                if (data.percentage < 100) {
                  isInProgress(true);
                  setProgress(data.percentage);
                }

                if (data.percentage === 100) {
                  isInProgress(false);
                  setProgress(100);

                  store.addNotification({
                    title: "Congratulations !!!",
                    message: "Building the classifier is completed",
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
            }
          }
        });
    } else {
      history.push(`/`);
    }
  }, []);

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
            {isInProgress ? (
              <h4 className="mb-4" style={{ fontWeight: "600" }}>
                Training in progress !!!
              </h4>
            ) : (
              <h4 className="mb-4" style={{ fontWeight: "600" }}>
                Training Completed !!!
              </h4>
            )}
            <p className="mt-3 mb-5" style={{ fontWeight: "400" }}>
              This process will take several minutes based on the dataset you
              have provided.
            </p>
            <Progress style={{ width: "60vw" }} theme={isInProgress ? "primary" : "success"} value={progress} animated>
              {progress}
            </Progress>
          </div>
        </>
      ) : null}
    </>
  );
}
