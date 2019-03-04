function generateDoughnutChart(elementId, data) {
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Positive", "Negative", 'Neutral'],
      datasets: [{
        label: '# tweet sentiments',
        data: data,
        backgroundColor: [
          'rgba(75, 192, 192, 0.2)',
          'rgba(255, 99, 132, 0.2)',
          'rgba(241, 90, 34, 0.2)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255,99,132,1)',
          'rgba(241, 90, 34, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });
}

function generateBarChart(elementId, data) {
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Female", "Male"],
      datasets: [{
        label: '# tweet counts by gender',
        data: data,
        backgroundColor: [
          'rgba(255, 192, 203, 0.2)',
          'rgba(0, 0, 255, 0.2)'
        ],
        borderColor: [
          'rgba(255, 192, 203, 1)',
          'rgba(0, 0, 255, 1)',
        ],
        borderWidth: 1
      }]
    },

  });
}

function generateTimeseriesData(elementId, data, label) {
  var s1 = {
    label: 'label',
    borderColor: 'blue',
    data: data
  };
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [s1]
    },
    options: {
      scales: {
        xAxes: [{
          type: 'time'
        }]
      }
    }
  })
}

function plotTimeseriesData(elementId, data1, data2, label1, label2) {
  var s1 = {
    label: label1,
    borderColor: 'blue',
    data: data1
  };
  var s2 = {
    label: label2,
    borderColor: 'red',
    data: data2
  };
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [s1, s2]
    },
    options: {
      scales: {
        xAxes: [{
          type: 'time'
        }]
      }
    }
  })
}

function plotTimeseriesDataStackedBar(elementId, data1, data2, label1, label2) {
  var s1 = {
    label: label1,
    borderColor: 'blue',
    data: data1
  };
  var s2 = {
    label: label2,
    borderColor: 'red',
    data: data2
  };
  var ctx = document.getElementById(elementId);
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: data1.concat(data2),
    options: {
      scales: {
        xAxes: [{
          stacked: true
        }],
        yAxes: [{
          stacked: true
        }],
      }
    }
  })
}

function amBarChart(divId, mc, fc) {
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create(divId, am4charts.XYChart);
chart.scrollbarX = new am4core.Scrollbar();

// Add data
chart.data = [{
  "gender": "Male",
  "count": mc
}, {
  "gender": "Female",
  "count": fc
}];

prepareParetoData();

function prepareParetoData(){
    var total = 0;

    for(var i = 0; i < chart.data.length; i++){
        var value = chart.data[i].visits;
        total += value;
    }

    var sum = 0;
    for(var i = 0; i < chart.data.length; i++){
        var value = chart.data[i].visits;
        sum += value;
        chart.data[i].pareto = sum / total * 100;
    }
}

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "gender";
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.renderer.minGridDistance = 60;
categoryAxis.tooltip.disabled = true;

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.renderer.minWidth = 50;
valueAxis.min = 0;
valueAxis.cursorTooltipEnabled = false;

// Create series
var series = chart.series.push(new am4charts.ColumnSeries());
series.sequencedInterpolation = true;
series.dataFields.valueY = "count";
series.dataFields.categoryX = "gender";
series.tooltipText = "[{categoryX}: bold]{valueY}[/]";
series.columns.template.strokeWidth = 0;
series.columns.template.width = am4core.percent(20);
series.tooltip.pointerOrientation = "vertical";

series.columns.template.column.cornerRadiusTopLeft = 10;
series.columns.template.column.cornerRadiusTopRight = 10;
series.columns.template.column.fillOpacity = 0.8;

// on hover, make corner radiuses bigger
var hoverState = series.columns.template.column.states.create("hover");
hoverState.properties.cornerRadiusTopLeft = 0;
hoverState.properties.cornerRadiusTopRight = 0;
hoverState.properties.fillOpacity = 1;

series.columns.template.adapter.add("fill", (fill, target)=>{
  return chart.colors.getIndex(target.dataItem.index);
})

/*
var paretoValueAxis = chart.yAxes.push(new am4charts.ValueAxis());
paretoValueAxis.renderer.opposite = true;
paretoValueAxis.min = 0;
paretoValueAxis.max = 100;
paretoValueAxis.strictMinMax = true;
paretoValueAxis.renderer.grid.template.disabled = true;
paretoValueAxis.numberFormatter = new am4core.NumberFormatter();
paretoValueAxis.numberFormatter.numberFormat = "#'%'"
paretoValueAxis.cursorTooltipEnabled = false;

var paretoSeries = chart.series.push(new am4charts.LineSeries())
paretoSeries.dataFields.valueY = "pareto";
paretoSeries.dataFields.categoryX = "country";
paretoSeries.yAxis = paretoValueAxis;
paretoSeries.tooltipText = "pareto: {valueY.formatNumber('#.0')}%[/]";
paretoSeries.bullets.push(new am4charts.CircleBullet());
paretoSeries.strokeWidth = 2;
paretoSeries.stroke = new am4core.InterfaceColorSet().getFor("alternativeBackground");
paretoSeries.strokeOpacity = 0.5;*/

// Cursor
chart.cursor = new am4charts.XYCursor();
chart.cursor.behavior = "panX";

var blue = "#0000FF";
var pink = "#FFC0CB";
var colorSet = new am4core.ColorSet();
colorSet.list = [blue, pink].map(function(color) {
  return new am4core.color(color);
});
series.fill = colorSet;
}


function amPieChart(divId, pos, neg, neu) {
am4core.useTheme(am4themes_material);
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create(divId, am4charts.PieChart);

// Add and configure Series
var pieSeries = chart.series.push(new am4charts.PieSeries());
pieSeries.dataFields.value = "percentage";
pieSeries.dataFields.category = "sentiment";

// Let's cut a hole in our Pie chart the size of 30% the radius
chart.innerRadius = am4core.percent(30);

// Put a thick white border around each Slice
pieSeries.slices.template.stroke = am4core.color("#fff");
pieSeries.slices.template.strokeWidth = 2;
pieSeries.slices.template.strokeOpacity = 1;
pieSeries.slices.template
  // change the cursor on hover to make it apparent the object can be interacted with
  .cursorOverStyle = [
    {
      "property": "cursor",
      "value": "pointer"
    }
  ];

pieSeries.alignLabels = false;
pieSeries.labels.template.bent = true;
pieSeries.labels.template.radius = 3;
pieSeries.labels.template.padding(0,0,0,0);

pieSeries.ticks.template.disabled = true;

// Create a base filter effect (as if it's not there) for the hover to return to
var shadow = pieSeries.slices.template.filters.push(new am4core.DropShadowFilter);
shadow.opacity = 0;

// Create hover state
var hoverState = pieSeries.slices.template.states.getKey("hover"); // normally we have to create the hover state, in this case it already exists

// Slightly shift the shadow and make it more prominent on hover
var hoverShadow = hoverState.filters.push(new am4core.DropShadowFilter);
hoverShadow.opacity = 0.7;
hoverShadow.blur = 5;

// Add a legend
chart.legend = new am4charts.Legend();

chart.data = [{
  "sentiment": "Positive",
  "percentage": pos
},{
  "sentiment": "Negative",
  "percentage": neg
}, {
  "sentiment": "Neutral",
  "percentage": neu
}];

var colorSet = new am4core.ColorSet();
var green = "#228B22";
var red = "#FF0000";
var orange = "#FF7F50";
colorSet.list = [green, red, orange].map(function(color) {
  return new am4core.color(color);
});
pieSeries.colors = colorSet;

}

function amAreaChart(elementId, data, party_1, party_2){
// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create(elementId, am4charts.XYChart);

chart.data = data;
// Set input format for the dates
chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

// Create axes
var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "Count";

// Create series
var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.valueY = party_1;
series.dataFields.dateX = "date";
series.tooltipText = party_1
series.strokeWidth = 2;
series.minBulletDistance = 15;
series.tooltip.getFillFromObject = false;
series.tooltip.background.fill = am4core.color("#000");
series.tooltip.getStrokeFromObject = true;
series.tooltip.background.strokeWidth = 3;
series.fillOpacity = 0.5;
series.stacked = true;



var series2 = chart.series.push(new am4charts.LineSeries());
series2.dataFields.valueY = party_2;
series2.dataFields.dateX = "date";
series2.tooltipText = party_2
series2.strokeWidth = 2;
series2.minBulletDistance = 15;
series2.tooltip.getFillFromObject = false;
series2.tooltip.background.fill = am4core.color("#000");
series2.tooltip.getStrokeFromObject = true;
series2.tooltip.background.strokeWidth = 3;
series2.fillOpacity = 0.5;
series2.stacked = true;

// Drop-shaped tooltips
/*
series2.tooltip.background.cornerRadius = 20;
series2.tooltip.background.strokeOpacity = 0;
series2.tooltip.pointerOrientation = "vertical";
series2.tooltip.label.minWidth = 40;
series2.tooltip.label.minHeight = 40;
series2.tooltip.label.textAlign = "middle";
series2.tooltip.label.textValign = "middle";*/

// Make bullets grow on hover
/*var bullet = series.bullets.push(new am4charts.CircleBullet());
bullet.circle.strokeWidth = 2;
bullet.circle.radius = 4;
bullet.circle.fill = am4core.color("#fff");

var bullethover = bullet.states.create("hover");
bullethover.properties.scale = 1.3;

var bullet2 = series2.bullets.push(new am4charts.CircleBullet());
bullet2.circle.strokeWidth = 2;
bullet2.circle.radius = 4;
bullet2.circle.fill = am4core.color("#fff");

var bullethover2 = bullet2.states.create("hover");
bullethover2.properties.scale = 1.3;*/

// Make a panning cursor
chart.cursor = new am4charts.XYCursor();
chart.cursor.behavior = "panXY";
chart.cursor.xAxis = dateAxis;
chart.cursor.snapToSeries = series;

// Create vertical scrollbar and place it before the value axis
/*
chart.scrollbarY = new am4core.Scrollbar();
chart.scrollbarY.parent = chart.leftAxesContainer;
chart.scrollbarY.toBack();

// Create a horizontal scrollbar with previe and place it underneath the date axis
chart.scrollbarX = new am4charts.XYChartScrollbar();
chart.scrollbarX.series.push(series);
chart.scrollbarX.parent = chart.bottomAxesContainer;

chart.events.on("ready", function () {
  dateAxis.zoom({start:0.79, end:1});
});*/

series.legendSettings.labelText = party_1;
series2.legendSettings.labelText = party_2;

chart.legend = new am4charts.Legend();
}

function amStackedColumnChart(elementId, data, party_1, party_2) {
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create(elementId, am4charts.XYChart);


// Add data
chart.data = data;
chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "date";
categoryAxis.renderer.grid.template.location = 0;


var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.renderer.inside = true;
valueAxis.renderer.labels.template.disabled = true;
valueAxis.min = 0;

// Create series
function createSeries(field, name) {

  // Set up series
  var series = chart.series.push(new am4charts.ColumnSeries());
  series.name = name;
  series.dataFields.valueY = field;
  series.dataFields.categoryX = "date";
  series.sequencedInterpolation = true;

  // Make it stacked
  series.stacked = true;

  // Configure columns
  series.columns.template.width = am4core.percent(60);
  series.columns.template.tooltipText = "[bold]{name}[/]\n[font-size:14px]{categoryX}: {valueY}";

  // Add label
  var labelBullet = series.bullets.push(new am4charts.LabelBullet());
  labelBullet.label.text = "{valueY}";
  labelBullet.locationY = 0.5;

  return series;
}

createSeries(party_1, party_1);
createSeries(party_2, party_2);


// Legend
chart.legend = new am4charts.Legend();
}

function amTrendLine(elementId, data, party_1, party_2) {
am4core.useTheme(am4themes_animated);
// Themes end

// Create chart instance
var chart = am4core.create(elementId, am4charts.XYChart);

// Enable chart cursor
chart.cursor = new am4charts.XYCursor();
chart.cursor.lineX.disabled = true;
chart.cursor.lineY.disabled = true;

// Enable scrollbar
chart.scrollbarX = new am4core.Scrollbar();

// Add data
chart.data = data;

// Create axes
var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.dataFields.category = "Date";
dateAxis.renderer.grid.template.location = 0.5;
dateAxis.dateFormatter.inputDateFormat = "yyyy-MM-dd";
dateAxis.renderer.minGridDistance = 40;
dateAxis.tooltipDateFormat = "MMM dd, yyyy";
dateAxis.dateFormats.setKey("day", "dd");

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

// Create series
var series = chart.series.push(new am4charts.LineSeries());
series.tooltipText = "{date}\n[bold font-size: 17px]value: {valueY}[/]";
series.dataFields.valueY = party_1;
series.dataFields.dateX = "date";
series.strokeDasharray = 3;
series.strokeWidth = 2
series.strokeOpacity = 0.3;
series.strokeDasharray = "3,3"

var bullet = series.bullets.push(new am4charts.CircleBullet());
bullet.strokeWidth = 2;
bullet.stroke = am4core.color("#fff");
bullet.setStateOnChildren = true;
bullet.propertyFields.fillOpacity = "opacity";
bullet.propertyFields.strokeOpacity = "opacity";

var hoverState = bullet.states.create("hover");
hoverState.properties.scale = 1.7;

var series2 = chart.series.push(new am4charts.LineSeries());
series2.tooltipText = "{date}\n[bold font-size: 17px]value: {valueY}[/]";
series2.dataFields.valueY = party_2;
series2.dataFields.dateX = "date";
series2.strokeDasharray = 3;
series2.strokeWidth = 2
series2.strokeOpacity = 0.3;
series2.strokeDasharray = "3,3"

var bullet2 = series2.bullets.push(new am4charts.CircleBullet());
bullet2.strokeWidth = 2;
bullet2.stroke = am4core.color("#fff");
bullet2.setStateOnChildren = true;
bullet2.propertyFields.fillOpacity = "opacity";
bullet2.propertyFields.strokeOpacity = "opacity";

var hoverState = bullet2.states.create("hover");
hoverState.properties.scale = 1.7;

/*function createTrendLine(data, key) {
  var trend = chart.series.push(new am4charts.LineSeries());
  trend.dataFields.valueY = key;
  trend.dataFields.dateX = "date";
  trend.strokeWidth = 2
  trend.stroke = trend.fill = am4core.color("#c00");
  trend.data = data;

  var bullet = trend.bullets.push(new am4charts.CircleBullet());
  bullet.tooltipText = "{date}\n[bold font-size: 17px]value: {valueY}[/]";
  bullet.strokeWidth = 2;
  bullet.stroke = am4core.color("#fff")
  bullet.circle.fill = trend.stroke;

  var hoverState = bullet.states.create("hover");
  hoverState.properties.scale = 1.7;

  return trend;
};

td = [data[0], data[data.length - 1]]
createTrendLine(td, party_1);
createTrendLine(td, party_2);*/


// Initial zoom once chart is ready
/*lastTrend.events.once("datavalidated", function(){
  series.xAxis.zoomToDates(new Date(2012, 0, 2), new Date(2012, 0, 13));
});*/
}

function amUpDownChart(elementId, data, party_1, party_2) {
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create(elementId, am4charts.XYChart);
chart.paddingRight = 20;



chart.data = data;

var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.renderer.grid.template.location = 0;
dateAxis.renderer.axisFills.template.disabled = true;
dateAxis.renderer.ticks.template.disabled = true;

function plotData(value, color) {
var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.tooltip.disabled = true;
valueAxis.renderer.minWidth = 35;
valueAxis.renderer.axisFills.template.disabled = true;
valueAxis.renderer.ticks.template.disabled = true;
//valueAxis.fill = color;

var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.dateX = "date";
series.dataFields.valueY = value;
series.stroke = color;
series.strokeWidth = 2;
series.tooltipText = "value: {valueY}, day change: {valueY.previousChange}";

// set stroke property field
series.propertyFields.stroke = "color";
series.legendSettings.labelText = value;
}

plotData(party_1, party1_color);
plotData(party_2, party2_color);
chart.cursor = new am4charts.XYCursor();

var scrollbarX = new am4core.Scrollbar();
chart.scrollbarX = scrollbarX;
var legend = new am4charts.Legend();
chart.legend = legend;

chart.events.on("ready", function(ev) {
  dateAxis.zoomToDates(
    data[0].date,
    data[data.length - 1].date
  );
});
}
