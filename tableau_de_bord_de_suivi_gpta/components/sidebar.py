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
                "w-full flex items-center text-left px-3 py-3 text-sm font-medium rounded-md bg-[#F68B1E] text-white transition-colors duration-150",
                "w-full flex items-center text-left px-3 py-3 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-100 hover:text-[#F68B1E] transition-colors duration-150",
            ),
        ),
        key=f"organ-item-{index}",
    )


def sidebar_component() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Organes",
                    class_name="text-lg font-semibold text-gray-800 mb-4",
                ),
                rx.el.button(
                    "Ajouter un Organe",
                    on_click=GptaState.toggle_add_organ_modal,
                    class_name="w-full px-4 py-2 text-sm font-medium text-white bg-[#F68B1E] rounded-md hover:bg-[#D67A1A] transition-colors duration-150",
                ),
                class_name="p-4",
            ),
            rx.el.nav(
                rx.el.ul(
                    rx.foreach(
                        GptaState.organs,
                        organ_sidebar_item,
                    ),
                    class_name="space-y-1",
                ),
                class_name="px-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.img(
                        src="/oncf_logo_new.png",
                        alt="Logo ONCF",
                        class_name="sidebar-logo",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.el.img(
                        src="/ensem_logo.png",
                        alt="Logo ENSEM",
                        class_name="sidebar-logo",
                    ),
                ),
                class_name="sidebar-logo-container",
            ),
            class_name="h-full flex flex-col",
        ),
        class_name="fixed top-16 left-0 w-72 h-[calc(100vh-4rem)] bg-white border-r border-gray-200 overflow-y-auto",
    )