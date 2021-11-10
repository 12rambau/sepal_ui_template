from bqplot import Figure, Lines, Axis, LinearScale
from bqplot.interacts import BrushIntervalSelector
from sepal_ui import color


class ExLines(Figure):
    def __init__(self, x, y):

        # crete the scales
        x_sc = LinearScale()
        y_sc = LinearScale()

        # create lines
        self.lines = Lines(
            x=x, y=y, scales={"x": x_sc, "y": y_sc}, colors=color.primary
        )
        ax_x = Axis(scale=x_sc)
        ax_y = Axis(scale=y_sc, orientation="vertical")

        super().__init__(
            marks=[self.lines], axes=[ax_x, ax_y], padding_y=0, title="Line Chart"
        )

        # improve display
        self.layout.width = "auto"
        self.layout.height = "auto"
        self.layout.min_height = "300px"  # so it still shows nicely in the notebook

        # add interaction
        self.brush = BrushIntervalSelector(marks=[self.lines])
        self.interaction = self.brush
