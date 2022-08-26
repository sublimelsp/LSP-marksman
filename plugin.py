import sublime

from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import Any, Optional

import os
import shutil
import urllib.request


USER_AGENT = 'Sublime Text LSP'

TAG = '2022-08-25'

MARKSMAN_RELEASES_BASE = 'https://github.com/artempyanykh/marksman/releases/download/{tag}/{platform}'
MARKSMAN_FILENAME = 'marksman'


def plat() -> Optional[str]:
    '''
    Returns the user friendly platform version that
    sublime is running on.
    '''
    if sublime.platform() == 'osx':
        return 'marksman-macos'
    elif sublime.platform() == 'windows':
        return 'marksman.exe'
    elif sublime.platform() == 'linux':
        return 'marksman-linux'
    else:
        return None


class Marksman(AbstractPlugin):
    '''
    Marksman is an AbstractPlugin implementation that provides
    the required functions to act as a helper package for the
    Markdown Language Server (marksman)
    '''

    @classmethod
    def name(cls) -> str:
        return "marksman"

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def server_version(cls) -> str:
        return TAG

    @classmethod
    def current_server_version(cls) -> Optional[str]:
        try:
            with open(os.path.join(cls.basedir(), "VERSION"), "r") as fp:
                return fp.read()
        except:
            return None

    @classmethod
    def _get_marksman_ls_path(cls) -> str:
        binary = 'marksman.exe' if sublime.platform() == 'windows' else 'marksman'
        command = get_setting(
            'command', [os.path.join(cls.basedir(), 'bin', binary)]
        )
        marksman_ls_binary = command[0].replace('${storage_path}', cls.storage_path())
        if sublime.platform() == 'windows' and not marksman_ls_binary.endswith('.exe'):
            marksman_ls_binary = marksman_ls_binary + '.exe'
        return marksman_ls_binary

    @classmethod
    def _is_marksman_ls_installed(cls) -> bool:
        return bool(cls._get_marksman_ls_path())

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        return not cls._is_marksman_ls_installed() or (cls.current_server_version() != cls.server_version())

    @classmethod
    def install_or_update(cls) -> None:
        if plat() is None:
            raise ValueError('System platform not detected or supported')
        
        os.makedirs(cls.basedir(), exist_ok=True)
        
        bin_url = MARKSMAN_RELEASES_BASE.format(
            tag=cls.server_version(), platform=plat())

        req = urllib.request.Request(
            bin_url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        marksman_ls = cls._get_marksman_ls_path()
        with urllib.request.urlopen(req) as fp:
            with open(os.path.join(cls.basedir(), "bin", marksman_ls), "wb") as f:
                f.write(fp.read())

        os.chmod(os.path.join(cls.basedir(), "bin", marksman_ls), 0o700)
        with open(os.path.join(cls.basedir(), 'VERSION'), 'w') as fp:
                fp.write(cls.server_version())


def get_setting(key: str, default=None) -> Any:
    settings = sublime.load_settings(
        'LSP-marksman.sublime-settings').get("settings", {})
    return settings.get(key, default)


def plugin_loaded():
    register_plugin(Marksman)


def plugin_unloaded():
    unregister_plugin(Marksman)
