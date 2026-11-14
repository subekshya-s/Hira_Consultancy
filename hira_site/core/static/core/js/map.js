// Reads the pins that the Django view sent, and draws them on the map.
(function () {
  const el = document.getElementById("project-map");
  if (!el || typeof L === "undefined") return;

  const points = JSON.parse(document.getElementById("map-points").textContent);

  // Start on Nepal; zoom to the pins if there are any.
  const map = L.map(el, { scrollWheelZoom: false }).setView([28.3949, 84.124], 7);
 L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

  const icon = L.divIcon({ className: "pin", iconSize: [16, 16], iconAnchor: [8, 8] });
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
    map.fitBounds(L.featureGroup(markers).getBounds().pad(0.3), { maxZoom: 12 });
  }
})();
