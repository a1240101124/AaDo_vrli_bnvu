import platform
from pathlib import Path
from typing import Optional

from nicegui import events, ui


class local_file_picker(ui.dialog):
    def __init__(
        self,
        directory: str,
        *,
        upper_limit: Optional[str] = ...,  # type: ignore
        multiple: bool = False,
        show_hidden_files: bool = False,
    ) -> None:  # type: ignore
        """本地文件选择器

        这是一个简单的文件选择器，允许你从运行 NiceGUI 的本地文件系统中选择文件。

        参数：
            directory: 文件选择器开始的目录。
            upper_limit: 文件选择器能到达的最高目录。(None: 无限制，默认值:开始的目录)。
            multiple: 是否允许选择多个文件。
            show_hidden_files: 是否显示隐藏文件。
        """
        super().__init__()

        self.path = Path(directory).expanduser()
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(directory if upper_limit == ... else upper_limit).expanduser()
        self.show_hidden_files = show_hidden_files

        # 创建界面组件
        with self, ui.card().classes("p-4"):
            # 添加输入组件
            with ui.row().classes("w-full items-center space-x-2"):
                self.path_input = (
                    ui.input(placeholder="请输入目录路径").props("square outlined dense").classes("flex-1")
                )
                ui.button("跳转", on_click=self.handle_path_input).classes(
                    "ml-2 h-10 px-4 bg-blue-500 text-white rounded-md"
                )

            self.add_drives_toggle()

            self.grid = (
                ui.aggrid(
                    {
                        "columnDefs": [{"field": "name", "headerName": "File"}],
                        "rowSelection": "multiple" if multiple else "single",
                    },
                    html_columns=[0],
                )
                .classes("w-96 h-96")
                .on("cellDoubleClicked", self.handle_double_click)
            )

            with ui.row().classes("w-full justify-end"):
                ui.button("关闭", on_click=self.close).props("outline")
                ui.button("确定", on_click=self._handle_ok)

        self.update_grid()

    # 该方法仅在 Windows 操作系统中起作用。
    # 它会获取系统中的所有逻辑驱动器，并创建一个 toggle 组件，让用户可以在不同的驱动器之间进行切换。
    def add_drives_toggle(self):
        if platform.system() == "Windows":
            import win32api  # type: ignore

            drives = win32api.GetLogicalDriveStrings().split("\000")[:-1]
            self.drives_toggle = ui.toggle(drives, value=drives[0], on_change=self.update_drive)

    # 根据 toggle 组件当前的值更新当前显示的目录路径，然后调用 update_grid 方法来刷新文件和目录列表
    def update_drive(self):
        self.path = Path(self.drives_toggle.value).expanduser()  # type: ignore
        self.update_grid()

    # 更新显示文件和目录列表的 aggrid 表格。
    def update_grid(self) -> None:
        paths = list(self.path.glob("*"))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith(".")]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options["rowData"] = [
            {
                "name": f"📁 <strong>{p.name}</strong>" if p.is_dir() else f"📄 {p.name}",  # 目录文件
                "path": str(p),
            }
            for p in paths
        ]
        if (self.upper_limit is None and self.path != self.path.parent) or (
            self.upper_limit is not None and self.path != self.upper_limit
        ):
            self.grid.options["rowData"].insert(
                0,
                {
                    "name": "⬅️ <strong>双击返回</strong>",  # 📁 返回上一级目录
                    "path": str(self.path.parent),
                },
            )
        self.grid.update()

    # 处理 aggrid 表格中单元格的双击事件。
    def handle_double_click(self, e: events.GenericEventArguments) -> None:
        self.path = Path(e.args["data"]["path"])
        if self.path.is_dir():
            self.update_grid()
        else:
            self.submit([self.path])

    # 处理跳转事件
    def handle_path_input(self):
        input_path = self.path_input.value
        if input_path:
            try:
                new_path = Path(input_path).expanduser()
                if new_path.is_dir():
                    self.path = new_path
                    self.update_grid()
                else:
                    ui.notify("输入的路径不是有效的目录", type="negative")
            except Exception as e:
                ui.notify(f"发生错误: {e!s}", type="negative")

    # 处理 “Ok” 按钮的点击事件
    async def _handle_ok(self):
        rows = await self.grid.get_selected_rows()  # 获取用户在表格中选择的行

        # 若 rows 列表不为空，说明用户选择了文件，则返回此文件或目录路径；否则将当前所在的目录路径作为结果提交。
        if rows:
            self.submit([Path(row["path"]) for row in rows])
        else:
            self.submit([self.path])
