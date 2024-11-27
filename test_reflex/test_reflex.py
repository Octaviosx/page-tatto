"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import requests
from PIL import Image
from rxconfig import config


class State(rx.State):
    """The app state."""

    # The images to show.
    img: list[str]

    @rx.event
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)


color = "#2596be"

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def navbar_user() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        "ART MOUT", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Inicio", "/#"),
                    navbar_link("Promociones", "/#"),
                    navbar_link("¿Quienes Somos?", "/#"),
                    navbar_link("Contacto", "/#"),
                    spacing="5",
                    color = "white",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="assets/images.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Reflex", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon("user"),
                            size="2",
                            radius="full",
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item("Settings"),
                        rx.menu.item("Earnings"),
                        rx.menu.separator(),
                        rx.menu.item("Log out"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        #bg=rx.color("accent", 3),
        bg="black",
        padding="1em",
        position="fixed",
        top="0px",
        z_index="1",
        width="100%",
    )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
        navbar_user(),
        rx.text(
            "Subir un archivo de prueba",
            size = "8",
            align = "center",
            color = "#2874a6",
            weight = "bold",
            padding_top = "5em"
        ),
        rx.upload(
            rx.vstack(
                rx.button(
                    "Selecciona Archivo",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Haz clic para subir una imagen",
                    color = "#2874a6",
                ),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("upload1"), rx.text
            )
        ),
        rx.button(
            "Subir imagen",
            on_click=State.handle_upload(
                rx.upload_files(upload_id="upload1")
            ),
        ),
        rx.button(
            "Limpiar",
            bg = "white",
            color = "black",
            on_click=rx.clear_selected_files("upload1"),
        ),
        rx.foreach(
            State.img,
            lambda img: rx.image(
                src=rx.get_upload_url(img)
            ),
        ),
        #padding="5em",
        bg = "white",
        align = "center",
    )


app = rx.App()
#app.add_page(navbar_user)
app.add_page(index)

