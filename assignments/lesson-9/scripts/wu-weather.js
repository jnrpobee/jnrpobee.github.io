
var requestURL = 'http://api.wunderground.com/api/603ff4987cc67f03/conditions/forecast/q/MN/Franklin.json';
var request = new XMLHttpRequest();
request.open('GET', requestURL, true );
request.send();

request.onload = function() {
    var franklinWeather = JSON.parse(request.responseText);
    console.log(franklinWeather);
    
     document.getElementById('desc').innerHTML = franklinWeather.current_observation.display_location.full;
    
    document.getElementById('windSd').innerHTML = franklinWeather.current_observation.wind_mph;
    
     document.getElementById('windDir').innerHTML = franklinWeather.current_observation.wind_dir;
    
     document.getElementById('tempF').innerHTML = franklinWeather.current_observation.temp_f;
    
    document.getElementById('iconImg').src = franklinWeather.current_observation.icon_url;
    
        
    document.getElementById('iconWd').innerHTML = franklinWeather.current_observation.icon;
    
    document.getElementById('currentPeriod').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['0'].fcttext;
    
    document.getElementById('relativE').innerHTML = franklinWeather.current_observation.relative_humidity;
    
}

return function();
