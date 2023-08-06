import os
import signal
import subprocess
import sys
import time
import traceback

import _thread

# This import does nothing, but it's necessary to avoid some race conditions
# in the threading module. See http://code.djangoproject.com/ticket/2330 .
try:
    import threading  # NOQA
except ImportError:
    pass

try:
    import termios
except ImportError:
    termios = None

USE_INOTIFY = False
try:
    # Test whether inotify is enabled and likely to work
    import pyinotify

    fd = pyinotify.INotifyWrapper.create().inotify_init()
    if fd >= 0:
        USE_INOTIFY = True
        os.close(fd)
except ImportError:
    pass

RUN_RELOADER = True

_mtimes = {}
_win = (sys.platform == "win32")

_exception = None
_error_files = []
_cached_modules = set()
_cached_filenames = []


def gen_filenames(only_new=False):
    """
    Return a list of filenames referenced in sys.modules and translation files.
    """
    # N.B. ``list(...)`` is needed, because this runs in parallel with
    # application code which might be mutating ``sys.modules``, and this will
    # fail with RuntimeError: cannot mutate dictionary while iterating
    global _cached_modules, _cached_filenames
    module_values = set(sys.modules.values())
    _cached_filenames = clean_files(_cached_filenames)
    if _cached_modules == module_values:
        # No changes in module list, short-circuit the function
        if only_new:
            return []
        else:
            return _cached_filenames + clean_files(_error_files)

    new_modules = module_values - _cached_modules
    new_filenames = clean_files(
        [filename.__file__ for filename in new_modules
         if hasattr(filename, '__file__')])

    _cached_modules = _cached_modules.union(new_modules)
    _cached_filenames += new_filenames
    if only_new:
        return new_filenames + clean_files(_error_files)
    else:
        return _cached_filenames + clean_files(_error_files)


def clean_files(filelist):
    filenames = []
    for filename in filelist:
        if not filename:
            continue
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if os.path.exists(filename):
            filenames.append(filename)
    return filenames


def inotify_code_changed():
    """
    Check for changed code using inotify. After being called
    it blocks until a change event has been fired.
    """
    class EventHandler(pyinotify.ProcessEvent):
        modified_code = None

        def process_default(self, event):
            EventHandler.modified_code = True

    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler())

    def update_watch(sender=None, **kwargs):
        if sender and getattr(sender, 'handles_files', False):
            # No need to update watches when request serves files.
            # (sender is supposed to be a django.core.handlers.BaseHandler subclass)
            return
        mask = (
            pyinotify.IN_MODIFY |
            pyinotify.IN_DELETE |
            pyinotify.IN_ATTRIB |
            pyinotify.IN_MOVED_FROM |
            pyinotify.IN_MOVED_TO |
            pyinotify.IN_CREATE |
            pyinotify.IN_DELETE_SELF |
            pyinotify.IN_MOVE_SELF
        )
        for path in gen_filenames(only_new=True):
            wm.add_watch(path, mask)

    # Block until an event happens.
    update_watch()
    notifier.check_events(timeout=None)
    notifier.read_events()
    notifier.process_events()
    notifier.stop()

    # If we are here the code must have changed.
    return EventHandler.modified_code


def code_changed():
    global _mtimes, _win
    for filename in gen_filenames():
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            try:
                del _error_files[_error_files.index(filename)]
            except ValueError:
                pass
            return True

    return False


def check_errors(fn):
    def wrapper(*args, **kwargs):
        global _exception
        try:
            fn(*args, **kwargs)
        except Exception:
            _exception = sys.exc_info()

            et, ev, tb = _exception

            if getattr(ev, 'filename', None) is None:
                # get the filename from the last item in the stack
                filename = traceback.extract_tb(tb)[-1][0]
            else:
                filename = ev.filename

            if filename not in _error_files:
                _error_files.append(filename)

            raise

    return wrapper


def raise_last_exception():
    global _exception
    if _exception is not None:
        raise _exception[1]


def ensure_echo_on():
    if termios:
        fd = sys.stdin
        if fd.isatty():
            attr_list = termios.tcgetattr(fd)
            if not attr_list[3] & termios.ECHO:
                attr_list[3] |= termios.ECHO
                if hasattr(signal, 'SIGTTOU'):
                    old_handler = signal.signal(signal.SIGTTOU, signal.SIG_IGN)
                else:
                    old_handler = None
                termios.tcsetattr(fd, termios.TCSANOW, attr_list)
                if old_handler is not None:
                    signal.signal(signal.SIGTTOU, old_handler)


def reloader_thread():
    ensure_echo_on()
    if USE_INOTIFY:
        fn = inotify_code_changed
    else:
        fn = code_changed
    while RUN_RELOADER:
        change = fn()
        if change:
            sys.exit(3)  # force reload

        time.sleep(1)


def restart_with_reloader():
    while True:
        args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions]
        args += sys.argv
        new_environ = os.environ.copy()
        new_environ["RUN_MAIN"] = 'true'
        exit_code = subprocess.call(args, env=new_environ)
        if exit_code != 3:
            return exit_code


def python_reloader(main_func, args, kwargs):
    if os.environ.get("RUN_MAIN") == "true":
        _thread.start_new_thread(main_func, args, kwargs)
        try:
            reloader_thread()
        except KeyboardInterrupt:
            pass
    else:
        try:
            exit_code = restart_with_reloader()
            if exit_code < 0:
                os.kill(os.getpid(), -exit_code)
            else:
                sys.exit(exit_code)
        except KeyboardInterrupt:
            pass


def main(main_func, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    wrapped_main_func = check_errors(main_func)
    python_reloader(wrapped_main_func, args, kwargs)
