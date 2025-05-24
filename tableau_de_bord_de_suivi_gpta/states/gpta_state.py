import reflex as rx
from typing import TypedDict, List, Optional, Dict
import math
import datetime
import pandas as pd


class Organ(TypedDict):
    name: str
    mtbf: Optional[float]
    mttr: Optional[float]
    lambda_val: Optional[float]
    reliability_at_t: Optional[float]
    availability: Optional[float]
    preventive_maintenance_period: Optional[float]


class FailureLogEntry(TypedDict):
    organ_name: str
    failure_date: str
    uptime_since_last_failure: float
    repair_duration: float
    description: str


class GptaState(rx.State):
    organs: List[Organ] = [
        {
            "name": "Groupe à vis",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
        {
            "name": "Moteur",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
        {
            "name": "Sécheur d'air",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
        {
            "name": "Électrovanne de régénération",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
        {
            "name": "ADCU (unité de commande)",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
        {
            "name": "Capteur de point de rosée",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
        {
            "name": "Soupape by-pass",
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        },
    ]
    failure_logs: List[FailureLogEntry] = [
        {
            "organ_name": "Groupe à vis",
            "failure_date": "2023-01-15",
            "uptime_since_last_failure": 2000,
            "repair_duration": 10,
            "description": "Défaillance roulement",
        },
        {
            "organ_name": "Groupe à vis",
            "failure_date": "2023-05-20",
            "uptime_since_last_failure": 2800,
            "repair_duration": 12,
            "description": "Fuite joint",
        },
        {
            "organ_name": "Moteur",
            "failure_date": "2023-03-10",
            "uptime_since_last_failure": 3500,
            "repair_duration": 24,
            "description": "Surchauffe",
        },
        {
            "organ_name": "Sécheur d'air",
            "failure_date": "2023-06-01",
            "uptime_since_last_failure": 4000,
            "repair_duration": 8,
            "description": "Colmatage filtre",
        },
        {
            "organ_name": "Groupe à vis",
            "failure_date": "2023-09-10",
            "uptime_since_last_failure": 2500,
            "repair_duration": 15,
            "description": "Vibration excessive",
        },
    ]
    selected_organ_name: Optional[str] = None
    target_uptime_t: float = 1000.0
    min_reliability_threshold: float = 0.95
    new_organ_name_input: str = ""
    show_add_organ_modal: bool = False
    show_add_failure_modal: bool = False
    new_failure_organ_name: str = ""
    new_failure_date: str = (
        datetime.date.today().isoformat()
    )
    new_failure_uptime: str = ""
    new_failure_repair_duration: str = ""
    new_failure_description: str = ""
    selected_year: int = datetime.date.today().year

    def _calculate_metrics_for_organ(
        self, organ_name: str
    ) -> Organ:
        relevant_logs = [
            log
            for log in self.failure_logs
            if log["organ_name"] == organ_name
        ]
        mtbf: Optional[float] = None
        mttr: Optional[float] = None
        lambda_val: Optional[float] = None
        reliability_at_t: Optional[float] = None
        availability: Optional[float] = None
        preventive_maintenance_period: Optional[float] = (
            None
        )
        if relevant_logs:
            total_uptime = sum(
                (
                    log["uptime_since_last_failure"]
                    for log in relevant_logs
                )
            )
            total_repair_duration = sum(
                (
                    log["repair_duration"]
                    for log in relevant_logs
                )
            )
            num_failures = len(relevant_logs)
            if num_failures > 0:
                mtbf = (
                    total_uptime / num_failures
                    if num_failures > 0
                    else None
                )
                mttr = (
                    total_repair_duration / num_failures
                    if num_failures > 0
                    else None
                )
            if mtbf is not None and mtbf > 0:
                lambda_val = 1 / mtbf
                reliability_at_t = math.exp(
                    -lambda_val * self.target_uptime_t
                )
                if (
                    self.min_reliability_threshold > 0
                    and lambda_val > 0
                ):
                    clamped_r = max(
                        1e-06,
                        min(
                            0.999999,
                            self.min_reliability_threshold,
                        ),
                    )
                    preventive_maintenance_period = (
                        -math.log(clamped_r) / lambda_val
                    )
            if (
                mtbf is not None
                and mttr is not None
                and (mtbf + mttr > 0)
            ):
                availability = mtbf / (mtbf + mttr)
        updated_organ_data: Organ = {
            "name": organ_name,
            "mtbf": mtbf,
            "mttr": mttr,
            "lambda_val": lambda_val,
            "reliability_at_t": reliability_at_t,
            "availability": availability,
            "preventive_maintenance_period": preventive_maintenance_period,
        }
        found = False
        for i, organ in enumerate(self.organs):
            if organ["name"] == organ_name:
                self.organs[i] = updated_organ_data
                found = True
                break
        if not found:
            self.organs.append(updated_organ_data)
        return updated_organ_data

    @rx.event
    def update_all_organ_metrics(self):
        for i in range(len(self.organs)):
            self._calculate_metrics_for_organ(
                self.organs[i]["name"]
            )
        self.organs = list(self.organs)

    @rx.var
    def selected_organ_details(self) -> Optional[Organ]:
        if self.selected_organ_name:
            for organ in self.organs:
                if (
                    organ["name"]
                    == self.selected_organ_name
                ):
                    return (
                        self._calculate_metrics_for_organ(
                            self.selected_organ_name
                        )
                    )
        return None

    @rx.var
    def selected_organ_failure_history(
        self,
    ) -> List[FailureLogEntry]:
        if self.selected_organ_name:
            return [
                log
                for log in self.failure_logs
                if log["organ_name"]
                == self.selected_organ_name
            ]
        return []

    @rx.event
    def set_selected_organ(self, organ_name: str):
        self.selected_organ_name = organ_name
        self._calculate_metrics_for_organ(organ_name)
        self.organs = list(self.organs)

    @rx.event
    def set_target_uptime_t(self, value: str):
        try:
            new_val = float(value)
            self.target_uptime_t = (
                new_val if new_val >= 0 else 0.0
            )
        except ValueError:
            pass
        yield GptaState.update_all_organ_metrics

    @rx.event
    def set_min_reliability_threshold(self, value: str):
        try:
            new_threshold = float(value)
            if 0 < new_threshold <= 1:
                self.min_reliability_threshold = (
                    new_threshold
                )
            elif new_threshold > 1:
                self.min_reliability_threshold = 1.0
            else:
                self.min_reliability_threshold = 1e-06
        except ValueError:
            pass
        yield GptaState.update_all_organ_metrics

    @rx.event
    def toggle_add_organ_modal(self):
        self.show_add_organ_modal = (
            not self.show_add_organ_modal
        )
        if not self.show_add_organ_modal:
            self.new_organ_name_input = ""

    @rx.event
    def add_new_organ(self):
        trimmed_name = self.new_organ_name_input.strip()
        if not trimmed_name:
            yield rx.toast(
                "Le nom de l'organe ne peut pas être vide.",
                duration=3000,
            )
            return
        if any(
            (o["name"] == trimmed_name for o in self.organs)
        ):
            yield rx.toast(
                f"Un organe nommé '{trimmed_name}' existe déjà.",
                duration=3000,
            )
            return
        new_organ_entry: Organ = {
            "name": trimmed_name,
            "mtbf": None,
            "mttr": None,
            "lambda_val": None,
            "reliability_at_t": None,
            "availability": None,
            "preventive_maintenance_period": None,
        }
        self.organs.append(new_organ_entry)
        self._calculate_metrics_for_organ(trimmed_name)
        self.new_organ_name_input = ""
        self.show_add_organ_modal = False
        yield GptaState.update_all_organ_metrics

    @rx.event
    def toggle_add_failure_modal(
        self, organ_name: Optional[str] = None
    ):
        self.show_add_failure_modal = (
            not self.show_add_failure_modal
        )
        if self.show_add_failure_modal:
            self.new_failure_organ_name = (
                organ_name
                if organ_name
                else (
                    self.selected_organ_name
                    if self.selected_organ_name
                    else (
                        self.organs[0]["name"]
                        if self.organs
                        else ""
                    )
                )
            )
            self.new_failure_date = (
                datetime.date.today().isoformat()
            )
            self.new_failure_uptime = ""
            self.new_failure_repair_duration = ""
            self.new_failure_description = ""

    @rx.event
    def handle_failure_log_submit(
        self, form_data: Dict[str, str]
    ):
        try:
            organ_name = form_data.get("organ_name", "")
            failure_date_str = form_data.get(
                "failure_date", ""
            )
            uptime_str = form_data.get(
                "uptime_since_last_failure", ""
            )
            repair_duration_str = form_data.get(
                "repair_duration", ""
            )
            description = form_data.get(
                "description", ""
            ).strip()
            if not all(
                [
                    organ_name,
                    failure_date_str,
                    uptime_str,
                    repair_duration_str,
                    description,
                ]
            ):
                yield rx.toast(
                    "Tous les champs sont obligatoires.",
                    duration=3000,
                )
                return
            uptime = float(uptime_str)
            repair_duration = float(repair_duration_str)
            if uptime <= 0 or repair_duration <= 0:
                yield rx.toast(
                    "Temps de fonctionnement et durée de réparation doivent être positifs.",
                    duration=3000,
                )
                return
            datetime.date.fromisoformat(failure_date_str)
            new_log: FailureLogEntry = {
                "organ_name": organ_name,
                "failure_date": failure_date_str,
                "uptime_since_last_failure": uptime,
                "repair_duration": repair_duration,
                "description": description,
            }
            self.failure_logs.append(new_log)
            self.new_failure_organ_name = ""
            self.new_failure_date = (
                datetime.date.today().isoformat()
            )
            self.new_failure_uptime = ""
            self.new_failure_repair_duration = ""
            self.new_failure_description = ""
            self.show_add_failure_modal = False
            yield GptaState.update_all_organ_metrics
            if organ_name == self.selected_organ_name:
                yield GptaState.set_selected_organ(
                    organ_name
                )
            yield rx.toast(
                "Relevé de panne ajouté avec succès.",
                duration=3000,
            )
        except ValueError:
            yield rx.toast(
                "Veuillez entrer des nombres valides pour les durées et une date valide.",
                duration=3000,
            )
        except Exception as e:
            yield rx.toast(
                f"Erreur inattendue: {str(e)}",
                duration=4000,
            )

    @rx.var
    def pareto_chart_data(
        self,
    ) -> List[Dict[str, str | int | float]]:
        failure_counts: Dict[str, int] = {}
        for log in self.failure_logs:
            failure_counts[log["organ_name"]] = (
                failure_counts.get(log["organ_name"], 0) + 1
            )
        all_organ_names = [
            organ["name"] for organ in self.organs
        ]
        for name in all_organ_names:
            if name not in failure_counts:
                failure_counts[name] = 0
        sorted_failures = sorted(
            failure_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        chart_data: List[Dict[str, str | int | float]] = []
        cumulative_percentage = 0.0
        total_failures = sum(failure_counts.values())
        if total_failures == 0:
            return [
                {
                    "name": name,
                    "pannes": 0,
                    "cumulatif": 0.0,
                }
                for name in all_organ_names
            ]
        for organ_name, count in sorted_failures:
            percentage = (
                count / total_failures * 100
                if total_failures > 0
                else 0.0
            )
            cumulative_percentage += percentage
            chart_data.append(
                {
                    "name": organ_name,
                    "pannes": count,
                    "cumulatif": round(
                        cumulative_percentage, 2
                    ),
                }
            )
        return chart_data

    @rx.var
    def reliability_curve_data_selected_organ(
        self,
    ) -> List[Dict[str, float]]:
        data: List[Dict[str, float]] = []
        selected = self.selected_organ_details
        if (
            selected
            and selected.get("lambda_val") is not None
            and (selected["lambda_val"] > 0)
        ):
            lambda_v = selected["lambda_val"]
            mtbf = selected.get("mtbf")
            max_t = (
                mtbf * 2
                if mtbf
                else self.target_uptime_t * 2
            )
            if max_t == 0:
                max_t = 1000
            if max_t <= 0:
                max_t = (
                    self.target_uptime_t
                    if self.target_uptime_t > 0
                    else 1000
                )
            step_size = int(max_t / 20) if max_t > 20 else 1
            if step_size <= 0:
                step_size = 1
            for t_step in range(
                0, int(max_t) + 1, step_size
            ):
                reliability = math.exp(-lambda_v * t_step)
                data.append(
                    {
                        "temps": float(t_step),
                        "fiabilite": round(reliability, 4),
                    }
                )
        if not data:
            data.append({"temps": 0.0, "fiabilite": 1.0})
            data.append(
                {
                    "temps": (
                        self.target_uptime_t
                        if self.target_uptime_t > 0
                        else 1000.0
                    ),
                    "fiabilite": 1.0,
                }
            )
        return data

    @rx.var
    def mtbf_mttr_chart_data_selected_organ(
        self,
    ) -> List[Dict[str, str | float]]:
        selected = self.selected_organ_details
        if selected:
            return [
                {
                    "metric": "MTBF",
                    "valeur": (
                        selected.get("mtbf")
                        if selected.get("mtbf") is not None
                        else 0.0
                    ),
                },
                {
                    "metric": "MTTR",
                    "valeur": (
                        selected.get("mttr")
                        if selected.get("mttr") is not None
                        else 0.0
                    ),
                },
            ]
        return [
            {"metric": "MTBF", "valeur": 0.0},
            {"metric": "MTTR", "valeur": 0.0},
        ]

    @rx.event
    def export_selected_organ_data_csv(self):
        if (
            not self.selected_organ_name
            or not self.selected_organ_details
        ):
            return rx.toast(
                "Aucun organe sélectionné pour l'exportation.",
                duration=3000,
            )
        details = self.selected_organ_details
        history = self.selected_organ_failure_history
        if not details:
            return rx.toast(
                "Détails de l'organe non trouvés.",
                duration=3000,
            )
        details_df = pd.DataFrame([details])
        history_df = (
            pd.DataFrame(history)
            if history
            else pd.DataFrame(
                columns=[
                    "organ_name",
                    "failure_date",
                    "uptime_since_last_failure",
                    "repair_duration",
                    "description",
                ]
            )
        )
        csv_string = "Details de l'Organe:\n"
        csv_string += details_df.to_csv(
            index=False, lineterminator="\n"
        )
        csv_string += "\n\nHistorique des Pannes:\n"
        if not history_df.empty:
            csv_string += history_df.to_csv(
                index=False, lineterminator="\n"
            )
        else:
            csv_string += "Aucune panne enregistrée."
        filename = (
            f"{self.selected_organ_name_safe}_rapport.csv"
        )
        return rx.download(
            data=csv_string.encode("utf-8"),
            filename=filename,
        )

    @rx.var
    def selected_organ_name_safe(self) -> str:
        name = (
            self.selected_organ_name
            if self.selected_organ_name
            else "organe_inconnu"
        )
        return "".join(
            (c if c.isalnum() else "_" for c in name)
        )

    @rx.event
    def set_selected_year(self, year: str):
        try:
            self.selected_year = int(year)
        except ValueError:
            pass
        yield GptaState.update_all_organ_metrics