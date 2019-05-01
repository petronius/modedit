import sublime


class Settings:

    SETTINGS_FILE = "ModEdit.sublime-settings"

    PROP_KEYS = [
        "edit_tree",
        "syntax_sigil",
        "syntax_file",
        "project_dir",
        "noedit_sigil",
        "image_open_cmd",
    ]

    def __init__(self):
        self._settings = sublime.load_settings(self.SETTINGS_FILE)
        self._load()
        for k in self.PROP_KEYS:
            self._settings.add_on_change(k, lambda *args, **kwargs: self._load())

    def _load(self):
        for k in self.PROP_KEYS:
            v = self._settings.get(k)
            setattr(self, k, v)
            if v is None:
                raise ValueError("%s cannot be empty or None!" % k)


