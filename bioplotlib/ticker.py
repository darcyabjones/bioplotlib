from matplotlib.ticker import ScalarFormatter

class SeqFormatter(ScalarFormatter):

    def __init__(self, start=0, **kwargs):
        self.start = start
        super(SeqFormatter, self).__init__(**kwargs)
        return

    def func(self, x, pos=None):
        x -= self.start
        if x <= 0:
            x += 1
        return x

    def __call__(self, x, pos=None):
        'Return the format for tick val *x* at position *pos*'
        if len(self.locs) == 0:
            return ''
        else:
            x = self.func(x, pos)
            s = self.pprint_val(x)
            return self.fix_minus(s)
