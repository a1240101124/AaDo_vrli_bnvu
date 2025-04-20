from nicegui import ui

with ui.card():
    ui.button("button A")
    ui.label("label A")

with ui.card():
    ui.button("button B")
    ui.label("label B")


ui.run()
