import inspect
import json
import os
import pkgutil
import logging

LOGGER = logging.getLogger(__name__)

class Plugin:
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    name = 'UNKOWN'
    plugin_config = {}

    def __init__(self, plugin_config=None):
        """
        init plugin with plugin_config
        :param plugin_config:
        """
        if plugin_config:
            self.set_plugin_config(plugin_config)

    def set_plugin_config(self, plugin_config):
        """
        set plugin config for plugin
        :param plugin_config:
        :return:
        """
        self.plugin_config = json.loads(plugin_config)

    def get_cls_str(self):
        """
        compile class string
        :return:
        """
        return '.'.join([self.__class__.__module__, self.__class__.__name__])

    def get_available_versions(self, product):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError

    def dl_fw(self, version):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError


class PluginCollection:
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_package):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.reload_plugins()

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        LOGGER.info('Looking for plugins under package %s', self.plugin_package)
        self.walk_package(self.plugin_package)

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=['blah'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, Plugin) & (c is not Plugin):
                        LOGGER.info('    Found plugin class: %s.%s', c.__module__, c.__name__)
                        self.plugins.append(c())

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])  # pylint: disable=R1721

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)
