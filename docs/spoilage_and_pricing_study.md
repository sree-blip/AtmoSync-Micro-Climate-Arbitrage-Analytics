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

### Quality Degradation over Time
The remaining quality index ($Q_t$, bounded between $1.0$ and $0.0$) of the avocados at time $t$ is modeled as:

$$Q_t = Q_0 - \int_{0}^{t} (\text{Base Decay Rate} \cdot M_{\text{decay}}) \, dt$$

Where:
- $Q_0$: Initial quality score (typically $1.0$ at harvest/loading)
- $\text{Base Decay Rate}$: $0.005$ per hour (yielding a maximum optimal shelf life of ~200 hours)

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
| `transit_hours` | `INTEGER` | Est. transit hours from current position to this market |
| `price_premium` | `DECIMAL(10,2)`| USD price per box for Premium quality grade |
| `price_standard`| `DECIMAL(10,2)`| USD price per box for Standard quality grade |
| `price_substandard`| `DECIMAL(10,2)`| USD price per box for Substandard quality grade |
| `rerouting_cost`| `DECIMAL(10,2)`| Cost penalty associated with rerouting transit (USD) |

---

## 3. Spoilage Arbitrage Calculation

Arbitrage evaluates whether the financial benefit of diverting a container to an alternative market exceeds the additional transportation and administrative costs.

$$\text{Value}_{\text{original}} = \text{Quantity} \cdot \text{Price}(\text{Original Market}, Q_{\text{original\_arrival}})$$

$$\text{Value}_{\text{rerouted}} = \text{Quantity} \cdot \text{Price}(\text{Reroute Market}, Q_{\text{reroute\_arrival}}) - \text{Rerouting Cost}$$

$$\text{Spoilage Arbitrage} = \text{Value}_{\text{rerouted}} - \text{Value}_{\text{original}}$$

### Decision Rule:
* If **$\text{Spoilage Arbitrage} > \$500$** (threshold), generate a rerouting alert on the dashboard.
