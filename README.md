# Bíró Feladatkezelő

Ez a program a Szegedi Tudományegyetemen kódellenőrzésre használt, bíró nevű szoftverhez készült. Segítségével nem kell az oldalt minden alkalommal meglátogatni egy adott projekt letöltéséhez, hanem az kényelmesen parancssorból is megtehető. A megoldás feltöltésére a program nem alkalmas.

## Használata
Forráskódból való futtatás esetén a szükséges modulok megtalálhatóak a *requirements.txt* állományban.

A program használatához szükséges a *config.json* fájl kitöltése.
```json
{
    // Az éppen használt bíró elérhetősége
    "biro_url": "https://biro.inf.u-szeged.hu/",
    // A letöltendő feladatok
    "save_path": "C:/Users/Felhasznalo/hazi",
    // A bírón használt név és jelszó páros
    "username": "",
    "password": "",
    // A használt szövegszerkesztő elérhetősége
    // ha ilyen nincs, üresen, vagy akár el is hagyható
    "editor": "C:/Users/Felhasznalo/AppData/Local/Programs/Microsoft VS Code/bin/code.cmd"
}
```
A letöltött projekteket tartalmazó mappák az átláthatóság, kompatibilitás és az ismétlődés elkerülésének érdekében a beadási határidő alapján kerülnek elnevezésre.

A projekt a letöltés után automatikusan megnyílik a konfigurációs fájlban megadott kódszerkesztőben, amennyiben az megadásra került.

## Saját szövegszerkesztő megadása
Saját kódszerkesztő megadására többféle lehetőség is rendelkezésre áll.
```json
{
    // Kódszerkesztő használatának mellőzése
    // ebben az esetben az adatsor akár törölhető is
    "editor":"",

    // Visual Studio Code
    "editor": "C:/Users/Felhasznalo/AppData/Local/Programs/Microsoft VS Code/bin/code.cmd",
    //vagy
    "editor": "/usr/bin/code",
    // vagy
    "editor": "code",

    // Atom
    "editor": "atom"

}
```
Olyan kódszerkesztő szoftver használata érdemes, amely képes mappák megnyitására, ellentétes esetben (pl. Notepad) valószínűleg hibaüzenet vagy hibás működés várható.

## Licensz
[GPl v3.0](https://choosealicense.com/licenses/gpl-3.0/)