<!-- Chart -->

  const ctxL = document.getElementById("line-chart").getContext("2d");
const gradientFill = ctxL.createLinearGradient(0, 0, 0, 290);
gradientFill.addColorStop(0, "hsla(218, 71%, 35%, 1)");
gradientFill.addColorStop(1, "hsla(218, 41%, 35%, 0.2)");

const dataLine = {
  type: "line",
  data: {
    labels: [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday ",
    ],
    datasets: [
      {
        label: "Traffic",
        data: [2112, 2343, 2545, 3423, 2365, 1985, 987],
        backgroundColor: gradientFill,
      },
    ],
  },
};

const chartOptions = {
  options: {
    legend: {
      display: false,
    },
    scales: {
      yAxes: [
        {
          ticks: {
            fontColor: "hsl(0, 0%, 80%)",
          },
        },
      ],
      xAxes: [
        {
          ticks: {
            fontColor: "hsl(0, 0%, 80%)",
          },
        },
      ],
    },
  },
};

new mdb.Chart(
  document.getElementById("line-chart"),
  dataLine,
  chartOptions
);


<!-- Map -->

  const map = document.getElementById("my-map");

new VectorMap(map, {
  readonly: true,
  stroke: "hsl(0, 0%, 100%)",
  fill: "hsl(219, 87%, 89%)",
  hoverFill: "hsl(219, 87%, 20%)",
  colorMap: [
    { fill: "hsl(218, 71%, 45%)", regions: ["US"] },
    { fill: "hsl(218, 71%, 65%)", regions: ["RU", "AU"] },
    {
      fill: "hsl(218, 71%, 75%)",
      regions: [
        "PL",
        "DE",
        "FR",
        "GB",
        "ES",
        "IT",
        "SE",
        "NO",
        "CZ",
        "NL",
        "BE",
        "CN",
        "IN",
      ],
    },
  ],
});


<!-- Sidenav -->

  //Initialize it with JS to make it instantly visible

  const slimInstance = new mdb.Sidenav(
    document.getElementById("sidenav-4")
  );
slimInstance.show();

document.getElementById("slim-toggler").addEventListener("click", () => {
  slimInstance.toggleSlim();
});
