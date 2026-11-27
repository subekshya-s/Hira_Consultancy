// Reads the pins that the Django view sent, and draws them on the map.
(function () {
  const el = document.getElementById("project-map");
  if (!el || typeof L === "undefined") return;

  const points = JSON.parse(document.getElementById("map-points").textContent);

  // Start on Nepal; zoom to the pins if there are any.
  const map = L.map(el, { scrollWheelZoom: false }).setView([28.3949, 84.124], 21);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 22,
  maxNativeZoom: 19,
  
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

    // Districts layer: all 77 outlined, the districts with projects filled in
  const districtsUrl = el.dataset.districts;
  if (districtsUrl) {
    const worked = new Set(points.map((p) => p.location.trim().toLowerCase()));
    fetch(districtsUrl)
      .then((res) => res.json())
      .then((data) => {
        const layer = L.geoJSON(data, {
          style: (feature) =>
            worked.has(feature.properties.name.toLowerCase())
              ? { color: "#1F3FBF", weight: 1.5, fillColor: "#1F3FBF", fillOpacity: 0.35 }
              : { color: "#8D97BE", weight: 0.6, fillOpacity: 0 },
          onEachFeature: (feature, polygon) => {
            if (worked.has(feature.properties.name.toLowerCase())) {
              polygon.bindTooltip(feature.properties.name);
            }
          },
        }).addTo(map);
        const bounds = layer.getBounds();
        map.setMaxBounds(bounds.pad(0.15));
        map.setMinZoom(map.getBoundsZoom(bounds));
      });
  }

  const icon = L.divIcon({ className: "pin", iconSize: [7, 7], iconAnchor: [3.5, 3.5] });
  const markers = points.map((p) => {
    // textContent (not innerHTML) so a project name can never inject HTML.
    const popup = document.createElement("div");
    const name = document.createElement("strong");
    name.textContent = p.name;
    const place = document.createElement("div");
    place.textContent = p.location;
    popup.append(name, place);
    return L.marker([p.lat, p.lng], { icon }).bindPopup(popup).addTo(map);
  });

  if (markers.length) {
    map.fitBounds(L.featureGroup(markers).getBounds().pad(0.1), { maxZoom: 12 });
  }
})();
