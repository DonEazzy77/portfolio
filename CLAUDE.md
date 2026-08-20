# CLAUDE.md — torsten-guenter.de

Projektregeln für agentische Arbeit an diesem Repo. Kurz halten; Ausführliches gehört ins
Playbook (`_Hub/playbooks/webprojekt_playbook.md`) oder in die Übergabe
(`_Hub/Uebergaben/uebergabe_portfolio.md`).

## Veröffentlichen

- **Netlify deployt bei jedem Push sofort live.** Nicht pushen — Torsten pusht selbst nach
  lokalem Blick. Lokal bauen und committen ist jederzeit erlaubt.
- Commit-Autor ist immer Torsten.
- Kein `git add -A`. Nur die Dateien stagen, die zum Auftrag gehören.

## Kommentare

- **Wer eine Seite anfasst, stellt ihre Kommentare im selben Zug auf JSX um.** `<!-- -->` landet
  im ausgelieferten Quelltext, `{/* */}` nicht. Interne Strukturmarken, Kundennamen,
  Freigabestände und Notizen zu unfertigen Funktionen gehören deshalb nie in HTML-Kommentare.
- Beim Umstellen nur die Template-Region anfassen (zwischen schließendem Frontmatter-`---` und
  dem ersten `<script>`/`<style>`). Innerhalb von `<style>`/`<script>` bedeutet `<!-- -->` etwas
  anderes. `<!doctype html>` ist kein Kommentar.

## Bilder

- Astro optimiert nur Dateien aus `src/assets/` (dort automatisch WebP). Alles unter `public/`
  wird 1:1 ausgeliefert. **Fotos und Screenshots nach `src/assets/` + `<Image>`**, Vektoren und
  Assets mit festem Pfad nach `public/`.
- Jedes `<img>` bekommt `width`/`height` (gegen Layout-Sprünge).
- SVGs, die per `set:html` eingebunden werden, brauchen `width`/`height` **als Attribut im SVG** —
  scoped CSS greift dort nicht.

## Struktur

- Anker-Ziele auf `/arbeiten` immer mit `style="scroll-margin-top: 6rem;"` (fixierte Navigation).
- `public/sitemap.xml` ist handgepflegt: neue Seite = neuer Eintrag, kanonische Form mit
  Trailing Slash.
- `BaseLayout` spiegelt og:/twitter: aus `title`/`description`. Für zu lange SEO-Titel gibt es
  `ogTitle`/`ogDescription` als Override — die Texte kommen aus S&R/Biz, hier wird nichts
  gekürzt und nichts umformuliert.
- Tailwind v4: `gap-*` ist buggy → stattdessen Inline-`style` mit `clamp()`.

## Copy

- **Fließtexte, Überschriften, Alt-Texte und CTA-Wording werden hier nicht erfunden und nicht
  umformuliert.** Sie kommen als freigegebener Stand aus dem jeweiligen Auftrag. Wer einen
  Textfehler findet, meldet ihn, statt ihn zu beheben.
