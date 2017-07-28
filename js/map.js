	  // initialize the map
	  var map = L.map('map').setView([42.35, -71.08], 13);
	  
  	  var Esri_WorldTopoMap = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
		attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
  		subdomains: 'abcd',
	      maxZoom: 17,
	      minZoom: 9,
  		ext: 'png'
  	  }).addTo(map);	



L.GridLayer.DebugCoords = L.GridLayer.extend({
    createTile: function (coords, done) {
    var tile = document.createElement('div');
    tile.innerHTML = [coords.x, coords.y, coords.z].join(', ');
    tile.style.outline = '1px solid red';

    setTimeout(function () {
        done(null, tile);	// Syntax is 'done(error, tile)'
    }, 50 + Math.random() * 1500);

    return tile;
}
});

L.gridLayer.debugCoords = function(opts) {
    return new L.GridLayer.DebugCoords(opts);
};
map.addLayer( L.gridLayer.debugCoords() );
    
	  map.setZoom(12);
	  $.getJSON("./data/data_test.geojson",function(data){
	    var locations = data.features.map(function(rat) {
	      // the heatmap plugin wants an array of each location
	      var location = rat.geometry.coordinates.reverse();
	      location.push(0.5);
	      return location; // e.g. [50.5, 30.5, 0.2], // lat, lng, intensity
	    });

	    var heat = L.heatLayer(locations, { radius: 35 });
	    map.addLayer(heat);
	  });



	  /* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}


// $(".program").on('click',function () {
//   $('li ul').toggle('');
// });

//this allows the drops to function independently
$('li.program').click(function() {
   $('li.program').not(this).find('ul');
   $(this).find('ul').toggle();
});
$('#myDropdown .drop').on({
	"click":function(e){
      e.stopPropagation();
    }
});


//attempt at highlighted onclick
function dropclick() {
    if (d3.select(this).style("background-color" == "f9f9f9")) {
        d3.select(this).style("fill", "red");
    }
    else {
        d3.select(this).style("background-color", "f9f9f9");
    }
        }

		

// Close the dropdown menu if the user clicks outside of it
// window.onclick = function(event) {
//   if (!event.target.matches('.dropbtn')) {

//     var dropdowns = document.getElementsByClassName("dropdown-content");
//     var i;
//     for (i = 0; i < dropdowns.length; i++) {
//       var openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains('show')) {
//         openDropdown.classList.remove('show');
//       }
//     }
//   }
// }


