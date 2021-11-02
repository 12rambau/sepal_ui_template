from bqplot import Figure, Hist, Axis, LinearScale


class ExHist(Figure):
    def __init__(self, y):

        # crete the scales
        x_sc = LinearScale()
        y_sc = LinearScale()

        # create hitogram
        self.hist = Hist(sample=y, bins=25, scales={"sample": x_sc, "count": y_sc})
        ax_x = Axis(scale=x_sc)
        ax_y = Axis(scale=y_sc, orientation="vertical")

        super().__init__(
            marks=[self.hist], axes=[ax_x, ax_y], padding_y=0, title="histogram"
        )

        # improve display
        self.layout.width = "auto"
        self.layout.height = "auto"
        self.layout.min_height = "300px"  # so it still shows nicely in the notebook
