# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import stat

from mir import xdg


def test_ensure(tmpdir):
    tmpdir = Path(str(tmpdir))
    foo = tmpdir / 'foo'
    xdg.ensure(foo)
    assert foo.is_dir()
    assert stat.S_IMODE(foo.stat().st_mode) == 0o700


def test_data_home_from_environ():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_DATA_HOME': '/foo'})
    assert dirs.data_home == Path('/foo')


def test_data_home_from_default():
    dirs = xdg.BaseDirs({'HOME': '/home/alice'})
    assert dirs.data_home == Path('/home/alice/.local/share')


def test_config_home_from_environ():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_CONFIG_HOME': '/foo'})
    assert dirs.config_home == Path('/foo')


def test_config_home_from_default():
    dirs = xdg.BaseDirs({'HOME': '/home/alice'})
    assert dirs.config_home == Path('/home/alice/.config')


def test_data_dirs_from_environ_single():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_DATA_DIRS': '/foo'})
    assert dirs.data_dirs == (Path('/foo'),)


def test_data_dirs_from_environ_many():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_DATA_DIRS': '/foo:/bar'})
    assert dirs.data_dirs == (Path('/foo'), Path('/bar'))


def test_data_dirs_from_default():
    dirs = xdg.BaseDirs({'HOME': '/home/alice'})
    assert dirs.data_dirs == (Path('/usr/local/share'), Path('/usr/share'))


def test_config_dirs_from_environ_single():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_CONFIG_DIRS': '/foo'})
    assert dirs.config_dirs == (Path('/foo'),)


def test_config_dirs_from_environ_many():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_CONFIG_DIRS': '/foo:/bar'})
    assert dirs.config_dirs == (Path('/foo'), Path('/bar'))


def test_config_dirs_from_default():
    dirs = xdg.BaseDirs({'HOME': '/home/alice'})
    assert dirs.config_dirs == (Path('/etc/xdg'),)


def test_runtime_dir_from_environ():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_RUNTIME_DIR': '/foo'})
    assert dirs.runtime_dir == Path('/foo')


def test_runtime_dir_from_default():
    dirs = xdg.BaseDirs({'HOME': '/home/alice'})
    assert dirs.runtime_dir is None


def test_state_home_from_environ():
    dirs = xdg.BaseDirs({'HOME': '/home/alice',
                         'XDG_STATE_HOME': '/foo'})
    assert dirs.state_home == Path('/foo')


def test_state_home_from_default():
    dirs = xdg.BaseDirs({'HOME': '/home/alice'})
    assert dirs.state_home == Path('/home/alice/.local/state')
