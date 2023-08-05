# coding=utf-8

import os
from pathlib import Path

import pytest

from emiz.mission import Mission
from emiz.miz import Miz

if os.path.exists('./test_files'):
    BASE_PATH = os.path.abspath('./test_files')
elif os.path.exists('./test/test_files'):
    BASE_PATH = os.path.abspath('./test/test_files')
else:
    raise RuntimeError('cannot find test files')

TEST_FILE = os.path.join(BASE_PATH, 'TRG_KA50.miz')
OUT_FILE = '{}_EMFT.miz'.format(TEST_FILE[:-4])
BAD_ZIP_FILE = os.path.join(BASE_PATH, 'bad_zip_file.miz')
MISSING_FILE = os.path.join(BASE_PATH, 'missing_files.miz')
ALL_OBJECTS = os.path.join(BASE_PATH, 'all_objects.miz')
BAD_FILES = ['bad_zip_file.miz', 'missing_files.miz']


class TestMizPath:
    @pytest.mark.parametrize('cls', [Miz])
    def test_init(self, tmpdir, cls):
        t = Path(str(tmpdir))

        f = t.joinpath('f.txt')

        with pytest.raises(FileNotFoundError):
            cls(f)

        with pytest.raises(TypeError):
            cls(t)

        f.write_text('')

        with pytest.raises(ValueError):
            cls(f)

        f = t.joinpath('f.miz')
        f.write_text('')

        cls(f)

    def test_unzip(self):
        m = Miz(TEST_FILE)
        m.unzip()

    def test_context(self):
        with Miz(TEST_FILE) as miz:
            assert isinstance(miz.mission, Mission)
            tmpdir = os.path.abspath(miz.temp_dir)

        assert not os.path.exists(tmpdir)
