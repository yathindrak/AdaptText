import React, { useEffect, useState } from "react";
import { store } from "react-notifications-component";
import { Badge, Button } from "shards-react";
import DataTable, { createTheme } from "react-data-table-component";
import { useRouteMatch } from "react-router-dom";
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
          if (response) {
            setTask(response?.task);

            if(response?.task.progress === 0) {
              // execute api call
              authFetch(`/api/task/execute/${parseInt(task_id)}`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
              })
                .then((response) => {
                  console.log("executed")
                  console.log(response);
                  console.log(JSON.stringify(response));
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
          <div>
            {/* <DataTable
              title="List Of Tasks"
              columns={columns}
              data={tasks}
              pagination
              fixedHeader
              highlightOnHover
            /> */}
          </div>
        </>
      ) : null}
    </>
  );
}
