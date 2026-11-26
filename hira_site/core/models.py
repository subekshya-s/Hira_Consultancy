from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """One row of text that appears across the site (hero, about, contact details)."""

    company_name = models.CharField(max_length=120, default="Hira Engineering Consultancy")
    tagline = models.CharField(max_length=200, default="Engineering that stands the test of time.")
    hero_text = models.TextField(
        default="Design, estimation and supervision for buildings and infrastructure, delivered with technical care."
    )
    about_text = models.TextField(blank=True)
    established = models.CharField(max_length=20, default="2076 B.S.")
    address = models.CharField(max_length=200, default="Koteshwor, Kathmandu")
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.company_name

    @classmethod
    def load(cls):
        """Always return the single settings row, creating it the first time."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers appear first.")
    slug = models.SlugField(max_length=140,blank=True)
    full_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="services/",blank=True)
    icon = models.CharField(max_length=40,blank=True,default="ti-map-2",help_text="Icon name from tabler-icons.io, for example ti-droplet",)
    def save(self,*args,**kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 2
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args,**kwargs)

    
    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=150)
    service = models.ForeignKey("Service",null=True,blank=True,on_delete=models.SET_NULL,related_name="projects",)
    location = models.CharField(max_length=150, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    

    class Meta:
        ordering = ["-year", "name"]

    def __str__(self):
        return self.name

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None


class Stat(models.Model):
    number = models.CharField(max_length=20, help_text="For example 150+")
    label = models.CharField(max_length=60)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.number} {self.label}"


class Partner(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to="partners/")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class QuoteRequest(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"

