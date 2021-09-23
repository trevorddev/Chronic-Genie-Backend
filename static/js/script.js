var tags1, tags2, tags3, tags4;

let query;
let info = {
  symptoms: {
    start: '',
    end: '',
  },
  daily: {
    start: '',
    end: '',
  },
};

var chart;

// Activities
var doughnutData = {
  labels: ["Total Count", "Filter Count"],
  datasets: [
    {
      data: [200, 300],
      backgroundColor: ["#23c6c8", "#a3e1d4"],
    },
  ],
};

var doughnutOptions = {
  responsive: false,
};

var ctx4 = document.getElementById("doughnutChart").getContext("2d");

// docuement ready
$(function () {
  tags1 = $("#tags1").magicSuggest({
    allowFreeEntries: true,
    data: ["Acquired Hemophilia", "Acute disseminated encephalomyelitis", "Scleritis"],
  });

  tags2 = $("#tags2").magicSuggest({
    allowFreeEntries: true,
    data: ["Abdominal Pain", "Dry Mouth", "Dry / Irritated Eyes", "Depression / Anxiety", "Musculoskeletal Pain", "Brain Fog / Headache", "Fatigue"],
  });

  tags3 = $("#tags3").magicSuggest({
    allowFreeEntries: true,
    data: ["Abdominal Pain", "Dry Mouth", "Dry / Irritated Eyes", "Depression / Anxiety", "Musculoskeletal Pain", "Brain Fog / Headache", "Fatigue"],
  });

  tags4 = $("#tags4").magicSuggest({
    allowFreeEntries: true,
    data: ["Imuran", "Plaquenil"],
  });

  $("#symptomstimes").daterangepicker(
    {
      timePicker: false,
      locale: {
        // format: "M/DD hh:mm A",
        format: "MM/DD/YYYY",
      },
    },
    function (start, end, label) {
      info.symptoms.start = start.format("YYYY-MM-DD");
      info.symptoms.end = end.format("YYYY-MM-DD");
    }
  );
  $("#dailytimes").daterangepicker(
    {
      timePicker: false,
      locale: {
        // format: "M/DD hh:mm A",
        format: "MM/DD/YYYY",
      },
    },
    function (start, end, label) {
      info.daily.start = start.format("YYYY-MM-DD");
      info.daily.end = end.format("YYYY-MM-DD");
    }
  );

  $(".dataTables_filter input").attr("placeholder", "Search here...").css({
    width: "300px",
    display: "inline-block",
  });

  $('#dailytimes, #symptomstimes').val('').attr("placeholder","Please Select Date");

  // call on load
  query = {
    info: info,
    medical: [],
    ssymptoms: [],
    rsymptoms: [],
    daily: [],
  };
  ajexPost(query);
});

function formSubmit() {
  let medical = $(".medical .ms-sel-ctn").find(".ms-sel-item").length;
  let ssymptoms = $(".ssymptoms .ms-sel-ctn").find(".ms-sel-item").length;
  let rsymptoms = $(".rsymptoms .ms-sel-ctn").find(".ms-sel-item").length;
  let daily = $(".daily .ms-sel-ctn").find(".ms-sel-item").length;

  $("#showResult").show();
  $(".spinner-div").css("display", "flex");
  $("#renderTable").html("");
  destroyDataTable();
  chart.destroy();

  query = {
    info: info,
    medical: medical,
    ssymptoms: ssymptoms,
    rsymptoms: rsymptoms,
    daily: daily,
  };
  ajexPost(query);
}

function ajexPost(body) {
  var settings = {
    url: "http://54.153.85.99/api/stats/customized_search",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/json",
    },
    data: JSON.stringify({
      page_number: 1,
      page_size: 10,
      filters: {
        medical_conditions: tags1.getValue(),
        selected_symptoms: tags2.getValue(),
        recorded_symptoms: {
          start_date: body.info.symptoms.start,
          end_date: body.info.symptoms.end,
          symptoms: tags3.getValue(),
        },
        daily_medications: {
          start_date: body.info.daily.start,
          end_date: body.info.daily.end,
          medicines: tags4.getValue(),
        },
      },
    }),
  };

  $.ajax(settings).done(function (response) {
    if (response) {
      let data = response.result;
      let html = `<table id="example" class="table table-hover responsive nowrap" style="width: 100%">
            <thead>
                <tr>
                    <th>Name & Email</th>
                    <th>DOB</th>
                    <th>Gender</th>
                    <th>Date of Join</th>
                    <th>Last Login</th>
                </tr>
            </thead>
            <tbody>`;
      if (response.result.length > 0) {
        data.map((data) => {
          html += `<tr>`;
          html += `<td>
                      <a href="#">
                          <div class="d-flex align-items-center">
                              <div class="avatar avatar-blue mr-3">${toTitleCase(
                                data.first_name[0]
                              )}</div>
                              <div>
                                  <p class="font-weight-bold mb-0">${toTitleCase(
                                    data.first_name
                                  )}</p>
                                  <p class="text-muted mb-0">${data.email}</p>
                              </div>
                          </div>
                      </a>
                  </td>`;
          html += `<td>${data.date_of_birth}</td>`;
          html += `<td>${toTitleCase(data.gender)}</td>`;
          html += `<td>${data.date_joined.split("T")[0]}</td>`;
          html += `<td>${data.last_login.split("T")[0]}</td>`;
          html += `</tr>`;
        });
      }

      html += `</tbody></table>`;
      $(".spinner-div").hide();
      $("#renderTable").html(html);
      var total = response.total_count;
      var filter = response.filter_count;
      if (total === filter ) {
        doughnutData.datasets = [
          {
            data: [total, 0],
            backgroundColor: ["#23c6c8", "#a3e1d4"],
          },
        ];
      } else {
        doughnutData.datasets = [
          {
            data: [total, filter],
            backgroundColor: ["#23c6c8", "#a3e1d4"],
          },
        ];
      }
      pieChart(ctx4, doughnutData, doughnutOptions);
      dataTableFunc();
      setTimeout(() => {
        toolTip();
      }, 100);
    }
  });
}

function pieChart(chartId, doughnutData, doughnutOptions) {
  chart = new Chart(chartId, {
    type: "doughnut",
    data: doughnutData,
    options: doughnutOptions,
  });
}

function dataTableFunc() {
  $("#example").DataTable({
    aaSorting: [],
    responsive: true,
    pageLength: 25,
    lengthMenu: [5, 25, 50, 75, 100],
    columnDefs: [
      {
        responsivePriority: 1,
        targets: 0,
      },
      {
        responsivePriority: 2,
        targets: -1,
      },
    ],
    language: {
      searchPlaceholder: "Search records",
    },
  });
}

function destroyDataTable() {
  $("#example").DataTable().destroy();
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

function toolTip() {
  $('[data-toggle="tooltip"]').tooltip();
}
