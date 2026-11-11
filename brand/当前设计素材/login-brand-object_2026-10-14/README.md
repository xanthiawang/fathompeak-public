# 沐仞登录页：旋转品牌岩片

Revision of the login artwork after the user rejected the detached mountain illustration.

- The front carries the existing website mountain symbol, 沐仞科技, and FathomPeak Tech. The back carries 栉风沐雨 / 登高万仞.
- The physical mesh rotates around its vertical axis. Typography is part of the surface texture and follows perspective and lighting. Pointer dragging and arrow keys rotate the mesh; Space toggles pause; Home returns to the front. Automatic rotation resumes four seconds after dragging.
- Exact local fonts: Noto Serif SC (brand/motto subset, OFL) and Fraunces. Generated mineral material is in `../../art/account/brand-mineral_2026-10-14.webp`.
- Three.js r180 is vendored locally with its MIT license. Module and texture load only when the desktop account artwork is visible. Static branded fallback stays available if rendering fails. Reduced-motion, hidden-tab and inactive-route guards stop the automatic loop.
- `index.html` here is a focused responsive review page generated from the website component by `build-preview.py`; the website itself remains the canonical source.
- This revision is local; it has not been published to GitHub Pages.

## Validation

- Browser: full automatic rotation observed, including front, side and correctly oriented back lettering. Pointer drag changes the actual viewing angle; Home and arrow keys work. Pause stops the loop, and resume restores it.
- Desktop login checked at 1280 × 800; no horizontal overflow. Local brand font loaded. Chinese / English control labels and drag instructions switch correctly.
- At 390 × 844 the original mobile form layout remains intact, artwork is hidden and its loop stops.
- Site and focused preview scripts pass Node syntax checks. No browser errors or warnings observed. Reduced-motion and context-recovery paths were reviewed in code; not forced in the browser.

## Reference

https://every.to/?utm_cta_source=studio_main_header_logo_item — observed the rotating, lettered stone and its 10-second looping WebM video. The reference video and logo were not reused.

## Built-in ImageGen texture prompt

Use case: stylized-concept.
Asset type: seamless material/albedo texture for a physically rendered rotating brand tablet. NOT a picture of a stone object.
Fill the entire square canvas with a single continuous flat-facing close-up of finely weathered basalt slate. Very fine mineral grit and shallow irregular natural pitting. Tactile charcoal grey with restrained dusk-purple mineral flecks. Premium editorial tactile print material, broad quiet areas so crisp white Chinese and English typography can later be printed on it. Uniform diffuse flat lighting, absolutely no directional shadow, no vignette, no highlights, no perspective. The surface must stay even in brightness from edge to edge.
Palette target: dominant #48434F and #3D314F, slightly lighter #665E70 flecks. Color muted and close in value. No blue glow, no gold, no neon.
No cracks larger than a hairline, no boulders, no mountain silhouette, no sky, no ground, no frame or visible boundary. No writing or words. Square texture tile, full bleed.
