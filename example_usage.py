"""
Example usage of Pulmonary Transpulmonary Pressure (Ptp) & Esophageal Manometry Skill.
Demonstrates ARDS parenchymal lung stiffness vs morbid obesity / elevated chest wall elastance.
"""

from client import TranspulmonaryPressureManometryClient

def main():
    client = TranspulmonaryPressureManometryClient()

    print("=== Case 1: ARDS Parenchymal Lung Stiffness ===")
    ards_case = client.evaluate_transpulmonary_mechanics(
        plateau_airway_pressure_cmh2o=32.0,
        peep_airway_pressure_cmh2o=14.0,
        esophageal_pressure_insp_cmh2o=8.0,
        esophageal_pressure_exp_cmh2o=5.0,
        tidal_volume_ml=420.0
    )
    print("Transpulmonary Pressures:")
    print(f"  Ptp Inspiratory: {ards_case['transpulmonary_pressures_cmh2o']['ptp_end_inspiratory_cmh2o']} cmH2O")
    print(f"  Ptp Expiratory:  {ards_case['transpulmonary_pressures_cmh2o']['ptp_end_expiratory_cmh2o']} cmH2O")
    print(f"  Lung Elastance Fraction: {ards_case['partitioned_mechanics']['lung_elastance_fraction']}")
    print(f"  Partitioning:    {ards_case['clinical_guidance']['partitioning_diagnosis']}")
    print(f"  Inspiratory Risk: {ards_case['clinical_guidance']['inspiratory_stress_status']}")

    print("\n=== Case 2: Morbid Obesity with Preserved Lung Parenchyma ===")
    obese_case = client.evaluate_transpulmonary_mechanics(
        plateau_airway_pressure_cmh2o=32.0,
        peep_airway_pressure_cmh2o=12.0,
        esophageal_pressure_insp_cmh2o=22.0,
        esophageal_pressure_exp_cmh2o=15.0,
        tidal_volume_ml=450.0
    )
    print("Transpulmonary Pressures:")
    print(f"  Ptp Inspiratory: {obese_case['transpulmonary_pressures_cmh2o']['ptp_end_inspiratory_cmh2o']} cmH2O (Safe despite high Paw!)")
    print(f"  Ptp Expiratory:  {obese_case['transpulmonary_pressures_cmh2o']['ptp_end_expiratory_cmh2o']} cmH2O")
    print(f"  Lung Elastance Fraction: {obese_case['partitioned_mechanics']['lung_elastance_fraction']}")
    print(f"  Partitioning:    {obese_case['clinical_guidance']['partitioning_diagnosis']}")
    print(f"  Inspiratory Risk: {obese_case['clinical_guidance']['inspiratory_stress_status']}")

if __name__ == "__main__":
    main()
