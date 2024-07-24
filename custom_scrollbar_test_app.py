from __future__ import annotations
import tkinter as tk
from custom_scrollbar_widget import CustomScrollbar, Point


class CirclePanel(tk.Canvas):
    """Egy kört, valamint a kör kiinduló méretét befoglaló és a kétszer akkora sugarú kört befoglaló négyzeteket rajzolja ki."""

    def __init__(self, master: CustomScrollBarTestApp):
        super().__init__(master, bg='white', width=550, height=220)
        # Kör kirajzolása a vásznon.
        r = 50  # A kör sugara.
        cp = Point(300, 110)  # A kör középpontja
        self._circle_id = self.create_oval((cp.x - r, cp.y - r), (cp.x + r, cp.y + r), fill='lightblue')
        # A kör kiinduló méretét befoglaló, valamint a kétszer akkora sugarúk kört befoglaló négyzetek kirajzolása.
        self.create_rectangle(self.bbox(self._circle_id), dash='.')
        self.create_rectangle((cp.x - 2 * r, cp.y - 2 * r), (cp.x + 2 * r, cp.y + 2 * r), dash='-.')
        self.center_point = cp
        self.radius = r

    def change_size(self, ratio):
        """A kör méretetét a ratio kétszeresére változtatja. Vagyis, ha a ratio 0..1 közötti szám, akkor a kör az
        eredeti mérethez képest a kétszeresére nőhet.
        """
        cp, r, q = self.center_point, self.radius, ratio
        self.coords(self._circle_id, cp.x - r * 2 * q, cp.y - r * 2 * q, cp.x + r * 2 * q, cp.y + r * 2 * q)


class SliderPositionViewPanel(tk.Frame):
    """A csúszka aktuális pozíciójáról tájékoztató komponens. A csúszkapozíció egy címkén jelenik meg számszerűen százalékban."""

    def __init__(self, master: CustomScrollBarTestApp):
        super().__init__(master)
        # Címkék létrehozása.
        lbl_position = tk.Label(self, text='A csúszka pozíciója a vezetőcsatorna hosszához képest:', font=('Noto', 12))
        lbl_slider_position_value = tk.Label(self, font=('Noto', 12))
        # A csúszkapozíció aktuális értékét tároló kontrollváltozó létrehozása.
        self.slider_position_var = tk.DoubleVar(self, name='slider_position')

        def format_slider_position_value(var_name, s, operation):
            """A címkén megjelenő számértéket formázza."""
            lbl_slider_position_value['text'] = '{:.1%}'.format(self.getvar(var_name))

        # A kontrollváltozó minden értékváltozásakor a számformátum meghatározó függvény meg lesz hívva.
        self.slider_position_var.trace_add('write', format_slider_position_value)
        self.slider_position_var.set(0)  # a kezdőérték beállítása.
        # A címkék lehelyezése.
        lbl_position.grid(row=0, column=0, sticky='w')
        lbl_slider_position_value.grid(row=0, column=1, sticky='w', padx=0, pady=10)


class ControlPanel(tk.LabelFrame):
    """Az egyéni görgetősáv paramétereinek változtatását teszi lehetővé."""

    def __init__(self, master: CustomScrollBarTestApp):
        super().__init__(master, text='Konfigurálás', font=('Source Sans Pro Semibold', 14))
        # A grafikus elemek és kontrollváltozóik létrehozása.
        common_options = dict(font=('Noto', 12))
        lbl_trough = tk.Label(self, text='Vezetőcsatorna', **common_options)
        lbl_trough_width = tk.Label(self, text='szélesség:', **common_options)
        trough_width_var = tk.IntVar(self, value=master.custom_scrollbar.cget('trough_width'))
        ent_trough_width = tk.Entry(self, width=10, textvariable=trough_width_var, **common_options)

        lbl_trough_height = tk.Label(self, text='magasság:', **common_options)
        trough_height_var = tk.IntVar(self, value=master.custom_scrollbar.cget('trough_height'))
        ent_trough_height = tk.Entry(self, width=10, textvariable=trough_height_var, **common_options)

        lbl_trough_color = tk.Label(self, text='szín:', **common_options)
        trough_color_var = tk.StringVar(self, value=master.custom_scrollbar.cget('trough_color'))
        ent_trough_color = tk.Entry(self, width=10, textvariable=trough_color_var, **common_options)

        lbl_slider = tk.Label(self, text='Csúszka', **common_options)
        lbl_slider_color = tk.Label(self, text='szín: ', **common_options)
        slider_color_var = tk.StringVar(self, value=master.custom_scrollbar.cget('slider_color'))
        ent_slider_color = tk.Entry(self, width=10, textvariable=slider_color_var, **common_options)

        lbl_resolution = tk.Label(self, text='Lépésköz:', **common_options)
        resolution_var = tk.IntVar(self, value=int(master.custom_scrollbar.cget('resolution')))
        ent_resolution = tk.Entry(self, width=10, textvariable=resolution_var, **common_options)

        btn_config = tk.Button(self, text='Konfiguráció aktualizálás', **common_options,
                               command=lambda: master.custom_scrollbar.config(trough_width=trough_width_var.get(),
                                                                              trough_height=trough_height_var.get(),
                                                                              trough_color=trough_color_var.get(),
                                                                              slider_color=slider_color_var.get(),
                                                                              resolution=resolution_var.get()))
        # A grafikus elemek lehelyezése rácsos elrendezésben.
        lbl_trough.grid(row=0, column=0, sticky='w')
        lbl_trough_width.grid(row=1, column=0, sticky='e')
        ent_trough_width.grid(row=1, column=1, sticky='w', padx=10, pady=2)

        lbl_trough_height.grid(row=2, column=0, sticky='e')
        ent_trough_height.grid(row=2, column=1, sticky='w', padx=10, pady=2)

        lbl_trough_color.grid(row=3, column=0, sticky='e')
        ent_trough_color.grid(row=3, column=1, sticky='w', padx=10, pady=2)

        lbl_slider.grid(row=4, column=0, sticky='w')
        lbl_slider_color.grid(row=5, column=0, sticky='e')
        ent_slider_color.grid(row=5, column=1, sticky='w', padx=10, pady=2)

        lbl_resolution.grid(row=6, column=0, sticky='w')
        ent_resolution.grid(row=6, column=1, sticky='w', padx=10, pady=2)

        btn_config.grid(row=7, column=0, sticky='we', columnspan=2, padx=10, pady=10)


class CustomScrollBarTestApp(tk.Tk):
    """Az egyéni görgetősáv működésének és konfigurálhatóságának tesztelését teszi lehetővé."""

    def __init__(self):
        super().__init__()
        self.title('Egyéni görgetősáv tesztalkalmazás')
        # A felületet alkotó komponenspéldányok létrehozása.
        circle = CirclePanel(self)
        self.custom_scrollbar = CustomScrollbar(self, trough_width=500)
        self.custom_scrollbar.config(slider_color='blue', trough_color='light yellow', trough_height=30)
        self.custom_scrollbar.config(command=lambda q: circle.change_size(q))
        slider_position_view_panel = SliderPositionViewPanel(self)
        self.custom_scrollbar.config(variable=slider_position_view_panel.slider_position_var)
        control_panel = ControlPanel(self)
        # A komponenspéldányok lehelyezése rácsos elrendezésben.
        circle.grid(row=0, column=0, sticky='news', padx=10, pady=10)
        self.custom_scrollbar.grid(row=1, column=0, sticky='news', padx=10, pady=10)
        slider_position_view_panel.grid(row=2, column=0, sticky='news', padx=10, pady=10)
        control_panel.grid(row=3, column=0, sticky='w', padx=10, pady=10)
        # A csúszka beállítása a vezetősáv közepére.
        self.custom_scrollbar.move_slider_to(self.custom_scrollbar.cget('trough_width')/2)

    def run(self):
        self.mainloop()


CustomScrollBarTestApp().run()
