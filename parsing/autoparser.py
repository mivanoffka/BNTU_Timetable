import urllib.request
from config import BASE_DIR
from pathlib import Path
from parsing import parser as p

if __name__ == "__main__":
    try:
        destination = Path(BASE_DIR / "parsing/sheets/1kurs.xls")
        url = 'https://files.bntu.by/s/hOCgaeBRU4ttDYt/download'
        urllib.request.urlretrieve(url, destination)

        destination = Path(BASE_DIR / "parsing/sheets/2kurs.xls")
        url = 'https://files.bntu.by/s/XF3MSbTbm7gKLQ7/download'
        urllib.request.urlretrieve(url, destination)

        print("Books are dowloaded.")
    except:
        print("Cannot dowload the books.")
    finally:
        p.main()
        