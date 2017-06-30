	  // initialize the map
	  var map = L.map('map').setView([42.35, -71.08], 13);
	  
  	  var Esri_WorldTopoMap = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
		attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
  		subdomains: 'abcd',
	      maxZoom: 17,
	      minZoom: 9,
  		ext: 'png'
  	  }).addTo(map);	
 
	  
    
	  map.setZoom(12);    
	$.getJSON("datagrid_exp.json", function (data) {
		var locations = data.map(function(traf){
		var begin = traf.begin_loc.reverse();
		begin.push(0.5);
		return begin;

		});

	    var heat = L.heatLayer(locations, { radius: 35 });
	    map.addLayer(heat);
	});


	  /* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

/*

/* Initialize the SVG layer 
map._initPathRoot()    

/* We simply pick up the SVG from the map object 
var svg = d3.select("#map").select("svg")

g = svg.append("g");
centres	= g.append('g').attr('id', 'centres')

	d3.csv("datagrid_exp.csv", function (dataset) {
		/* Add a LatLng object to each item in the dataset 
			centres.selectAll('.centre')
			.data(dataset)
			.enter()
			.append('circle')
			.on('mouseover', function (d) {
				// reset style on others elements
				d3.selectAll('.route').classed('highlight', false);
				// apply style to element(s)
				d3.selectAll('.route.' + idify(d.MOA)).classed('highlight', true);
			})
			.on('mouseout', function () {
				d3.selectAll('.route').classed('highlight', false);
		})

		
		map.on("viewreset", update);
		update();

		function update() {
			feature.attr("transform", 
			function(d) { 
				return "translate("+ 
					map.latLngToLayerPoint(d.LatLng).x +","+ 
					map.latLngToLayerPoint(d.LatLng).y +")";
				})}

		})


