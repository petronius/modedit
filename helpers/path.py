import os.path
import shutil

from .settings import Settings


class MEPath:

    def __init__(self, path):
        self.settings = Settings()

        self._original = path

        if not self.in_edit_tree(path) and not self.in_project_dir(path):
            raise ValueError("Path does not exist in project dir or edit tree!")

        self.edit_tree_path = self._path_in_edit_tree(path)
        self.project_path = self._path_in_project(path)

        if os.path.isdir(self.edit_tree_path) != os.path.isdir(self.project_path):
            raise Exception("Path exists in both dirs, but is different kinds!")


    def copy_to_project(self):
        if not os.path.exists(self.project_path):
            os.makedirs(os.path.dirname(self.project_path), exist_ok=True)
            print("Copying %s to %s for editing" % (self.edit_tree_path, self.project_path))
            shutil.copyfile(self.edit_tree_path, self.project_path)

    def has_any_ext(self, exts):
        return any([self._original.endswith(ext) for ext in exts])

    @property
    def exists_in_edit_tree(self):
        return os.path.exists(self.edit_tree_path)

    @property
    def exists_in_project(self):
        return os.path.exists(self.project_path)

    @property
    def from_edit_tree(self):
        return self.in_edit_tree(self._original)

    @property
    def from_project_dir(self):
        return self.in_project_dir(self._original)

    @staticmethod
    def in_edit_tree(path):
        settings = Settings()
        return path.startswith(settings.edit_tree)

    @staticmethod
    def in_project_dir(path):
        settings = Settings()
        return path.startswith(settings.project_dir)
 
    def _path_in_project(self, path_in_edit_tree, make=False):
        edit_tree = self.settings.edit_tree
        project_dir = self.settings.project_dir
        if self.in_project_dir(path_in_edit_tree):
            return path_in_edit_tree
        elif self.in_edit_tree(path_in_edit_tree):
            dest_path = os.path.join(project_dir, os.path.relpath(path_in_edit_tree, edit_tree))
            return dest_path
        else:
            raise ValueError("Not a path in the edit tree or the project dir!")

    def _path_in_edit_tree(self, path_in_project):
        edit_tree = self.settings.edit_tree
        project_dir = self.settings.project_dir
        if self.in_project_dir(path_in_project):
            return os.path.join(edit_tree, os.path.relpath(path_in_project, project_dir))
        elif self.in_edit_tree(path_in_project):
            return path_in_project
        else:
            raise ValueError("Not a path in the edit tree or the project dir!")
