import os
os.environ['MPLBACKEND'] = 'Agg'  # Set backend variable before all imports
from flask import Flask, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import traceback

app = Flask(__name__)

data_path = "DomesticTransportUsageByMode.csv"
if os.path.exists(data_path):
    data = pd.read_csv(data_path)
    # Rename columns to match the expected format
    data = data.rename(columns={
        'date': 'Date',
        'transport_type': 'Transport Mode',
        'value': 'Usage'
    })
else:
    data = pd.DataFrame(columns=["Date", "Transport Mode", "Usage"])

def filter_data(date_range=None, transport_type=None):
    filtered_data = data.copy()
    
    # Set default time range to last 6 months if no range is specified
    if not date_range:
        latest_date = pd.to_datetime(filtered_data['Date']).max()
        start_date = (latest_date - pd.DateOffset(months=6)).strftime('%Y-%m-%d')
        end_date = latest_date.strftime('%Y-%m-%d')
        print(f"No date range specified. Using default range: {start_date} to {end_date}")
    else:
        start_date, end_date = date_range.split(',')
    
    # Convert dates to datetime for better comparison
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Limit time range to maximum of 12 months
    if (end_date - start_date).days > 365:
        end_date = start_date + pd.DateOffset(days=365)
        print(f"Date range limited to 12 months: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    filtered_data = filtered_data[
        (filtered_data['Date'] >= start_date) & 
        (filtered_data['Date'] <= end_date)
    ]
    
    if transport_type:
        filtered_data = filtered_data[filtered_data['Transport Mode'] == transport_type]
    
    # Convert dates back to string for output
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
    return filtered_data

@app.route('/visualization', methods=['GET'])
def visualize_data():
    try:
        if data.empty:
            print("Dataset is empty!")
            return jsonify({"error": "Dataset not found or empty"}), 404
        
        vis_type = request.args.get('type', 'line')
        date_range = request.args.get('date_range', None)
        transport_type = request.args.get('transport_type', None)
        
        # Validate visualization type
        if vis_type not in ['line', 'bar', 'heatmap']:
            return jsonify({"error": f"Invalid visualization type: {vis_type}. Allowed types: line, bar, heatmap"}), 400
        
        filtered_data = filter_data(date_range, transport_type)
        
        if filtered_data.empty:
            return jsonify({"error": "No data found for the selected date range/transport type"}), 404
        
        print(f"Visualization type: {vis_type}")
        print(f"Filtered data shape: {filtered_data.shape}")
        print(f"Filtered data columns: {filtered_data.columns.tolist()}")
        
        # Create new figure
        plt.figure(figsize=(12, 8))
        
        if vis_type == 'line':
            sns.lineplot(data=filtered_data, x='Date', y='Usage', hue='Transport Mode')
            plt.xticks(rotation=45)
            plt.title('Transport Usage Over Time')
        elif vis_type == 'bar':
            # Reduce data points for bar chart
            monthly_data = filtered_data.copy()
            monthly_data['Date'] = pd.to_datetime(monthly_data['Date']).dt.strftime('%Y-%m')
            monthly_data = monthly_data.groupby(['Date', 'Transport Mode'])['Usage'].mean().reset_index()
            sns.barplot(data=monthly_data, x='Date', y='Usage', hue='Transport Mode')
            plt.xticks(rotation=45)
            plt.title('Average Monthly Transport Usage')
        elif vis_type == 'heatmap':
            filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
            filtered_data['Month'] = filtered_data['Date'].dt.strftime('%Y-%m')
            pivot_table = filtered_data.groupby(['Month', 'Transport Mode'])['Usage'].mean().unstack()
            print(f"Pivot table shape: {pivot_table.shape}")
            
            sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt='.2f')
            plt.title('Transport Usage Heatmap')
            plt.xlabel('Transport Mode')
            plt.ylabel('Month')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save plot to BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=300)
        plt.close('all')
        img.seek(0)
        
        return send_file(img, mimetype='image/png')
    except Exception as e:
        print(f"Error in visualize_data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/export', methods=['GET'])
def export_data():
    if data.empty:
        return jsonify({"error": "Dataset not found or empty"}), 404
    
    date_range = request.args.get('date_range', None)
    transport_type = request.args.get('transport_type', None)
    filtered_data = filter_data(date_range, transport_type)
    export_path = "/mnt/data/exported_data.csv"
    filtered_data.to_csv(export_path, index=False)
    return send_file(export_path, as_attachment=True)

if __name__ == '__main__':
    try:
        print("Starting server...")
        print(f"Data loaded: {not data.empty}")
        print(f"Data shape: {data.shape if not data.empty else 'No data'}")
        # Set server to production mode for better stability
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        app.run(host='127.0.0.1', port=5001, threaded=False)
    except OSError:
        print("Port 5001 is already in use. Try using a different port.")
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        print(traceback.format_exc())
