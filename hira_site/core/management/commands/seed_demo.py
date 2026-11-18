from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Project, Service, SiteSettings, Stat

PHOTOS = Path(__file__).resolve().parents[2] / "seed_photos"

ABOUT = (
    "Hira Engineering Consultancy is a Nepal-based consultancy established in 2019 (2076 B.S.). "
    "It began as a field-oriented survey and engineering practice and has grown into hydropower "
    "survey, transmission-line survey, UAV-LiDAR mapping and technical reporting.\n\n"
    "Our approach links field control, terrain data, river information, GIS, CAD and engineering "
    "documentation in one workflow, so project layouts rest on reliable, consistent data. "
    "For multidisciplinary studies we bring in specialists as each project requires."
)

SERVICES = [
    ("Survey & UAV-LiDAR Mapping",
     "UAV-LiDAR, GNSS/DGPS/RTK control, total-station and levelling survey, river profiles and cross-sections."),
    ("Transmission Line Survey",
     "Route and detailed topographical survey for power lines from 33 kV to 220 kV, with plan-profile and GIS outputs."),
    ("Hydrology & Hydromet",
     "Catchment and rainfall analysis, river discharge measurement, flow and flood assessment, and gauge monitoring."),
    ("Planning & Feasibility",
     "Desk studies, alternative layouts and capacity assessment, with cost, schedule and risk inputs for feasibility and DPR reports."),
    ("Engineering Design & Documentation",
     "CAD drawings, plan-profile and sections, road and drainage design, quantities, cost estimates and technical reports."),
    ("Master Planning & Infrastructure",
     "Site planning, public facilities, parks, roads, bridges, land development and boundary demarcation."),
]

STATS = [
    ("11", "LiDAR hydropower surveys"),
    ("7", "Districts covered"),
    ("159.11 km", "Certified transmission-line survey"),
    ("2019", "Established"),
]

# Pins are district-level, not project sites. Coordinates are approximate and slightly spread
# so projects in the same district do not sit on top of each other.
# (name, location, year, description, lat, lng, featured, photo)
PROJECTS = [
    ("Super Humla Karnali Nadi HPP (152.725 MW)", "Humla", 2026,
     "UAV-LiDAR topographical survey with GNSS-supported control, flown with a Matrice 400 and Zenmuse L3 "
     "during a six-day deployment in June 2026. Delivered terrain models, profiles and CAD/GIS data.",
     29.96, 81.78, True, "super_humla.jpg"),
    ("Hilsa Karnali HPP (80.3 MW)", "Humla", 2026,
     "UAV-LiDAR based topographical survey with GNSS control, mapping and a field report in high Himalayan terrain.",
     30.02, 81.88, True, "hilsa_karnali.jpg"),
    ("Myardi Khola HPP (30 MW)", "Lamjung", 2026,
     "UAV-LiDAR based survey with terrain products, profiles and a report along the access and project corridor.",
     28.30, 84.40, True, "myardi_khola.jpg"),
    ("Chyamni Khola HPP (19.5 MW)", "Mugu", 2026,
     "UAV-LiDAR survey with GNSS control, point cloud, terrain products, mapping and a field report.",
     29.58, 82.05, True, "chyamni_khola.jpg"),
    ("Talak Khola HPP (7.49 MW)", "Mugu", None, "", 29.50, 82.14, False, ""),
    ("Shobha Khola HPP (7 MW)", "Mugu", None, "", 29.62, 82.18, False, ""),
    ("Rauli Khola HPP (7.4 MW)", "Humla", None, "", 29.90, 81.92, False, ""),
    ("Super Irkhuwa Khola HPP (5 MW)", "Bhojpur", None, "", 27.17, 87.05, False, ""),
    ("Super Dar Khola HPP (3 MW)", "Myagdi", 2026, "", 28.40, 83.50, False, ""),
    ("Satiya Khola HPP (7 MW)", "Jajarkot", None, "", 28.70, 82.20, False, ""),
    # District differs between the two company documents, so no location or pin until confirmed.
    ("Alle Khola HPP (4.69 MW)", "", None, "", None, None, False, ""),
]


class Command(BaseCommand):
    help = "Load Hira's real company content. Use --reset to replace content that is already there."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing services, stats and projects first.")

    def handle(self, *args, **options):
        reset = options["reset"]
        if reset:
            Service.objects.all().delete()
            Stat.objects.all().delete()
            Project.objects.all().delete()

        site = SiteSettings.load()
        if reset or not site.about_text:
            site.company_name = "Hira Engineering Consultancy"
            site.tagline = "A complete engineering and geospatial solution"
            site.hero_text = (
                "Survey-led engineering for hydropower and infrastructure: UAV-LiDAR, GNSS control, "
                "terrain models and engineering documentation."
            )
            site.about_text = ABOUT
            site.established = "2076 B.S."
            site.address = "Koteshwor-32, Kathmandu, Nepal"
            site.phone = "+977 9851407332"
            site.email = "hira.eng.cpl@gmail.com"
            site.save()

        if not Service.objects.exists():
            for i, (title, desc) in enumerate(SERVICES, start=1):
                Service.objects.create(title=title, description=desc, order=i)

        if not Stat.objects.exists():
            for i, (number, label) in enumerate(STATS, start=1):
                Stat.objects.create(number=number, label=label, order=i)

        if not Project.objects.exists():
            for name, location, year, desc, lat, lng, featured, photo in PROJECTS:
                project = Project.objects.create(
                    name=name, location=location, year=year, description=desc,
                    latitude=lat, longitude=lng, featured=featured,
                )
                path = PHOTOS / photo if photo else None
                if path and path.exists():
                    with path.open("rb") as fh:
                        project.image.save(photo, File(fh), save=True)

        self.stdout.write(self.style.SUCCESS("Hira content loaded."))
