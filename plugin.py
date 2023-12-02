from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import Dict, Optional
from shutil import which
import os
import sublime
import urllib.request


MARKSMAN_TAG = '2023-11-29'
MARKSMAN_RELEASES_BASE = 'https://github.com/artempyanykh/marksman/releases/download/{tag}/{platform}'
USER_AGENT = 'Sublime Text LSP'


def marksman_binary() -> Optional[str]:
    platform_arch = '{}_{}'.format(sublime.platform(), sublime.arch())
    if platform_arch in {'osx_x64', 'osx_arm64'}:
        return 'marksman-macos'
    if platform_arch == 'windows_x64':
        return 'marksman.exe'
    if platform_arch == 'linux_arm64':
        return 'marksman-linux-arm64'
    if platform_arch == 'linux_x64':
        return 'marksman-linux-x64'
    return None


class Marksman(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return 'marksman'

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def marksman_path(cls) -> str:
        return os.path.join(cls.basedir(), 'bin', marksman_binary() or 'unsupported_platform')

    @classmethod
    def additional_variables(cls) -> Optional[Dict[str, str]]:
        return {
            'marksman_bin': marksman_binary() or 'unsupported_platform'
        }

    @classmethod
    def server_version(cls) -> str:
        return MARKSMAN_TAG

    @classmethod
    def current_server_version(cls) -> Optional[str]:
        try:
            with open(os.path.join(cls.basedir(), 'VERSION'), 'r') as fp:
                return fp.read()
        except Exception:
            return None

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        if marksman_binary() is None:
            raise ValueError('Platform "{} ({})" is not supported'.format(sublime.platform(), sublime.arch()))
        return which(cls.marksman_path()) is None or cls.current_server_version() != cls.server_version()

    @classmethod
    def install_or_update(cls) -> None:
        marksman_path = cls.marksman_path()
        os.makedirs(os.path.dirname(marksman_path), exist_ok=True)
        bin_url = MARKSMAN_RELEASES_BASE.format(tag=cls.server_version(), platform=marksman_binary())
        req = urllib.request.Request(
            bin_url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        with urllib.request.urlopen(req) as fp:
            with open(marksman_path, 'wb') as f:
                f.write(fp.read())

        os.chmod(marksman_path, 0o700)
        with open(os.path.join(cls.basedir(), 'VERSION'), 'w') as fp:
            fp.write(cls.server_version())


def plugin_loaded() -> None:
    register_plugin(Marksman)


def plugin_unloaded() -> None:
    unregister_plugin(Marksman)
