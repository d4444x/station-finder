var right = true;
$(document).ready(function () {	
	
	setPrefs();

	if (getCookie('stations') != "") {
		$("#last").removeClass('disabled');
		$("#next").removeClass('disabled');
		next(null);
	}

	$("#last").click(last);
	$("#next").click(next);

	$("#find").click(getLocation);
	$("#learn").click(learn);

	$("#prefs").click(function(event) {
		$("#main").addClass('hidden');
		$("#prefV").removeClass('hidden');
	});

	$("#cancel").click(function(event) {
		$("#main").removeClass('hidden');
		$("#prefV").addClass('hidden');
	});

	$("#save").click(function(event) {		
		save();

		$("#main").removeClass('hidden');
		$("#prefV").addClass('hidden');
	});

	$(".cat").click(function(event) {
        var scroll = $(document).scrollTop();
		if (!$(this).hasClass('btn-selected')) {
			$(this).addClass('btn-selected');
			$(this).append('<span class="pull-right"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span></span>');
		} else {
			$(this).removeClass('btn-selected');
			$(this).html("");
			$(this).text($(this).attr('id'));
		}
        setTimeout(function() {window.scrollTo(scroll,scroll);}, 10);
	});

	$("#select").click(function(event) {
		$(".cat").each(function(index) {
            var scroll = $(document).scrollTop();
			if (!$(this).hasClass('btn-selected')) {
				$(this).addClass('btn-selected');
				$(this).append('<span class="pull-right"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span></span>');
			}
            setTimeout(function() {window.scrollTo(scroll,scroll);}, 10);
		});
	});

	$("#remove").click(function(event) {
		$(".cat").each(function(index) {
            var scroll = $(document).scrollTop();
			if ($(this).hasClass('btn-selected')) {
				$(this).removeClass('btn-selected');
				$(this).html("");
				$(this).text($(this).attr('id'));
			}
            setTimeout(function() {window.scrollTo(scroll,scroll);}, 10);
		});
	});

	$("#reset").click(function(event) {
		delCookie('prefs');
		delCookie('stations')
		location.reload();
	});
});

function last(event) {
	var stations = getCookie("stations").split(',');
	var cur = stations.pop();
	$("#station").html(cur);
	stations.unshift(cur);
	if (right) {
		cur = stations.pop();
		$("#station").html(cur);
		stations.unshift(cur);		
	}
	setCookie('stations', stations)
	right = false;
}

function next(event) {
	var stations = getCookie("stations").split(',');
	var cur = stations.shift();
	$("#station").html(cur);
	stations.push(cur);
	if (!right) {
		cur = stations.shift();
		$("#station").html(cur);
		stations.push(cur);
	}
	setCookie('stations', stations)
	right = true;
}

function save() {
	var prefs = "";
	$(".btn-selected").each(function(index) {
		prefs += $(this).attr('id') + ",";
	});

	setCookie('prefs', prefs);
}

function setPrefs() {
	if (getCookie('prefs') != "") {
		var prefs = getCookie('prefs').split(',');
		prefs.pop(); // gets rid of the last comma's empty item
		for(var pref in prefs) {
			$("#"+prefs[pref]).addClass('btn-selected');
			$("#"+prefs[pref]).append('<span class="pull-right"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span></span>');
		}
	}
}

function learn(event) {
	console.log("Requesting facts...");
	// $.ajax({ url: '/getStation?zip='+zip,
	// 		success: handleStation,
	// 		error: function(error, msg, ex) {
    //      		console.log("The following error occured: " + msg);
    //         	}
	// });
	handleLearn({'msg': 'This is a test'});
}

function handleLearn(json) {
	console.log("Received info");
	if ('speechSynthesis' in window) {
		var msg = new SpeechSynthesisUtterance(json.msg);
    	window.speechSynthesis.speak(msg);
	} else {
		alert("Your browser does not support SpeechSynthesisUtterance")
		console.log("SpeechSynthesisUtterance not supported")
		var audio = new Audio();
		audio.src = 'http://translate.google.com/translate_tts?ie=UTF-8&q=Hello%20World&tl=en-us';
		audio.play();
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

function delCookie(cname) {
	var expiration_date = new Date();
	expiration_date.setFullYear(expiration_date.getFullYear() + 1);
	
    document.cookie = cname + "=;expires=Thu, 01 Jan 1970 00:00:01 GMT;";
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
	var state = json.results[0].address_components[5].long_name;
	var city = json.results[0].address_components[3].long_name;
	var lng = json.results[0].geometry.location.lng;
	var lat = json.results[0].geometry.location.lat;
	console.log("Current Zipcode: " + zip);
	getRadioStation([city, state, zip, lng, lat]);
}

function getRadioStation(data) {
	console.log("Requesting station...");
	$.ajax({ url: '/get_station?city='+data[0]+
					'&state='+data[1]+
					'&zip='+data[2]+
					'&categories='+getCookie('prefs')+
					'&lng='+data[3]+
					'&lat='+data[4],
			success: handleStation,
			error: function(error, msg, ex) {
            		console.log("The following error occured: " + msg);
            	}
	});
}

function handleStation(json) {
	console.log("Received station");
	console.log("Recommended stations: " + json.stations);
	var stations = json.stations.join(",");
	if (stations.length == 0) {
		return;
	}
	$("#last").removeClass('disabled');
	$("#next").removeClass('disabled');
	setCookie('stations', stations);
	next(null);
}