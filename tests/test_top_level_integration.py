import os
import pickle

from afinipy.base import Afinipy

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


class TestTopLevel:
    """Test the disk_io module"""

    def setup_class(self):
        self.mdir = TEST_DIR
        self.rootdir = os.path.join(self.mdir, 'top_level_test')

        with open(os.path.join(self.mdir, 'compare_strings.pickle'), 'rb') as to_load:
            self.ground_truth = pickle.load(to_load)
            to_load.close()

    def _load_init(self, mpath):
        with open(os.path.join(mpath, '__init__.py')) as f:
            return f.read()

    def test_default_settings(self):
        """test afinipy with the default settings on the top level example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['top_level_default']

        base = Afinipy(self.rootdir)
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)

    def test_package_name(self):
        """test afinipy with package name on the top level example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['top_level_package_name']

        base = Afinipy(self.rootdir, package='testing')
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)

    def test_exclude_classes(self):
        """test afinipy with exclusion of classes on the top level example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['top_level_exclude_classes']

        base = Afinipy(self.rootdir, exclude='classes')
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)

    def test_exclude_functions(self):
        """test afinipy with exclusion of functions on the top level example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['top_level_exclude_functions']

        base = Afinipy(self.rootdir, exclude='functions')
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)

    def test_recursive(self):
        """test afinipy with recursive mode on the top level example"""
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['top_level_recursive_mode']

        base = Afinipy(self.rootdir, mode='recursive')
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)

    def test_exclusion_path(self):
        assert os.path.exists(self.rootdir), 'root directory path does not exist'
        gtruth = self.ground_truth['top_level_exclusion_path']

        exclusion_path = os.path.join(self.mdir, '.exclude')
        base = Afinipy(self.rootdir, exclusion_path=exclusion_path)
        base.build_init()
        assert gtruth == self._load_init(self.rootdir)
