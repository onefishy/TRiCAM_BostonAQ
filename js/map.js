	  // initialize the map
	  var map = L.map('map').setView([42.35, -71.08], 13);
	  
  	  var Stamen_TonerLite = L.tileLayer('http://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.{ext}', {
  		attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  		subdomains: 'abcd',
	      maxZoom: 17,
	      minZoom: 9,
  		ext: 'png'
  	  }).addTo(map);	
 
	  
    
	  map.setZoom(12);
	  $.getJSON("./data/rodents.geojson",function(data){
	    var locations = data.features.map(function(rat) {
	      // the heatmap plugin wants an array of each location
	      var location = rat.geometry.coordinates.reverse();
	      location.push(0.5);
	      return location; // e.g. [50.5, 30.5, 0.2], // lat, lng, intensity
	    });

	    var heat = L.heatLayer(locations, { radius: 35 });
	    map.addLayer(heat);
	  });