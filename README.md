# Value Tracking Framework + GUI
A data-driven framework and desktop app for managing business initiatives and tracking the metrics that matter. This project combines a SQL Server database schema with a Python GUI to support transformation assessments, ROI modeling, and value realization.

# Purpose
This toolkit is designed for transformation leaders, analysts, and value management teams who need to:

- Track initiatives, events, and retirement plan-level activities
- Record and analyze weekly performance metrics
- Connect business actions to measurable value outcomes
- Interact with the data using a desktop application (built with Tkinter)

# Architecture Overview

**Backend:**
- SQL Server schema with normalized tables for:
- `initiatives`, `events`, `rplans`, `metrics`, `metric_values`
- Designed to support weekly tracking granularity without excessive data volume

**Frontend:**
- Python GUI (Tkinter) to:
  - View, add, and update initiative-related records
  - Visualize metric trends (planned)
