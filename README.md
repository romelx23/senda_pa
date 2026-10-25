# Landing de Senda Pa

Sitio estático, sin framework, sin build, sin cookies y sin dependencias externas. Es un proyecto independiente del juego: no necesita Godot para servirse y se puede subir a cualquier hosting estático tal cual.

Repositorio: <https://github.com/romelx23/senda_pa>

## Rutas

- `/` — landing principal.
- `/privacidad/` — política de privacidad.
- `/terminos/` — términos de uso.

Cuando actives GitHub Pages, la URL para Google Play Console será:

```text
https://romelx23.github.io/senda_pa/privacidad/
```

## Probar en local

Desde esta carpeta:

```powershell
python -m http.server 4173
```

Abre `http://127.0.0.1:4173/`.

## Publicar

### GitHub Pages

1. Entra en **Settings → Pages** de este repositorio.
2. En **Build and deployment**, elige **Deploy from a branch**, rama `main` y carpeta `/ (root)`.
3. La landing queda en `https://romelx23.github.io/senda_pa/` y la privacidad en `https://romelx23.github.io/senda_pa/privacidad/`.
4. El archivo `.nojekyll` ya está incluido para que GitHub Pages no procese el sitio con Jekyll.

### Netlify

1. Entra en [Netlify Drop](https://app.netlify.com/drop).
2. Arrastra esta carpeta.
3. La privacidad queda en `https://NOMBRE.netlify.app/privacidad/`.
4. Si quieres un dominio propio, añádelo en Domain settings.

### Cloudflare Pages

1. Crea un proyecto con "Direct upload".
2. Sube esta carpeta.
3. La privacidad queda en `https://NOMBRE.pages.dev/privacidad/`.

### Dominio propio

Si compras `sendapa.app` o similar, apunta el dominio al hosting y usa:

```text
https://sendapa.app/privacidad/
```

No hace falta cambiar las rutas: las páginas usan enlaces relativos.

## Antes de publicar

- **El correo `hola@sendapa.app` es un marcador de posición.** Reemplázalo en `index.html`, `privacidad/index.html` y `terminos/index.html` por un correo real que revises antes de publicar. Play Console pide un contacto de privacidad que funcione.
- Revisa la fecha de "Última actualización" en las dos páginas legales.
- Si publicas en GitHub Pages, cambia `og:image` por una URL absoluta (por ejemplo `https://romelx23.github.io/senda_pa/assets/og-image.jpg`) para que las vistas previas sociales funcionen. Si usas un dominio propio, usa la URL de ese dominio.
- Comprueba que la política sigue siendo cierta si añades anuncios, compras, analítica o un backend. En ese caso hay que actualizarla **antes** de publicar la función.
- No subas la carpeta de claves del juego ni `CREDENCIALES.txt`. No forman parte del sitio.

## Regenerar capturas y assets

Si cambias las capturas del juego, ejecuta desde esta carpeta:

```powershell
python tools/prepare_site_assets.py
```

El script lee las capturas de `..\flutter\cubil\docs\` y `..\flutter\cubil\build\` y escribe aquí las versiones WebP, el icono, el favicon, la textura de papel y la imagen Open Graph. Si el proyecto de Godot está en otra ruta, define la variable de entorno `SENDA_PA_GAME` con la ruta correcta.

`tools/` solo se usa para mantenimiento; la web publicada no lo necesita.

## Créditos

- Tipografías: **Fredoka** y **Nunito**, SIL Open Font License. El texto completo de la licencia está en `assets/fonts/OFL.txt`.
- Capturas y arte: Senda Pa.
- Hecho con Godot.
