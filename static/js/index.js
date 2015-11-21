$(window).load(function() {
    var southWest = [43.388313, -80.588576], northEast = [43.501130, -80.432299];
    var data = [[43.472556, -80.542194],[43.472088, -80.537151], [43.472917, -80.537606], [43.472660, -80.538221], [43.472858, -80.537737]];
    var map = L.map('map').setView([43.448954, -80.506585], 13).setMaxBounds(L.latLngBounds(southWest, northEast));
    map.options.minZoom = 12;
    map.options.maxZoom = 18;
    mapLink = 
    '<a href="http://openstreetmap.org">OpenStreetMap</a>';
L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; ' + mapLink + ' Contributors',
    maxZoom: 18,
    }).addTo(map);

var heat = L.heatLayer(data,{
    radius: 20,
    blur: 15, 
    maxZoom: 17,
}).addTo(map);
});
