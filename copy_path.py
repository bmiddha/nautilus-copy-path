from typing import List

import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Nautilus", "4.1")

from gi.repository import Gdk, GObject, Nautilus


class CopyPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def _copy_path(self, _menu: Nautilus.MenuItem, text: str) -> None:
        display = Gdk.Display.get_default()
        if display is None:
            raise RuntimeError("Unable to access the display clipboard")
        display.get_clipboard().set(text)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        paths = [file.get_location().get_path() for file in files]
        if not paths or any(path is None for path in paths):
            return []

        multiple = len(paths) > 1
        item = Nautilus.MenuItem(
            name="CopyPathExtension::CopyPath",
            label="Copy Paths" if multiple else "Copy Path",
            tip="Copy selected paths" if multiple else "Copy the selected path",
        )
        item.connect("activate", self._copy_path, "\n".join(paths))
        return [item]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        path = current_folder.get_location().get_path()
        if path is None:
            return []

        item = Nautilus.MenuItem(
            name="CopyPathExtension::CopyCurrentFolderPath",
            label="Copy Path",
            tip="Copy the current folder path",
        )
        item.connect("activate", self._copy_path, path)
        return [item]
