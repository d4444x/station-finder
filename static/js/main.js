
$(document).ready(function () {
	var audio = new Audio();
	audio.src ='http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=Hello%20World.';
	//audio.play();
	$(".navbar-nav li a").click(function(event) {
    	$(".navbar-collapse").collapse('hide');
	});

	$("#find").click(getLocation);
	$("#learn").click(learn);
	$("#prefs").click(prefs);
});

function learn(event) {

}

function prefs(event) {

}

function getLocation(event) {
	console.log("Requesting geolocation...");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(handlePosition); // could use watch position instead of get position
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}


function handlePosition(position) {
	console.log("Received geolocation");
	console.log("Requesting address json...");
	$.ajax({ url:'http://maps.googleapis.com/maps/api/geocode/json?latlng='+ position.coords.latitude+','+position.coords.longitude+'&sensor=true',
        	success: handleLocationJson,
        	error: function(error, msg, ex) {
         		console.log("The following error occured: " + msg);
        	}
	});
}

function handleLocationJson(json) { // example data: http://maps.googleapis.com/maps/api/geocode/json?latlng=36.157769099999996,-86.7688226&sensor=true
	console.log("Received address json");
	var zip = json.results[0].address_components[7].long_name;
	console.log("Current Zipcode: " + zip);
	getRadioStation(zip);
}

function getRadioStation(zip) {
	console.log("Requesting station...");
	// $.ajax({ url: '/getStation?zip='+zip,
	// 		success: handleStation,
	// 		error: function(error, msg, ex) {
 //         		console.log("The following error occured: " + msg);
 //         	}
	// });
	handleStation({'station': '89.1'});
}

function handleStation(json) {
	console.log("Received station");
	console.log("Recommended station: " + json.station);
	$("#station").text(json.station);
}