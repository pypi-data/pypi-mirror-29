"""
Sampler metadata
"""


class Sampler(object):
    method_name = None

    def __init__(self):
        pass


class GibbsSampler(Sampler):
    method_name = 'gibbs'

    def __init__(self, n_iter=1000, n_burnin=100, n_thread=1):
        # super(GibbsSampler, self).__init__()
        self.n_iter = n_iter
        self.n_burnin = n_burnin
        self.n_thread = n_thread


class MAPtpx(Sampler):
    method_name = 'maptpx'


SAMPLERS = [(cls.method_name, cls) for cls in (GibbsSampler, MAPtpx)]
