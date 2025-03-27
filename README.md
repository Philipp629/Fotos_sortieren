# Foto-Sortierer

Dieses Python-Skript sortiert JPEG-Bilder anhand der EXIF-Daten (Aufnahmedatum) in eine Verzeichnisstruktur, die nach Jahren und Monaten organisiert ist. Es wurde entwickelt, um Fotografen bei der automatischen Archivierung ihrer Bilder zu unterstützen, z. B. auf einem NAS.

## Funktionen
- Sortiert JPEG-Dateien in eine Verzeichnisstruktur: `Jahr\Monat` (z. B. `2023\01_Januar`).
- Unterstützt alle gängigen JPEG-Endungen (`.jpg`, `.jpeg`, `.JPG`, `.JPEG`).
- Flexibler Einsatz: Verarbeitet das aktuelle Verzeichnis oder benutzerdefinierte Quell- und Zielverzeichnisse.
- Option zum Kopieren oder Verschieben der Dateien (`--copy` oder `--move`).
- Erstellt Verzeichnisse automatisch, falls sie nicht existieren.
- Behandelt Dateikonflikte durch automatische Umbenennung (z. B. `foto.jpg` → `foto_1.jpg`).

## Verzeichnisstruktur
Die Bilder werden in folgender Struktur organisiert:
sorted_photos

2023

01_Januar

foto1.jpg
07_Juli

foto2.jpg


## Voraussetzungen
- **Python 3.x**: Stellen Sie sicher, dass Python installiert ist (`python --version`).
- **exifread**: Eine Bibliothek zum Auslesen von EXIF-Daten.
  Installieren Sie sie mit:
  ```bash
  pip install exifread
