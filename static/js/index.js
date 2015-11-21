function loadData(callback) {
    d3.json('data', function(error, data){
        callback(data);
    });
}

$(window).load(function() {
    loadData(function(data) {
    // var southWest = [43.388313, -80.588576], northEast = [43.501130, -80.432299];
    var southWest = [43.388313, -80.588576], northEast = [43.558371, -80.409971];
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

    // var raw = [[43.472556, -80.542194],[43.472088, -80.537151], [43.472917, -80.537606], [43.472660, -80.538221], [43.472858, -80.537737]];
    // var data = raw.map(function(latlng) {
    //     return {latlng: latlng, freq: Math.floor(Math.random() * 50)};
    // });
    //
    data = data.map(function(d) {
        if (d.name.indexOf("SOGO") != -1) console.log(d);
        return {latlng: [d.latitude, d.longitude], name: d.name, freq: d.infractions};
    });

    map._initPathRoot();
    var svg = d3.select("#map").select("svg"),
    g = svg.append('g');
    var infobox = d3.select('#map').append('div')
                  .attr('class', 'infobox');

    infobox.append('div').attr('class', 'name');
    var small = 5, large = 10;
    var maxInfractions = 50;
    var dots = g.selectAll('circle')
        .data(data)
        .enter().append('circle')
        .style('stroke', 'black')
        .style('opacity', .9)
        .style('fill', function (d) {
            var red = (Math.floor((d.freq/maxInfractions)*255));
            var color = 'rgb('+red+','+(255-red)+',0)';
            return color;
        })
        .style("cursor", "pointer")
        .attr('r', small);

    map.on('viewreset', update);
    update();

    function update() {
        dots.attr('transform', function (d) {
            return 'translate('+map.latLngToLayerPoint(d.latlng).x+','+
                map.latLngToLayerPoint(d.latlng).y+')';
        });
    }
    dots.on('mouseover', function(d) {
        d3.select(this).attr('r', large);
        infobox.select('.name').html(d.name);
        infobox.style('display', 'block');
    });
    dots.on('mouseout', function(d) {
        d3.select(this).attr('r', small);
        infobox.style('display', 'none');
    });
    dots.on('mouseclick', function(d) {
        alert('hi');
    });
    dots.on('mousemove', function(d) {
        infobox.style('top', (d3.event.pageY - $("#map")[0].getBoundingClientRect().top + 2) + 'px')
        .style('left', (d3.event.pageX - $("#map")[0].getBoundingClientRect().left + 2) + 'px');
        // infobox.style('top', (d3.mouse(this)[1] + 2) + 'px')
        // .style('left', (d3.mouse(this)[0] + 2) + 'px');
    });

    // var heat = L.heatLayer(data,{
    //     radius: 20,
    //     blur: 15,
    //     maxZoom: 17,
    // }).addTo(map);
    
    });
});
