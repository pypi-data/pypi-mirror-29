import os
import stat
from mako.lookup import TemplateLookup
from zc.buildout import UserError


class Recipe:
    """Buildout recipe for making files out of Mako templates.

    All part options are directly available to the template. In addition,
    all options from all buildout parts are available to the templates
    through ``parts[<part>][<key>]``.
    """

    def __init__(self, buildout, name, options):
        """Prepare recipe, any issue with options will be resolved on this step.

        On this step:
        * parse ``directories`` option and resolve paths,
        * parse``files`` option, detect collision, resolve targets paths.
        * create Makos ``lookup`` object with provided ``directories`` as a parameter
        """
        self.buildout = buildout
        self.options = options
        self.files = _parse_files_option(options.get('files'))
        directories = _parse_directories_option(
            options.get('directories', buildout["buildout"]["directory"]))
        self.lookup = TemplateLookup(directories=directories)

    def install(self):
        """One by one render ``template`` and write result to ``destination``."""
        kwargs = dict(self.options)
        kwargs.setdefault('parts', dict(self.buildout))
        for template, target, is_executable in self.files:
            self.options.created(target)
            with open(target, "w") as f:
                f.write(self.lookup.get_template(template).render(**kwargs))
            if is_executable:
                os.chmod(target, os.stat(target).st_mode | stat.S_IEXEC)
        return self.options.created()

    update = install


def _parse_list_values(value):
    """Transform string `values` into list of striped lines, remove empty lines.

    For example:

    .. code-block:: python

        >>> value = ' a \\n \\n b \\n'
        >>> list(_parse_list_values(value))
        ['a', 'b']

    """
    items = (i.strip() for i in value.strip().split('\n'))
    items = (i for i in items if i)
    return items


def _parse_directories_option(value):
    """Parse string value and return a list of resolved absolute paths.

    For example:

    .. code-block:: python

        >>> import os; os.chdir('/tmp')
        >>> _parse_directories_option('/data')
        ['/data']
        >>> _parse_directories_option('data')
        ['/tmp/data']

    """
    directories = (os.path.abspath(i) for i in _parse_list_values(value))
    return list(directories)


def _parse_files_option(value):
    """Transform string `values` into list of source-target files, detect collisions.

    Input format:

    .. code-block::

        source : target [: is_executable(true or false)[ :collision_allowed(just a flag))]]
        ...

    Output format is following:

    .. code-block:: python

        [(template, target_resolved_abs_path, is_executable), ...]

    For example:

    .. code-block:: python

        >>> import os; os.chdir('/tmp')
        >>> _parse_files_option('a:b:yes')
        [('a', '/tmp/b', True)]
        >>> _parse_files_option('a:/b')
        [('a', '/b', False)]
        >>> _parse_files_option('a:/b::collision_allowed')
        [('a', '/b', False)]

    """
    sources = set()
    targets = set()
    files = []

    for line in _parse_list_values(value):
        options = tuple(i.strip() for i in line.split(':'))

        if not (1 < len(options) < 5):
            raise UserError(
                "Malformed file option '{}'\nallowed format is "
                "'source:target[:is_executable(true or false)[:collision_allowed]]'"
                "".format(line)
            )

        source = options[0]
        target = os.path.abspath(options[1])
        is_executable = len(options) > 2 and _to_bool(options[2])
        collision_allowed = len(options) > 3 and options[3] == 'collision_allowed'

        if not collision_allowed and source in sources:
            raise UserError("Template collision is detected at '{}'".format(line))

        if not collision_allowed and target in targets:
            raise UserError("Target collision is detected at '{}'".format(line))

        sources.add(source)
        targets.add(target)
        files.append((source, target, is_executable))

    return files


def _to_bool(value):
    """Transform string value to bool.

    Return `True` is input `value` is "yes" or "true", or "1" or "on",
    return `False` for all other cases.

    For example:

    .. code-block:: python

        >>> _to_bool('yes')
        True
        >>> _to_bool('no')
        False
        >>> _to_bool('')
        False

    """
    return value.lower() in ("yes", "true", "1", "on")
