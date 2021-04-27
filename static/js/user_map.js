function confirmFavAdded(results) {
    alert(results);
};


$("#map").on("click", ".favorite-button", (evt) => {
    console.log("nice click");
    console.log(evt.target);
    const button = $(evt.target);
    console.log(button.attr("id")); //check jQuery notes
    // const favParkId = button.attr("id");
    // make ajax request to server (need new route to receive args, make endpoint request, and crud function to add to fav parks table - post??, alert to show added)

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
                            icon:{url:place.icon}, // can scale the size later (see bears)
                            map: userMap    
                            }
                        );
                        const placeInfoContent = (`
                        <h1>${place.name}</h1>
                        <p>${place.formatted_address}</p>
                        <button class="favorite-button" id="${place.place_id}">Save to favorites</button>
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