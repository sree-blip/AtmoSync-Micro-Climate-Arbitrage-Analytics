# Spoilage & Pricing Study

This document outlines the analytical logic and formulas for predicting avocado degradation and calculating spoilage arbitrage under the AtmoSync project.

---

## 1. Avocado Spoilage Curve Model

Avocados have an optimal transport environment (typically **5°C** and **85% to 90% humidity**). Deviations from these levels accelerate decay.

### Spoilage Rate Formula
The decay multiplier ($M_{\text{decay}}$) is calculated relative to optimal transport parameters:

$$M_{\text{decay}} = e^{k_T \cdot (T - T_{\text{opt}})} \cdot e^{k_H \cdot (H - H_{\text{opt}})}$$

Where:
- $T$: Current temperature inside the container (°C)
- $T_{\text{opt}}$: Optimal temperature (5°C)
- $H$: Current relative humidity (%)
- $H_{\text{opt}}$: Optimal relative humidity (85%)
- $k_T$: Temperature sensitivity coefficient ($0.08$)
- $k_H$: Humidity sensitivity coefficient ($0.02$)

### Quality Degradation over Time (Discrete Interval Accumulation)
To implement this in dbt/SQL over telemetry events, degradation is accumulated incrementally for each specific telemetry time interval ($\Delta t$ in hours). 

The quality index $Q_t$ at time $t$ is calculated from the previous interval's quality $Q_{t-1}$ as:

$$Q_t = \max\left(0, \min\left(1, Q_{t-1} - \text{Base Decay Rate} \cdot M_{\text{decay}} \cdot \Delta t\right)\right)$$

Where:
- $Q_0$: Initial quality score (defaults to $1.0$ at shipment start)
- $\Delta t$: Elapsed time in hours since the previous telemetry log
- $\text{Base Decay Rate}$: $0.005$ per hour
- Bounding logic ($\max(0, \min(1, \dots))$) is strictly enforced so that $Q_t \in [0.0, 1.0]$.


### Quality Grade Mapping
At any given arrival time, the quality score maps to a price tier:
- **Premium ($Q_t \geq 0.85$)**: High value.
- **Standard ($0.60 \leq Q_t < 0.85$)**: Moderate value.
- **Substandard ($Q_t < 0.60$)**: Low value, close to spoilage.

---

## 2. Commodity Pricing Dataset Schema

To calculate margins, the container telemetry must be joined with a destination market pricing table containing:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `market_id` | `VARCHAR` | Unique identifier for each destination market |
| `market_name` | `VARCHAR` | City/Location name (e.g., Chicago, New York) |
| `transit_hours` | `INTEGER` | Remaining transit hours from the container's current position to this candidate market |
| `price_premium` | `DECIMAL(10,2)`| USD price per box for Premium quality grade |
| `price_standard`| `DECIMAL(10,2)`| USD price per box for Standard quality grade |
| `price_substandard`| `DECIMAL(10,2)`| USD price per box for Substandard quality grade |
| `rerouting_cost`| `DECIMAL(10,2)`| Cost penalty associated with rerouting transit (USD) |

---

## 3. Spoilage Arbitrage Calculation

Arbitrage evaluates whether the financial benefit of diverting a container to an alternative market exceeds the additional transportation and administrative costs.

$$\text{Value}_{\text{original}} = \text{Quantity} \cdot \text{Price}(\text{Original Market}, Q_{\text{original}})$$

$$\text{Value}_{\text{rerouted}} = \text{Quantity} \cdot \text{Price}(\text{Reroute Market}, Q_{\text{rerouted}}) - \text{Rerouting Cost}$$

$$\text{Spoilage Arbitrage} = \text{Value}_{\text{rerouted}} - \text{Value}_{\text{original}}$$

### Decision Rule:
* If **Spoilage Arbitrage > $500** (threshold), generate a rerouting alert on the dashboard.
