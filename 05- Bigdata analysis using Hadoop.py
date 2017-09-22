from flask import Flask
import os
import csv
import time

app = Flask(__name__)
app.secret_key = ''
user_cont='''
<!DOCTYPE html>
<meta charset="utf-8">

<head>
	<style>

	.axis {
	  font: 10px sans-serif;
	}

	.axis path,
	.axis line {
	  fill: none;
	  stroke: #000;
	  shape-rendering: crispEdges;
	}

	</style>
</head>

<body>
	
<script src="http://d3js.org/d3.v3.min.js"></script>

<script>

var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = 600 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

// Parse the date / time
//var	parseDate = d3.time.format("%Y-%m").parse;

var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

var y = d3.scale.linear().range([height,0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(10);

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

d3.csv("/data", function(error, data) {

    data.forEach(function(d) {
        d.names =d.names;
        d.count = +d.count;
    });
	
  x.domain(data.map(function(d) { return d.names; }));
  y.domain([0, d3.max(data, function(d) { return d.count; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Value ($)");

  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) { return x(d.names); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return height - y(d.count); });

});


</script>

</body>

'''
content='''
<form action='/random' method='POST'>
Year:<input type='text' name='year'/>
Date Range:<input type='text' name='from'/><input type='text' name='to'/>
<input type='submit' value='Submit'/><br>
</form>


'''
@app.route('/hadoop')
def run_hadoop():
	start_time = time.time()
	year=request.forms.get('year')
	month_from=request.forms.get('from')
	month_to=request.forms.get('to')


	cmd='''

	/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.0.jar -Dmapred.map.tasks=5 -Dmapred.reduce.tasks=1 -mapper 'python mapper.py {0}' -reducer 'python reducer.py {1} {2}' -file mapper.py -file reducer.py   -input myip/* -output myop4908 

	'''.format(year,month_from,month_to)
	
	os.system(cmd)

	return "--- %s seconds ---" % (time.time() - start_time)


@app.route('/')
def index():
	return content

@app.route('/data')
def data_extract():
	os.chdir('/home/ubuntu/myop4908')
	f=open('part-00000','r')

	return f.read()
