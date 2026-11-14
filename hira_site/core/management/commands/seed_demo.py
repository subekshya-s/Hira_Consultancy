from django.core.management.base import BaseCommand

from core.models import Project, Service, SiteSettings, Stat

SERVICES = [
    ("Structural Design", "Safe, economical structural design and analysis for buildings."),
    ("Architectural Design", "Plans, elevations and layouts that fit your site and budget."),
    ("Cost Estimation & BOQ", "Detailed quantity and cost estimates before work begins."),
    ("Construction Supervision", "On-site monitoring for quality, safety and schedule."),
    ("Land Survey & Mapping", "Topographic and boundary surveys to support design."),
    ("Project Management", "Planning, coordination and reporting from start to handover."),
]


class Command(BaseCommand):
    help = "Fill an empty database with placeholder content so the demo site looks complete."

    def handle(self, *args, **options):
        site = SiteSettings.load()
        if not site.about_text:
            site.about_text = (
                "Hira Engineering Consultancy has served clients from Koteshwor since 2076 B.S. "
                "[ADD: what the firm does, your team and the kinds of projects you take on.]"
            )
            site.save()

        if not Service.objects.exists():
            for i, (title, desc) in enumerate(SERVICES, start=1):
                Service.objects.create(title=title, description=desc, order=i)

        if not Stat.objects.exists():
            for i, label in enumerate(
                ["Projects completed", "Years of experience", "Clients served", "Active sites"], start=1
            ):
                Stat.objects.create(number="[00]+", label=label, order=i)

        if not Project.objects.exists():
            Project.objects.create(
                name="[PROJECT NAME]", location="Koteshwor", year=2024, featured=True,
                description="[ADD: two or three sentences on the project, its scope and size.]",
                latitude=27.6770, longitude=85.3470,
            )
            Project.objects.create(
                name="[PROJECT NAME]", location="Lalitpur", year=2023, featured=True,
                description="[ADD: two or three sentences on the project, its scope and size.]",
                latitude=27.6588, longitude=85.3247,
            )

        self.stdout.write(self.style.SUCCESS("Demo content added."))
