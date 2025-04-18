from nicegui import ui

with ui.left_drawer(value=True).props("width=150").classes("bg-blue-grey-1"):
    ui.label("1111")


ui.run()
