"""
Pulmonary Transpulmonary Pressure (Ptp) & Esophageal Manometry Client.
Zero-mock pure Python standard library implementation.
Calculates end-inspiratory and end-expiratory transpulmonary pressures,
chest wall elastance, lung elastance, and partitioning of respiratory mechanics.
"""

import math
from typing import Dict, Any, Optional


class TranspulmonaryPressureManometryClient:
    """
    Evaluates transmural lung stress and strain via esophageal balloon catheter manometry:
    - Ptp = Paw - Pes (pleural pressure approximated by esophageal pressure)
    - Ptp_insp = Pplat - Pes_insp (alveolar distending pressure at end-inspiration)
    - Ptp_exp = PEEP - Pes_exp (alveolar stability pressure at end-expiration)
    - Elung = delta Ptp / Vt
    - Ecw = delta Pes / Vt
    - Ers = delta Paw / Vt = Elung + Ecw
    - Lung fraction = Elung / Ers
    """

    def __init__(self):
        pass

    def evaluate_transpulmonary_mechanics(
        self,
        plateau_airway_pressure_cmh2o: float,
        peep_airway_pressure_cmh2o: float,
        esophageal_pressure_insp_cmh2o: float,
        esophageal_pressure_exp_cmh2o: float,
        tidal_volume_ml: float,
        patient_weight_kg: Optional[float] = 70.0
    ) -> Dict[str, Any]:
        """
        Calculates transpulmonary pressures and partitioned respiratory elastances.
        plateau_airway_pressure_cmh2o: end-inspiratory airway pause pressure (Pplat).
        peep_airway_pressure_cmh2o: positive end-expiratory pressure (PEEP).
        esophageal_pressure_insp_cmh2o: end-inspiratory esophageal balloon pressure (Pes_insp).
        esophageal_pressure_exp_cmh2o: end-expiratory esophageal balloon pressure (Pes_exp).
        tidal_volume_ml: delivered tidal volume in mL.
        """
        if tidal_volume_ml <= 0:
            raise ValueError("Tidal volume must be strictly positive.")
        if plateau_airway_pressure_cmh2o < peep_airway_pressure_cmh2o:
            raise ValueError("Plateau airway pressure cannot be less than PEEP.")

        # Transpulmonary pressures
        ptp_insp = plateau_airway_pressure_cmh2o - esophageal_pressure_insp_cmh2o
        ptp_exp = peep_airway_pressure_cmh2o - esophageal_pressure_exp_cmh2o

        # Pressure swings
        delta_paw = plateau_airway_pressure_cmh2o - peep_airway_pressure_cmh2o
        delta_pes = esophageal_pressure_insp_cmh2o - esophageal_pressure_exp_cmh2o
        delta_ptp = ptp_insp - ptp_exp

        # Tidal volume in Liters
        vt_liters = tidal_volume_ml / 1000.0

        # Elastances (cmH2O / L)
        ers = delta_paw / vt_liters if vt_liters > 0 else 0.0
        ecw = delta_pes / vt_liters if vt_liters > 0 else 0.0
        elung = delta_ptp / vt_liters if vt_liters > 0 else 0.0

        # Compliances (mL / cmH2O)
        crs = (tidal_volume_ml / delta_paw) if delta_paw > 0 else 0.0
        clung = (tidal_volume_ml / delta_ptp) if delta_ptp > 0 else 0.0
        ccw = (tidal_volume_ml / delta_pes) if delta_pes > 0 else 0.0

        # Lung elastance fraction
        lung_fraction = elung / ers if ers > 0 else 0.5

        # Clinical barotrauma & atelectrauma risk staging:
        # Ptp_insp safe limit: <= 20.0 to 25.0 cmH2O (prevents overdistension / barotrauma)
        # Ptp_exp safe target: >= 0.0 to 2.0 cmH2O (prevents cyclic derecruitment / atelectrauma)
        if ptp_insp > 25.0:
            inspiratory_risk = "High Volutrauma / Alveolar Hyperinflation Risk (Ptp_insp > 25 cmH2O)"
        elif ptp_insp > 20.0:
            inspiratory_risk = "Upper Borderline Lung Stress (Ptp_insp 20-25 cmH2O)"
        else:
            inspiratory_risk = "Safe Inspiratory Lung Stress (Ptp_insp <= 20 cmH2O)"

        if ptp_exp < 0.0:
            expiratory_risk = "Expiratory Alveolar Collapse / Cyclic Derecruitment (Ptp_exp < 0 cmH2O)"
        elif ptp_exp < 2.0:
            expiratory_risk = "Marginal End-Expiratory Alveolar Stability"
        else:
            expiratory_risk = "Protective End-Expiratory Lung Recruitment (Ptp_exp >= 2 cmH2O)"

        # Partitioning diagnosis
        if lung_fraction >= 0.70:
            partitioning_diagnosis = "Predominant Parenchymal Lung Stiffness (ARDS / Fibrosis / Consolidation)"
        elif lung_fraction <= 0.40:
            partitioning_diagnosis = "Predominant Chest Wall / Abdominal Non-Compliance (Obesity / Ascites / IAH)"
        else:
            partitioning_diagnosis = "Balanced Lung-Chest Wall Mechanics"

        return {
            "status": "success",
            "transpulmonary_pressures_cmh2o": {
                "ptp_end_inspiratory_cmh2o": round(ptp_insp, 1),
                "ptp_end_expiratory_cmh2o": round(ptp_exp, 1),
                "delta_transpulmonary_cmh2o": round(delta_ptp, 1)
            },
            "airway_and_esophageal_pressures_cmh2o": {
                "plateau_airway_cmh2o": round(plateau_airway_pressure_cmh2o, 1),
                "peep_airway_cmh2o": round(peep_airway_pressure_cmh2o, 1),
                "esophageal_insp_cmh2o": round(esophageal_pressure_insp_cmh2o, 1),
                "esophageal_exp_cmh2o": round(esophageal_pressure_exp_cmh2o, 1)
            },
            "partitioned_mechanics": {
                "elastance_respiratory_system_cmh2o_per_l": round(ers, 1),
                "elastance_lung_cmh2o_per_l": round(elung, 1),
                "elastance_chest_wall_cmh2o_per_l": round(ecw, 1),
                "compliance_respiratory_system_ml_per_cmh2o": round(crs, 1),
                "compliance_lung_ml_per_cmh2o": round(clung, 1),
                "compliance_chest_wall_ml_per_cmh2o": round(ccw, 1),
                "lung_elastance_fraction": round(lung_fraction, 2)
            },
            "clinical_guidance": {
                "inspiratory_stress_status": inspiratory_risk,
                "expiratory_stability_status": expiratory_risk,
                "partitioning_diagnosis": partitioning_diagnosis
            }
        }
