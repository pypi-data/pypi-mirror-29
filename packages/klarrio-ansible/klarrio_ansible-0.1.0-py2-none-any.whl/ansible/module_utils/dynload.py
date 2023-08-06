from ansible.errors import AnsibleModuleError
from ansible.plugins.loader import module_utils_loader as ml


def dynload(filename, obj):
    """
    Custom module loader for dynamically loading module_utils into Action Plugins.
    Works for module_utils in the same role as well as from other (dependent) roles.

    :param filename: The file name of the Python module to load
    :type filename: str
    :param obj: The object to import from the module
    :type obj: str
    """

    # Check if we can find the requested plugin file
    fp = ml.find_plugin(filename)

    if not fp:
        raise AnsibleModuleError("Cannot resolve module_utils dependency '{}'".format(filename))

    # Load the module and return the requested object handle
    do = getattr(ml._load_module_source(filename, fp), obj)

    if do is None:
        raise AnsibleModuleError("Could not load object '{}' from module {}".format(obj, filename))

    return do
