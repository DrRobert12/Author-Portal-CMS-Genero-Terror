# Author-Portal-CMS-Genero-Terror
Sitio en línea especializado en la representación literaria de un escritor de horror.

# 🌑 Author Portal: Horror Genre CMS

[![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_Standalone-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com/)

**Technical Case Study**: Plataforma de autogestión para autores literarios. Este repositorio expone la arquitectura backend, la implementación de patrones de diseño y la estrategia de optimización de recursos en la nube.

---

## 🛠️ Backend Engineering & Design Patterns

### 1. Singleton Pattern Implementation
Para garantizar la integridad de la identidad del autor, se implementó un **Patrón Singleton** a nivel de modelo en Django. Esto restringe la creación de múltiples perfiles, asegurando que el cliente solo pueda editar un único registro de "Autor" y "Mensaje de Bienvenida", evitando errores de redundancia en el frontend.

### 2. Cloud-Native Media Strategy
Se integró **Cloudinary** de forma nativa para el manejo de media. 
* **Beneficio**: Las imágenes se transforman y optimizan automáticamente en el edge, reduciendo el LCP (Largest Contentful Paint) y eliminando el almacenamiento de archivos pesados en el servidor de aplicaciones.

### 3. Honeypot Security Layer
En lugar de utilizar ReCaptcha (que rompe la estética inmersiva del sitio), se desarrolló un **Honeypot dinámico** en el formulario de contacto.
* **Mecánica**: Un campo oculto mediante CSS que, si es completado (comportamiento típico de bots), invalida automáticamente el envío sin alertar al atacante.

---

## 🎨 Dev-Experience: Standalone Tailwind
Una decisión técnica clave fue evitar la dependencia de **Node.js/NPM** en el entorno de producción y desarrollo. 
* Se utilizó el ejecutable **Tailwind Standalone CLI** para compilar el diseño "Void/Blood", simplificando el despliegue y reduciendo la superficie de ataque al no tener una carpeta `node_modules` masiva.

---

## 🚀 Arquitectura de la App

```mermaid
graph LR
    A[Django Admin] -->|Administered by| B(Singleton Models)
    B --> C[(PostgreSQL/SQLite)]
    D[Tailwind CLI] -->|Compiles| E[Static Assets]
    F[User Input] -->|Honeypot Validation| G[Contact App]
    G -->|SMTP| H[Author Email]
    I[Media Upload] -->|API Proxy| J[Cloudinary CDN]
