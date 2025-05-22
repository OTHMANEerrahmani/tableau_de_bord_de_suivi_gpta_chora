import reflex as rx
from tableau_de_bord_de_suivi_gpta.states.gpta_state import (
    GptaState,
    FailureLogEntry,
    Organ,
)
from tableau_de_bord_de_suivi_gpta.components.charts import (
    reliability_curve_chart,
    mtbf_mttr_bar_chart,
    pareto_chart_component,
)
from typing import Optional


def metric_card(
    title: str,
    value: rx.Var[float | None],
    unit: str = "",
    is_percentage: bool = False,
    precision: int = 2,
    alert_style: Optional[rx.Var[str]] = None,
) -> rx.Component:
    value_p_class = alert_style if alert_style is not None else "text-indigo-600 text-2xl font-semibold mt-1"
    display_value = rx.cond(
        value.is_none(),
        "N/A",
        rx.cond(
            is_percentage,
            f"{{:.{precision}f}} %".format(value.to(float) * 100),
            f"{{:.{precision}f}}".format(value.to(float)) + (f" {unit}" if unit else ""),
        ),
    )
    return rx.el.div(
        rx.el.h4(
            title,
            class_name="text-sm font-medium text-gray-500 truncate",
        ),
        rx.el.p(display_value, class_name=value_p_class),
        class_name="bg-white p-4 rounded-lg shadow border border-gray-200 flex flex-col justify-between",
    )


def failure_log_table_row(
    log_entry: FailureLogEntry, index: int
) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            log_entry["failure_date"],
            class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            log_entry[
                "uptime_since_last_failure"
            ].to_string(),
            class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-600 text-right",
        ),
        rx.el.td(
            log_entry["repair_duration"].to_string(),
            class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-600 text-right",
        ),
        rx.el.td(
            log_entry["description"],
            class_name="px-4 py-3 text-sm text-gray-600 max-w-xs truncate",
        ),
        class_name=rx.cond(
            index % 2 == 0, "bg-gray-50", "bg-white"
        ),
    )


def organ_detail_view() -> rx.Component:
    details: rx.Var[Organ | None] = (
        GptaState.selected_organ_details
    )
    reliability_value_class = rx.cond(
        details["reliability_at_t"].is_none()
        | (
            details["reliability_at_t"]
            >= GptaState.min_reliability_threshold
        ),
        "text-green-600 text-2xl font-semibold mt-1",
        "text-red-600 animate-pulse text-2xl font-semibold mt-1",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Détails pour: ",
                rx.el.span(
                    GptaState.selected_organ_name,
                    class_name="text-indigo-700 font-bold",
                ),
                class_name="text-2xl font-semibold text-gray-800",
            ),
            rx.el.button(
                "Exporter en CSV",
                on_click=GptaState.export_selected_organ_data_csv,
                class_name="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.h4(
                "Paramètres de Calcul",
                class_name="text-md font-medium text-gray-700 mb-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Temps de fonctionnement visé (t) en heures:",
                        class_name="block text-sm font-medium text-gray-600 mr-2",
                    ),
                    rx.el.input(
                        type="number",
                        default_value=GptaState.target_uptime_t.to_string(),
                        on_change=GptaState.set_target_uptime_t.debounce(
                            500
                        ),
                        class_name="w-32 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    ),
                    class_name="flex items-center mb-2",
                ),
                rx.el.div(
                    rx.el.label(
                        "Fiabilité minimale souhaitée (R):",
                        class_name="block text-sm font-medium text-gray-600 mr-2",
                    ),
                    rx.el.input(
                        type="number",
                        step="0.01",
                        min="0.000001",
                        max="0.999999",
                        default_value=GptaState.min_reliability_threshold.to_string(),
                        on_change=GptaState.set_min_reliability_threshold.debounce(
                            500
                        ),
                        class_name="w-32 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    ),
                    rx.el.span(
                        f" (Actuel: {GptaState.min_reliability_threshold.to(float) * 100.0:.2f}% )",
                        class_name="ml-2 text-sm text-gray-500",
                    ),
                    class_name="flex items-center",
                ),
                class_name="p-4 bg-gray-50 rounded-lg shadow-sm border border-gray-200 mb-6",
            ),
        ),
        rx.el.div(
            metric_card("MTBF", details["mtbf"], "heures"),
            metric_card("MTTR", details["mttr"], "heures"),
            metric_card(
                "Taux de Défaillance (λ)",
                details["lambda_val"],
                precision=6,
            ),
            metric_card(
                f"Fiabilité R(t={GptaState.target_uptime_t.to(float):.0f}h)",
                details["reliability_at_t"],
                is_percentage=True,
                alert_style=reliability_value_class,
            ),
            metric_card(
                "Disponibilité (D)",
                details["availability"],
                is_percentage=True,
            ),
            metric_card(
                "Période Maintenance Préventive",
                details["preventive_maintenance_period"],
                "heures",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6",
        ),
        rx.el.div(
            reliability_curve_chart(),
            mtbf_mttr_bar_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    "Historique des Pannes",
                    class_name="text-lg font-medium text-gray-700",
                ),
                rx.el.button(
                    "Ajouter un Relevé",
                    on_click=lambda: GptaState.toggle_add_failure_modal(
                        GptaState.selected_organ_name
                    ),
                    class_name="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700",
                ),
                class_name="flex justify-between items-center mb-3",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date Panne",
                                class_name="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Temps Fonct. (h)",
                                class_name="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Durée Répar. (h)",
                                class_name="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Description",
                                class_name="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            GptaState.selected_organ_failure_history,
                            failure_log_table_row,
                        ),
                        rx.cond(
                            GptaState.selected_organ_failure_history.length()
                            == 0,
                            rx.el.tr(
                                rx.el.td(
                                    "Aucune panne enregistrée pour cet organe.",
                                    col_span=4,
                                    class_name="px-4 py-3 text-sm text-gray-500 text-center",
                                )
                            ),
                            rx.fragment(),
                        ),
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="overflow-x-auto bg-white rounded-lg shadow border border-gray-200",
            ),
        ),
        key=GptaState.selected_organ_name,
    )


def placeholder_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Bienvenue au Tableau de Bord GPTA",
            class_name="text-2xl font-semibold text-gray-700 mb-4",
        ),
        rx.el.p(
            "Sélectionnez un organe dans la barre latérale pour afficher ses détails de performance et de maintenance.",
            class_name="text-gray-600",
        ),
        rx.el.div(
            pareto_chart_component(), class_name="mt-8"
        ),
        class_name="flex flex-col items-center justify-center h-full p-8 text-center",
    )


def main_content_area() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.cond(
                GptaState.selected_organ_name.is_not_none(),
                organ_detail_view(),
                placeholder_view(),
            ),
            class_name="py-8 px-4 sm:px-6 lg:px-8",
        ),
        class_name="flex-1 overflow-y-auto ml-72 pt-16",
    )