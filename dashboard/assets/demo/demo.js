type = ['primary', 'info', 'success', 'warning', 'danger'];

demo = {
  initPickColor: function() {
    $('.pick-class-label').click(function() {
      var new_class = $(this).attr('new-class');
      var old_class = $('#display-buttons').attr('data-class');
      var display_div = $('#display-buttons');
      if (display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
      }
    });
  },


  

  initDocChart: function() {
    chartColor = "#FFFFFF";

    // General configuration for the charts with Line gradientStroke
    gradientChartOptionsConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      tooltips: {
        bodySpacing: 4,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
        xPadding: 10,
        yPadding: 10,
        caretPadding: 10
      },
      responsive: true,
      scales: {
        yAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }],
        xAxes: [{
          display: 0,
          gridLines: 0,
          ticks: {
            display: false
          },
          gridLines: {
            zeroLineColor: "transparent",
            drawTicks: false,
            display: false,
            drawBorder: false
          }
        }]
      },
      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 15,
          bottom: 15
        }
      }
    };

    ctx = document.getElementById('lineChartExample').getContext("2d");

    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, '#80b6f4');
    gradientStroke.addColorStop(1, chartColor);

    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");


    

    myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Active Users",
          borderColor: "#f96332",
          pointBorderColor: "#FFF",
          pointBackgroundColor: "#f96332",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 1,
          pointRadius: 4,
          fill: true,
          backgroundColor: gradientFill,
          borderWidth: 2,
          data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
        }]
      },
      options: gradientChartOptionsConfiguration
    });
  },

  initDashboardPageCharts: function() {

    gradientChartOptionsConfigurationWithTooltipBlue = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#2380f7"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#2380f7"
          }
        }]
      }
    };

    gradientChartOptionsConfigurationWithTooltipPurple = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(225,78,202,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }]
      }
    };

    gradientChartOptionsConfigurationWithTooltipOrange = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 50,
            suggestedMax: 110,
            padding: 20,
            fontColor: "#ff8a76"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(220,53,69,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#ff8a76"
          }
        }]
      }
    };

    gradientChartOptionsConfigurationWithTooltipGreen = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 50,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(0,242,195,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };


    gradientBarChartConfiguration = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{

          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 120,
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{

          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };

    // var ctx = document.getElementById("chartLinePurple").getContext("2d");
    //
    // var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);
    //
    // gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
    // gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    // gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colorsleftbuttom
    //
    // var data = {
    //   labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
    //   datasets: [{
    //     label: "Data",
    //     fill: true,
    //     backgroundColor: gradientStroke,
    //     borderColor: '#d048b6',
    //     borderWidth: 2,
    //     borderDash: [],
    //     borderDashOffset: 0.0,
    //     pointBackgroundColor: '#d048b6',
    //     pointBorderColor: 'rgba(255,255,255,0)',
    //     pointHoverBackgroundColor: '#d048b6',
    //     pointBorderWidth: 20,
    //     pointHoverRadius: 4,
    //     pointHoverBorderWidth: 15,
    //     pointRadius: 4,
    //     data: [80, 100, 70, 80, 120, 80],
    //   }]
    // };
    //
    // var myChart = new Chart(ctx, {
    //   type: 'line',
    //   data: data,
    //   options: gradientChartOptionsConfigurationWithTooltipPurple
    // });

    setTimeout(function () {
      $.ajax({
        url:"http://192.168.1.101:8090/historical/total/",
        success:function(json){
          var ctxGreen = document.getElementById("chartLineGreen").getContext("2d");

          var gradientStroke = ctxGreen.createLinearGradient(0, 230, 0, 50);

          gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
          gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
          gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

          let histotal = JSON.parse(json);
          let labels = histotal["name"];
          let numbers = histotal["data"];

          var data = {
            labels: labels,
            datasets: [{
              label: "Crowd number in that time",
              fill: true,
              backgroundColor: gradientStroke,
              borderColor: '#00d6b4',
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: '#00d6b4',
              pointBorderColor: 'rgba(255,255,255,0)',
              pointHoverBackgroundColor: '#00d6b4',
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: numbers,
            }]
          };

          var myChart = new Chart(ctxGreen, {
            type: 'line',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipGreen

          });;


        }
      })
    },1);


    setTimeout(function() {
      $.ajax({
        url:"http://192.168.1.101:8090/historical/zone1",
        success:function(json){
          let datum = JSON.parse(json);
          var chart_labels = datum["name"];
          var chart_data1 = datum["data"];
          var chart_data2 = datum["data"];
          // console.log(datum);


          var ctx = document.getElementById("chartBig1").getContext('2d');

          var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

          gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
          gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
          gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
          var config = {
            type: 'line',
            data: {
              labels: chart_labels,
              datasets: [
                {
                  label: "Average Number in this time",
                  fill: true,
                  backgroundColor: gradientStroke,
                  borderColor: '#d346b1',
                  borderWidth: 2,
                  borderDash: [],
                  borderDashOffset: 0.0,
                  pointBackgroundColor: '#d346b1',
                  pointBorderColor: 'rgba(255,255,255,0)',
                  pointHoverBackgroundColor: '#d346b1',
                  pointBorderWidth: 20,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 15,
                  pointRadius: 4,
                  data: chart_data1,
                },

              ]
            },
            options: gradientChartOptionsConfigurationWithTooltipPurple
          };
          var myChartData = new Chart(ctx, config);
          $("#0").click(function() {
            var chart_data = chart_data1;
            var data = myChartData.config.data;
            data.datasets[0].data = chart_data;
            data.labels = chart_labels;
            myChartData.update();
          });
          $("#1").click(function() {
            $.ajax(
                {
                  url:"http://192.168.1.101:8090/historical/zone2",
                  success:function(json) {
                    let datum1 = JSON.parse(json);
                    var chart_data2 = datum1["data"];
                    var chart_data = chart_data2;
                    var data = myChartData.config.data;
                    data.datasets[0].data = chart_data;
                    data.labels = chart_labels;
                    myChartData.update();
                  }})
          });

        }
      })
    },1);

    setTimeout(function () {
      $.ajax({
        url:"http://192.168.1.101:8090/current/",
        success:function(json){
          var ctx = document.getElementById("CountryChart").getContext("2d");

          var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

          gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
          gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
          gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

          let datum = JSON.parse(json);
          let labels = datum["Name"];
          let data = datum["data"];

          var myChart = new Chart(ctx, {
            type: 'bar',
            responsive: true,
            legend: {
              display: false
            },
            data: {
              labels: labels,
              datasets: [{
                label: "Number",
                fill: true,
                backgroundColor: gradientStroke,
                hoverBackgroundColor: gradientStroke,
                borderColor: '#1f8ef1',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                data: data,
              }]
            },
            options: gradientBarChartConfiguration
          });


        }
      })
    },1);

    setInterval(function () {
      $.ajax({
        url:"http://192.168.1.101:8090/current/",
        success:function(json){
          var ctx = document.getElementById("CountryChart").getContext("2d");

          var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

          gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
          gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
          gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

          let datum = JSON.parse(json);
          let labels = datum["Name"];
          let data = datum["data"];

          var myChart = new Chart(ctx, {
            type: 'bar',
            responsive: true,
            legend: {
              display: false
            },
            data: {
              labels: labels,
              datasets: [{
                label: "Number",
                fill: true,
                backgroundColor: gradientStroke,
                hoverBackgroundColor: gradientStroke,
                borderColor: '#1f8ef1',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                data: data,
              }]
            },
            options: gradientBarChartConfiguration
          });
          
          
        }
      })
    },5000);


      $.ajax({
        url:"http://192.168.1.101:8090/total/",
        success:function(data){
          // var ctx = document.getelementbyid("totalnumber");
          $('#TotalNumber').text(new String(data));
          console.log(data);

        }
      })

    setInterval(function (){
      $.ajax({
        url:"http://192.168.1.101:8090/total/",
        success:function(data){
          // var ctx = document.getelementbyid("totalnumber");
          $('#TotalNumber').text(new String(data));
          console.log(data);

        }
      })
    },5000)


    $.ajax({
      url: "http://192.168.1.101:8090/status/",
      success:function (json){
        let lightinfo = JSON.parse(json)

        for (let i in lightinfo) { $('#StatusTable').append(`<tr><td>${lightinfo[i]["name"]}</td><td class="text-center">${lightinfo[i]["status"]}</td></tr>`);
          console.log(lightinfo[i]);
        }

      }
    })

    // setInterval(function (){
    //   $.ajax({
    //     url: "http://127.0.0.1:8090/status/",
    //     success:function (json){
    //       let lightinfo = JSON.parse(json)
    //
    //       for (let i in lightinfo) { $('#StatusTable').append(`<tr><td>${lightinfo[i]["name"]}</td><td class="text-center">${lightinfo[i]["status"]}</td></tr>`);
    //         console.log(lightinfo[i]);
    //       }
    //
    //     }
    //   })
    // },5000)

    $.ajax({
      url: "http://192.168.1.101:8090/light/",
      success:function (json){
        let lightinfo = JSON.parse(json)

      for (let i in lightinfo) { $('#TableID').append(`<tr><td>${lightinfo[i]["name"]}</td><td class="text-center">${lightinfo[i]["light"]}</td></tr>`);
        console.log(lightinfo[i]);
      }

      }
      })


  },

  initGoogleMaps: function() {
    var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
    var mapOptions = {
      zoom: 13,
      center: myLatlng,
      scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
      styles: [{
          "elementType": "geometry",
          "stylers": [{
            "color": "#1d2c4d"
          }]
        },
        {
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#8ec3b9"
          }]
        },
        {
          "elementType": "labels.text.stroke",
          "stylers": [{
            "color": "#1a3646"
          }]
        },
        {
          "featureType": "administrative.country",
          "elementType": "geometry.stroke",
          "stylers": [{
            "color": "#4b6878"
          }]
        },
        {
          "featureType": "administrative.land_parcel",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#64779e"
          }]
        },
        {
          "featureType": "administrative.province",
          "elementType": "geometry.stroke",
          "stylers": [{
            "color": "#4b6878"
          }]
        },
        {
          "featureType": "landscape.man_made",
          "elementType": "geometry.stroke",
          "stylers": [{
            "color": "#334e87"
          }]
        },
        {
          "featureType": "landscape.natural",
          "elementType": "geometry",
          "stylers": [{
            "color": "#023e58"
          }]
        },
        {
          "featureType": "poi",
          "elementType": "geometry",
          "stylers": [{
            "color": "#283d6a"
          }]
        },
        {
          "featureType": "poi",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#6f9ba5"
          }]
        },
        {
          "featureType": "poi",
          "elementType": "labels.text.stroke",
          "stylers": [{
            "color": "#1d2c4d"
          }]
        },
        {
          "featureType": "poi.park",
          "elementType": "geometry.fill",
          "stylers": [{
            "color": "#023e58"
          }]
        },
        {
          "featureType": "poi.park",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#3C7680"
          }]
        },
        {
          "featureType": "road",
          "elementType": "geometry",
          "stylers": [{
            "color": "#304a7d"
          }]
        },
        {
          "featureType": "road",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#98a5be"
          }]
        },
        {
          "featureType": "road",
          "elementType": "labels.text.stroke",
          "stylers": [{
            "color": "#1d2c4d"
          }]
        },
        {
          "featureType": "road.highway",
          "elementType": "geometry",
          "stylers": [{
            "color": "#2c6675"
          }]
        },
        {
          "featureType": "road.highway",
          "elementType": "geometry.fill",
          "stylers": [{
            "color": "#9d2a80"
          }]
        },
        {
          "featureType": "road.highway",
          "elementType": "geometry.stroke",
          "stylers": [{
            "color": "#9d2a80"
          }]
        },
        {
          "featureType": "road.highway",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#b0d5ce"
          }]
        },
        {
          "featureType": "road.highway",
          "elementType": "labels.text.stroke",
          "stylers": [{
            "color": "#023e58"
          }]
        },
        {
          "featureType": "transit",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#98a5be"
          }]
        },
        {
          "featureType": "transit",
          "elementType": "labels.text.stroke",
          "stylers": [{
            "color": "#1d2c4d"
          }]
        },
        {
          "featureType": "transit.line",
          "elementType": "geometry.fill",
          "stylers": [{
            "color": "#283d6a"
          }]
        },
        {
          "featureType": "transit.station",
          "elementType": "geometry",
          "stylers": [{
            "color": "#3a4762"
          }]
        },
        {
          "featureType": "water",
          "elementType": "geometry",
          "stylers": [{
            "color": "#0e1626"
          }]
        },
        {
          "featureType": "water",
          "elementType": "labels.text.fill",
          "stylers": [{
            "color": "#4e6d70"
          }]
        }
      ]
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    var marker = new google.maps.Marker({
      position: myLatlng,
      title: "Hello World!"
    });

    // To add the marker to the map, call setMap();
    marker.setMap(map);
  },

  showNotification: function(from, align) {
    color = Math.floor((Math.random() * 4) + 1);

    $.notify({
      icon: "tim-icons icon-bell-55",
      message: "Welcome to <b>Black Dashboard</b> - a beautiful freebie for every web developer."

    }, {
      type: type[color],
      timer: 8000,
      placement: {
        from: from,
        align: align
      }
    });
  }

};