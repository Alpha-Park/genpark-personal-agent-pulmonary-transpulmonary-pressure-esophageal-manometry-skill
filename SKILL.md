---
name: genpark-personal-agent-pulmonary-transpulmonary-pressure-esophageal-manometry-skill
version: 1.0.0
description: Calculates transpulmonary pressures (Ptp = Paw - Pes) and partitions lung vs chest wall elastance via esophageal manometry.
license: Apache-2.0
compatibility:
  python: ">=3.9"
  openclaw: ">=1.0.0"
  mcp: ">=1.0.0"
---

# Pulmonary Transpulmonary Pressure ($P_{\text{tp}}$) & Esophageal Manometry Skill

A zero-dependency personal agent skill for calculating transpulmonary distending pressure ($P_{\text{tp}} = P_{\text{aw}} - P_{\text{es}}$) and partitioning respiratory system mechanics into lung vs chest wall components.

## Features
- **Inspiratory Stress Assessment**: Computes end-inspiratory transpulmonary pressure ($P_{\text{tp,insp}} \le 20-25\text{ cmH}_2\text{O}$ safe target) to prevent alveolar overdistension and volutrauma.
- **Expiratory Stability Evaluation**: Computes end-expiratory transpulmonary pressure ($P_{\text{tp,exp}} \ge 0-2\text{ cmH}_2\text{O}$ target) to protect against cyclic derecruitment and atelectrauma.
- **Elastance Partitioning**: Quantifies lung elastance ($E_{\text{lung}}$), chest wall elastance ($E_{\text{cw}}$), and lung elastance fraction ($E_{\text{lung}} / E_{\text{rs}}$).
- **Etiology Differentiation**: Differentiates parenchymal lung injury (ARDS, fibrosis) from chest wall stiffness (morbid obesity, abdominal hypertension, ascites).

## MCP Server Integration
Exposes `evaluate_transpulmonary_mechanics` for autonomous respiratory wellness and mechanical ventilation stress monitoring.
