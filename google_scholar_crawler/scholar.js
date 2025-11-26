fetch('/google_scholar_crawler/stats.json')
  .then(r => r.json())
  .then(data => {
      document.getElementById("citations").textContent =
          `${data.citations} citations — h-index: ${data.h_index} — i10-index: ${data.i10_index}`;
  })
  .catch(err => {
      document.getElementById("citations").textContent = "Unavailable";
  });
