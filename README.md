# Nitro Dome

Autoball in einer achteckigen Neon-Kuppel — Raketenautos, ein übergroßer Ball, zwei Tore.
Three.js, eigene Physik, keine Engine, keine Assets.

**Spielen:** https://madd1in.github.io/nitro-dome/

## Steuerung

| Aktion | Taste |
| --- | --- |
| Gas / Rückwärts | `W` · `S` |
| Lenken | `A` · `D` |
| Sprung / Flip | `Leertaste` |
| Boost | `Shift` |
| Driften · Luftrolle | `Strg` |
| Kamera umschalten | `C` |
| Wiederholung | `R` |
| Quick-Chat | `1` – `4` |
| Musik · Ton | `N` · `M` |
| Vollbild · Pause | `F` · `Esc` |

Gamepad wird unterstützt (`RT` Gas, `LT` Bremse, `A` Sprung, `B`/`X` Boost, Schultertasten Drift),
auf Touch-Geräten erscheinen automatisch Bildschirmtasten.

Der zweite Sprung mit gedrückter Richtung ist ein **Flip** — die stärkste Schussquelle im Spiel.
Mit Überschall (> 88 Einheiten/s) zerlegst du gegnerische Autos.

## Wie es funktioniert

**Eine Signed Distance Field beschreibt die Arena.** Dieselbe Funktion erzeugt das Mesh
und beantwortet jede Kollisionsabfrage, deshalb decken sich Optik und Trefferzone exakt.
Die Verrundung zwischen Boden und Wand ist der Grund, warum echtes Wandfahren funktioniert:
Das Auto klebt oberhalb einer Mindestgeschwindigkeit an der Fläche und fällt darunter ab.
Die Tormäuler werden im Wand-Shader per `discard` ausgeschnitten, statt die Geometrie zu zerschneiden.

**Fahrphysik** mit Beschleunigungskurve, Seitenführung, Driftmodus, Boost, Doppelsprung,
gerichtetem Flip mit Drehimpuls und voller Luftkontrolle über Nick-, Gier- und Rollachse.

**Die KI simuliert den Ball voraus** (105 Schritte à 1/30 s inklusive Wandabprallern) und
wählt den frühesten Punkt der Flugbahn, den sie rechtzeitig erreicht. Rollen — Angriff,
Unterstützung, Verteidigung, Torwart — werden pro Frame nach Ballnähe und Torgefahr neu vergeben.
Sie fährt Boostpads an, die ohnehin auf dem Weg liegen, flippt am Anstoß und geht ab
Schwierigkeitsgrad *Legende* in Luftduelle.

**Post-Processing** ist von Hand gebaut (Bright-Pass, zwei Gauß-Durchgänge, Composite mit
Bloom, Radial-Blur ab Überschall, chromatischer Aberration, Vignette und Korn) — es wird nur
die Kernbibliothek geladen, keine `examples/`-Module. Reflexionen kommen aus einer einmalig
gebackenen Cube-Map der leeren Arena.

**Musik und Sound** sind komplett in WebAudio synthetisiert: ein Synthwave-Sequenzer mit
Bass, Arpeggio, Pad und Drums bei 126 BPM, dazu Motor, Boost, Aufpralle und Torfanfare.
Keine einzige Audiodatei.

## Aufbau

```
src/game.html   die einzige Quelle (Artifact-Format, ohne doctype/html/head/body)
build.py        umschließt sie mit doctype + Metadaten
index.html      erzeugt — das, was GitHub Pages ausliefert
```

Änderungen: `src/game.html` bearbeiten → `python build.py` → committen und pushen.
`index.html` niemals von Hand bearbeiten, der nächste Build überschreibt es.

Three.js r128 kommt vom CDN, sonst gibt es keine Abhängigkeiten.
