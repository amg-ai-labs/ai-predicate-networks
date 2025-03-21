# FDA AI Predicate Network Dashboard

This is a Dash-based interactive dashboard that visualizes predicate networks of FDA-cleared AI medical devices. It allows filtering by specialty, year, and FDA approval pathway, and displays device-level information dynamically.

## Features

- Load and explore device predicate relationships by specialty
- Filter by FDA pathway (510(k), De Novo, Premarket)
- Adjust time range with an approval year slider
- Search and highlight specific submission numbers
- View device details in a side panel with links to summaries (if available)
  
## Deployment

The dashboard is deployed on PythonAnywhere and is publicly accessible.  
Visit [KXerxes on PythonAnywhere](https://www.pythonanywhere.com/user/KXerxes/) to have a play and explore the dashboard in action.

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

## Usage

1. **Install dependencies:**  
   Run the following command in your terminal to install required packages:
   ```bash
   pip install -r requirements.txt
    ```

2. **Prepare the data:**
  Make sure your Excel data file predicate_data_main.xlsx is placed in the project root (this file is excluded from the repo).

3. **Run the app:**
  Start the dashboard locally with:
  ```bash
  pip install -r requirements.txt
  ```
Then navigate to http://127.0.0.1:8050 in your browser.
