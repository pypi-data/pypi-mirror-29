"""PytSite Plugman Events Handlers
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, lang as _lang, package_info as _package_info, events as _events, \
    logger as _logger, semver as _semver
from . import _api, _error


def update_stage_2():
    _console.print_info(_lang.t('pytsite.plugman@upgrading_plugins'))

    # Update all installed plugins
    _console.run_command('plugman:update', {'reload': False})

    # Install/update required plugins
    for plugin_spec in _package_info.requires_plugins('app'):
        try:
            _api.install(plugin_spec)
        except _error.PluginInstallError as e:
            raise _console.error.CommandExecutionError(e)


def app_load():
    # Finish installing/updating plugins
    for p_name, upd_info in _api.get_update_info().items():
        plugin = _api.get(p_name)

        v_from = _semver.Version(upd_info['version_from'])
        v_to = _semver.Version(upd_info['version_to'])
        _logger.debug(_lang.t('pytsite.plugman@run_plugin_update_hook', {
            'plugin': p_name,
            'version_from': v_from,
            'version_to': v_to,
        }))

        # plugin_install()
        if hasattr(plugin, 'plugin_install') and callable(plugin.plugin_install):
            plugin.plugin_install()
        _events.fire('pytsite.plugman@install', name=p_name)

        # plugin_update()
        if hasattr(plugin, 'plugin_update') and callable(plugin.plugin_update):
            plugin.plugin_update(v_from=v_from)
        _events.fire('pytsite.plugman@update', name=p_name, v_from=v_from)

        # Remove info from update queue
        _api.rm_update_info(p_name)
