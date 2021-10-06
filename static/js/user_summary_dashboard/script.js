var chart;
var daysName = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thrusday",
  "Friday",
  "Saturday",
];

var monthsName = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];
// Activities
// total time spent monthly
var barData = {
  labels: [],
  datasets: [
    {
      label: "",
      backgroundColor: "rgba(26,179,148,0.5)",
      borderColor: "rgba(26,179,148,0.7)",
      pointBackgroundColor: "rgba(26,179,148,1)",
      pointBorderColor: "#fff",
      data: [],
    },
  ],
};

var barOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    yAxes: [{
      ticks: {
        min: 0, // it is for ignoring negative step.
        beginAtZero: true,
        callback: function(value, index, values) {
            if (Math.floor(value) === value) {
                return value;
            }
        }
    }
      }
    ]
  }
};
var dataStores;

var ctx2 = document.getElementById("barChart").getContext("2d");

// docuement ready
$(function () {
  ajexPost();
});

function ajexPost() {
  var settings = {
    url: "http://54.153.85.99/api/stats/users_summary",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/json",
    },
  };

  $.ajax(settings).done(function (response) {
    if (response) {
      dataStores = response;
      $("#total").text(dataStores.Total)
      filterData(dataStores.Weekly, "week").then((result) => {
        barData.labels = result.label;
        barData.datasets[0].label = "Weekly";
        barData.datasets[0].data = result.data;
        barChart(ctx2, barData, barOptions);
        $(".spinner-div").hide();
      });
    }
  });
}

$("#selectButton > .btn").on("click", function () {
  chart.destroy();
  $(".spinner-div").show();
  $(".cs-select-btn > .btn").removeClass("active");
  $(this).addClass("active");

  switch ($(this).data("id")) {
    case "week":
      filterData(dataStores.Weekly, "week").then((result) => {
        barData.labels = result.label;
        barData.datasets[0].label = "Weekly";
        barData.datasets[0].data = result.data;
        barChart(ctx2, barData, barOptions);
        $(".spinner-div").hide();
      });
      break;
    case "month":
      filterData(dataStores.Monthly, "month").then((result) => {
        barData.labels = result.label;
        barData.datasets[0].label = "Monthly";
        barData.datasets[0].data = result.data;
        barChart(ctx2, barData, barOptions);
        $(".spinner-div").hide();

      });
      break;
    case "year":
      filterData(dataStores.Yearly, "year").then((result) => {
        barData.labels = result.label;
        barData.datasets[0].label = "Yearly";
        barData.datasets[0].data = result.data;
        barChart(ctx2, barData, barOptions);
        $(".spinner-div").hide();
      });
      break;
    case "all":
      filterData(dataStores.all, 'all').then((result) => {
        barData.labels = result.label;
        barData.datasets[0].label = "All";
        barData.datasets[0].data = result.data;
        barChart(ctx2, barData, barOptions);
        $(".spinner-div").hide();
      });
      break;
  }
});

function filterData(data, checkLevel) {
  let dataSet = [];
  let labelSet = [];
  return new Promise((resolve) => {
    data.forEach((value) => {
      dataSet.push(value.count);
      switch (checkLevel) {
        case "week":
          tempDate = new Date(value.date)
          labelSet.push(tempDate.getDate() + ' ' + monthsName[tempDate.getMonth()]);
          break;
        case "month":
          tempDate = new Date(value.date)
          labelSet.push(tempDate.getDate() + ' ' + monthsName[tempDate.getMonth()]);
          break;
        case "year":
          tempDate = new Date(value.date)
          labelSet.push(monthsName[tempDate.getMonth()] + ' ' + tempDate.getFullYear());
          break;
        case "all":
          labelSet.push(value.date);
          break;
      }
    });
    resolve({
      label: labelSet,
      data: dataSet,
    });
  });
}

function barChart(chartId, barData, barOptions) {
  chart = new Chart(chartId, {
    type: "bar",
    data: barData,
    options: barOptions,
  });
}

function toTitleCase(str) {
  if (str) {
    return str
      .toLowerCase()
      .split(" ")
      .map(function (word) {
        return word.charAt(0).toUpperCase() + word.slice(1);
      })
      .join(" ");
  }
}
