# Tibber Data Refresh

A Home Assistant custom integration that exposes **Tibber energy prices** in a clean, structured format, optimized for automations, dashboards, and price-aware scheduling.

This integration reuses the **official Tibber integration** and does **not** create a separate Tibber connection.

---

## Features

- One **energy price sensor per Tibber home**
- Uses data provided by the official Tibber integration (`pyTibber`)
- Supports **hourly and 15-minute pricing** (including NL quarter-hour prices)
- Exposes **raw time-series price data** with timestamps
- Lightweight, polling-only (no realtime subscriptions)
- Fully compatible with popular price visualisation cards

---

## Price sensor format

The integration creates a sensor with:

- **State**: current electricity price
- **Unit**: `<currency>/kWh`
- **Attributes** containing a full price timeline

### Attributes

```yaml
attributes:
  data:
    - start_time: "2026-01-09T00:00:00+01:00"
      price_per_kwh: 0.238
    - start_time: "2026-01-09T00:15:00+01:00"
      price_per_kwh: 0.236
  currency: "EUR"
  interval_minutes: 15
```

### Attribute details

| Attribute | Description |
|---------|------------|
| `data` | List of price intervals |
| `start_time` | ISO-8601 timestamp (timezone aware) |
| `price_per_kwh` | Electricity price in currency/kWh |
| `currency` | Currency (e.g. `EUR`, `NOK`) |
| `interval_minutes` | Length of each interval (15 or 60) |

---

## Compatibility

### ha-price-timeline-card ✅

This integration is **fully compatible** with  
**ha-price-timeline-card** by Neisi.

No templates, helpers, or adapters are required.

Example Lovelace usage:

```yaml
type: custom:price-timeline-card
entity: sensor.<your_home>_energy_price
```

The card directly consumes:

- `attributes.data`
- `start_time`
- `price_per_kwh`
- `currency`
- `interval_minutes`

as exposed by this integration.

---

## Requirements

- Home Assistant Core
- Official **Tibber** integration configured and authenticated
- At least one active Tibber subscription

---

## Installation (HACS)

1. Open **HACS**
2. Go to **Integrations**
3. Click **Custom repositories**
4. Add this repository:

```text
https://github.com/chessspider/tibber_data_refresh
```

Category: **Integration**

5. Install **Tibber Data Refresh**
6. Restart Home Assistant
7. Add the integration via **Settings → Devices & Services**

---

## Configuration

During setup, you select which existing **Tibber account** to use.  
No additional credentials are required.

---

## Notes

- Grid price vs energy price is intentionally **not split**
- The exposed price represents the **total electricity price per kWh**
- Designed for **automation and visualisation**, not billing accuracy

---

## License

MIT
