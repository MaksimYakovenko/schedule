import flet as ft

def main(page: ft.Page):
    page.title = "My Flet Web App"
    page.add(ft.Text("Hello from Flet!"))

ft.app(target=main)
