import os
import pickle

from afinipy import Afinipy

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


class TestRecursive:
    """Test the disk_io module"""

    def setup_class(self):
        self.mdir = TEST_DIR
        self.rootdir = os.path.join(self.mdir, 'recursive_test')

        with open(os.path.join(self.mdir, 'compare_strings.pickle'), 'rb') as to_load:
            self.ground_truth = pickle.load(to_load)
            to_load.close()

    def _load_init(self, mpath):
        with open(os.path.join(mpath, '__init__.py')) as f:
            return f.read()

    def test_default_settings(self):
        """test afinipy with the default settings on the recursive example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['recursive_default']

        base = Afinipy(self.rootdir)
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)

    def test_recursive(self):
        """test afinipy with recursive mode on the recursive example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['recursive_recursive']

        base = Afinipy(self.rootdir, mode='recursive')
        base.build_init()
        assert gtruth['recursive_example'] == self._load_init(os.path.join(self.rootdir))
        assert gtruth['L1a'] == self._load_init(os.path.join(self.rootdir, 'L1a'))
        assert gtruth['L2a'] == self._load_init(os.path.join(self.rootdir, 'L1a', 'L2a'))
        assert gtruth['L3a'] == self._load_init(os.path.join(self.rootdir, 'L1a', 'L2a', 'L3a'))
        assert gtruth['L1b'] == self._load_init(os.path.join(self.rootdir, 'L1b'))

    def test_package_name(self):
        """test afinipy with package name on the recursive example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['recursive_package']

        base = Afinipy(self.rootdir, mode='recursive', package='testing')
        base.build_init()
        assert gtruth['L1a'] == self._load_init(os.path.join(self.rootdir, 'L1a'))
        assert gtruth['L2a'] == self._load_init(os.path.join(self.rootdir, 'L1a', 'L2a'))
        assert gtruth['L3a'] == self._load_init(os.path.join(self.rootdir, 'L1a', 'L2a', 'L3a'))
        assert gtruth['L1b'] == self._load_init(os.path.join(self.rootdir, 'L1b'))

    def test_exclusion_path(self):
        """test afinipy with exclusion_path on the recursive example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['recursive_exclusion_path']

        exclusion_path = os.path.join(self.mdir, '.exclude')
        base = Afinipy(self.rootdir, mode='recursive', exclusion_path=exclusion_path)
        base.build_init()
        assert gtruth['L1a'] == self._load_init(os.path.join(self.rootdir, 'L1a'))
        assert gtruth['L2a'] == self._load_init(os.path.join(self.rootdir, 'L1a', 'L2a'))
        assert gtruth['L1b'] == self._load_init(os.path.join(self.rootdir, 'L1b'))
