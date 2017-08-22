// Scripted D3 on the chart
//
var chartCircles = function(data){
	var chart = d3.select('#chart');
	// set chart width and height from data
	//chart.attr('height', data.height).attr('width', data.width);
	// create some circles using data
	chart.selectAll('circle').data(data.circles)
		.enter()
		.append('circle')
		.attr('cx', function(d) { return d.x })
		.attr('cy', function(d) { return d.y })
		.attr('r', function(d) { return d.r });
};
var myData= {
	width: 300, height: 150,
	circles: [
		{'x':50, 'y':30, 'r':20},
		{'x':70, 'y':80, 'r':10},
		{'x':160, 'y':60, 'r':10},
		{'x':200, 'y':100, 'r':5},
	]
};
chartCircles(myData);



// Iterating over an object
// (tricky because of prototype chain)
var obj = {a:3, b:2, c:4}
for (var prop in obj) {
  if( obj.hasOwnProperty( prop ) ) {
    console.log("o." + prop + " = " + obj[prop]);
  }
}

// more recent way (but for Arrays only)
var list = [3, 2, 4]
list.forEach(function(value, index){ console.log("list[" + index + "] = " + value); });



// Classes in javascript (one way)
// 
var Citizen = function(name, country){
  this.name = name;
  this.country = country;
};
Citizen.prototype = { //methods here will overwrite any in proto chain and be inherited
  printDetails: function() {
    console.log('Citizen '+this.name+' from '+this.country);
  }
};
var c = new Citizen('Groucho M.', 'Freedonia');
c.printDetails();

// Newer way from ES5 which doesn't need 'new'
var Citizen = {
  setCitizen: function(name, country){
    this.name = name;
    this.country = country;
    return this;
  },
  printDetails: function(){
    console.log('Citizen '+this.name+' from '+this.country);
  }
};  // Citizen is now an object rather than a construction function - think of as base house
var Winner = Object.create(Citizen); //inherits from Citizen
Winner.setWinner = function(name, country, category, year){ 
  this.setCitizen(name, country);
  this.category = category;
  this.year = year;
  return this;
};
Winner.printDetails = function(){
  console.log('Winner '+this.name+' in '+this.category+'('+this.year+') from '+this.country);
};
var albert = Object.create(Winner).setWinner('Albert Einstein', 'Switzerland', 'Physics', 1921);
albert.printDetails();


// Closures in JS
//
function Counter(inc) {
	var count = 0;
	var api = {};
	api.add = function() {
		count += inc;
		console.log('Current count: ' + count);
		return api;
	}
	api.sub = function() {
		count -= inc;
		console.log('Current count: ' + count);
		return api;
	}
	api.reset = function() {
		count = 0;
		console.log('Current count: ' + count);
		return api;
	}
	return api;
}
cntr = Counter(3);
cntr.add().add().add()
cntr.sub()
cntr.reset()

