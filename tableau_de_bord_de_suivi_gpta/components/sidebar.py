import reflex as rx
from tableau_de_bord_de_suivi_gpta.states.gpta_state import GptaState, Organ
from typing import cast


def organ_sidebar_item(
    organ: Organ, index: int
) -> rx.Component:
    is_selected = (
        GptaState.selected_organ_name == organ["name"]
    )
    reliability_value = organ["reliability_at_t"]
    is_reliability_alert_condition = (
        reliability_value != None
    ) & (
        reliability_value
        < GptaState.min_reliability_threshold
    )
    dot_span_class_name = rx.cond(
        is_reliability_alert_condition,
        "bg-red-500 animate-pulse w-3 h-3 rounded-full ml-2",
        "bg-green-500 w-3 h-3 rounded-full ml-2",
    )
    return rx.el.li(
        rx.el.button(
            rx.el.span(
                organ["name"], class_name="flex-1 truncate"
            ),
            rx.cond(
                reliability_value == None,
                rx.fragment(),
                rx.el.span(class_name=dot_span_class_name),
            ),
            on_click=lambda: GptaState.set_selected_organ(
                organ["name"]
            ),
            class_name=rx.cond(
                is_selected,
                "w-full flex items-center text-left px-3 py-3 text-sm font-medium rounded-md bg-indigo-100 text-indigo-700 transition-colors duration-150",
                "w-full flex items-center text-left px-3 py-3 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors duration-150",
            ),
        ),
        key=f"organ-item-{index}",
    )


def sidebar_component() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.h2(
                "Organes GPTA",
                class_name="text-xl font-semibold text-gray-800 mb-6 px-3",
            ),
            rx.el.ul(
                rx.foreach(
                    GptaState.organs, organ_sidebar_item
                ),
                role="list",
                class_name="space-y-1",
            ),
            rx.el.div(
                rx.el.button(
                    "Ajouter un Organe",
                    on_click=GptaState.toggle_add_organ_modal,
                    class_name="mt-6 w-full px-3 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                ),
                class_name="px-3",
            ),
            class_name="py-6",
        ),
        class_name="w-72 bg-white border-r border-gray-200 shadow-sm h-screen overflow-y-auto fixed top-0 left-0 pt-16",
    )