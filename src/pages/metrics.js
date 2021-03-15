import React, { useEffect, useState } from "react";
import { Button, Container, Progress, Row, Col } from "shards-react";
import { useRouteMatch } from "react-router-dom";
import { useHistory } from "react-router-dom";
import { ResponsivePie } from "@nivo/pie";
import { ResponsiveHeatMap } from "@nivo/heatmap";
import { authFetch, useAuth } from "../auth";
import NavigationBar from "../components/navbar";

export default function Metrics() {
  const [logged] = useAuth();
  const history = useHistory();
  let task_obj = useRouteMatch("/task/metrics/:id");
  let task_id = task_obj?.params?.id;
  const [task, setTask] = useState();
  const [accuracy, setAccuracy] = useState([]);
  const [confusionMatrix, setConfusionMatrix] = useState([]);
  const [rocImage, setRocImage] = useState("");
  let data = [
    {
      id: "elixir",
      label: "elixir",
      value: 552,
      color: "hsl(169, 70%, 50%)",
    },
    {
      id: "haskell",
      label: "haskell",
      value: 572,
      color: "hsl(297, 70%, 50%)",
    },
    {
      id: "javascript",
      label: "javascript",
      value: 490,
      color: "hsl(193, 70%, 50%)",
    },
    {
      id: "php",
      label: "php",
      value: 365,
      color: "hsl(317, 70%, 50%)",
    },
    {
      id: "hack",
      label: "hack",
      value: 547,
      color: "hsl(186, 70%, 50%)",
    },
  ];

  let confusionMatrix1 = [
    {
      actual: "AD",
      "hot dog": 8,
      "hot dogColor": "hsl(110, 70%, 50%)",
      burger: 54,
      burgerColor: "hsl(118, 70%, 50%)",
      sandwich: 63,
      sandwichColor: "hsl(251, 70%, 50%)",
      kebab: 7,
      kebabColor: "hsl(114, 70%, 50%)",
      fries: 11,
      friesColor: "hsl(203, 70%, 50%)",
      donut: 97,
      donutColor: "hsl(165, 70%, 50%)",
      junk: 73,
      junkColor: "hsl(354, 70%, 50%)",
      sushi: 33,
      sushiColor: "hsl(359, 70%, 50%)",
      ramen: 70,
      ramenColor: "hsl(195, 70%, 50%)",
      curry: 51,
      curryColor: "hsl(304, 70%, 50%)",
      udon: 29,
      udonColor: "hsl(196, 70%, 50%)",
    },
    {
      actual: "AE",
      "hot dog": 92,
      "hot dogColor": "hsl(220, 70%, 50%)",
      burger: 77,
      burgerColor: "hsl(160, 70%, 50%)",
      sandwich: 21,
      sandwichColor: "hsl(157, 70%, 50%)",
      kebab: 60,
      kebabColor: "hsl(255, 70%, 50%)",
      fries: 69,
      friesColor: "hsl(164, 70%, 50%)",
      donut: 97,
      donutColor: "hsl(206, 70%, 50%)",
      junk: 57,
      junkColor: "hsl(296, 70%, 50%)",
      sushi: 100,
      sushiColor: "hsl(327, 70%, 50%)",
      ramen: 51,
      ramenColor: "hsl(194, 70%, 50%)",
      curry: 71,
      curryColor: "hsl(194, 70%, 50%)",
      udon: 65,
      udonColor: "hsl(199, 70%, 50%)",
    },
    {
      actual: "AF",
      "hot dog": 97,
      "hot dogColor": "hsl(119, 70%, 50%)",
      burger: 43,
      burgerColor: "hsl(269, 70%, 50%)",
      sandwich: 72,
      sandwichColor: "hsl(322, 70%, 50%)",
      kebab: 2,
      kebabColor: "hsl(136, 70%, 50%)",
      fries: 26,
      friesColor: "hsl(201, 70%, 50%)",
      donut: 71,
      donutColor: "hsl(144, 70%, 50%)",
      junk: 16,
      junkColor: "hsl(317, 70%, 50%)",
      sushi: 94,
      sushiColor: "hsl(155, 70%, 50%)",
      ramen: 82,
      ramenColor: "hsl(328, 70%, 50%)",
      curry: 48,
      curryColor: "hsl(152, 70%, 50%)",
      udon: 32,
      udonColor: "hsl(39, 70%, 50%)",
    },
    {
      actual: "AG",
      "hot dog": 99,
      "hot dogColor": "hsl(338, 70%, 50%)",
      burger: 89,
      burgerColor: "hsl(81, 70%, 50%)",
      sandwich: 44,
      sandwichColor: "hsl(256, 70%, 50%)",
      kebab: 78,
      kebabColor: "hsl(201, 70%, 50%)",
      fries: 79,
      friesColor: "hsl(246, 70%, 50%)",
      donut: 34,
      donutColor: "hsl(17, 70%, 50%)",
      junk: 0,
      junkColor: "hsl(72, 70%, 50%)",
      sushi: 26,
      sushiColor: "hsl(150, 70%, 50%)",
      ramen: 45,
      ramenColor: "hsl(105, 70%, 50%)",
      curry: 20,
      curryColor: "hsl(14, 70%, 50%)",
      udon: 81,
      udonColor: "hsl(291, 70%, 50%)",
    },
    {
      actual: "AI",
      "hot dog": 14,
      "hot dogColor": "hsl(83, 70%, 50%)",
      burger: 74,
      burgerColor: "hsl(265, 70%, 50%)",
      sandwich: 31,
      sandwichColor: "hsl(216, 70%, 50%)",
      kebab: 37,
      kebabColor: "hsl(175, 70%, 50%)",
      fries: 90,
      friesColor: "hsl(132, 70%, 50%)",
      donut: 77,
      donutColor: "hsl(322, 70%, 50%)",
      junk: 48,
      junkColor: "hsl(53, 70%, 50%)",
      sushi: 97,
      sushiColor: "hsl(233, 70%, 50%)",
      ramen: 78,
      ramenColor: "hsl(5, 70%, 50%)",
      curry: 4,
      curryColor: "hsl(181, 70%, 50%)",
      udon: 81,
      udonColor: "hsl(213, 70%, 50%)",
    },
    {
      actual: "AL",
      "hot dog": 34,
      "hot dogColor": "hsl(206, 70%, 50%)",
      burger: 32,
      burgerColor: "hsl(206, 70%, 50%)",
      sandwich: 77,
      sandwichColor: "hsl(280, 70%, 50%)",
      kebab: 47,
      kebabColor: "hsl(138, 70%, 50%)",
      fries: 1,
      friesColor: "hsl(188, 70%, 50%)",
      donut: 37,
      donutColor: "hsl(223, 70%, 50%)",
      junk: 76,
      junkColor: "hsl(191, 70%, 50%)",
      sushi: 9,
      sushiColor: "hsl(118, 70%, 50%)",
      ramen: 50,
      ramenColor: "hsl(305, 70%, 50%)",
      curry: 25,
      curryColor: "hsl(42, 70%, 50%)",
      udon: 2,
      udonColor: "hsl(357, 70%, 50%)",
    },
    {
      actual: "AM",
      "hot dog": 45,
      "hot dogColor": "hsl(353, 70%, 50%)",
      burger: 100,
      burgerColor: "hsl(199, 70%, 50%)",
      sandwich: 15,
      sandwichColor: "hsl(65, 70%, 50%)",
      kebab: 55,
      kebabColor: "hsl(80, 70%, 50%)",
      fries: 57,
      friesColor: "hsl(204, 70%, 50%)",
      donut: 67,
      donutColor: "hsl(186, 70%, 50%)",
      junk: 91,
      junkColor: "hsl(210, 70%, 50%)",
      sushi: 54,
      sushiColor: "hsl(48, 70%, 50%)",
      ramen: 12,
      ramenColor: "hsl(144, 70%, 50%)",
      curry: 30,
      curryColor: "hsl(76, 70%, 50%)",
      udon: 77,
      udonColor: "hsl(156, 70%, 50%)",
    },
    {
      actual: "AO",
      "hot dog": 66,
      "hot dogColor": "hsl(149, 70%, 50%)",
      burger: 96,
      burgerColor: "hsl(105, 70%, 50%)",
      sandwich: 81,
      sandwichColor: "hsl(337, 70%, 50%)",
      kebab: 39,
      kebabColor: "hsl(338, 70%, 50%)",
      fries: 5,
      friesColor: "hsl(203, 70%, 50%)",
      donut: 66,
      donutColor: "hsl(284, 70%, 50%)",
      junk: 86,
      junkColor: "hsl(78, 70%, 50%)",
      sushi: 34,
      sushiColor: "hsl(72, 70%, 50%)",
      ramen: 52,
      ramenColor: "hsl(189, 70%, 50%)",
      curry: 22,
      curryColor: "hsl(105, 70%, 50%)",
      udon: 97,
      udonColor: "hsl(155, 70%, 50%)",
    },
    {
      actual: "AQ",
      "hot dog": 11,
      "hot dogColor": "hsl(182, 70%, 50%)",
      burger: 69,
      burgerColor: "hsl(208, 70%, 50%)",
      sandwich: 39,
      sandwichColor: "hsl(312, 70%, 50%)",
      kebab: 14,
      kebabColor: "hsl(192, 70%, 50%)",
      fries: 46,
      friesColor: "hsl(283, 70%, 50%)",
      donut: 27,
      donutColor: "hsl(356, 70%, 50%)",
      junk: 93,
      junkColor: "hsl(264, 70%, 50%)",
      sushi: 23,
      sushiColor: "hsl(136, 70%, 50%)",
      ramen: 99,
      ramenColor: "hsl(194, 70%, 50%)",
      curry: 4,
      curryColor: "hsl(137, 70%, 50%)",
      udon: 41,
      udonColor: "hsl(36, 70%, 50%)",
    },
  ];

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
            setTask(response?.task);

            let conf_matrix = response?.task["meta_data.conf_matrix"];

            console.log("---------------------");
            // console.log(conf_matrix)
            console.log(confusionMatrix1);

            let classes = ["one", "two", "three"];

            let zzz = conf_matrix.map((row, index) => {
              let y = row.map((i, idx) => {
                // let keyname = classes[idx]
                return { [classes[idx]]: i };
              });

              // console.log(y)

              return {
                actual: classes[index],
                ...y,
                // "hot dog": 11,
                // "hot dogColor": "hsl(182, 70%, 50%)",
                // burger: 69,
              };
            });

            console.log(zzz);
            setConfusionMatrix(zzz);

            // },
            // {
            //   actual: "AQ",
            //   "hot dog": 11,
            //   "hot dogColor": "hsl(182, 70%, 50%)",
            //   burger: 69,

            let accuracy_pie_data = [
              {
                id: "Accuracy",
                label: "accuracy",
                value:
                  Math.round(response?.task["meta_data.accuracy"] * 100 * 100) /
                  100,
                color: "hsl(169, 70%, 50%)",
                key: 1,
              },
              {
                // id: "rest",
                // label: "rest",
                value:
                  Math.round(
                    (100 - response?.task["meta_data.accuracy"] * 100) * 100
                  ) / 100,
                color: "hsl(0, 0%, 50%)",
                key: 2,
              },
            ];

            setAccuracy(accuracy_pie_data);

            // // set initial progress from db
            // if (response?.task?.progress !== 100) {
            //   history.push(`/tasks`);
            //   return;
            // }

            authFetch(`/api/plot_roc/${parseInt(task_id)}`, {
              headers: {
                "Content-Type": "application/json",
              },
            })
              .then((response) => {
                if (response.status === 400 || response.status === 404) {
                  history.push(`/`);
                  return null;
                }
                return response.blob();
              })
              .then((response) => {
                setRocImage();
                // console.log(JSON.parse(response))
                // let res_img = URL.createObjectURL(response);
                // console.log(res_img);
              });
            //
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
            }}
          >
            <h4 className="mb-4" style={{ fontWeight: "600" }}>
              Training CompleteZXd !!!
            </h4>
            <p className="mt-3 mb-5 ml-4" style={{ fontWeight: "400" }}>
              Tkjlkjljlhis process will take several minutes based on the
              dataset you have provided.
            </p>

            <Container>
              <Row>
                <Col style={{ height: "24rem" }}>
                  <ResponsiveHeatMap
                    data={confusionMatrix1}
                    keys={[
                      "hot dog",
                      "burger",
                      "sandwich",
                      "kebab",
                      "fries",
                      "donut",
                      "junk",
                      "sushi",
                      "ramen",
                      "curry",
                      "udon",
                    ]}
                    height="400"
                    indexBy="actual"
                    margin={{ top: -30, right: 60, bottom: 60, left: 60 }}
                    forceSquare={true}
                    colors="oranges"
                    axisTop={null}
                    axisRight={null}
                    axisBottom={{
                      orient: "bottom",
                      tickSize: 5,
                      tickPadding: 5,
                      tickRotation: -90,
                      legend: "Predicted",
                      legendPosition: "middle",
                      legendOffset: 54,
                    }}
                    axisLeft={{
                      orient: "left",
                      tickSize: 5,
                      tickPadding: 5,
                      tickRotation: 0,
                      legend: "actual",
                      legendPosition: "middle",
                      legendOffset: -40,
                    }}
                    cellOpacity={1}
                    cellBorderColor={{
                      from: "color",
                      modifiers: [["darker", 0.4]],
                    }}
                    labelTextColor={{
                      from: "color",
                      modifiers: [["darker", 1.8]],
                    }}
                    defs={[
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(0, 0, 0, 0.1)",
                        rotation: -45,
                        lineWidth: 4,
                        spacing: 7,
                      },
                    ]}
                    fill={[{ id: "lines" }]}
                    animate={true}
                    motionConfig="default"
                    motionStiffness={80}
                    motionDamping={9}
                    hoverTarget="cell"
                    cellHoverOthersOpacity={0.25}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                      transform: "translateY(-2rem)",
                    }}
                  >
                    Confusion Matrix
                  </h6>
                </Col>
                <Col style={{ height: "14rem" }}>
                  {/* <ResponsivePie
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
                    legends={[]}
                  /> */}
                  <img
                    style={{ width: "20rem", height: "auto" }}
                    src={`/api/plot_roc/${parseInt(task_id)}`}
                  />
                  <h6
                    style={{
                      textAlign: "center",
                    }}
                  >
                    ROC Curve
                  </h6>
                </Col>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={accuracy}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
              </Row>
              <hr />
              {/*  */}
              <Row>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
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
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
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

                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
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
              </Row>

              <Row>
                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
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
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
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

                <Col style={{ height: "14rem" }}>
                  <ResponsivePie
                    data={data}
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    startAngle={-90}
                    endAngle={90}
                    innerRadius={0.5}
                    padAngle={0.7}
                    cornerRadius={3}
                    colors={{ scheme: "nivo" }}
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
                    defs={[
                      {
                        id: "dots",
                        type: "patternDots",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        size: 4,
                        padding: 1,
                        stagger: true,
                      },
                      {
                        id: "lines",
                        type: "patternLines",
                        background: "inherit",
                        color: "rgba(255, 255, 255, 0.3)",
                        rotation: -45,
                        lineWidth: 6,
                        spacing: 10,
                      },
                    ]}
                    fill={[
                      {
                        match: {
                          id: "ruby",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "c",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "go",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "python",
                        },
                        id: "dots",
                      },
                      {
                        match: {
                          id: "scala",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "lisp",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "elixir",
                        },
                        id: "lines",
                      },
                      {
                        match: {
                          id: "javascript",
                        },
                        id: "lines",
                      },
                    ]}
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
              </Row>
            </Container>
          </div>
        </>
      ) : null}
    </>
  );
}
