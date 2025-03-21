# FDA AI Predicate Network Dashboard

This is a Dash-based interactive dashboard that visualizes predicate networks of FDA-cleared AI medical devices. It allows filtering by specialty, year, and FDA approval pathway, and displays device-level information dynamically.

## Features

- Load and explore device predicate relationships by specialty
- Filter by FDA pathway (510(k), De Novo, Premarket)
- Adjust time range with an approval year slider
- Search and highlight specific submission numbers
- View device details in a side panel with links to summaries (if available)


## File Structure

```
ai-predicate-network/
├── app.py                  # Main Dash app instance and run server
├── layout.py               # UI layout and component setup
├── callbacks.py            # Dash callback functions
├── data.py                 # Data loading and preprocessing
├── graph_utils.py          # Predicate graph construction and visualization
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── predicate_data_main.xlsx  # Excel data file (not included in repo)
```
