try {
  window.onload = function () {
    drawBeam()
  };
} catch (e) {
  console.log(e);
}



function drawBeam() {
  var canvas = document.getElementById('paper');
  if (canvas.getContext) {
    var ctx = canvas.getContext('2d');

    var beam_length = document.getElementsByName("draw_beam_length")[0].value;
    ctx.fillRect(0, 0, ctx.width, ctx.height);
    ctx.fillStyle = "#3b73c7";
    ctx.fillRect(50, 150, 400, 10);
    // c.fillRect(x, y, widgth, height)

    try {
      var beam_point_load = document.getElementsByName("draw_beam_pointLoad");
      var beam_point_load_distance = document.getElementsByName("draw_beam_pointLoad_distance");
      console.log(beam_point_load.length);
      for (var i = 0; i < beam_point_load.length; i++) {
        pointLoad(ctx, beam_point_load[i].value, beam_point_load_distance[i].value, beam_length);
      }
    } catch (e) {
      console.log(e);
    }

    try {
      var beam_moment_load = document.getElementsByName("draw_beam_momentLoad");
      var beam_moment_load_distance = document.getElementsByName("draw_beam_momentLoad_distance");
      console.log(beam_moment_load.length);
      for (var i = 0; i < beam_moment_load.length; i++) {
        momentLoad(ctx, beam_moment_load[i].value, beam_moment_load_distance[i].value, beam_length);
      }
    } catch (e) {
      console.log(e);
    }

    try {
      var beam_distributed_load_start = document.getElementsByName("draw_beam_distributedLoad_start");
      var beam_distributed_load_distance_start = document.getElementsByName("draw_beam_distributedLoad_distance_start");
      var beam_distributed_load_end = document.getElementsByName("draw_beam_distributedLoad_end");
      var beam_distributed_load_distance_end = document.getElementsByName("draw_beam_distributedLoad_distance_end");

      console.log(beam_distributed_load_start.length);

      for (var i = 0; i < beam_distributed_load_start.length; i++) {
        distributedLoad(ctx, beam_distributed_load_start[i].value, beam_distributed_load_distance_start[i].value,
          beam_distributed_load_end[i].value, beam_distributed_load_distance_end[i].value, beam_length);
      }
    } catch (e) {
      console.log(e);
    }

    try {
      var beam_supprt = document.getElementsByName("draw_beam_support");
      var supprt_type1 = beam_supprt[0].value;
      var beam_supprt_distance1 = document.getElementsByName("draw_beam_support_distance");
      var beam_supprt_distance1 = beam_supprt_distance1[0].value;

      if (supprt_type1 == 'PIN SUPPORT' || supprt_type1 == 'ROLLER SUPPORT') {
        pin_support(ctx, supprt_type1, beam_supprt_distance1, beam_length);
      } else {
        fixed_support(ctx, supprt_type1, beam_supprt_distance1, beam_length);
      }


    } catch (e) {
      console.log(e);
    };


    try {

      var beam_supprt = document.getElementsByName("draw_beam_support");
      var supprt_type2 = beam_supprt[1].value;
      var beam_supprt_distance2 = document.getElementsByName("draw_beam_support_distance");
      var beam_supprt_distance2 = beam_supprt_distance2[1].value;

      if (supprt_type2 == 'PIN SUPPORT' || supprt_type2 == 'ROLLER SUPPORT') {
        pin_support(ctx, supprt_type2, beam_supprt_distance2, beam_length);
      } else {
        fixed_support(ctx, supprt_type2, beam_supprt_distance2, beam_length);
      }

    } catch (e) {
      console.log(e);
    };




  }
}


function pointLoad(ctx, point_load, point_load_distance, beam_length) {

  if (point_load_distance > 0) {
    point_load_distance = 45 + point_load_distance*400/beam_length
  } else {
    point_load_distance = point_load_distance
  }

  console.log("point load_distance: ", point_load_distance);

  ctx.beginPath();
  ctx.lineWidth = 2;
  ctx.strokeStyle = "red";
  ctx.fillStyle = "red";
  ctx.font = "15px Helvetica";
  ctx.fillText(point_load, point_load_distance, 95);
  if (point_load > 0) {
    canvas_arrow(ctx, point_load_distance, 150, point_load_distance, 100);
  } else {
    canvas_arrow(ctx, point_load_distance, 100, point_load_distance, 150);
  }
}





function momentLoad(ctx, moment_load, moment_load_distance, beam_length) {
  console.log("moment_load_distance: ", moment_load_distance);

  if (moment_load_distance > 0) {
    moment_load_distance = 45 + moment_load_distance*400/beam_length
  } else {
    moment_load_distance = moment_load_distance
  }

  console.log("moment_load_distance: ", moment_load_distance);

  ctx.beginPath();
  ctx.lineWidth = 2;
  ctx.fillStyle = "#c28039";
  ctx.font = "15px Helvetica";
  ctx.fillText(moment_load, moment_load_distance, 125);

  if (moment_load > 0) {
    ctx.strokeStyle = "#c28039";
    ctx.beginPath();
    ctx.arc(moment_load_distance,155,20,1.5*Math.PI,0.5*Math.PI)
    ctx.stroke();
  } else {
    ctx.strokeStyle = "#c28039";
    ctx.beginPath();
    ctx.arc(moment_load_distance,155,20,0.5*Math.PI,1.5*Math.PI)
    ctx.stroke();
  }

}



function distributedLoad(ctx, beam_distributed_load_start, beam_distributed_load_distance_start,
  beam_distributed_load_end, beam_distributed_load_distance_end, beam_length) {

  if (beam_distributed_load_distance_start > 0) {
    beam_distributed_load_distance_start = 45 + beam_distributed_load_distance_start*400/beam_length
    beam_distributed_load_distance_end = 45 + beam_distributed_load_distance_end*400/beam_length
  } else {
    beam_distributed_load_distance_start = beam_distributed_load_distance_start
    beam_distributed_load_distance_end = beam_distributed_load_distance_end
  }

  console.log("beam_distributed_load_start: ", Math.abs(beam_distributed_load_start));
  console.log("beam_distributed_load_end: ", Math.abs(beam_distributed_load_end));

  ctx.beginPath();
  ctx.lineWidth = 2;
  ctx.strokeStyle = "#37bfc4";
  ctx.fillStyle = "#37bfc4";

  ctx.font = "15px Helvetica";
  ctx.fillText(beam_distributed_load_start, beam_distributed_load_distance_start, 95);
  ctx.fillText(beam_distributed_load_end, beam_distributed_load_distance_end, 95);
  if (Math.abs(beam_distributed_load_start) < Math.abs(beam_distributed_load_end)) {
    start_y = 100;
    end_y = 70;
  } else if (Math.abs(beam_distributed_load_start) > Math.abs(beam_distributed_load_end)) {
    start_y = 70;
    end_y = 100;
  } else {
    start_y = 100;
    end_y = 100;
  }
  console.log("start_y, end_y: ", start_y, end_y);
  ctx.beginPath();
  ctx.moveTo(beam_distributed_load_distance_start, start_y); // start point
  ctx.lineTo(beam_distributed_load_distance_end, end_y); // end at thia point
  ctx.lineTo(beam_distributed_load_distance_end, 150); // end at thia point
  ctx.lineTo(beam_distributed_load_distance_start, 150); // end at thia point
  ctx.closePath();
  ctx.stroke();
}









function canvas_arrow(context, fromx, fromy, tox, toy){

    var headlen = 10;   // length of head in pixels
    var angle = Math.atan2(toy-fromy,tox-fromx);
    context.moveTo(fromx, fromy);
    context.lineTo(tox, toy);
    context.lineTo(tox-headlen*Math.cos(angle-Math.PI/6),toy-headlen*Math.sin(angle-Math.PI/6));
    context.moveTo(tox, toy);
    context.lineTo(tox-headlen*Math.cos(angle+Math.PI/6),toy-headlen*Math.sin(angle+Math.PI/6));
    context.stroke();
}



function pin_support(ctx, supprt_type, support_distance, beam_length) {
  if (support_distance > 0) {
    support_distance = 45 + support_distance*400/beam_length
  } else {
    support_distance = support_distance
  }

  ctx.beginPath();
  ctx.lineWidth = 3;
  ctx.strokeStyle = "black";
  ctx.arc(5+support_distance, 165, 5, 0, Math.PI*2, false)
  ctx.stroke();
}


function fixed_support(ctx, supprt_type, support_distance, beam_length) {
  if (support_distance > 0) {
    support_distance = 50 + support_distance*400/beam_length
  } else {
    support_distance = support_distance*1 + 50
  }

  if (supprt_type == "FIXED SUPPORT") {

      ctx.strokeStyle = "black";
      ctx.beginPath();
      ctx.lineWidth = 3;
      ctx.moveTo(support_distance, 115);
      // start point
      ctx.lineTo(support_distance, 200);
      // end at thia point
      ctx.stroke();

  } else {
    console.log("free support");
  }

}






































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
    backgroundColor: "rgba(199,43,82,0.3)",
    pointRadius: 0.01,
  }];


  var bending_momentData = [{
    label: 'Bending Moment',
    data: data_bendingMoment,
    backgroundColor: "rgba(199,43,82,0.3)",
    pointRadius: 0.01,
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
