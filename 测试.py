from datetime import datetime

from nicegui import ui


@ui.refreshable
def time():
    ui.label(f"Time: {datetime.now()}")


@ui.page("/global_refreshable")
def demo():
    time()
    ui.button("Refresh", on_click=time.refresh)


ui.link("Open demo", demo)

ui.run()
