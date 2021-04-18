import React, { useEffect, useState } from "react";
import { store } from "react-notifications-component";
import { Badge, Button } from "shards-react";
import DataTable, { createTheme } from "react-data-table-component";

import { login, authFetch, useAuth, logout } from "../auth";
import NavigationBar from "../components/navbar";

export default function Tasks() {
  const [logged] = useAuth();
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    authFetch("/api/tasks", {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((response) => {
        if (response && response.tasks) {
          let tasks_arr = response.tasks.map((item) => {
            return {
              id: item.id,
              name: item.name,
              description: item.name,
              model: item.model_path,
              progress: item.progress,
              accuracy: item["meta_data.accuracy"],
              error: item["meta_data.err"],
              created_at: item.date_created,
            };
          });

          setTasks(tasks_arr);
        }
      });
  }, []);

  const columns = [
    {
      name: "ID",
      selector: "id",
      sortable: true,
      maxWidth: "100px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => <p style={{margin: 0}}>{row.id}</p>,
    },
    {
      name: "Name",
      selector: "name",
      sortable: true,
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => {
      let model_path = `task/${row.id}` || '#'
        return (<a href={model_path} target="_blank" rel="noopener noreferrer">
          {row.name}
        </a>)
      },
      
    },
    {
      name: "Description",
      selector: "description",
      sortable: true,
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => <p style={{margin: 0}}>{row.description}</p>,
    },
    {
      name: "Accuracy",
      selector: "accuracy",
      sortable: true,
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => {
        let accuracy = row.accuracy || "N/A"
        return(<p style={{margin: 0}}>{accuracy}</p>)
      },
    },
    {
      name: "Error rate",
      selector: "error",
      sortable: true,
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => {
        let error = row.error || "N/A"
        return(<p style={{margin: 0}}>{error}</p>)
      },
    },
    {
      name: "Model Path",
      selector: "model",
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => {
        let model_path = row.model || '/'
        return (<span>{model_path}</span>)
      },
    },
    {
      name: "Get Predictions",
      selector: "prediction",
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => {
        let model_path = `prediction/${row.id}` || '#'
        return (<a href={model_path} target="_blank" rel="noopener noreferrer">
          Predict
        </a>)
      },
    },
    {
      name: "Status",
      selector: "progress",
      sortable: true,
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => {
        let progress = row.progress || 0
        if(progress === 100){
          return <Badge theme="success">Completed</Badge>
        } else {
          return <Badge theme="info">N/A</Badge>
        }
      },
    },
    {
      name: "Created At",
      selector: "created_at",
      sortable: true,
      maxWidth: "300px", // when using custom you should use width or maxWidth, otherwise, the table will default to flex grow behavior
      cell: (row) => <p style={{margin: 0}}>{row.created_at}</p>,
    },
    // {
    //   name: "Plot Format",
    //   selector: "plot",
    //   wrap: true,
    //   sortable: true,
    //   format: (row) => `${row.plot.slice(0, 200)}...`,
    // },
    // {
    //   name: "Genres",

    //   cell: (row) => (
    //     <div>
    //       {row.genres.map((genre, i) => (
    //         <div key={i}>{genre}</div>
    //       ))}
    //     </div>
    //   ),
    // },
    // {
    //   name: "Thumbnail",
    //   grow: 0,
    //   cell: (row) => (
    //     <img height="84px" width="56px" alt={row.name} src={row.posterUrl} />
    //   ),
    // },
    // {
    //   name: "Poster Link",
    //   button: true,
    //   cell: (row) => (
    //     <a href={row.posterUrl} target="_blank" rel="noopener noreferrer">
    //       Download
    //     </a>
    //   ),
    // },
    // {
    //   name: "Poster Button",
    //   button: true,
    //   cell: () => <Button>Download Poster</Button>,
    // },
  ];

  // const data = [{ id: 1, title: "Conan the Barbarian", year: "1982" }];

  return (
    <>
      {logged ? (
        <>
          <NavigationBar />
          <div>
            <DataTable
              title="List Of Tasks"
              columns={columns}
              data={tasks}
              pagination
              fixedHeader
              highlightOnHover
            />
          </div>
        </>
      ) : (
        <></>
      )}
    </>
  );
}
