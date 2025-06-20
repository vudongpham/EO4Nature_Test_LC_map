const max_zoom = 15
const tile_center = [52.52337,8.82571]

var map = L.map('map', {
    center: tile_center,
    zoom: 11,
    minZoom: 8,  // Minimum zoom level
    maxZoom: max_zoom   // Maximum zoom level
});

var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: max_zoom,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: max_zoom,
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

var baseMaps = {
    "OpenStreetMap": osm,
    "Esri satellite": Esri_WorldImagery,
};

Esri_WorldImagery.addTo(map)
L.control.layers(baseMaps).addTo(map);

tile_map = L.tileLayer('data/images/tiles/{z}/{x}/{y}.webp', {tms:true});
tile_map.addTo(map);
tile_map.bringToFront();


var slider = document.getElementById('slider');
var sliderValue = document.getElementById('slider-value');

slider.addEventListener('input', function(e) {
    tile_map.setOpacity(parseInt(e.target.value, 10) / 100)
    sliderValue.textContent = e.target.value + '%';
});