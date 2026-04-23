let weather = document.getElementById("weather");

function emoji(code) {

const codeString = String(code); 

if (!code || codeString === 'null' || codeString === 'undefined') {
    return '❓';
  }
  else if (codeString.includes("01")) {
    console.log("test2") 
    return "☀️";
  } 
  else if (codeString.includes("02") || codeString.includes("03") || codeString.includes("04")) {
    return "☁️";
  } 
  else if (codeString.includes("09") || codeString.includes("10") || codeString.includes("11")) {
    return "🌧️";
  } 
  else if (codeString.includes("13")) {
    return "❄️";
  }
  else if (codeString.includes("50")) {
    return "🌫️";
  }
  else {
    return "🌎"; 
  }
}

const Dyn_weather = () => {
  if (!navigator.geolocation) {
      return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      try {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        const res = await fetch("/weather", {
          method: "POST",
          headers: { "Content-type": "application/json" },
          body: JSON.stringify({ lat, lon })
        });
        
        //console.log("Test for success");
         
        if (!res.ok) {
            throw new Error(`Server did not respond! ${res.status}`);
        }

        const data = await res.json();
        console.log(data)
        const temp = Math.round(data.main.temp);
        const loc = data.name;
        const code = data.weather[0].icon;
        const details = data.weather[0].main;

        weather.innerHTML = `${emoji(code)} ${temp}°C | ${loc} | ${details}`;
      } catch (err) {
        console.log(`log: ${err.message}`);
      }
    },
    (error) => {
      console.error("Geolocation denied or failed:", error.message);
      weather.innerHTML = "";
    }
  );
};

Dyn_weather();