# Tibber Data Refresh

A Home Assistant custom integration that exposes **detailed Tibber electricity price data**
(current price, today/tomorrow price series, and derived attributes) while reusing the
**official Tibber integration and pyTibber**.

This integration exists to provide **stable, script- and automation-friendly price data**
that was previously available via the deprecated `tibber-data` integration.

---

## Features

For each active Tibber home:

- Current electricity price
- Today’s hourly prices
- Tomorrow’s hourly prices (when available)
- Raw price data with timestamps
- Derived attributes:
  - minimum / maximum price today
  - average price today
  - cheapest hour today
  - intraday price rank

The integration **does not duplicate authentication** and relies entirely on the
existing Tibber config entry.

---

## Requirements

- Home Assistant Core **2026.1 or newer**
- The official **Tibber** integration must already be configured and working
- An active Tibber subscription with price data available

---

## Installation (HACS)

### 1. Add custom repository

1. Open **HACS**
2. Go to **Integrations**
3. Open the menu (top right) → **Custom repositories**
4. Add:
   - **Repository**:  
     `https://github.com/chessspider/tibber_data_refresh`
   - **Category**:  
     `Integration`
5. Click **Add**

---

### 2. Install the integration

1. In HACS → **Integrations**
2. Search for **Tibber Data Refresh**
3. Click **Install**
4. Restart Home Assistant

---

### 3. Configure

1. Go to **Settings → Devices & Services**
2. Click **Add integration**
3. Search for **Tibber Data Refresh**
4. Select the **existing Tibber account** you want to use

That’s it. No credentials or tokens are required.

---

## Entities

### Sensor: Electricity price

**Entity ID example**
``` 
sensor.<home_name>_electricity_price
``` 

**State**
- Current electricity price (currency / kWh)

**Attributes**
``` 
today: [0.23, 0.22, 0.21, ...]
raw_today:
  - time: "2026-01-09T13:00:00+01:00"
    total: 0.21
tomorrow: [...]
raw_tomorrow: [...]
tomorrow_valid: true
price_rank: 0.42
min_today: 0.19
max_today: 0.27
avg_today: 0.231
cheapest_today:
  time: "2026-01-09T03:00:00+01:00"
  total: 0.19
``` 

All timestamps are **timezone-aware** and aligned with Tibber’s data.

---

## Design notes

- Uses the **official Tibber integration runtime**
- No additional polling beyond Tibber updates
- One sensor per Tibber home
- No grid price separation (total price is exposed directly)
- Written to be simple, explicit, and automation-friendly

---

## Troubleshooting

**Integration does not show up**
- Ensure Home Assistant is restarted after installation
- Ensure the Tibber integration is already configured

**No price data**
- Verify the Tibber app shows current prices
- Tomorrow prices are only available later in the day (region-dependent)

---

## Development

For local development, you can symlink the integration into:

``` 
config/custom_components/tibber_data_refresh
``` 

Restart Home Assistant after changes.

---

## License

MIT

---

## Disclaimer

This project is **not affiliated with Tibber**.
Tibber is a registered trademark of Tibber AS.
