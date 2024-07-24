import tkinter as tk
from collections import namedtuple

Point = namedtuple('Point', 'x y')


class CustomScrollbar(tk.Frame):
    """A görgetősávhoz (Scrollbar) hasonló grafikus vezérlőelem, amelynél a csúszkát (slider) a vezetőcsatornában (trough)
    két módon lehet mozgatni:
    - a bal vagy jobb oldali nyomógombokkal az aktuális lépésközzel, vagy
    - a bal egérgombbal a vezetőcsatornába történő klikkeléssel. Ekkor a csúszka erre a helyre ugrik.\n
    A csúszka legkisebb elmozdulási lépésköze (resolution) alapértelmezetten a példányosításkor megadott vezetőcsatorna-hossz 1%-a, ami felülírható.
    Tehát, ha a csatornahossz 300 pixel, akkor a csúszka minimálisan 3 pixelt mozdul el.\n
    A csúszka minden egyes elmozdulásakor a command paraméternek értékül adott hívható objektum meg lesz hívva, és
    argumentumként a csúszkának a vezetőcsatorna hosszában való helyzetének arányszámát kapja a 0..1 intervallumból.
    Tehát, ha a csúszka a vezetőcsatorna felénél van, akkor híváskor 0.5 lesz az átadott érték.\n
    A beállítható konfigurációs paraméterek:
      trough_width:  a vezetőcsatorna szélessége pixelben
      trough_height: a vezetőcsatorna magassága pixelben
      trough_color:  a vezetőcsatorna színe
      slider_color:  a csúszka színe
      resolution:    az a pixelben mért lépésköz, amellyel a bal vagy jobb gombok megnyomásakor a csúszka elmozdul.
      command:       hívható objektum, amelynek híváskor a csúszka vezetőcsatornabeli relatív helyzete float számként át lesz adva.
      variable:      egy DoubleVar vagy StringVar típusú kontrollváltozó, amellyel a csúszka aktuális relatív helyzete kikérhető.
    """

    def __init__(self, master, **options):
        super().__init__(master)
        # A beállítható konfigurációs paraméterek alapértelmezett értékeinek meghatározása.
        self.options_defaults = dict(trough_width=300, trough_height=25, trough_color='white', slider_color='black', resolution=3,
                                     command=lambda ratio: None, variable=None)
        # A beállítható konfigurációs paraméterek értékeinek aktualizálása a példányosításkor megadott értékek szerint.
        self.options = self.options_defaults | options
        self.options.update(dict(resolution=self.options.get('trough_width') * 0.01))

        # A vezetőcsatorna megvalósítása.
        self._canvas = tk.Canvas(self, width=self.cget('trough_width'), height=self.cget('trough_height'),
                                 bg=self.cget('trough_color'), highlightthickness=0)
        # A csúszka megvalósítása.
        self._create_slider()
        # Mivel a beállítható konfigurációs paraméterek neve eltér a csúszkát és a vezetőcsatornát megvalósító grafikus elemek
        # paraméterneveitől, ezért a konfigurálhatóság megvalósításához a neveket meg kell feleltetni.
        self._trough_options_alias = {'trough_width': 'width', 'trough_height': 'height', 'trough_color': 'bg'}
        self._slider_options_alias = {'slider_color': 'fill'}

        # A bal és jobb oldali nyomógombok létrehozása, és a csúszkamozgató metódusok hozzárendelése.
        btn_configs = dict(repeatinterval=30, repeatdelay=100, font=('DejaVu Sans Mono', int(9 / 25 * self.cget('trough_height'))))
        btn_left = tk.Button(self, text=chr(0x25c0), **btn_configs,
                             command=lambda: self._move_slider('left', self.cget('resolution')))

        btn_right = tk.Button(self, text=chr(0x25b6), **btn_configs,
                              command=lambda: self._move_slider('right', self.cget('resolution')))
        # A grafikus elemek elrendezése.
        btn_left.pack(side=tk.LEFT, fill=tk.BOTH)
        self._canvas.pack(side=tk.LEFT)
        btn_right.pack(side=tk.LEFT, fill=tk.BOTH)
        # A vezetőcsatornát megvalósító Canvas elemhez hozzárendeljük a bal egérgomblenyomás eseményt és a csúszka egérpozícióhoz
        # ugrását megvalósító metódust mint eseménykezelőt.
        self._canvas.bind('<Button 1>', self._jump_slider_to_mouse_cursor)

    def _create_slider(self):
        """A csúszka megvalósítása egy a Canvas elemen megjelenő rombusz alakú sokszög rajzelemként, aminek magassága és szélessége
        igazodik a vezetőcsatorna, azaz a Canvas elem magasságához.
        """
        through_height: int | float = self.cget('trough_height')
        initial_slider_points = (Point(0, 0), Point(through_height / 4, through_height / 2),
                                 Point(0, through_height), Point(-through_height / 4, through_height / 2))

        self._canvas.create_polygon(*initial_slider_points, fill=self.options.get('slider_color'), width=0, tags=('slider',))

    def _coords_to_points(self, iterable_of_x_and_y) -> list[Point]:
        """Az x,y koordinták sorozatát Point példányok listájává alakítja."""
        itr = iter(iterable_of_x_and_y)
        return [Point(x, y) for x, y in zip(itr, itr)]

    def _points_to_coords(self, iterable_of_points) -> list[int | float]:
        """A Point példányok sorozatát x,y koordinták listájává alakítja."""
        coords = []
        for point in iterable_of_points:
            coords.extend(point)
        return coords

    def _get_slider_top_point(self) -> Point:
        """A csúszka felső csúcspontját adja vissza."""
        slider_points: list[Point] = self._coords_to_points(self._canvas.coords('slider'))
        top_point: Point = list(sorted(slider_points, key=lambda point: point.y)).pop(0)
        return top_point

    def _expose_slider_position_ratio(self) -> float:
        """A csúszka vezetősávhosszhoz viszonyított relatív pozíciójával tér vissza, amire a kontrollváltozó értékét is beállítja."""
        ratio = self._get_slider_top_point().x / self.cget('trough_width')
        if tk_var := self.cget('variable'):
            tk_var.set(ratio)
        return ratio

    def _exec_command(self):
        """A command paraméter értékeként szereplő hívható objektum meghívása átadva a csúszka
        vezetősávhosszhoz viszonyított relatív pozícióját.
        """
        self.cget('command')(self._expose_slider_position_ratio())

    def _move_slider(self, direction, resolution):
        """A csúszka resolution lépésközzel direction szerinti bal vagy jobb irányba történő mozgatása."""
        top_point: Point = self._get_slider_top_point()
        if direction == tk.LEFT:
            if top_point.x - resolution >= 0:
                self._canvas.move('slider', -resolution, 0)
            else:
                self._canvas.move('slider', -top_point.x, 0)

        if direction == tk.RIGHT:
            if top_point.x + resolution <= int(self._canvas.cget('width')):
                self._canvas.move('slider', +resolution, 0)
            else:
                self._canvas.move('slider', int(self._canvas.cget('width')) - top_point.x, 0)

        self._exec_command()

    def _jump_slider_to_mouse_cursor(self, event):
        """A csúszka áthelyezése a vezetősávon belül az egérmutató szerinti pozícióba."""
        self.move_slider_to(event.x)

    def move_slider_to(self, x):
        """A csúszka áthelyezése a vezetősávon belül az x koordináta szerinti pozícióba."""
        # A csúszka szélességének kiszámítása.
        x_coords = self._canvas.coords('slider')[0:7:2]
        slider_length = max(x_coords) - min(x_coords)
        # A csúszka mozgatása a megfelelő pozícióba.
        self._canvas.moveto('slider', int(x - slider_length / 2), 0)
        # A csúszkapozíció változása miatt a command szerinti hívható objektum meghívása.
        self._exec_command()

    def cget(self, option_name: str = ''):
        """Az option_name konfigurációs paraméter értékének lekérdezése.
        Argumentum nélkül meghívva egy szótárt ad vissza, amely az összes paraméter-érték párt tartalmazza.
        """
        if not option_name:
            return self.options
        try:
            return self.options[option_name]
        except KeyError:
            raise ValueError(f'Nincs ilyen lekérdezhető konfigurációs paraméter: {option_name}')

    def config(self, **kw):
        """Az érvényes konfigurációs paraméterek értékét változtatja meg."""
        # Csak azokkal a konfigurációs paraméterekkel foglalkozunk, amelyek érvényes névvel lettek megadva.
        valid_options = {k: v for k, v in kw.items() if (k in self.options)}

        for option_name, option_value in valid_options.items():
            # Csak akkor foglalkozunk az adott konfigurációs paraméterrel, ha annak értékében változás történt.
            if option_value != self.cget(option_name):

                # Ha a kontrollváltozó megváltozott, ennek értékét be kell állítani.
                if option_name == 'variable':
                    self._expose_slider_position_ratio()

                # A csúszka konfigurációját érintő változás.
                if option_name in self._slider_options_alias:
                    self._canvas.itemconfigure('slider', {self._slider_options_alias[option_name]: option_value})

                # A vezetőcsatorna konfigurációját érintő változás.
                if option_name in self._trough_options_alias:
                    self._canvas.config({self._trough_options_alias[option_name]: option_value})

                    # A csúszka pozícióját igazítani kell a vezetőcsatorna új szélességéhez.
                    if option_name == 'trough_width':
                        old_through_width: int | float = self.cget('trough_width')
                        dx = (option_value / old_through_width - 1) * self._get_slider_top_point().x
                        self._canvas.move('slider', dx, 0)

                    if option_name == 'trough_height':
                        # A csúszka magasságát igazítani kell a vezetőcsatorna új magasságához.
                        through_height: int | float = self.cget('trough_height')
                        r = option_value / through_height
                        p0 = self._get_slider_top_point()
                        self._canvas.scale('slider', *p0, r, r)
                        x_coords = self._canvas.coords('slider')[0:7:2]
                        self._slider_length = max(x_coords) - min(x_coords)

                        # A nyomógombok feliratának karakterméretét igazítani kell a vezetőcsatorna új magasságához.
                        new_fontsize = int(9 / 25 * option_value)
                        for widget in self.slaves():
                            if type(widget) is tk.Button:
                                btn: tk.Button = widget
                                current_font = widget.cget('font').split()
                                current_font_family = current_font[0].strip('{}')
                                new_font = (current_font_family, new_fontsize)
                                btn.config(font=new_font)
        # A változások aktualizálása a konfigurációs nyilvántartásban.
        self.options.update(valid_options)

    configure = config
