import reflex as rx
from tableau_de_bord_de_suivi_gpta.states.gpta_state import GptaState
from tableau_de_bord_de_suivi_gpta.components.sidebar import sidebar_component
from tableau_de_bord_de_suivi_gpta.components.main_content import main_content_area
from tableau_de_bord_de_suivi_gpta.components.modals import (
    add_organ_modal,
    add_failure_log_modal,
)


def app_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1(
                "Tableau de Bord de Maintenance GPTA",
                class_name="text-2xl font-bold text-white",
            ),
            class_name="container mx-auto px-4 py-4 flex justify-between items-center",
        ),
        class_name="bg-indigo-700 shadow-md fixed top-0 left-0 right-0 z-40",
    )


def index() -> rx.Component:
    return rx.el.div(
        app_header(),
        sidebar_component(),
        main_content_area(),
        add_organ_modal(),
        add_failure_log_modal(),
        rx.toast.provider(),
        on_mount=GptaState.update_all_organ_metrics,
        class_name="flex h-screen bg-gray-100",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/custom_styles.css"],
)
app.add_page(index, title="GPTA Dashboard")