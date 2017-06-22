
	var width = 1000,
        height = 800;

    var svg = d3.select('#map')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    var g = svg.append('g');

    var albersProjection = d3.geoAlbers()
      .scale(190000)
      .rotate([71.057, 0])
      .center([0, 42.313])
      .translate([width/2, height/2]);

    var geoPath = d3.geoPath()
        .projection(albersProjection);

    g.selectAll('path')
      .data(neighborhoods_json.features)
      .enter()
      .append('path')
      .attr( "fill", "#E0E0E0" )
      .attr( "stroke", "#333")
      .attr('d', geoPath);
	  
	var rodents = svg.append( "g" );

	rodents.selectAll( "path" )
		.data( rodents_json.features )
		.enter()
		.append( "path" )
		.attr( "fill", "#FF8906" )
		.attr( "stroke", "#515151" )
		.attr( "d", geoPath );

 console.log('loaded')