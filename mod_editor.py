import os
import os.path
import shutil
import shlex
import subprocess

import sublime
import sublime_plugin

from .helpers.settings import Settings
from .helpers.path import MEPath


settings = None

def plugin_loaded():
    global settings
    settings = Settings()


class MEEventListener(sublime_plugin.EventListener):

    def on_load(self, view):
        path = MEPath(view.file_name())

        if path.from_edit_tree:
            print("%s is in noedit tree root, setting readonly" % path.edit_tree_path)
            view.set_read_only(True)

        if (path.from_edit_tree or path.from_project_dir) \
           and path.has_any_ext(settings.syntax_sigil):

            print("Detected syntax sigil, setting syntax to %s" % settings.syntax_file)
            try:
                view.set_syntax_file(settings.syntax_file)
            except Exception as e:
                print("Couldn't set syntax: %s" % e)

        if path.has_any_ext(settings.noedit_sigil):
            print("Detected noedit sigil, setting readonly")
            view.set_read_only(True)


class ModEditEditCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file = MEPath(self.view.file_name())
        file.copy_to_project()
        self.view.window().open_file(file.project_path)
        self.view.window().run_command("reveal_in_side_bar")


class ModEditShowOriginalCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        open_file = MEPath(self.view.file_name())

        if open_file.exists_in_edit_tree:
            self.view.window().open_file(open_file.edit_tree_path)
            self.view.window().run_command("reveal_in_side_bar")
        else:
            print("No such file: %s" % open_file.edit_tree_path)


class ModEditWriteSimilarCommand(sublime_plugin.TextCommand):

    class FileInputHandler(sublime_plugin.TextInputHandler):

        def __init__(self, o_dir, fname):
            self.dir = o_dir
            self.fname = fname

        def initial_text(self):
            return self.fname

        def placeholder(self):
            return self.fname

        def preview(self, text):
            preview_dir = os.path.relpath(self.dir, settings.project_dir)
            return os.path.join(preview_dir, text)

        def description(self, text):
            return "The filename to create"

        def next_input(self, *args, **kwargs):
            return None


    def input(self, *args, **kwargs):
        path = MEPath(self.view.file_name())
        return self.FileInputHandler(*os.path.split(path.project_path))

    def run(self, edit, file=None):
        desired_name = file

        file = MEPath(self.view.file_name())
        if file.from_edit_tree:

            dest_path = file.project_path
            dest_path, f = os.path.split(dest_path)
            name, ext = os.path.splitext(f)
            ext = ext or (name if name.startswith(".") else "")

            out_name = desired_name or "untitled%s" % ext
            out_path = os.path.join(dest_path, out_name)

        elif file.from_project_dir:

            dest_path, f = os.path.split(file)
            name, ext = os.path.splitext(f)
            ext = ext or (name if name.startswith(".") else "")

            out_name = desired_name or "untitled%s" % ext

            out_path = os.path.join(dest_path, out_name)

        else:
            raise ValueError("Not in edit tree or project dir, will not make similar")

        new_view = self.view.window().open_file(out_path)



class ModEditConfigureCommand(sublime_plugin.WindowCommand):

    def run(self):
        edit_tree = settings.edit_tree
        project_dir = settings.project_dir

        self.view.window().set_project_data({
            "folders": [
                {
                    "path": edit_tree,
                    "name": os.path.basename(edit_tree),
                    "folder_exclude_patterns": [],
                    "follow_symlinks": True
                },
                {
                    "path": project_dir,
                    "name": os.path.basename(project_dir),
                    "file_exclude_patterns": [],
                    "follow_symlinks": True
                }
            ],
            "settings":
            {
                "tab_size": 4
            }
        })


class ModEditEditImageCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file = MEPath(self.view.file_name())
        file.copy_to_project()
        cmd = shlex.split(settings.image_open_cmd % file.project_path)
        subprocess.call(cmd)
        

