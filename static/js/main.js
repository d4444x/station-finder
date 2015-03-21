
$(document).ready(function () {	
	


	$(".navbar-nav li a").click(function(event) {
    	$(".navbar-collapse").collapse('hide');
	});

	$("#find").click(getLocation);
	$("#learn").click(learn);

	$("#prefs").click(function(event) {
		$("#main").addClass('hidden');
		$("#prefV").removeClass('hidden');
	});

	$("#save").click(function(event) {
		setCookie("test", "tester");
		console.log(getCookie("test"));
		$("#main").removeClass('hidden');
		$("#prefV").addClass('hidden');
	});
});

function learn(event) {
	if ('speechSynthesis' in window) {
		var msg = new SpeechSynthesisUtterance('Hello World');
    	window.speechSynthesis.speak(msg);
	}	
}

function setCookie(cname, cvalue) {
	var expiration_date = new Date();
	expiration_date.setFullYear(expiration_date.getFullYear() + 1);
	
    document.cookie = cname + "=" + cvalue + "; expires=" + expiration_date.toGMTString();
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
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