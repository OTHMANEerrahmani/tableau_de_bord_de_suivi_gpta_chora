import reflex as rx
from tableau_de_bord_de_suivi_gpta.states.gpta_state import GptaState, Organ


def add_organ_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h3(
                "Ajouter un Nouvel Organe",
                class_name="text-lg font-medium leading-6 text-gray-900 mb-4",
            ),
            rx.el.input(
                placeholder="Nom de l'organe",
                on_change=GptaState.set_new_organ_name_input,
                class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#F68B1E] focus:border-[#F68B1E] sm:text-sm mb-4",
                default_value=GptaState.new_organ_name_input,
            ),
            rx.el.div(
                rx.el.button(
                    "Annuler",
                    on_click=GptaState.toggle_add_organ_modal,
                    class_name="mr-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-transparent rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#F68B1E]",
                ),
                rx.el.button(
                    "Ajouter",
                    on_click=GptaState.add_new_organ,
                    class_name="px-4 py-2 text-sm font-medium text-white bg-[#F68B1E] border border-transparent rounded-md shadow-sm hover:bg-[#D67A1A] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#F68B1E]",
                ),
                class_name="flex justify-end",
            ),
            class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
        ),
        open=GptaState.show_add_organ_modal,
        class_name="fixed inset-0 z-50 open:flex items-center justify-center p-4",
    )


def add_failure_log_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h3(
                "Ajouter un Relevé de Panne",
                class_name="text-lg font-medium leading-6 text-gray-900 mb-4",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Organe:",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.select(
                        rx.foreach(
                            GptaState.organs,
                            lambda organ: rx.el.option(
                                organ["name"],
                                value=organ["name"],
                            ),
                        ),
                        default_value=GptaState.new_failure_organ_name,
                        name="organ_name",
                        class_name="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#F68B1E] focus:border-[#F68B1E] sm:text-sm",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Date de la panne:",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        type="date",
                        default_value=GptaState.new_failure_date,
                        name="failure_date",
                        class_name="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#F68B1E] focus:border-[#F68B1E] sm:text-sm",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Temps de fonctionnement depuis la dernière panne (heures):",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        type="number",
                        step="0.1",
                        min="0",
                        default_value=GptaState.new_failure_uptime,
                        name="uptime_since_last_failure",
                        class_name="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#F68B1E] focus:border-[#F68B1E] sm:text-sm",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Durée de la réparation (heures):",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        type="number",
                        step="0.1",
                        min="0",
                        default_value=GptaState.new_failure_repair_duration,
                        name="repair_duration",
                        class_name="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#F68B1E] focus:border-[#F68B1E] sm:text-sm",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description de la panne:",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.textarea(
                        default_value=GptaState.new_failure_description,
                        name="description",
                        class_name="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#F68B1E] focus:border-[#F68B1E] sm:text-sm",
                        required=True,
                        rows=3,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Annuler",
                        type="button",
                        on_click=GptaState.toggle_add_failure_modal,
                        class_name="mr-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-transparent rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#F68B1E]",
                    ),
                    rx.el.button(
                        "Ajouter",
                        type="submit",
                        class_name="px-4 py-2 text-sm font-medium text-white bg-[#F68B1E] border border-transparent rounded-md shadow-sm hover:bg-[#D67A1A] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#F68B1E]",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=GptaState.handle_failure_log_submit,
            ),
            class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
        ),
        open=GptaState.show_add_failure_modal,
        class_name="fixed inset-0 z-50 open:flex items-center justify-center p-4",
    )