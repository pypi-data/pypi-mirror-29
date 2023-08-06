# Copyright (C) 2018 Allen Li
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

"""XDG Base Directory support

The standard directory paths are implemented using BaseDirs, but most
users can use module level constants defined at import time:

DATA_HOME
CONFIG_HOME
DATA_DIRS
CONFIG_DIRS
CACHE_HOME
RUNTIME_DIR
STATE_HOME

Note that STATE_HOME is not in the specification.

ensure() can be used to create directories if they do not exist in
compliance with the specification.
"""

__version__ = '1.0.0'

from pathlib import Path
import os


def ensure(dirpath: 'PathLike'):
    """Ensure directory exists according to XDG Base Directory spec."""
    os.makedirs(dirpath, mode=0o700, exist_ok=True)


class BaseDirs:

    """XDG Base Directory class.

    >>> b = BaseDirs({'HOME': '/home/alice'})
    >>> assert b.data_home == Path('/home/alice/.local/share')
    """

    def __init__(self, environ):
        home = Path(environ['HOME'])
        if 'XDG_DATA_HOME' in environ:
            self.data_home = Path(environ['XDG_DATA_HOME'])
        else:
            self.data_home = home / '.local/share'

        if 'XDG_CONFIG_HOME' in environ:
            self.config_home = Path(environ['XDG_CONFIG_HOME'])
        else:
            self.config_home = home / '.config'

        if 'XDG_DATA_DIRS' in environ:
            self.data_dirs = tuple(Path(p) for p in environ['XDG_DATA_DIRS'].split(':'))
        else:
            self.data_dirs = (Path('/usr/local/share'), Path('/usr/share'))

        if 'XDG_CONFIG_DIRS' in environ:
            self.config_dirs = tuple(Path(p) for p in environ['XDG_CONFIG_DIRS'].split(':'))
        else:
            self.config_dirs = (Path('/etc/xdg'),)

        if 'XDG_CACHE_HOME' in environ:
            self.cache_home = Path(environ['XDG_CACHE_HOME'])
        else:
            self.cache_home = home / '.cache'

        if 'XDG_RUNTIME_DIR' in environ:
            self.runtime_dir = Path(environ['XDG_RUNTIME_DIR'])
        else:
            self.runtime_dir = None

        # Not contained in specification
        if 'XDG_STATE_HOME' in environ:
            self.state_home = Path(environ['XDG_STATE_HOME'])
        else:
            self.state_home = home / '.local/state'


_dirs = BaseDirs(os.environ)
DATA_HOME = _dirs.data_home
CONFIG_HOME = _dirs.config_home
DATA_DIRS = _dirs.data_dirs
CONFIG_DIRS = _dirs.config_dirs
CACHE_HOME = _dirs.cache_home
RUNTIME_DIR = _dirs.runtime_dir
STATE_HOME = _dirs.state_home
