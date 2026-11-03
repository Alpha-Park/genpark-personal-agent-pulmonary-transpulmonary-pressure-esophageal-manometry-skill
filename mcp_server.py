"""
MCP Server for Pulmonary Transpulmonary Pressure (Ptp) & Esophageal Manometry.
Exposes tools for partitioned lung-chest wall elastance and barotrauma/atelectrauma prevention.
"""

import json
from typing import Dict, Any, Optional
from client import TranspulmonaryPressureManometryClient


def handle_evaluate_transpulmonary(params: Dict[str, Any]) -> Dict[str, Any]:
    plateau_airway_pressure_cmh2o = float(params.get("plateau_airway_pressure_cmh2o", 28.0))
    peep_airway_pressure_cmh2o = float(params.get("peep_airway_pressure_cmh2o", 10.0))
    esophageal_pressure_insp_cmh2o = float(params.get("esophageal_pressure_insp_cmh2o", 14.0))
    esophageal_pressure_exp_cmh2o = float(params.get("esophageal_pressure_exp_cmh2o", 9.0))
    tidal_volume_ml = float(params.get("tidal_volume_ml", 450.0))
    patient_weight_kg = float(params.get("patient_weight_kg", 70.0))

    client = TranspulmonaryPressureManometryClient()
    return client.evaluate_transpulmonary_mechanics(
        plateau_airway_pressure_cmh2o=plateau_airway_pressure_cmh2o,
        peep_airway_pressure_cmh2o=peep_airway_pressure_cmh2o,
        esophageal_pressure_insp_cmh2o=esophageal_pressure_insp_cmh2o,
        esophageal_pressure_exp_cmh2o=esophageal_pressure_exp_cmh2o,
        tidal_volume_ml=tidal_volume_ml,
        patient_weight_kg=patient_weight_kg
    )


TOOLS = {
    "evaluate_transpulmonary_mechanics": {
        "description": "Calculates end-inspiratory and end-expiratory transpulmonary pressures (Ptp = Paw - Pes) and partitions lung vs chest wall elastance via esophageal manometry.",
        "parameters": {
            "type": "object",
            "properties": {
                "plateau_airway_pressure_cmh2o": {
                    "type": "number",
                    "description": "Airway plateau pressure Pplat during inspiratory hold in cmH2O (e.g. 28.0)."
                },
                "peep_airway_pressure_cmh2o": {
                    "type": "number",
                    "description": "Positive end-expiratory airway pressure PEEP in cmH2O (e.g. 10.0)."
                },
                "esophageal_pressure_insp_cmh2o": {
                    "type": "number",
                    "description": "End-inspiratory esophageal balloon catheter pressure in cmH2O (e.g. 14.0)."
                },
                "esophageal_pressure_exp_cmh2o": {
                    "type": "number",
                    "description": "End-expiratory esophageal balloon catheter pressure in cmH2O (e.g. 9.0)."
                },
                "tidal_volume_ml": {
                    "type": "number",
                    "description": "Delivered tidal volume in mL (e.g. 450.0)."
                },
                "patient_weight_kg": {
                    "type": "number",
                    "description": "Predicted or actual body weight in kg, default 70.0."
                }
            },
            "required": ["plateau_airway_pressure_cmh2o", "peep_airway_pressure_cmh2o", "esophageal_pressure_insp_cmh2o", "esophageal_pressure_exp_cmh2o", "tidal_volume_ml"]
        },
        "handler": handle_evaluate_transpulmonary
    }
}


def process_request(request_str: str) -> str:
    try:
        req = json.loads(request_str)
        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["parameters"]
                }
                for name, spec in TOOLS.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name not in TOOLS:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })

            result = TOOLS[tool_name]["handler"](args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": f"Unsupported method '{method}'"}
            })

    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            print(process_request(line))
            sys.stdout.flush()
