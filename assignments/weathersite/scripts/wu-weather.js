var requestURL = '//api.wunderground.com/api/603ff4987cc67f03/conditions/forecast/q/MN/Franklin.json';
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
    
 //for a period of 7days   
    
    document.getElementById('daY1').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['1'].fcttext;
    document.getElementById('iconD1').src = franklinWeather.forecast.txt_forecast.forecastday['1'].icon_url;
    
    document.getElementById('daY2').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['2'].fcttext;
    document.getElementById('iconD2').src = franklinWeather.forecast.txt_forecast.forecastday['2'].icon_url;
    
    document.getElementById('daY3').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['3'].fcttext;
    document.getElementById('iconD3').src = franklinWeather.forecast.txt_forecast.forecastday['3'].icon_url;
    
    document.getElementById('daY4').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['4'].fcttext;
    document.getElementById('iconD4').src = franklinWeather.forecast.txt_forecast.forecastday['4'].icon_url;
    
    document.getElementById('daY5').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['5'].fcttext;
    document.getElementById('iconD5').src = franklinWeather.forecast.txt_forecast.forecastday['5'].icon_url;
    
    document.getElementById('daY6').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['6'].fcttext;
    document.getElementById('iconD6').src = franklinWeather.forecast.txt_forecast.forecastday['6'].icon_url;
    
    document.getElementById('daY7').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['7'].fcttext;
    document.getElementById('iconD7').src = franklinWeather.forecast.txt_forecast.forecastday['7'].icon_url;
    
    /*
    document.getElementById('daY8').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['8'].fcttext;
    document.getElementById('iconD8').src = franklinWeather.forecast.txt_forecast.forecastday['8'].icon_url;
    
    document.getElementById('daY9').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['9'].fcttext;
    document.getElementById('iconD9').src = franklinWeather.forecast.txt_forecast.forecastday['9'].icon_url;
    
    document.getElementById('daY10').innerHTML = franklinWeather.forecast.txt_forecast.forecastday['10'].fcttext;
    document.getElementById('iconD10').src = franklinWeather.forecast.txt_forecast.forecastday['10'].icon_url;
    -->*/
    
};