<?php /**
 * Created by IntelliJ IDEA.
 * User: tal
 * Date: 4/8/17
 * Time: 2:52 AM
 */ ?>


<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="map.css">
  </head>
  <body>
    <h3>My Google Maps Demo</h3>
    <div id="map"></div>
    <script>
      function initMap() {
          var uluru = {lat: -25.363, lng: 131.044};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBqOiPiy5Ru_bNVidCTRzWtt8dZBFjp28s&callback=initMap">
    </script>
  </body>
</html>