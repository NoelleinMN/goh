function confirmFavAdded(results) {
    alert(results);
};


$("#map").on("click", ".favorite-button", (evt) => {
    console.log("nice click");
    console.log(evt.target);
    const button = $(evt.target);
    console.log(button.attr("id")); //check jQuery notes
    // const favParkId = button.attr("id");
    
    // ajax request to server and success function alert to show added)
    const formInputs = {"favParkId":button.attr("id")};
    console.log(formInputs);
    $.post("/api/add_favorite", formInputs, confirmFavAdded);
});



function initMap() {

    $.get("/user_address.json", (data) => {
        const userAddress = data.address;
        console.log(userAddress);
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode(data, (result, status) => {
            if (status === 'OK'){
                const userLocation = result[0].geometry.location;
                console.log(userLocation.lat(), userLocation.lng());
                const userCoords = {lat:userLocation.lat(), lng:userLocation.lng()};
                
                $.get("/user_map.json", userCoords,(response) => {
                    console.log(response);
                    const places = response.results;
                    const userMap = new google.maps.Map(
                        document.querySelector('#map'),
                        {center: userCoords,
                        zoom: 11}
                    );
                    const placeInfo = new google.maps.InfoWindow();
                    for (const place of places){
                        const placeMarker = new google.maps.Marker(
                            {position: {lat:place.geometry.location.lat, lng:place.geometry.location.lng},
                            title: place.name,
                            icon:{url: '/static/images/gold-marker.png'}, // can scale the size later (see bears)
                            map: userMap    
                            }
                        );
                        const placeInfoContent = (`
                        
                        <h3 style="color:rgb(15, 30, 235)">${place.name}</h3>
                        <b><a href="https://duckduckgo.com/?q=\\${place.name}${place.formatted_address}" target=_blank>Learn More about ${place.name}</a></b>
                        <br><br><div class="info"
                        <p><i>${place.formatted_address}</i></p>
                        <p>Avg user rating: <b>${place.rating} / 5 stars</b></p>
                        <p>Location type: <b>${place.types[0]}</b></p>
                        <button class="favorite-button" id="${place.place_id}">Save to favorites</button></div>
                        `);
                        placeMarker.addListener('click', ()=>{
                            placeInfo.close();
                            placeInfo.setContent(placeInfoContent);
                            placeInfo.open(userMap, placeMarker);
                        });
                    }


                });
            }
            else {console.log("Could not geocode this address.")}
        });

    }); 


    }