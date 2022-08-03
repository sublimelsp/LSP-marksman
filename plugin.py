import sublime

from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import cast, Any, List, Optional

import os
import sys
import shutil
import urllib.request
import platform


USER_AGENT = 'Sublime Text LSP'

TAG = '2022-07-31'

MARKSMAN_RELEASES_BASE = 'https://github.com/artempyanykh/marksman/releases/download/{tag}/{platform}'
MARKSMAN_FILENAME_BASE = '{platform}'


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
    def _is_marksman_ls_installed(cls) -> bool:
        return bool(cls._get_marksman_ls_path())

    @classmethod
    def _get_marksman_ls_path(cls) -> Optional[str]:
        marksman_ls_binary = cast(List[str], get_setting('command', [os.path.join(cls.basedir(), 'marksman')]))
        return shutil.which(marksman_ls_binary[0]) if len(marksman_ls_binary) else None

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        return not cls._is_marksman_ls_installed() or (cls.current_server_version() != cls.server_version())

    @classmethod
    def install_or_update(cls) -> None:
        if plat() is None:
            raise ValueError('System platform not detected or supported')

        marksman_path = cls._get_marksman_ls_path()
        if marksman_ls_path:
            os.remove(marksman_ls_path)

        os.makedirs(cls.basedir(), exist_ok=True)

        bin_url = MARKSMAN_RELEASES_BASE.format(
            tag=cls.server_version(), platform=plat())
        bin_file = os.path.join(cls.basedir(), MARKSMAN_FILENAME_BASE.format(
            platform=plat()))

        req = urllib.request.Request(
            bin_url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        with urllib.request.urlopen(req) as fp:
            with open(bin_file, "wb") as f:
                f.write(fp.read())

        marksman_ls = 'marksman-macos' | 'marksman-linux' if plat() != 'windows' else 'marksman.exe'
        os.chmod(os.path.join(cls.basedir(), marksman_ls), 0o700)

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
