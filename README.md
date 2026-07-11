# Spain Top 50 Songs Analysis

## 📊 Project Overview

This comprehensive analysis project examines the top 50 songs in Spain, providing deep insights into content maturity, release lifecycle patterns, and playlist rotation dynamics.

### Key Analysis Components

- **Content Maturity Assessment**: Evaluation of explicit content and correlation with chart performance
- **Release Lifecycle Analysis**: Singles vs albums performance patterns and lifecycle stages
- **Playlist Location Classification**: Chart segmentation (Top 10, Top 11-25, Top 26-50) analysis
- **Engagement Metrics**: Combined scoring of position and popularity factors
- **Popularity Stability**: Analysis of how popularity correlates with chart positioning
- **Data Normalization**: Popularity scores normalized to 0-1 scale for comparison

---

## 🚀 Quick Start

### Installation

1. Clone or navigate to the project directory:
```bash
cd "Atlantic RC"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📱 Running the Applications

### Option 1: Streamlit Web Application (Recommended)

The easiest way to explore the data with an interactive dashboard:

```bash
streamlit run streamlit_app.py
```

This opens an interactive web interface with:
- 🏠 **Home**: Overview and quick statistics
- 📈 **Dashboard**: Interactive charts and visualizations
- 🔍 **Detailed Analysis**: Deep dive into all metrics
- 📋 **Data Explorer**: Filter and explore raw data

### Option 2: Flask Web Application

For a traditional web framework approach:

```bash
python app.py
```

Then navigate to `http://localhost:5000` in your browser.

### Option 3: Python Analysis Script

Run the analysis directly and generate reports:

```bash
python analysis.py
```

This will:
- Process the CSV data
- Calculate all KPIs
- Generate visualizations (saved to `./visualizations/`)
- Create a comprehensive JSON report

---

## 📂 Project Structure

```
Atlantic RC/
├── Atlantic_Spain.csv          # Raw data: Top 50 songs
├── analysis.py                 # Core analysis engine
├── streamlit_app.py            # Streamlit web application
├── app.py                      # Flask web application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── analysis_report.json        # Generated analysis report
│
├── templates/                  # Flask HTML templates
│   ├── index.html             # Home page
│   ├── dashboard.html         # Dashboard page
│   └── analysis.html          # Detailed analysis page
│
├── static/                    # Static files
│   ├── style.css              # Styling
│   ├── dashboard.js           # Dashboard JavaScript
│   ├── analysis.js            # Analysis page JavaScript
│   └── home.js                # Home page JavaScript
│
└── visualizations/            # Generated charts (PNG files)
    ├── 01_popularity_distribution.png
    ├── 02_position_vs_popularity.png
    ├── 03_album_type_distribution.png
    ├── 04_explicit_content.png
    ├── 05_duration_vs_popularity.png
    ├── 06_chart_segments.png
    ├── 07_maturity_distribution.png
    └── 08_engagement_score.png
```

---

## 📊 Data Fields

The `Atlantic_Spain.csv` file contains the following fields:

| Field | Description |
|-------|-------------|
| `date` | Date of chart snapshot (DD-MM-YYYY) |
| `position` | Chart position (1-50) |
| `song` | Song title |
| `artist` | Artist name(s) |
| `popularity` | Popularity score (0-100) |
| `duration_ms` | Track duration in milliseconds |
| `album_type` | Type of release (single/album) |
| `total_tracks` | Total tracks on album/EP |
| `is_explicit` | Whether content is explicit (TRUE/FALSE) |
| `album_cover_url` | URL to album artwork |

---

## 🔍 Key Performance Indicators (KPIs)

The analysis calculates 8 major KPIs:

1. **Average Popularity**: Mean popularity score across all songs
2. **Median Popularity**: Median popularity for distribution analysis
3. **Explicit Content %**: Proportion of explicit songs in chart
4. **Average Duration**: Mean song length in minutes
5. **Average Engagement Score**: Combined position and popularity metric
6. **Singles %**: Percentage of single releases
7. **Albums %**: Percentage of album releases
8. **Average Maturity Level**: Overall content maturity baseline

---

## 📈 Analysis Outputs

### Generated Files

1. **`analysis_report.json`**: Comprehensive analysis report with all metrics
2. **`visualizations/`**: 8 PNG charts showing key data patterns

### Streamlit Features

- **Interactive Filtering**: Filter by album type, explicit content, popularity range
- **Real-time Calculations**: All metrics update instantly
- **Data Export**: Download filtered data as CSV or JSON
- **Multiple Tabs**: Organized information across analysis categories
- **Responsive Charts**: Matplotlib visualizations embedded in interface

### Flask Features

- **RESTful API Endpoints**: Query specific metrics via HTTP
- **Responsive HTML**: Modern, CSS-styled web interface
- **Data Tables**: Display top songs and detailed breakdowns

---

## 🎯 Analytical Methodology

1. **Data Preparation**: Load CSV and normalize popularity scores
2. **Lifecycle Construction**: Classify songs by release type
3. **Content Classification**: Categorize by explicit content and attributes
4. **Playlist Location Analysis**: Segment by chart position
5. **Engagement Scoring**: Calculate combined metrics
6. **Stability Assessment**: Analyze popularity consistency

---

## 💡 Usage Examples

### Streamlit Dashboard

1. Open the Streamlit app: `streamlit run streamlit_app.py`
2. Navigate to "📈 Dashboard" to see all visualizations
3. Go to "📋 Data Explorer" to filter and explore specific songs
4. Visit "🔍 Detailed Analysis" for deep metrics breakdown

### Generating Reports

```bash
python analysis.py
```

This generates:
- `analysis_report.json` with all metrics
- PNG files in `visualizations/` folder with 8 charts

### Filtering Data

In Streamlit's Data Explorer tab:
1. Select album types (Singles/Albums)
2. Choose explicit content filter
3. Adjust popularity range slider
4. Download filtered results as CSV or JSON

---

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib/Seaborn**: Data visualization
- **Streamlit**: Interactive web framework
- **Flask**: Traditional web framework
- **Chart.js**: JavaScript charting library

---

## 📝 Notes

- The analysis is based on chart snapshot from **May 18, 2024**
- All popularity scores are normalized to 0-100 scale in the source data
- Maturity level calculation includes explicit flag and duration factors
- Engagement score combines chart position and popularity with 50/50 weighting

---

## 🤝 Contributing

To extend this analysis:

1. Add new KPIs in the `SpanishChartsAnalysis` class
2. Create new visualization functions
3. Add API endpoints in Flask app
4. Create new Streamlit tabs for additional analysis

---

## Atlantic RC
