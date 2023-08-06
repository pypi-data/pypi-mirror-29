from pathlib import Path
import numpy as np
import subprocess
import sys
import tempfile

from tmscc import JARFILE_PATH
from sampler import GibbsSampler


class TopicModelBase(object):
    def __init__(self, outdir, sampler='default'):
        self.outdir = Path(outdir).expanduser().resolve()
        if not self.outdir.is_dir():
            raise AssertionError('{0} is not an directory.'.format(self.outdir))
        if sampler == 'default':
            self.sampler = GibbsSampler(n_iter=1000, n_burnin=100)
        else:
            self.sampler = sampler


class LDA(TopicModelBase):
    def __init__(self, n_topics, profile, outdir, sampler='default'):
        """
        params:
        n_topics:
            the number of topics
        profile:
            gene expression profile,
            a pandas dataframe whose shape is (n_genes, n_cells)
            profile's index should be the gene names
        """
        super(LDA, self).__init__(outdir, sampler)
        self.n_topics = int(n_topics)
        self.profile = profile
        profile.astype = int

        outputfile_fmt = str(self.outdir.resolve()) + '/{0}-{1}'
        self.theta_file = Path(
            outputfile_fmt.format(self.n_topics, 'theta.txt'))
        self.phi_file = Path(
            outputfile_fmt.format(self.n_topics, 'phi.txt'))

        self.is_trained = False
        self.theta = None
        self.phi = None

    def _estimate_mallet(self):
        """
        the result will be stored in the outdir you specified
        """
        sys.stderr.write('\rreading daraframe...')
        datafp = tempfile.NamedTemporaryFile()
        np.savetxt(datafp.name, self.profile.T, delimiter=',', fmt='%d')
        genefp = tempfile.NamedTemporaryFile()
        genefp.write(str.encode(','.join(self.profile.index.tolist())))
        sys.stderr.flush()

        sys.stderr.write('\rexecuting commands...')
        cmd = ['java',
               '-jar',
               str(JARFILE_PATH.resolve()),
               str(self.n_topics),
               datafp.name,
               genefp.name,
               str(self.theta_file.resolve()),
               str(self.phi_file.resolve()),
               str(self.sampler.n_thread),
               str(self.sampler.n_burnin)]
        
        print(' '.join(cmd))
        proc = subprocess.Popen(' '.join(cmd), shell=True)
        proc.wait()
        sys.stderr.flush()

        datafp.close()
        genefp.close()

    def _estimate_celltree(self):
        # TODO
        pass

    def estimate(self):
        self.is_trained = True
        if isinstance(self.sampler, GibbsSampler):
            self._estimate_mallet()
        else:
            self._estimate_celltree()

    def load_params(self):
        """
        load results of estimate()
        parameters will be in self.theta (cells*topics matrix) and
        self.phi (words*topics matrix).
        """
        if not self.theta_file.exists():
            raise AssertionError('execute estimate() before calling this'
                                 'method.')
        else:
            self.theta = np.loadtxt(self.theta_file.resolve(), delimiter=',')
        
        if not self.phi_file.exists():
            raise AssertionError('execute estimate() before calling this'
                                 'method.')
        else:
            self.phi = np.loadtxt(self.phi_file.resolve(), delimiter=',')

        return (self.theta, self.phi)

    def __repr__(self):
        return '''
        LDA Model:
        n_topics: {0}
        trained: {1},
        sampler: {2}
        '''.format(self.n_topics, self.is_trained, self.sampler)
        
