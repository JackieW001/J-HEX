// --------------------------- HANDLE DATA ---------------------------


var keys = Object.keys(csvdata);
var len = keys.length;


// --------------------------- SET INITIAL VARIABLES ---------------------------
var w = 950;
var h = 605;
var padding = 75;

var svg = d3.select("#graph")
	.append("svg")
	.attr("width", w)
	.attr("height", h);

d3.select('svg')
    .append('line')
    .attr('id', 'bestfit');

d3.select('svg')
    .append('text')
    .attr('transform', 'translate(12, 300)rotate(-90)')
    .attr({'id': 'yL', 'text-anchor': 'middle'})
    .text('Current Money');

d3.select('svg')
    .append('text')
    .attr({'id': 'xLabel', 'x': 500, 'y': 600, 'text-anchor': 'middle'})
    .text("Day");

var lobfeq = d3.select("#lobfeq");
var lobfreg = d3.select("#lobfreg");

var color = d3.scale.category20();

// --------------------------- DRAW AXES ---------------------------
// helper method to get the minimum value for a particular dataset
var getMinVal = function( dataset ) {
    var min = 9999999;

    for (var i = 0; i < len; i++){
	var key = keys[i];
	value = csvdata[key];
	//console.log(value);
	value = parseFloat(value);
	if (value < min) {
	    min = value;
	}
    }    
    return min;
};

// helper method to get the maximum value for a particular dataset
var getMaxVal = function( dataset ) {   
    var max = -9999999;

    for (var i = 0; i < len; i++){
	var key = keys[i];
	value = csvdata[key];
	value = parseFloat(value);
	if (value > max) {	    
	    max = value;
	}
    }    
    return max;
}

// helper method to get the minimum value for a particular dataset
var getMinDate = function( dataset ) {
    var min = Object.keys(dataset)[0];
    return new Date(min);
}

// helper method to get the maximum value for a particular dataset
var getMaxDate = function( dataset ) {
    var max = Object.keys(dataset)[Object.keys(dataset).length - 1];
    return new Date(max);
}

// the scale function for the x-axis (set by setXScale)
var xScale;
// set the xScale
var min = getMinDate( csvdata );
var max = getMaxDate( csvdata );

xScale = d3.time.scale().range([padding, w - padding]);
xScale.domain([min, max]);

// the scale function for the y-axis
var yScale;
// set the yScale
var lifeExMin = getMinVal(csvdata);
var lifeExMax = getMaxVal(csvdata);
yScale = d3.scale.linear()
    .domain( [ lifeExMin + lifeExMin/5, lifeExMax + lifeExMax/5] )
    .range( [h - padding, 0] );


// sets the scale function for the x-axis given a particular dataset
var setXScale = function() {
    var min = getMinDate( currentSet );
    var max = getMaxDate( currentSet );
    xScale.range( [ min - min/100, max + max/100 ] ) // the values we can enter, offset to prevent awkward ends
};


// define the y axis
var yAxis = d3.svg.axis()
    .orient("left")
    .scale(yScale);

// define the y axis
var xAxis = d3.svg.axis()
    .orient("bottom")
    .scale(xScale);

var valueline = d3.svg.line()
    .x(function(d) { return xScale(getDate(d)); })
    .y(function(d) { return yScale(csvdata[d]); });

// draw y axis with labels and move in from the size by the amount of padding
svg.append("g")
    .attr("transform", "translate("+padding+",0)")
    .call(yAxis);

// draw x axis with labels and move to the bottom of the chart area
svg.append("g")
    .attr("class", "xaxis")   // give it a class so it can be used to select only xaxis labels  below
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);



// --------------------------- DRAW POINTS ---------------------------

// set the initial points by adding the data and setting the attributes
console.log(svg);

var getDate = function(d) {
    return new Date(d);
}

svg.selectAll(".dot")
    .data(keys)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("r", 5)
    .attr("cx", function(d) {
	    //console.log(d);
	    return xScale(getDate(d));
	})
    .attr("cy", function(d) {
	    return yScale(csvdata[d]);
	})
    .style("fill", function(d) { return "red";});


svg.append("path")
    .attr("class", "line")
    .attr("d", valueline(keys))
    .attr("stroke", "black")
    .attr("stroke-width", 2)
    .attr("fill", "none");

