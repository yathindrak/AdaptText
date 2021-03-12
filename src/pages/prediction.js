import React, { useEffect, useState } from "react";
import { useRouteMatch } from "react-router-dom";
import { store } from "react-notifications-component";
import { FilePond, registerPlugin } from "react-filepond";
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import {
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  FormInput,
  FormTextarea,
  Container,
  Row,
  Col,
  Button,
  FormCheckbox,
  Tooltip,
} from "shards-react";
import { useHistory } from "react-router-dom";
import { login, authFetch, useAuth, logout } from "../auth";
import NavigationBar from "../components/navbar";

registerPlugin(FilePondPluginFileValidateType);

export default function Prediction() {
  const [logged] = useAuth();
  let task_obj = useRouteMatch("/prediction/:id");
  let task_id = task_obj?.params?.id;
  const [token, setToken] = useState("");

  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState("");
  const [subText, setSubText] = useState("");
  const [textColumnDropdown, setTextColumnDropdown] = useState(false);
  const [labelColumnDropdown, setLabelColumnDropdown] = useState(false);
  const [continuous_train, setContinuous_train] = useState(true);
  const [
    isClassificationModelLoaded,
    setIsClassificationModelLoaded,
  ] = useState(false);

  const history = useHistory();

  const handleTextChange = (event) => {
    setSubText("");
    setText(event.target.value);
  };

  const onSubmitPredict = (e) => {
    if (task_id) {
      authFetch(`/api/predict/${task_id}/${text}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status === 400) {
            // setMessage("Sorry you aren't authorized!");
            store.addNotification({
              title: "Error",
              message: "Please fill valid values!",
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
            return null;
          }
          return response.json();
        })
        .then((response) => {
          if (response) {
            setPrediction(response['predicted_label']);
          }
          // if (response && response.tasks) {
          //   let tasks_arr = response.tasks.map((item) => {
          //     return {
          //       id: item.id,
          //       name: item.name,
          //       description: item.name,
          //       model: item.model_path,
          //       progress: item.progress,
          //       accuracy: item["meta_data.accuracy"],
          //       error: item["meta_data.err"],
          //       created_at: item.date_created,
          //     };
          //   });
          //   // setTasks(tasks_arr);
          // }
        });
    } else {
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
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("REACT_TOKEN_AUTH_KEY");
    if (!token) {
      history.push(`/login`);
    }
    setToken(JSON.parse(token).access_token);

    if (task_id) {
      authFetch(`/api/prediction/${parseInt(task_id)}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status === 400) {
            // setMessage("Sorry you aren't authorized!");
            history.push(`/`);
            return null;
          } else if (response.status === 200) {
            // model already exists
            setSubText("Model loaded !!!");
            setIsClassificationModelLoaded(true);
          } else {
            setSubText("Model is downloading... !!!");
          }
          return response.json();
        })
        .then((response) => {
          if (response) {
            console.log(response);
          }

          // if (response && response.tasks) {
          //   let tasks_arr = response.tasks.map((item) => {
          //     return {
          //       id: item.id,
          //       name: item.name,
          //       description: item.name,
          //       model: item.model_path,
          //       progress: item.progress,
          //       accuracy: item["meta_data.accuracy"],
          //       error: item["meta_data.err"],
          //       created_at: item.date_created,
          //     };
          //   });

          //   // setTasks(tasks_arr);
          // }
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
            id="step-progress-wrapper"
            className="mt-5"
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div style={{ display: "flex" }}>
              <FormInput
                onChange={handleTextChange}
                value={text}
                placeholder="Enter text to classify"
              />
              <Button
                onClick={onSubmitPredict}
                style={{ width: "20rem" }}
                className="ml-3"
              >
                Predict
              </Button>
            </div>

            <p className="mt-3">{subText}</p>
            <h5 className="mt-5">Predicted class: {prediction}</h5>
          </div>
        </>
      ) : null}
    </>
  );
}
