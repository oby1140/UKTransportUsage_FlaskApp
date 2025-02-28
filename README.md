# UK Transport Usage Visualization

A Flask web application for visualizing UK transport usage data through interactive charts and heatmaps.

## Features

- **Multiple Visualization Types:**
  - Line charts for temporal analysis
  - Bar charts for comparative analysis
  - Heatmaps for pattern recognition
- **Data Filtering:**
  - Filter by date range
  - Filter by transport mode
- **Data Export:**
  - Export filtered data as CSV

## Setup

1. Clone the repository:
```bash
git clone https://github.com/oby1140/UKTransportUsage_FlaskApp.git
cd UKTransportUsage_FlaskApp
```

2. Install required dependencies:
```bash
pip install flask pandas matplotlib seaborn
```

3. Run the application:
```bash
python UKTransportUsage_FlaskApp.py
```

The server will start at `http://127.0.0.1:5001`

## Usage

### Visualization Endpoints

Access visualizations through the following URL patterns:

1. **Line Chart:**
```
http://127.0.0.1:5001/visualization?type=line&date_range=2020-03-01,2020-12-31
```

2. **Bar Chart:**
```
http://127.0.0.1:5001/visualization?type=bar&date_range=2020-03-01,2020-12-31
```

3. **Heatmap:**
```
http://127.0.0.1:5001/visualization?type=heatmap&date_range=2020-03-01,2020-12-31
```

### Optional Parameters

- `transport_type`: Filter by specific transport mode
- `date_range`: Format is 'YYYY-MM-DD,YYYY-MM-DD'

### Data Export

Export filtered data using:
```
http://127.0.0.1:5001/export?date_range=2020-03-01,2020-12-31
```

## Data Source

The application uses the `DomesticTransportUsageByMode.csv` file containing UK transport usage data with the following columns:
- Date
- Transport Mode
- Usage

## Development

- Test data generation script: `UKTransportUsageTool_TestDataGenerator.py`
- Test cases: `UKTransportUsage_TestCases.txt`
- User stories: `UKTransportUsageTool_UserStories.txt`

## Notes

- The server runs in production mode with threading disabled for stability
- Matplotlib backend is set to 'Agg' for better compatibility
- Date ranges are automatically limited to 12 months for performance
- Default date range is set to the last 6 months if not specified 