"use strict";

function initMap() {
  const map = new google.maps.Map($('#map')[0], {
    center: {
      lat: 44,
      lng: -97
    },
    scrollwheel: false,
    zoom: 5,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    // styles: MAPSTYLES,  // mapStyles is defined in mapstyles.js
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  // When a user clicks on a bear, an info window about that bear will appear.
  //
  // When they click on another bear, we want the previous info window to
  // disappear, so that only one window is open at a time.
  //
  // To do this, we'll define a single InfoWindow instance. All markers will
  // share this instance.
  const parkInfo = new google.maps.InfoWindow();

  // Retrieving the information with AJAX.
  //
  // If you want to see what `/api/bears` returns, you should check `server.py`
  $.get('/api/user_parks', (userParks) => {
    for (const park of userParks) {
      // Define the content of the infoWindow
      const parkInfoContent = (`
        <div class="window-content">
          <div class="bear-thumbnail">
            <img
              src="/static/img/runtime.png"
              alt="runtime"
            />
          </div>

          <ul class="park-info">                            
            <li><b>Bear gender: </b>${userParks.gender}</li>
            <li><b>Bear birth year: </b>${userParks.birthYear}</li>
            <li><b>Year captured: </b>${userParks.capYear}</li>
            <li><b>Collared: </b>${userParks.collared}</li>
            <li><b>Location: </b>${userParks.capLat}, ${userParks.capLong}</li>
          </ul>
        </div>
      `);

      // ABOVE ^^^ need data variable names // BELOW VVV need lat/long and data variable names

      const parkMarker = new google.maps.Marker({
        position: {
          lat: userParks.capLat,
          lng: userParks.capLong
        },
        title: `Park Name: ${userParks.bearId}`,
        icon: {
          url: '/static/img/white-marker.png',
          scaledSize: new google.maps.Size(50, 50)
        },
        map: map,
      });

      parkMarker.addListener('click', () => {
        parkInfo.close();
        parkInfo.setContent(parkInfoContent);
        parkInfo.open(map, parkMarker);
      });
    }
  }).fail(() => {
    alert((`
      We were unable to retrieve data about parks :(

    `));
  });

  // Google Maps also provides a built-in control panel that allows users to
  // toggle different map styles.
  //
  // Here's how you do it:
  //
  // Create a new StyledMapType object, passing it the array of styles,
  // as well as the name of the map style.
  //
  // The name will be displayed in a button on the map-type control panel.
  //
  // const styledMap = new google.maps.StyledMapType(
  //  MAPSTYLES,
  //  { name: "Arctic Map" }
  // );
  //
  // You would then set 'styles' in Map() constructor's options to 'styledMap'.
  // For example:
  //
  // const map = new google.maps.Map(document.getElementById('bear-map', {
  //   center: mapCenter,
  //   // ... etc.
  //   styles: styledMap
  // });
  //
  // Finally, you must associate the styled map with the MapTypeId and
  // set it to display.
  //
  // map.mapTypes.set('map_style', styledMap);
  // map.setMapTypeId('map_style');
}

