from sepal_ui import sepalwidgets as sw
from bqplot import pyplot as plt
import ipywidgets as widgets
import numpy as np
import ipyvuetify as v

from component import widget as cw


class ExampleTile(sw.Tile):
    def __init__(self):

        # create base data
        n = 2000
        self.x = np.linspace(0.0, 10.0, n)
        self.y = np.cumsum(np.random.randn(n) * 10).astype(int)

        # create the bqplot figure
        self.hist = cw.ExHist(self.y)
        self.lines = cw.ExLines(self.x, self.y)

        # create the widgets
        w_slider = v.Slider(thumb_label="always", class_="mt-5", v_model=30)

        styles = ["dashed", "solid", "dotted"]
        w_styles = v.Select(
            items=styles, label="line style", v_model=styles[0], class_="mb-2"
        )

        super().__init__(
            "example_tile",
            "Example Tile",
            inputs=[w_styles, w_slider, self.lines, self.hist],
            btn=sw.Btn("download hitogram", icon="mdi-download"),
        )

        # add js behaviour
        widgets.link((w_slider, "v_model"), (self.hist.hist, "bins"))
        widgets.link((w_styles, "v_model"), (self.lines.lines, "line_style"))
        self.lines.brush.observe(self.update_range, "selected")
        self.btn.on_event("click", self.save_hist)

    def update_range(self, change):

        selected = change["new"]

        if selected is not None and len(selected) == 2:
            xmin, xmax = selected
            mask = (self.x > xmin) & (self.x < xmax)
            self.hist.hist.sample = self.y[mask]

        return

    def save_hist(self, widget, event, data):

        self.hist.save_png(f"example_histogram_{self.slider.v_model}.png")

        return
