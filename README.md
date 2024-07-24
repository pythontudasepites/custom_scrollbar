# Egyéni görgetősáv

A ***custom_scrollbar_widget*** modulban található *CustomScrollbar* osztály egy olyan egyéni grafikus vezérlőelemet valósít meg, amely a *tkinter* modul által kínált görgetősávhoz (Scrollbar) hasonló, és amelynél a csúszkát (slider) a vezetőcsatornában (trough) két módon lehet mozgatni:

    - a bal vagy jobb oldali nyomógombokkal az aktuálisan érvényes lépésközzel (resolution), vagy
    
    - a bal egérgombbal a vezetőcsatornába történő klikkeléssel. Ekkor a csúszka erre a helyre ugrik.

A lépésköz, ha nem írjuk felül, alapértelmezésben a vezérlőelem példányosításakor megadott vezetőcsatorna-hossz 1%-a. Tehát, ha mondjuk a csatornahossz 300 pixel, akkor a csúszka minimálisan 3 pixelt mozdul el.

A csúszka vezérlésre úgy használható, hogy minden egyes elmozdulásakor a *command* nevű konfigurációs paraméternek értékül adott hívható objektum meg lesz hívva, és argumentumként a csúszka vezetőcsatornabeli relatív helyzetének 0..1 intervallumbeli arányszámát kapja meg. Tehát, ha például a csúszka a vezetőcsatorna felénél van, akkor híváskor 0.5 lesz az átadott érték.

Hasonlóan a *tkinter* grafikus vezérlőihez (widget) a *CustomScrollbar* is rendelkezik néhány beállítható konfigurációs paraméterrel (options). Ezek a következők:

_trough\_width_: a vezetőcsatorna szélessége pixelben

_trough\_height_: a vezetőcsatorna magassága pixelben

_trough\_color_: a vezetőcsatorna színe

_slider\_color_: a csúszka színe

_resolution_: az a pixelben mért lépésköz, amellyel a bal vagy jobb gombok megnyomásakor a csúszka elmozdul.

_command_: hívható objektum, amelynek híváskor a csúszka vezetőcsatornabeli relatív helyzete float számként át lesz adva.

_variable_: egy *DoubleVar* vagy *StringVar* típusú kontrollváltozó, amellyel a csúszka aktuális relatív helyzete kikérhető.

Ahogy más *tkinter* grafikus elemek esetében, a *CustomScrollbar* esetében is a felsorolt konfigurációs paraméterek értékét ki lehet kérni a *CustomScrollbar* példányra meghívott **cget()** metódussal, valamint az értéküket be lehet állítani a **config()** vagy **configure()** metódusokkal. Az említett két nyilvános metóduson felül az osztályban definiált **move_slider_to()** nyilvános metódussal lehet a csúszkát egy adott pozícióba állítani.

Azt, hogy az elkészült *CustomScrollbar* teljesíti-e az előírt követelményeket a szkriptként futtatandó ***custom_scrollbar_test_app*** modulban levő tesztalkalmazással ellenőrizzük. Ez az egyéni görgetősáv működésének és konfigurálhatóságának tesztelését teszi lehetővé olyan módon, hogy az alkalmazás indításakor kirajzol egy kört, valamint a kör kiinduló méretét befoglaló és a kétszer akkora sugarú kört befoglaló négyzeteket. Ezek alatt jelenik meg az egyéni görgetősáv. Ez alatt pedig egy olyan vezérlőpanel, ahol a görgetősáv konfigurálható paramétereinek értékét lehet állítani. Az új értékeket a megfelelő beviteli mezőkbe kell beírni, és a „Konfiguráció aktualizálás” gombra kattintva érvényesíteni. Ekkor a görgetősáv az új konfiguráció szerint fog megjelenni. A lépésköz változtatásának hatását természetesen csak a csúszka jobb vagy bal oldali gombokkal történő mozgatásakor érzékeljük. Ha a csúszka elmozdul, akkor a kör mérete csökken vagy nő. Növelni legfeljebb a kiinduló méret kétszeresére lehet.

A futtatáshoz Python 3.10+ szükséges.

Az alábbi képernyőképek különböző konfigurációs beállítások és csúszkaállások mellett mutatják az egyéni görgetősáv kinézetét, valamint a tesztkör méretét.

<img src="https://github.com/pythontudasepites/custom_scrollbar/blob/main/custom_scrollbar_1.jpg" width="623" height="327">

<img src="https://github.com/pythontudasepites/custom_scrollbar/blob/main/custom_scrollbar_2.jpg" width="623" height="336">
