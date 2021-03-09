import React, { useEffect, useState } from "react";
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

export default function Home() {
  const [logged] = useAuth();
  const [files, setFiles] = useState([]);
  const [pond, setPond] = useState();
  const [task_id, setTask_id] = useState();
  const [token, setToken] = useState("");

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [filePath, setFilePath] = useState("");
  const [columnNames, setColumnNames] = useState([]);
  const [textColumnDropdown, setTextColumnDropdown] = useState(false);
  const [labelColumnDropdown, setLabelColumnDropdown] = useState(false);
  const [textColumnName, setTextColumnName] = useState("");
  const [labelColumnName, setLabelColumnName] = useState("");
  const [continuous_train, setContinuous_train] = useState(true);
  const [
    isOpenContinousTrainTooltip,
    setIsOpenContinousTrainTooltip,
  ] = useState(false);

  const history = useHistory();

  const handleInit = () => {
    console.log("FilePond instance has initialised", pond);
  };

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const toggleTextColumn = (nr) => {
    setTextColumnDropdown(!textColumnDropdown);
  };

  const toggleLabelColumn = (nr) => {
    setLabelColumnDropdown(!labelColumnDropdown);
  };

  const handleTextColumnName = (e) => {
    e.preventDefault();
    setTextColumnName(e.target.textContent);
  };

  const handleLabelColumnName = (e) => {
    e.preventDefault();
    setLabelColumnName(e.target.textContent);
  };

  const toggleContinousTrain = (e) => {
    e.preventDefault();
    setContinuous_train(!continuous_train);
  };

  const toggleContinousTrainTooltip = (e) => {
    setIsOpenContinousTrainTooltip(!isOpenContinousTrainTooltip);
  };

  const onSubmitExecute = (e) => {
    if (
      title &&
      description &&
      filePath &&
      textColumnName &&
      labelColumnName &&
      continuous_train
    ) {
      let req_body = {
        name: title,
        description: description,
        ds_path: filePath,
        ds_text_col: textColumnName,
        ds_label_col: labelColumnName,
        continuous_train: continuous_train,
      };
      authFetch(`/api/task/initiate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(req_body),
      })
        .then((response) => {
          if (response.status === 401) {
            // setMessage("Sorry you aren't authorized!");
            return null;
          } else if (response.status === 400) {
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
            let meta_data = response.meta_data;
            console.log(meta_data);
            history.push(`/task/${task_id}`);
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
    setTask_id(1);
    const token = localStorage.getItem("REACT_TOKEN_AUTH_KEY");
    if (!token) {
      history.push(`/login`);
    }
    setToken(JSON.parse(token).access_token);
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
            <h4
              className="mb-5"
              style={{
                fontWeight: "500",
              }}
            >
              Import Text Data
            </h4>
            <div className="csv-uploader">
              <FormInput
                onChange={handleTitleChange}
                value={title}
                placeholder="Title"
                className="mb-3"
              />
              <FormTextarea
                onChange={handleDescriptionChange}
                value={description}
                placeholder="Description"
                className="mb-3"
              />

              <FilePond
                ref={(ref) => setPond(ref)}
                acceptedFileTypes={[
                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                  "application/vnd.ms-excel",
                  "text/x-csv",
                  "application/csv",
                  "text/csv",
                ]}
                files={files}
                allowMultiple={false}
                labelFileTypeNotAllowed="Only .csv files allowed."
                server={{
                  url: `/api/task/upload`,
                  process: {
                    headers: {
                      Authorization: `Bearer ${token}`,
                    },
                    onload: (response) => {
                      setFilePath(JSON.parse(response).file_path);
                      setColumnNames(JSON.parse(response).column_names);
                    },
                  },
                }}
                oninit={() => handleInit()}
                onupdatefiles={(fileItems) => {
                  console.log(fileItems[0]?.filename);
                  setFiles(fileItems.map((fileItem) => fileItem.file));
                }}
                labelIdle='Drag and drop the csv or <span class="filepond--label-action">Browse</span>'
              ></FilePond>

              {columnNames?.length > 0 ? (
                <Container>
                  <Row>
                    <Col>
                      <h6
                        className="mr-md-4 mr-sm-1"
                        style={{
                          alignSelf: "center",
                          fontWeight: "400",
                        }}
                      >
                        Text Column
                      </h6>
                      <Dropdown
                        className="dataset-col-dropdown"
                        outline
                        theme="success"
                        open={textColumnDropdown}
                        toggle={() => toggleTextColumn(2)}
                      >
                        <DropdownToggle caret outline theme="secondary">
                          {textColumnName || "None"}
                        </DropdownToggle>
                        <DropdownMenu>
                          {columnNames.map((item, i) => (
                            <>
                              <DropdownItem
                                key={i}
                                onClick={handleTextColumnName}
                              >
                                {item}
                              </DropdownItem>
                            </>
                          ))}
                        </DropdownMenu>
                      </Dropdown>
                    </Col>
                    <Col>
                      <h6
                        className="mr-md-4 mr-sm-1"
                        style={{
                          alignSelf: "center",
                          fontWeight: "400",
                        }}
                      >
                        Label Column
                      </h6>
                      <Dropdown
                        className="dataset-col-dropdown"
                        outline
                        theme="success"
                        open={labelColumnDropdown}
                        toggle={() => toggleLabelColumn(2)}
                      >
                        <DropdownToggle caret outline theme="secondary">
                          {labelColumnName || "None"}
                        </DropdownToggle>
                        <DropdownMenu>
                          {columnNames.map((item) => (
                            <>
                              <DropdownItem onClick={handleLabelColumnName}>
                                {item}
                              </DropdownItem>
                            </>
                          ))}
                        </DropdownMenu>
                      </Dropdown>
                    </Col>
                  </Row>
                </Container>
              ) : null}
            </div>
            <div className="mt-4" style={{ display: "flex" }}>
              <FormCheckbox
                checked={continuous_train}
                onChange={(e) => toggleContinousTrain(e)}
              >
                Help us to improve AdaptText ?
              </FormCheckbox>
              <svg
                id="continousTrainTooltip"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-info-circle-fill"
                viewBox="0 0 16 16"
                style={{ marginTop: "2px", marginLeft: "6px" }}
              >
                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412l-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z" />
              </svg>
            </div>
            <Tooltip
              open={isOpenContinousTrainTooltip}
              target="#continousTrainTooltip"
              toggle={toggleContinousTrainTooltip}
            >
              By ticking, Your data would be used to optimize the algorithm
            </Tooltip>
            <Button
              onClick={onSubmitExecute}
              style={{ width: "20rem" }}
              className="mt-5"
            >
              Execute
            </Button>
          </div>
        </>
      ) : null}
    </>
  );
}
