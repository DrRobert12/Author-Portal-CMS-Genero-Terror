from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    # AGREGADO: Campo slug único
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    editorial = models.CharField(max_length=255, blank=True)
    sinopsis = models.TextField(blank=True)
    descripcion = models.TextField(blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    portada = CloudinaryField("image", folder="libros/portadas", blank=True, null=True)
    enlace_compra = models.URLField(blank=True)
    destacado = models.BooleanField(default=False)

    # AGREGADO: Método para obtener la URL absoluta 
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('libro_detalle', kwargs={'slug': self.slug})

    class Meta:
        ordering = ["-destacado", "-fecha_publicacion", "titulo"]

    def __str__(self) -> str:
        return self.titulo

    # AGREGADO: Autogeneración del slug al guardar (Igual que en Articulo)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)[:50]
            slug = base_slug
            contador = 1
            # Evita duplicados
            while Libro.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    # Fecha y hora completa del evento para poder separar próximos/pasados
    fecha_hora = models.DateTimeField(null=True, blank=True)
    # Campo de solo fecha opcional, útil para mostrar o migrar datos antiguos
    fecha = models.DateField(null=True, blank=True)
    lugar = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)
    enlace = models.URLField(blank=True)
    flyer = CloudinaryField("image", folder="eventos", blank=True, null=True)

    class Meta:
        ordering = ["-fecha_hora", "-fecha", "titulo"]

    def __str__(self) -> str:  # type: ignore[override]
        return self.titulo


class HeroSlide(models.Model):
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255, blank=True)
    imagen_fondo = CloudinaryField("image", folder="hero_slides", blank=False, null=False)
    cta_texto = models.CharField(max_length=100, default="Ver más")
    cta_enlace = models.URLField(blank=True)
    orden = models.PositiveIntegerField(default=0, help_text="Controla el orden de aparición en el carrusel.")
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self) -> str:  # type: ignore[override]
        return self.titulo


class MensajeAutor(models.Model):
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    imagen_firma = CloudinaryField("image", folder="autor", blank=True, null=True)

    class Meta:
        verbose_name = "Mensaje del autor"
        verbose_name_plural = "Mensaje del autor"

    def __str__(self) -> str:  # type: ignore[override]
        return self.titulo

    def clean(self):
        # Evitar más de una instancia en total (patrón singleton sencillo)
        if not self.pk and MensajeAutor.objects.exists():
            raise ValidationError("Solo puede existir un MensajeAutor. Edita el existente en lugar de crear uno nuevo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class PerfilAutor(models.Model):
    nombre_completo = models.CharField(max_length=255)
    biografia = models.TextField()
    foto_principal = CloudinaryField("image", folder="autor/perfil", blank=True, null=True)
    cita_destacada = models.TextField()
    premios_reconocimientos = models.TextField(blank=True)
    # Opcional: enlaces para kit de prensa
    foto_prensa_url = models.URLField(blank=True)
    bio_corta_pdf_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Perfil del autor"
        verbose_name_plural = "Perfil del autor"

    def __str__(self) -> str:  # type: ignore[override]
        return self.nombre_completo

    def clean(self):
        # Singleton: solo puede existir un PerfilAutor
        if not self.pk and PerfilAutor.objects.exists():
            raise ValidationError("Solo puede existir un PerfilAutor. Edita el existente en lugar de crear uno nuevo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Podcast(models.Model):
    class Plataforma(models.TextChoices):
        SPOTIFY = "spotify", "Spotify"
        YOUTUBE = "youtube", "YouTube"
        APPLE = "apple_podcasts", "Apple Podcasts"
        RADIO = "radio", "Radio"
        INTAGRAM = "instagtam", "Instagram"

    titulo = models.CharField(max_length=255)
    descripcion_corta = models.TextField()
    plataforma = models.CharField(max_length=32, choices=Plataforma.choices)
    url_externa = models.URLField()
    imagen_cover = CloudinaryField("image", folder="podcasts", blank=True, null=True)
    fecha = models.DateField(null=True, blank=True)
    destacado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-destacado", "-fecha", "titulo"]
        verbose_name = "Podcast / Entrevista"
        verbose_name_plural = "Podcasts / Entrevistas"

    def __str__(self) -> str:  # type: ignore[override]
        return self.titulo


class Articulo(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"

    titulo = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    extracto = models.TextField(blank=True)
    contenido = RichTextField()
    imagen_destacada = CloudinaryField("image", folder="blog", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
    )

    class Meta:
        ordering = ["-fecha_publicacion", "titulo"]
        verbose_name = "Artículo del blog"
        verbose_name_plural = "Artículos del blog"

    def __str__(self) -> str:  # type: ignore[override]
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)[:50]
            slug = base_slug
            contador = 1
            while Articulo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ArticuloImagen(models.Model):
    articulo = models.ForeignKey(
        Articulo,
        related_name="imagenes",
        on_delete=models.CASCADE,
    )
    imagen = CloudinaryField("image", folder="blog", blank=False, null=False)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Imagen del artículo"
        verbose_name_plural = "Imágenes del artículo"

    def __str__(self) -> str:  # type: ignore[override]
        return f"Imagen de {self.articulo.titulo}"
