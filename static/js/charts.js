function init() {

var session_data = JSON.parse(eval_list_data)
  // Use the list of sample names to populate the select options
  d3.json("../resources/evaluated_tweets.json").then((data) => {

    if (eval_list_data != '{}') {
       console.log("Found the session data.")      
       data = session_data;
    }
    console.log(data);

    buildCharts(data);
    buildTrendingTags(data);
  });
}

// Initialize the dashboard
init();


// Demographics Panel 
function buildTrendingTags(session_data) {
  d3.json("../resources/evaluated_tweets.json").then((data) => {

    if (eval_list_data != '{}') {
      data = session_data;
   }
    var tags = data.tags;

    // Use d3 to select the panel with id of `#sample-metadata`
    var PANEL = d3.select("#trending-tags");

    // Use `.html("") to clear any existing metadata
    PANEL.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    console.log(tags)
    PANEL.append("h6").text('Rank / Tag')
    Object.entries(tags).forEach(([key, value]) => {
      PANEL.append("h6").text(`${key}   ${value}`);
    });

  });
}

// 1. Create the buildCharts function.https://iprudhomme.github.io/plotly_deployment/
function buildCharts(session_data) {
  // 2. Use d3.json to load and retrieve the evaluated_tweets.json file 
  d3.json("../resources/evaluated_tweets.json").then((data) => {

    if (eval_list_data != '{}') {
      data = session_data;
    }
    // Create a variable that holds the samples array. 
    var plot_data = data.plot_data;
    
    // 6. Create variables that hold the tags, positives, and negatives.
    var tags = plot_data.tags;
    console.log(tags);
    var positives = plot_data.positives;
    console.log(positives);
    var negatives = plot_data.negatives;
    console.log(negatives);

    // 3. Create a variable that holds the total count.
    var total_count =  data.total_count;
    console.log(total_count);

    var total_positives = data.positive_count
    console.log(total_positives)

    var totals = data.totals

    // Create the Bar graph
    var trace1 = {
      x: tags,
      y: negatives,
      name: 'Negative',
      type: 'bar'
    };
    
    var trace2 = {
      x: tags,
      y: positives,
      name: 'Positive',
      type: 'bar'
    };
    
    var barData = [trace1, trace2];
    
    var barLayout = {barmode: 'group'};
    
    Plotly.newPlot('bar', barData, barLayout);


    // Create the trace for the gauge chart.
    var gaugeData = [{
      type : "indicator",
      mode : "gauge+number",
      value: total_positives/total_count *100,
      title: {text: "<b>Current Trending Tweet Sentiment</b><br>Percent Positive"},

      gauge: {
        axis: { range: [null, 100], tickwidth: 2, tickcolor: "darkblue" },
        bar: { color: "black" },
        borderwidth: 2,
        bordercolor: "gray",

        steps: [
          { range: [0,20], color: "red" },
          { range: [20,40], color: "orange"},
          { range: [40,60], color: "yellow" },
          { range: [60,80], color: "lightgreen"},
          { range: [80,100], color: "green"}
        ]
      }
    }];
    
    // Create the layout for the gauge chart.
    var gaugeLayout = { 
      plot_bgcolor: 'rgb(230, 230,230)',
      paper_bgcolor: 'rgb(230,230,230)',
      margin: { t: 25, r: 25, l: 25, b: 25 },
      font: {
        family: 'Times New Roman, serif'}
        };

    // Use Plotly to plot the gauge data and layout.
    Plotly.newPlot("gauge", gaugeData, gaugeLayout);


// Create the Totals Bar graph
var Bar2Trace1 = {
  x: ['Total Tweets'],
  y: [totals.counts[0]],
  name: totals.predictions[0],
  type: 'bar'
};

var Bar2Trace2 = {
  x: ['Total Tweets'],
  y: [totals.counts[1]],
  name: totals.predictions[1],
  type: 'bar'
};

var barData = [Bar2Trace1,Bar2Trace2];

var barLayout = {barmode: 'group'};

Plotly.newPlot('bar2', barData, barLayout);
    



  });
}