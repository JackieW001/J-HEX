
var test = {};
for (var i = 0; i < JACKIE.length; i++){
    if (JACKIE[i]["expType"] == "eatOut"){
	test["dining"] = parseInt(JACKIE[i]["expAmt"]);
    }
    else{
	test[JACKIE[i]["expType"]] = parseInt(JACKIE[i]["expAmt"]);
    }
}

var data = test;

/*
 * Expend accessors
 */
var expend_svg = document.getElementById("expend");
var expend_label = document.getElementById("expend_label");

/*
 * get_val
 * get values of dictionary
 */
var get_val = function(dict){
    var vals = [];
    for (var key in dict){
	vals.push(dict[key]);
    }
    return vals;
}

/*
 * calc_stroke_dasharray( values, total, radius )
 * creates segments of pie chart
 */
var calc_stroke_dasharray = function(val,total, r){
    var circ = 2*Math.PI*r;
    var percent = ((val/total)*circ);
    return percent+' '+circ;
};

/*
 * calc_dashoffset( data, index, total, radius )
 * calculates how much to shift pie segment at index i
 */
var calc_dashoffset = function(data, index, total, r){
    var circ = 2*Math.PI*r;
    var sum = 0;
    for (var i = 0; i < index; i++){
	sum += data[i];
    }
    var offset = ((sum/total)*circ);
    return -offset;
    
};

/*
 * get_rand_color()
 * returns random color
 */
var get_rand_color = function() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

/*
 * get_tot(data)
 * returns the total sum of data
 */
var get_tot = function(data){
    console.log(data);
    var total = 0;
    for (var i=0; i<data.length; i++) {
	total += data[i];
    }
    return total;
}

/*
 * mouseOverEffect()
 * changes label inside pie chart
 */

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

var mouseOverEffect = function(e){
    console.log(this.innerHTML);
    var text = this.getAttribute("textstuff").capitalize();
    expend_label.innerHTML = text;

};


/*
 * setPie(svg_id, data, radius, cx, cy, stroke_width, offset)
 * creates pie chart
 */
var setPie = function (svg_id, data, r, cx, cy, stroke_width, offset){
    var vals = get_val(data);    
    var total = get_tot(vals);
 
    
    var cont = d3.select(svg_id);
    var circles = cont.selectAll("circle").data(vals).enter();
    circles.append("circle")
	.attr("r", r)
	.attr("cx", cx)
	.attr("cy", cy)
	.attr("fill", "transparent")
	.attr("stroke", function(d){return get_rand_color();})
	.attr("stroke-width", stroke_width)
	.attr("stroke-dasharray", function(d){return calc_stroke_dasharray(d,total,r);})
	.attr("stroke-dashoffset", function(d,i){return calc_dashoffset(vals, i, total,r);})

    
    var keys = Object.keys(data);
    var label2 = document.getElementsByTagName("circle");
    for (var i = 0; i < label2.length; i++){
	label2[i].setAttribute("textstuff", keys[i] + ": <br>" + data[keys[i]]);
    }
    

}


setPie(expend_svg, data, 100, "50%", "50%", 30, 100*2*Math.PI/4);
expend_label.setAttribute("style", "transform: translate(0px,-230px)");

/*
 * attaches eventlisteners to each segment of the pie charts
 */
var circles = document.getElementsByTagName("circle");

for (var i = 0; i < circles.length; i++){
    circles[i].addEventListener('mouseover', mouseOverEffect);
};




