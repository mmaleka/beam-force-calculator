
var chartOptions = {
  scales: {
    xAxes: [{
            gridLines: {
                display:false
            },
            ticks: {
              beginAtZero: true,

              callback: function(value, index, values) {
                  if (Math.floor(value) === value) {
                      return value;
                  }
              }

            },
        }],

        yAxes: [{
          ticks: {
            beginAtZero: true,
          },
          gridLines: {
            display: false
          }
        }]
  }
};


function plotDiagrams() {

  var ctx = document.getElementById('shear_force_Chart').getContext('2d');
  var ctx_bending_moment = document.getElementById('bending_moment_Chart').getContext('2d');



  var data_x_list = document.getElementsByName("x_list")[0].value;
  var labels = JSON.parse(data_x_list);

  labels = labels.map(function(each_element){
      return Number(each_element.toFixed(3));
  });

  var data_shearForce = document.getElementsByName("V_shearQ")[0].value;
  var data_shearForce = JSON.parse(data_shearForce);

  data_shearForce = data_shearForce.map(function(each_element){
      return Number(each_element.toFixed(2));
  });



  var data_bendingMoment = document.getElementsByName("M_momentM")[0].value;
  var data_bendingMoment = JSON.parse(data_bendingMoment);

  var shear_forceData = [{
    label: 'Shear Force',
    data: data_shearForce,
    backgroundColor: "rgba(57,91,148,0.4)"
  }];


  var bending_momentData = [{
    label: 'Bending Moment',
    data: data_bendingMoment,
    backgroundColor: "rgba(57,91,148,0.4)"
  }];


  var shear_force_data = {
    labels: labels,
    datasets: data_shearForce,

  };

  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: shear_forceData
    },
    options: chartOptions,
  });


  var myChart_bendingMoment = new Chart(ctx_bending_moment, {
    type: 'line',
    data: {
      labels: labels,
      datasets: bending_momentData,
    },
    options: chartOptions,
  });

}


try {
  plotDiagrams();
} catch (e) {
  console.log("error plotting diagrams: ", e);
}





function remove_duplicates_es6(arr) {
    let s = new Set(arr);
    let it = s.values();
    return Array.from(it);
}
