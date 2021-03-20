import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "shards-react";
import { useRouteMatch } from "react-router-dom";
import { useHistory } from "react-router-dom";
import { ResponsivePie } from "@nivo/pie";
import { authFetch, useAuth } from "../auth";
import NavigationBar from "../components/navbar";

export default function Metrics() {
  const [logged] = useAuth();
  const history = useHistory();
  let task_obj = useRouteMatch("/task/metrics/:id");
  let task_id = task_obj?.params?.id;
  const [task, setTask] = useState();
  const [errorRate, setErrorRate] = useState([]);
  const [accuracy, setAccuracy] = useState([]);
  const [f1Score, setF1Score] = useState([]);
  const [precision, setPrecision] = useState([]);
  const [recall, setRecall] = useState([]);
  const [matthewsCorr, setMatthewsCorr] = useState(0);
  const [confusionMatrix, setConfusionMatrix] = useState("");
  const [rocImage, setRocImage] = useState("");

  useEffect(() => {
    if (task_id) {
      authFetch(`/api/task/${parseInt(task_id)}`, {
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status === 400 || response.status === 404) {
            history.push(`/tasks`);
            return null;
          }
          return response.json();
        })
        .then((response) => {
          if (response && response?.task) {
            let taskObj = response?.task;
            setTask(taskObj);

            setConfusionMatrix(taskObj["meta_data.conf_matrix"]);
            setRocImage(taskObj["meta_data.roc_curve"]);

            let accuracy_pie_data = [
              {
                id: "Accuracy",
                label: "accuracy",
                value:
                  Math.round(response?.task["meta_data.accuracy"] * 100 * 100) /
                  100,
                color: "#FF6B45",
                key: 1,
              },
              {
                // id: "rest",
                // label: "rest",
                value:
                  Math.round(
                    (100 - response?.task["meta_data.accuracy"] * 100) * 100
                  ) / 100,
                color: "#DDDDDD",
                key: 2,
              },
            ];

            setAccuracy(accuracy_pie_data);

            let error_pie_data = [
              {
                id: "Error Rate",
                label: "error-rate",
                value:
                  Math.round(response?.task["meta_data.err"] * 100 * 100) / 100,
                color: "#FF6B45",
                key: 1,
              },
              {
                // id: "rest",
                // label: "rest",
                value:
                  Math.round(
                    (100 - response?.task["meta_data.err"] * 100) * 100
                  ) / 100,
                color: "#DDDDDD",
                key: 2,
              },
            ];

            setErrorRate(error_pie_data);

            let f1_pie_data = [
              {
                id: "F1 Score",
                label: "f1-score",
                value:
                  Math.round(
                    response?.task["meta_data.weighted_f1"] * 100 * 100
                  ) / 100,
                color: "#FF6B45",
                key: 1,
              },
              {
                // id: "rest",
                // label: "rest",
                value:
                  Math.round(
                    (100 - response?.task["meta_data.weighted_f1"] * 100) * 100
                  ) / 100,
                color: "#DDDDDD",
                key: 2,
              },
            ];

            setF1Score(f1_pie_data);

            let precision_pie_data = [
              {
                id: "Precision",
                label: "precision",
                value:
                  Math.round(
                    response?.task["meta_data.weighted_precision"] * 100 * 100
                  ) / 100,
                color: "#FF6B45",
                key: 1,
              },
              {
                // id: "rest",
                // label: "rest",
                value:
                  Math.round(
                    (100 -
                      response?.task["meta_data.weighted_precision"] * 100) *
                      100
                  ) / 100,
                color: "#DDDDDD",
                key: 2,
              },
            ];

            setPrecision(precision_pie_data);

            let recall_pie_data = [
              {
                id: "Recall",
                label: "recall",
                value:
                  Math.round(
                    response?.task["meta_data.weighted_recall"] * 100 * 100
                  ) / 100,
                color: "#FF6B45",
                key: 1,
              },
              {
                // id: "rest",
                // label: "rest",
                value:
                  Math.round(
                    (100 - response?.task["meta_data.weighted_recall"] * 100) *
                      100
                  ) / 100,
                color: "#DDDDDD",
                key: 2,
              },
            ];

            setRecall(recall_pie_data);

            setMatthewsCorr(
              (response?.task["meta_data.matthews_corr_coef"]).toFixed(3)
            );
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
            }}
          >
            <h4 className="mb-5 mt-5" style={{ fontWeight: "600" }}>
              Evaluation Metrics
            </h4>

            <Container>
              <Row>
                <Col style={{ height: "24rem" }}>
                  <img
                    style={{ width: "20rem", height: "auto" }}
                    src={confusionMatrix}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      marginTop: "2rem",
                    }}
                  >
                    Confusion Matrix
                  </h6>
                </Col>
                <Col style={{ height: "14rem" }}>
                  <img
                    style={{ width: "20rem", height: "auto" }}
                    src={rocImage}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      marginTop: "2rem",
                    }}
                  >
                    ROC Curve
                  </h6>
                </Col>
                <Col style={{ height: "14rem" }}>
                  <h3 className="mt-5 mb-5 text-center">{matthewsCorr}</h3>
                  <h6 className="text-center" style={{ marginTop: "11.5rem" }}>
                    Matthews Correlation Coefficient
                  </h6>
                </Col>
              </Row>
              <hr />

              <Row>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={accuracy}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={(d) => d?.data?.color}
                    borderWidth={1}
                    borderColor={{
                      from: "color",
                      modifiers: [["darker", 0.2]],
                    }}
                    enableRadialLabels={false}
                    radialLabelsSkipAngle={10}
                    radialLabelsTextColor="#333333"
                    radialLabelsLinkColor={{ from: "color" }}
                    sliceLabelsSkipAngle={10}
                    sliceLabelsTextColor="#333333"
                    legends={[]}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      transform: "translateY(-2rem)",
                    }}
                  >
                    Accuracy
                  </h6>
                </Col>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={precision}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={(d) => d?.data?.color}
                    borderWidth={1}
                    borderColor={{
                      from: "color",
                      modifiers: [["darker", 0.2]],
                    }}
                    enableRadialLabels={false}
                    radialLabelsSkipAngle={10}
                    radialLabelsTextColor="#333333"
                    radialLabelsLinkColor={{ from: "color" }}
                    sliceLabelsSkipAngle={10}
                    sliceLabelsTextColor="#333333"
                    legends={[]}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      transform: "translateY(-2rem)",
                    }}
                  >
                    Precision
                  </h6>
                </Col>

                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={recall}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={(d) => d?.data?.color}
                    borderWidth={1}
                    borderColor={{
                      from: "color",
                      modifiers: [["darker", 0.2]],
                    }}
                    enableRadialLabels={false}
                    radialLabelsSkipAngle={10}
                    radialLabelsTextColor="#333333"
                    radialLabelsLinkColor={{ from: "color" }}
                    sliceLabelsSkipAngle={10}
                    sliceLabelsTextColor="#333333"
                    legends={[]}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      transform: "translateY(-2rem)",
                    }}
                  >
                    Recall
                  </h6>
                </Col>
              </Row>

              <Row>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={f1Score}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={(d) => d?.data?.color}
                    borderWidth={1}
                    borderColor={{
                      from: "color",
                      modifiers: [["darker", 0.2]],
                    }}
                    enableRadialLabels={false}
                    radialLabelsSkipAngle={10}
                    radialLabelsTextColor="#333333"
                    radialLabelsLinkColor={{ from: "color" }}
                    sliceLabelsSkipAngle={10}
                    sliceLabelsTextColor="#333333"
                    legends={[]}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      transform: "translateY(-2rem)",
                    }}
                  >
                    F1 Score
                  </h6>
                </Col>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={errorRate}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={(d) => d?.data?.color}
                    borderWidth={1}
                    borderColor={{
                      from: "color",
                      modifiers: [["darker", 0.2]],
                    }}
                    enableRadialLabels={false}
                    radialLabelsSkipAngle={10}
                    radialLabelsTextColor="#333333"
                    radialLabelsLinkColor={{ from: "color" }}
                    sliceLabelsSkipAngle={10}
                    sliceLabelsTextColor="#333333"
                    legends={[]}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      transform: "translateY(-2rem)",
                    }}
                  >
                    Error Rate
                  </h6>
                </Col>

                <Col style={{ height: "14rem" }}></Col>
              </Row>
            </Container>
          </div>
        </>
      ) : null}
    </>
  );
}
