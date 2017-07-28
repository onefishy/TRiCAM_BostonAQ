// set the dimensions and margins of the graph
				var margin = {top: 10, right: 20, bottom: 50, left: 30},
				    width = 0.1*$(document).width()- margin.left - margin.right,
				    height = 0.12*$(document).height() - margin.top - margin.bottom;

				// parse the date / time
				var parseTime = d3.timeParse("%d-%b-%y");

				// set the ranges
				var x = d3.scaleTime()
						.range([0, width]);
				var y = d3.scaleLinear()
						.range([height, 0]);


				// define the 1st line
				var valueline = d3.line()
				    .x(function(d) { return x(d.date); })
				    .y(function(d) { return y(d.close); });

				// define the 2nd line
				var valueline2 = d3.line()
				    .x(function(d) { return x(d.date); })
				    .y(function(d) { return y(d.open); });

				// append the svg obgect to the body of the page
				// appends a 'group' element to 'svg'
				// moves the 'group' element to the top left margin
				var svg = d3.select("#graph_window").append("svg")
							//adds a class, which we style in style.css
							.classed("svg-container", true)
							//says to preserve aspect ratio as window resizes
							//needs the viewBox to work
							.attr("preserveAspectRatio", "XMinYMin meet")
							//says where and what size to initially place the graph
							.attr("viewBox", "0 0 150 100")
				  			.append("g")
				    		.attr("transform",
				          "translate(" + margin.left + "," + margin.top + ")");

				// Get the data
				d3.csv("data/data2.csv", function(error, data) {
				  if (error) throw error;

				  // format the data
				  data.forEach(function(d) {
				      d.date = parseTime(d.date);
				      d.close = +d.close;
				      d.open = +d.open;
				  });

				  // Scale the range of the data
				  x.domain(d3.extent(data, function(d) { return d.date; }));
				  y.domain([0, d3.max(data, function(d) {
					  return Math.max(d.close, d.open); })]);

				  // Add the valueline path.
				  svg.append("path")
				      .data([data])
				      .attr("class", "line")
				      .attr("d", valueline);

				  // Add the valueline2 path.
				  svg.append("path")
				      .data([data])
				      .attr("class", "line")
				      .style("stroke", "red")
				      .attr("d", valueline2);

				  // Add the X Axis
				svg.append("g")
				  .attr("class", "axis")
				  .attr("transform", "translate(0," + height + ")")
				  .call(d3.axisBottom(x).ticks(21))
				  .selectAll("text")	
				    .style("text-anchor", "end")
				    .attr("dx", "-.8em")
				    .attr("dy", ".15em")
				    .attr("transform", "rotate(-65)");

			  // Add the Y Axis
				svg.append("g")
				  .attr("class", "axis")
				  .call(d3.axisLeft(y));	
				});