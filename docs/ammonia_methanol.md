# Ammonia and Methanol Production Technologies - Techno-Economic Parameters

This document summarizes the key techno-economic parameters for ammonia and methanol production technologies implemented in MacroEnergy.jl.

## Overview

The codebase includes six production technologies:
- **Thermal Ammonia** (without CCS)
- **Thermal Ammonia with CCS**
- **Synthetic Ammonia** (electrochemical)
- **Thermal Methanol** (without CCS)
- **Thermal Methanol with CCS**
- **Synthetic Methanol** (electrochemical)

---

## 1. Ammonia Production Technologies

### 1.1 Thermal Ammonia (without CCS)

**File:** `src/model/assets/thermalammonia.jl`

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Electricity Consumption** | 0.03787 | MWh/MWh NH₃ | Source: [Literature](https://www.sciencedirect.com/science/article/pii/S0306261920313453) |
| **Fuel Consumption** | 1.3095 | MWh CH₄/MWh NH₃ | Natural gas consumption |
| **CO₂ Emission Rate** | 0.181048235160161 | tons CO₂/MWh CH₄ | Direct emissions |
| **Investment Cost** | 2,093,045.41 | $/MW | Capital cost |
| **Fixed O&M Cost** | 84,025.0649 | $/MW-yr | Annual fixed operating cost |
| **Variable O&M Cost** | 0.9015 | $/MWh NH₃ | Variable operating cost |
| **Lifetime** | 30 | years | Asset lifetime |

**Inputs:**
- Natural gas (CH₄)
- Electricity

**Outputs:**
- Ammonia (NH₃)
- CO₂ emissions

---

### 1.2 Thermal Ammonia with CCS

**File:** `src/model/assets/thermalammoniaccs.jl`

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Electricity Consumption** | 0.07342 | MWh/MWh NH₃ | 1.93× higher than without CCS |
| **Fuel Consumption** | 1.3095 | MWh CH₄/MWh NH₃ | Same as without CCS |
| **CO₂ Emission Rate** | 0.0091 | tons CO₂/MWh CH₄ | 5% emission rate (95% reduction) |
| **CO₂ Capture Rate** | 0.17195 | - | 95% capture rate |
| **Investment Cost** | 2,720,959.03 | $/MW | 130% of thermal ammonia without CCS |
| **Fixed O&M Cost** | 109,232.584 | $/MW-yr | Higher than without CCS |
| **Variable O&M Cost** | 1.17195 | $/MWh NH₃ | Higher than without CCS |
| **Lifetime** | 30 | years | Asset lifetime |

**Inputs:**
- Natural gas (CH₄)
- Electricity

**Outputs:**
- Ammonia (NH₃)
- CO₂ emissions (reduced)
- CO₂ captured

**Key Differences from Thermal Ammonia:**
- 94% higher electricity consumption
- 30% higher investment cost
- 95% CO₂ capture rate
- 5% residual emissions

---

### 1.3 Synthetic Ammonia (Electrochemical)

**File:** `src/model/assets/syntheticammonia.jl`

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **H₂ Consumption** | 1.1484 | MWh H₂/MWh NH₃ | Hydrogen input |
| **N₂ Consumption** | 0.1597 | tonnes N₂/MWh NH₃ | Nitrogen input |
| **Electricity Consumption** | 0.2473 | MWh/MWh NH₃ | Electrical energy |
| **Investment Cost** | 1,461,749.91 | $/MW | Capital cost |
| **Fixed O&M Cost** | 2,512.7481 | $/MW-yr | Annual fixed operating cost |
| **Variable O&M Cost** | 0.02027 | $/MWh NH₃ | Variable operating cost |
| **Lifetime** | 30 | years | Asset lifetime |

**Inputs:**
- Hydrogen (H₂)
- Nitrogen (N₂)
- Electricity

**Outputs:**
- Ammonia (NH₃)

**Key Characteristics:**
- Zero direct CO₂ emissions (if H₂ is green)
- Lower investment cost than thermal with CCS
- Much lower O&M costs
- Requires hydrogen and nitrogen feedstocks
- Source: DECHEMA 2017 and Danish Energy Agency

---

## 2. Methanol Production Technologies

### 2.1 Thermal Methanol (without CCS)

**File:** `src/model/assets/thermalmethanol.jl`

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Electricity Consumption** | -0.10 | MWh/MWh CH₃OH | Negative = co-generation (produces electricity) |
| **Fuel Consumption** | 1.66586 | MWh CH₄/MWh CH₃OH | Natural gas consumption |
| **CO₂ Emission Rate** | 0.110645539 | tons CO₂/MWh CH₃OH | Direct emissions (1 ton/ton) |
| **Investment Cost** | 934,641.774 | $/MW | Capital cost |
| **Fixed O&M Cost** | 37,456.44 | $/MW-yr | Annual fixed operating cost |
| **Variable O&M Cost** | 1.8325 | $/MWh CH₃OH | Variable operating cost |
| **Lifetime** | 30 | years | Asset lifetime |

**Inputs:**
- Natural gas (CH₄)
- Electricity (net producer)

**Outputs:**
- Methanol (CH₃OH)
- CO₂ emissions

**Key Characteristics:**
- Net electricity producer (co-generation)
- Source: [OSTI](https://www.osti.gov/biblio/1601964)

---

### 2.2 Thermal Methanol with CCS

**File:** `src/model/assets/thermalmethanolccs.jl`

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Electricity Consumption** | 0.0 | MWh/MWh CH₃OH | No net electricity production |
| **Fuel Consumption** | 1.7158 | MWh CH₄/MWh CH₃OH | 103% of thermal methanol without CCS |
| **CO₂ Emission Rate** | 0.0110645539 | tons CO₂/MWh CH₃OH | 90% reduction |
| **CO₂ Capture Rate** | 0.099576 | - | 90% capture rate |
| **Investment Cost** | 981,373.863 | $/MW | 105% of thermal methanol without CCS |
| **Fixed O&M Cost** | 39,328.8 | $/MW-yr | 105% of thermal methanol without CCS |
| **Variable O&M Cost** | 1.924125 | $/MWh CH₃OH | 105% of thermal methanol without CCS |
| **Lifetime** | 30 | years | Asset lifetime |

**Inputs:**
- Natural gas (CH₄)
- Electricity

**Outputs:**
- Methanol (CH₃OH)
- CO₂ emissions (reduced)
- CO₂ captured

**Key Differences from Thermal Methanol:**
- No net electricity production (loss of co-generation benefit)
- 3% higher fuel consumption
- 5% higher investment cost
- 90% CO₂ capture rate
- 10% residual emissions

---

### 2.3 Synthetic Methanol (Electrochemical)

**File:** `src/model/assets/syntheticmethanol.jl`

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Electricity Consumption** | 0.271 | MWh/MWh CH₃OH | Electrical energy |
| **H₂ Consumption** | 1.138 | MWh H₂/MWh CH₃OH | Hydrogen input |
| **CO₂ Consumption** | 0.248 | tonnes CO₂/MWh CH₃OH | Captured CO₂ input |
| **CO₂ Emission Rate** | 0.10 | - | 10% of CO₂ consumed is emitted |
| **Investment Cost** | 685,961.676 | $/MW | Capital cost |
| **Fixed O&M Cost** | 1,175.6697 | $/MW-yr | Annual fixed operating cost |
| **Variable O&M Cost** | 0.0121 | $/MWh CH₃OH | Variable operating cost |
| **Lifetime** | 20 | years | Asset lifetime (shorter than thermal) |

**Inputs:**
- Hydrogen (H₂)
- Captured CO₂ (CO₂Captured)
- Electricity

**Outputs:**
- Methanol (CH₃OH)
- CO₂ emissions (10% of CO₂ consumed)

**Key Characteristics:**
- Uses captured CO₂ as feedstock
- Lower investment cost than thermal with CCS
- Much lower O&M costs
- Shorter lifetime (20 years vs 30 years)
- Requires hydrogen and captured CO₂ feedstocks
- 10% of consumed CO₂ is emitted during process
- Source: DECHEMA 2017 and Agora Energiewende (2018)

---

## 3. Technology Comparison Summary

### 3.1 Ammonia Production Comparison

| Technology | Investment Cost ($/MW) | Electricity (MWh/MWh) | Fuel/H₂ (MWh/MWh) | CO₂ Emissions | CCS Capture |
|------------|----------------------|----------------------|-------------------|---------------|-------------|
| **Thermal Ammonia** | 2,093,045 | 0.03787 | 1.3095 (CH₄) | 0.181 tons/MWh CH₄ | No |
| **Thermal Ammonia CCS** | 2,720,959 | 0.07342 | 1.3095 (CH₄) | 0.0091 tons/MWh CH₄ | 95% |
| **Synthetic Ammonia** | 1,461,750 | 0.2473 | 1.1484 (H₂) | 0 (if green H₂) | N/A |

**Key Insights:**
- Synthetic ammonia has the lowest investment cost
- Thermal with CCS has 30% higher investment but 95% emission reduction
- Synthetic requires 6.5× more electricity but zero emissions (with green H₂)
- Synthetic has much lower O&M costs

### 3.2 Methanol Production Comparison

| Technology | Investment Cost ($/MW) | Electricity (MWh/MWh) | Fuel/H₂ (MWh/MWh) | CO₂ Emissions | CCS Capture |
|------------|----------------------|----------------------|-------------------|---------------|-------------|
| **Thermal Methanol** | 934,642 | -0.10 (produces) | 1.66586 (CH₄) | 0.111 tons/MWh | No |
| **Thermal Methanol CCS** | 981,374 | 0.0 | 1.7158 (CH₄) | 0.011 tons/MWh | 90% |
| **Synthetic Methanol** | 685,962 | 0.271 | 1.138 (H₂) | 0.10 (10% of CO₂ consumed) | Uses CO₂ |

**Key Insights:**
- Thermal methanol without CCS produces electricity (co-generation)
- Thermal with CCS loses co-generation benefit
- Synthetic methanol uses CO₂ as feedstock (carbon utilization)
- Synthetic has lowest investment cost
- Synthetic has much lower O&M costs but shorter lifetime

### 3.3 Cost Structure Comparison

| Technology | Investment ($/MW) | Fixed O&M ($/MW-yr) | Variable O&M ($/MWh) | Lifetime |
|------------|------------------|---------------------|---------------------|----------|
| **Thermal Ammonia** | 2,093,045 | 84,025 | 0.9015 | 30 years |
| **Thermal Ammonia CCS** | 2,720,959 | 109,233 | 1.1720 | 30 years |
| **Synthetic Ammonia** | 1,461,750 | 2,513 | 0.0203 | 30 years |
| **Thermal Methanol** | 934,642 | 37,456 | 1.8325 | 30 years |
| **Thermal Methanol CCS** | 981,374 | 39,329 | 1.9241 | 30 years |
| **Synthetic Methanol** | 685,962 | 1,176 | 0.0121 | 20 years |

**Key Observations:**
- Synthetic technologies have significantly lower O&M costs
- Thermal with CCS has higher costs across all categories
- Synthetic methanol has very low variable O&M (0.0121)
- Synthetic methanol has shorter lifetime (20 vs 30 years)

---

## 4. Notes on Parameter Units

- **Electricity/Fuel Consumption**: MWh per MWh of output product (NH₃ or CH₃OH)
- **CO₂ Emissions**: tons CO₂ per MWh of input fuel or output product
- **Investment Cost**: $/MW - Capital cost per MW of capacity
- **Fixed O&M Cost**: $/MW-yr - Annual fixed operating and maintenance cost per MW of capacity
- **Variable O&M Cost**: $/MWh - Variable operating cost per MWh of output product (NH₃ or CH₃OH)
- **Lifetime**: Asset operational lifetime in years

---

## 5. Data Sources

- **Thermal Ammonia**: 2018 USD, [Literature](https://www.sciencedirect.com/science/article/pii/S0306261920313453) - for chemical looping (not the main stream technology for ammonia production)
- **Thermal Methanol**: 2011 USD, [OSTI](https://www.osti.gov/biblio/1601964)
- **Thermal Methanol CCS**: 105% of thermal methanol without CCS (all cost parameters)
- **Synthetic Ammonia**: 2015 USD, Source: DECHEMA 2017 and Danish Energy Agency
- **Synthetic Methanol**: 2017 USD, Source: DECHEMA 2017 and Agora Energiewende (2018)
- **CCS Technologies**: Parameters scaled from base thermal technologies

---

## 6. Implementation Files

All technologies are implemented in `src/model/assets/`:
- `thermalammonia.jl` - Thermal ammonia without CCS
- `thermalammoniaccs.jl` - Thermal ammonia with CCS
- `syntheticammonia.jl` - Synthetic (electrochemical) ammonia
- `thermalmethanol.jl` - Thermal methanol without CCS
- `thermalmethanolccs.jl` - Thermal methanol with CCS
- `syntheticmethanol.jl` - Synthetic (electrochemical) methanol