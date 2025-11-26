fetch('stats.json?nocache=' + Date.now())
  .then(response => response.json())
  .then(data => {
      document.getElementById("citations").textContent =
          `${data.citations} citations — h-index: ${data.h_index} — i10-index: ${data.i10_index}`;
  })
  .catch(error => {
      console.error("Error loading stats.json:", error);
      document.getElementById("citations").textContent = "Unavailable";
  });
