import sublime

from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import cast, Any, List, Optional

import os
import sys
import shutil
import platform


USER_AGENT = 'Sublime Text LSP'

TAG = '2022-06-23'

MARKSMAN_RELEASES_BASE = 'https://github.com/artempyanykh/marksman/releases/{tag}/{platform}'
MARKSMAN_FILENAME_BASE = 'marksman{platform}'


def plat() -> Optional[str]:
    '''
    Returns the user friendly platform version that
    sublime is running on.
    '''
    if sublime.platform() == 'osx':
        return 'darwin'
    elif sublime.platform() == 'windows':
        return 'windows'
    elif sublime.platform() == 'linux':
        if platform.system() == 'Linux':
            return 'linux'
        else:
            return None
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
    def install_or_update(cls) -> None:
        if plat() is None:
            raise ValueError('System platform not detected or supported')

        marksman_path = cls._get_marksman_path()
        if marksman_path:
            os.remove(marksman_path)

        os.makedirs(cls.basedir(), exist_ok=True)

        bin_url = MARKSMAN_RELEASES_BASE.format(
            tag=cls.server_version(), platform=plat())
        bin_file = os.path.join(cls.basedir(), MARKSMAN_FILENAME_BASE.format(
            tag=cls.server_version(), platform=plat()))


        marksman = 'marksman' if plat() != 'windows' else 'marksman.exe'
        os.chmod(os.path.join(cls.basedir(), marksman), 0o700)

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
