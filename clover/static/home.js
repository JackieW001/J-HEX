//console.log(JACKIE)
var test = {};
for (var i = 0; i < JACKIE.length; i++){
    if (JACKIE[i]["expType"] == "eatOut"){
	test["dining"] = parseInt(JACKIE[i]["expAmt"]);
    }
    else{
	test[JACKIE[i]["expType"]] = parseInt(JACKIE[i]["expAmt"]);
    }
}
console.log(test);

//var data = {"cat4": 70, "cat1": 50, "cat2": 30, "cat3": 20 };
//var data = {"cat3": 20, "cat2": 30, "cat1": 50, "cat4": 70};
var data = test;

var expend_svg = document.getElementById("expend");
var expend_label = document.getElementById("expend_label");

var get_val = function(dict){
    var vals = [];
    for (var key in dict){
	vals.push(dict[key]);
    }
    return vals;
}


var calc_stroke_dasharray = function(val,total, r){
    var circ = 2*Math.PI*r;
    var percent = ((val/total)*circ);
    return percent+' '+circ;
};

var calc_dashoffset = function(data, index, total, r){
    var circ = 2*Math.PI*r;
    var sum = 0;
    for (var i = 0; i < index; i++){
	sum += data[i];
    }
    var offset = ((sum/total)*circ);
    return -offset;
    
};

var get_rand_color = function() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

var get_tot = function(data){
    console.log(data);
    var total = 0;
    for (var i=0; i<data.length; i++) {
	total += data[i];
    }
    return total;
}

var posPieLabel = function(label_id){
    label_id.setAttribute("transform", "translateY(-100px)");

}


var mouseOverEffect = function(e){
    console.log(this.innerHTML);
    expend_label.innerHTML = this.getAttribute("textstuff");

};

/*
var mouseOutEffect = function(){
    //text.removeAttribute("text");
};*/



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

setPie(expend_svg, data, 100, 130, 130, 30, 100*2*Math.PI/4);
expend_label.setAttribute("style", "transform: translate(60px,-280px)");


var circles = document.getElementsByTagName("circle");

for (var i = 0; i < circles.length; i++){
    circles[i].addEventListener('mouseover', mouseOverEffect);
    //circles[i].addEventListener('mouseout', mouseOutEffect);
};




