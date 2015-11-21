$(document).ready(function(){
    $('#example').DataTable({
        'searching': false
    });
});

function initialize() {
    var pos = {lat: 43.4689, lng: -80.5400};

    var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: pos
    });

    var marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: 'Address:'
    });
}
window.addEventListener('load', initialize);
