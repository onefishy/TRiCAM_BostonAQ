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

//add heat layer
var heat;
$.getJSON("./data/rodents.geojson",function(data){
      //var locations is an array of coordinates
    var locations = data.features.map(function(rat) {
        // the heatmap plugin wants an array of each location
      var location = rat.geometry.coordinates.reverse();
        location.push(0.5);
        return location; // e.g. [50.5, 30.5, 0.2], // lat, lng, intensity
      });
  heat = L.heatLayer(locations, { radius: 35 }); 
    });

//adds neighborhoods layer

var neigh;
var cam;
var newton;

$.getJSON("./data/cambridge.geojson",function(hoodData){
  cam = L.geoJson(hoodData, {
  //specifies styling for neighborhoods
    style: function(feature){
    return { color: "#999", weight: 1, fillColor: "#ffffcc", fillOpacity: .4 };
    },
    //adds popup of neighborhood name
    onEachFeature: function( feature, layer ){
      layer.bindPopup( "<strong>" + feature.properties.NAME)// + "</strong><br/>" + heat.properties.density + " rats per square mile" )
    }
  }  );
});

$.getJSON("./data/newton.geojson",function(hoodData){
  newton = L.geoJson(hoodData, {
  //specifies styling for neighborhoods
    style: function(feature){
    return { color: "#999", weight: 1, fillColor: "#ffffcc", fillOpacity: .4 };
    },
    //adds popup of neighborhood name
    onEachFeature: function( feature, layer ){
      layer.bindPopup("<strong>" + "Ward " + feature.properties.Ward + "</strong><br/>"+ "Precinct " + feature.properties.Precinct)
    }
  }  );
});

$.getJSON("./data/neighborhoods.geojson",function(hoodData){
	neigh = L.geoJson(hoodData, {
	//specifies styling for neighborhoods
    style: function(feature){
		//initializes fillColor    
		var fillColor,
		//neighborhoods has rat density data encoded in it as below
		density = feature.properties.density;
		//specifies colors
		if ( density > 80 ) fillColor = "#006837";
		else if ( density > 40 ) fillColor = "#31a354";
		else if ( density > 20 ) fillColor = "#78c679";
		else if ( density > 10 ) fillColor = "#c2e699";
		else if ( density > 0 ) fillColor = "#ffffcc";
		else fillColor = "#f7f7f7";  // no data
    //this is rat data so I'm just going to leave it here until we have
    //something more useful, and fill in one fill color for now
		return { color: "#999", weight: 1, fillColor: "#ffffcc", fillOpacity: .4 };
		},
		//adds popup of neighborhood name
    onEachFeature: function( feature, layer ){
      layer.bindPopup( "<strong>" + feature.properties.Name)// + "</strong><br/>" + heat.properties.density + " rats per square mile" )
    }
  }  );
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


//controls highlighted onclick
function dropclick(id){
  var tag = document.getElementById(id);
  //if not already clicked, highlight button and add layer
    if (tag.style.backgroundColor=="papayawhip"){
        tag.style.backgroundColor = "#f9f9f9"; 
        map.removeLayer(heat);//getheat();
    }
    else{
        tag.style.backgroundColor = "papayawhip";
        heat.addTo(map);//getheat();
    }

}

function clickneigh(id){
  var tag = document.getElementById(id);
  //if not already clicked, highlight button and add layer
    if (tag.style.backgroundColor=="papayawhip"){
        tag.style.backgroundColor = "#f9f9f9"; 
        //removes neighborhoods layers
        map.removeLayer(neigh);
        map.removeLayer(cam);
        map.removeLayer(newton);
    }
    else{
        tag.style.backgroundColor = "papayawhip";
        //adds neighborhood layers
        neigh.addTo(map);
        cam.addTo(map)
        newton.addTo(map);
    }

}



