var requestURL = '//api.wunderground.com/api/603ff4987cc67f03/conditions/forecast/q/OR/Springfield.json';
var request = new XMLHttpRequest();
request.open('GET', requestURL, true);
request.send();

request.onload = function () {
    var franklinWeather = JSON.parse(request.responseText);
    console.log(franklinWeather);
   
     document.getElementById('desc').innerHTML = franklinWeather.current_observation.display_location.full;
    
    document.getElementById('windSd').innerHTML = franklinWeather.current_observation.wind_mph;
    
     document.getElementById('windDir').innerHTML = franklinWeather.current_observation.wind_dir;
    
     document.getElementById('tempF').innerHTML = franklinWeather.current_observation.temp_f;
    
    
    var icon_path = franklinWeather.current_observation.icon_url;
    var urlString = document.location.href;
    console.log(urlString);
    var found = urlString.indexOf("https");
    console.log(found);
    
    if (found >= 0) {
        icon_path = icon_path.replace("http", "https");
    }
    
    
    document.getElementById('iconImg').src = icon_path;
        
    document.getElementById('iconWd').innerHTML = franklinWeather.current_observation.icon;
    
    document.getElementById('currentPeriod').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['0'].fcttext;
    
    document.getElementById('relativE').innerHTML = franklinWeather.current_observation.relative_humidity;
    
};