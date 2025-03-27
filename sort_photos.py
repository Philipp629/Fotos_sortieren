import os
import shutil
import exifread
import argparse
from datetime import datetime

# Monatsnamen auf Deutsch
MONATE = {
    1: "01_Januar", 2: "02_Februar", 3: "03_März", 4: "04_April",
    5: "05_Mai", 6: "06_Juni", 7: "07_Juli", 8: "08_August",
    9: "09_September", 10: "10_Oktober", 11: "11_November", 12: "12_Dezember"
}

# Unterstützte JPEG-Endungen
JPEG_EXTENSIONS = ('.jpg', '.jpeg', '.JPG', '.JPEG')

def get_exif_date(file_path):
    """Liest das Aufnahmedatum aus den EXIF-Daten der Datei."""
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            date_str = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
            if date_str:
                return datetime.strptime(str(date_str), '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Fehler beim Lesen der EXIF-Daten von {file_path}: {e}")
    return None

def get_file_date(file_path):
    """Liest das Änderungsdatum der Datei, falls keine EXIF-Daten vorhanden sind."""
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime)
    except Exception as e:
        print(f"Fehler beim Lesen des Dateidatums von {file_path}: {e}")
        return None

def sort_photos(source_dir, target_dir, move=False):
    """Sortiert JPEG-Dateien in die Zielstruktur basierend auf EXIF-Daten oder Dateidatum."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(JPEG_EXTENSIONS):
            source_path = os.path.join(source_dir, filename)
            
            # Zuerst EXIF-Daten auslesen
            date = get_exif_date(source_path)
            date_source = "EXIF-Daten"
            
            # Wenn keine EXIF-Daten vorhanden sind, auf Dateidatum zurückgreifen
            if not date:
                print(f"Kein Aufnahmedatum in EXIF-Daten für {source_path} gefunden, verwende Dateidatum.")
                date = get_file_date(source_path)
                date_source = "Dateidatum"
            
            if date:
                year = str(date.year)
                month = MONATE[date.month]
                target_subdir = os.path.join(target_dir, year, month)
                
                if not os.path.exists(target_subdir):
                    os.makedirs(target_subdir)
                
                target_path = os.path.join(target_subdir, filename)
                # Prüfen, ob die Datei bereits im Zielverzeichnis existiert
                if os.path.exists(target_path):
                    print(f"Duplikat gefunden: {filename} existiert bereits in {target_subdir}, übersprungen.")
                    continue
                
                action = shutil.move if move else shutil.copy
                try:
                    action(source_path, target_path)
                    print(f"{'Verschoben' if move else 'Kopiert'} (basierend auf {date_source}): {source_path} -> {target_path}")
                except Exception as e:
                    print(f"Fehler beim {'Verschieben' if move else 'Kopieren'} von {source_path}: {e}")
            else:
                print(f"Kein Datum für {source_path} verfügbar, übersprungen.")

def main():
    parser = argparse.ArgumentParser(description="Sortiert JPEG-Dateien nach EXIF-Datum oder Dateidatum in Jahr/Monat-Verzeichnisse.")
    parser.add_argument("source", nargs='?', default=os.getcwd(), help="Quellverzeichnis (Standard: aktuelles Verzeichnis)")
    parser.add_argument("target", nargs='?', default=os.path.join(os.getcwd(), "sorted_photos"), help="Zielverzeichnis (Standard: sorted_photos im aktuellen Verzeichnis)")
    parser.add_argument("--move", action="store_true", help="Verschiebt Dateien statt sie zu kopieren (Standard: Kopieren)")
    
    args = parser.parse_args()
    sort_photos(args.source, args.target, args.move)

if __name__ == "__main__":
    main()