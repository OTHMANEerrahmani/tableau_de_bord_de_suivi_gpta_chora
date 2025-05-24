import reflex as rx
from tableau_de_bord_de_suivi_gpta.states.gpta_state import GptaState
from typing import List, Dict, Any


def pareto_chart_component() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Pareto des Pannes par Organe",
            class_name="text-lg font-medium text-gray-700 mb-3",
        ),
        rx.recharts.composed_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3"
            ),
            rx.recharts.x_axis(
                data_key="name",
                angle=-30,
                text_anchor="end",
                height=70,
                interval=0,
            ),
            rx.recharts.y_axis(
                y_axis_id="left",
                orientation="left",
                stroke="#F68B1E",
                label={
                    "value": "Nb Pannes",
                    "angle": -90,
                    "position": "insideLeft",
                    "fill": "#F68B1E",
                },
            ),
            rx.recharts.y_axis(
                y_axis_id="right",
                orientation="right",
                stroke="#D67A1A",
                label={
                    "value": "Cumulatif (%)",
                    "angle": -90,
                    "position": "insideRight",
                    "fill": "#D67A1A",
                },
                domain=[0, 100],
            ),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.bar(
                data_key="pannes",
                y_axis_id="left",
                name="Nombre de Pannes",
                fill="#F68B1E",
                bar_size=30,
            ),
            rx.recharts.line(
                type="monotone",
                data_key="cumulatif",
                y_axis_id="right",
                name="Pourcentage Cumulatif",
                stroke="#D67A1A",
                stroke_width=2,
                dot={"r": 4},
            ),
            data=GptaState.pareto_chart_data,
            height=300,
            margin={
                "top": 5,
                "right": 20,
                "bottom": 20,
                "left": 30,
            },
        ),
        class_name="p-4 bg-white rounded-lg shadow border border-gray-200",
    )


def reliability_curve_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            f"Courbe de Fiabilité R(t) pour {GptaState.selected_organ_name}",
            class_name="text-lg font-medium text-gray-700 mb-3",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3"
            ),
            rx.recharts.x_axis(
                data_key="temps",
                type="number",
                label={
                    "value": "Temps (heures)",
                    "position": "insideBottom",
                    "offset": -5,
                    "fill": "#6B7280",
                },
                domain=["dataMin", "dataMax"],
            ),
            rx.recharts.y_axis(
                label={
                    "value": "Fiabilité R(t)",
                    "angle": -90,
                    "position": "insideLeft",
                    "fill": "#6B7280",
                },
                domain=[0, 1],
            ),
            rx.recharts.tooltip(
                formatter="(value, name) => [value.toFixed(4), name]"
            ),
            rx.recharts.legend(),
            rx.recharts.line(
                type="monotone",
                data_key="fiabilite",
                name="Fiabilité",
                stroke="#F68B1E",
                stroke_width=2,
                dot=False,
            ),
            data=GptaState.reliability_curve_data_selected_organ,
            height=300,
            margin={
                "top": 5,
                "right": 20,
                "bottom": 20,
                "left": 30,
            },
        ),
        class_name="p-4 bg-white rounded-lg shadow border border-gray-200 mt-6",
    )


def mtbf_mttr_bar_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            f"MTBF & MTTR pour {GptaState.selected_organ_name}",
            class_name="text-lg font-medium text-gray-700 mb-3",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3"
            ),
            rx.recharts.x_axis(data_key="metric"),
            rx.recharts.y_axis(
                label={
                    "value": "Heures",
                    "angle": -90,
                    "position": "insideLeft",
                    "fill": "#6B7280",
                }
            ),
            rx.recharts.tooltip(),
            rx.recharts.bar(
                data_key="valeur",
                name="Heures",
                fill="#F68B1E",
                bar_size=50,
            ),
            data=GptaState.mtbf_mttr_chart_data_selected_organ,
            height=300,
            margin={
                "top": 5,
                "right": 20,
                "bottom": 5,
                "left": 20,
            },
        ),
        class_name="p-4 bg-white rounded-lg shadow border border-gray-200 mt-6",
    )