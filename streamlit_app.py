"""
Streamlit Web Application for Spain Charts Analysis
Content Maturity, Release Lifecycle & Playlist Rotation
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import SpanishChartsAnalysis
from pathlib import Path
import json

# Set page configuration
st.set_page_config(
    page_title="Spain Charts Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set style
sns.set_style("whitegrid")

# Load CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
@st.cache_resource
def load_analysis():
    """Load and cache the analysis"""
    analysis = SpanishChartsAnalysis('Atlantic_Spain.csv')
    return analysis

# Title and Introduction
st.markdown("# 🎵 Spain Top 50 Songs Analysis")
st.markdown("### Content Maturity, Release Lifecycle & Playlist Rotation")
st.divider()

# Load analysis
analysis = load_analysis()

# Sidebar Navigation
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["🏠 Home", "📈 Dashboard", "🔍 Detailed Analysis", "📋 Data Explorer"]
)

# PAGE 1: HOME
if page == "🏠 Home":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Songs", len(analysis.df))
    with col2:
        st.metric("Avg Popularity", f"{analysis.df['popularity'].mean():.1f}")
    with col3:
        st.metric("Explicit %", f"{(analysis.df['is_explicit'].sum() / len(analysis.df) * 100):.1f}%")
    with col4:
        st.metric("Avg Duration", f"{(analysis.df['duration_ms'] / 60000).mean():.1f} min")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Project Overview")
        st.write("""
        This comprehensive analysis examines the top 50 songs in Spain, providing insights into:
        
        - **Content Maturity**: Evaluation of explicit content and its correlation with performance
        - **Release Lifecycle**: Analysis of singles vs albums and their performance patterns
        - **Playlist Rotation**: Understanding of how songs perform across different chart positions
        - **Engagement Metrics**: Combined scoring of popularity and chart positioning
        - **Stability Analysis**: How popularity correlates with chart position stability
        """)
    
    with col2:
        st.markdown("### 🎯 Key Features")
        st.write("""
        ✅ **Data Normalization**: Popularity scores normalized to 0-1 scale
        
        ✅ **Interactive Dashboard**: Explore KPIs and metrics
        
        ✅ **Detailed Analysis**: Deep dive into lifecycle and content patterns
        
        ✅ **Data Explorer**: Filter and explore raw data
        
        ✅ **Visualizations**: 8+ comprehensive charts and graphs
        
        ✅ **Export Capabilities**: Download analysis reports as JSON
        """)
    
    st.divider()
    
    st.markdown("### 📊 Analysis Highlights")
    
    kpis = analysis.calculate_kpis()
    lifecycle = analysis.lifecycle_construction_analysis()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Singles Performance")
        st.write(f"""
        - Count: {lifecycle['single']['count']}
        - Avg Popularity: {lifecycle['single']['avg_popularity']:.2f}
        - Avg Position: {lifecycle['single']['avg_position']:.1f}
        """)
    
    with col2:
        st.markdown("#### Albums Performance")
        st.write(f"""
        - Count: {lifecycle['album']['count']}
        - Avg Popularity: {lifecycle['album']['avg_popularity']:.2f}
        - Avg Position: {lifecycle['album']['avg_position']:.1f}
        """)
    
    with col3:
        st.markdown("#### Content Attributes")
        st.write(f"""
        - Explicit Songs: {analysis.df['is_explicit'].sum()}
        - Avg Maturity Level: {kpis['average_maturity_level']:.2f}
        - Engagement Score: {kpis['average_engagement_score']:.3f}
        """)

# PAGE 2: DASHBOARD
elif page == "📈 Dashboard":
    st.markdown("## 📊 Interactive Dashboard")
    
    # KPIs Section
    st.markdown("### Key Performance Indicators")
    kpis = analysis.calculate_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Popularity", f"{kpis['average_popularity']:.2f}")
    with col2:
        st.metric("Median Popularity", f"{kpis['median_popularity']:.2f}")
    with col3:
        st.metric("Explicit %", f"{kpis['explicit_percentage']:.1f}%")
    with col4:
        st.metric("Avg Engagement", f"{kpis['average_engagement_score']:.3f}")
    
    st.divider()
    
    # Charts Section
    st.markdown("### Visualizations")
    
    col1, col2 = st.columns(2)
    
    # Popularity Distribution
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(analysis.df['popularity'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Popularity Score')
        ax.set_ylabel('Number of Songs')
        ax.set_title('Distribution of Popularity Scores')
        st.pyplot(fig)
    
    # Album Type Distribution
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        album_counts = analysis.df['album_type'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']
        ax.pie(album_counts, labels=album_counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax.set_title('Distribution of Album Types')
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    # Position vs Popularity
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        scatter = ax.scatter(analysis.df['position'], analysis.df['popularity'], 
                            c=analysis.df['maturity_level'], cmap='coolwarm', 
                            s=100, alpha=0.6, edgecolors='black')
        ax.set_xlabel('Chart Position')
        ax.set_ylabel('Popularity Score')
        ax.set_title('Position vs Popularity')
        plt.colorbar(scatter, ax=ax, label='Maturity Level')
        st.pyplot(fig)
    
    # Duration vs Popularity
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        duration_min = analysis.df['duration_ms'] / 60000
        ax.scatter(duration_min, analysis.df['popularity'], 
                  s=100, alpha=0.6, c=analysis.df['position'], 
                  cmap='viridis', edgecolors='black')
        ax.set_xlabel('Duration (minutes)')
        ax.set_ylabel('Popularity Score')
        ax.set_title('Song Duration vs Popularity')
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    # Chart Segments
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        segment_stats = analysis.df.groupby('chart_segment')['popularity'].agg(['mean', 'std'])
        x_pos = np.arange(len(segment_stats))
        ax.bar(x_pos, segment_stats['mean'], yerr=segment_stats['std'], 
               capsize=5, alpha=0.7, color=['#FFD93D', '#6BCB77', '#4D96FF'])
        ax.set_xticks(x_pos)
        ax.set_xticklabels(segment_stats.index)
        ax.set_ylabel('Average Popularity')
        ax.set_title('Average Popularity by Chart Segment')
        st.pyplot(fig)
    
    # Maturity Distribution
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(analysis.df['maturity_level'], bins=20, color='coral', 
                edgecolor='black', alpha=0.7)
        ax.set_xlabel('Maturity Level')
        ax.set_ylabel('Number of Songs')
        ax.set_title('Distribution of Content Maturity Levels')
        st.pyplot(fig)

# PAGE 3: DETAILED ANALYSIS
elif page == "🔍 Detailed Analysis":
    st.markdown("## 🔍 Detailed Analysis")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "KPIs", "Lifecycle", "Explicit Content", "Playlist Location", "Popularity Stability"
    ])
    
    # Tab 1: KPIs
    with tab1:
        st.markdown("### Key Performance Indicators")
        kpis = analysis.calculate_kpis()
        
        kpi_data = {
            'Metric': [
                'Average Popularity',
                'Median Popularity',
                'Explicit Content %',
                'Average Duration (min)',
                'Average Engagement Score',
                'Singles %',
                'Albums %',
                'Average Maturity Level'
            ],
            'Value': [
                f"{kpis['average_popularity']:.2f}",
                f"{kpis['median_popularity']:.2f}",
                f"{kpis['explicit_percentage']:.1f}%",
                f"{kpis['average_duration_minutes']:.2f}",
                f"{kpis['average_engagement_score']:.3f}",
                f"{kpis['single_percentage']:.1f}%",
                f"{kpis['album_percentage']:.1f}%",
                f"{kpis['average_maturity_level']:.2f}"
            ]
        }
        
        st.dataframe(pd.DataFrame(kpi_data), use_container_width=True)
    
    # Tab 2: Lifecycle Analysis
    with tab2:
        st.markdown("### Release Lifecycle Analysis")
        lifecycle = analysis.lifecycle_construction_analysis()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Singles")
            singles_data = {
                'Count': lifecycle['single']['count'],
                'Avg Popularity': f"{lifecycle['single']['avg_popularity']:.2f}",
                'Avg Position': f"{lifecycle['single']['avg_position']:.1f}",
                'Popularity Std Dev': f"{lifecycle['single']['popularity_std']:.2f}",
                'Avg Total Tracks': f"{lifecycle['single']['avg_total_tracks']:.1f}"
            }
            for key, value in singles_data.items():
                st.metric(key, value)
        
        with col2:
            st.markdown("#### Albums")
            albums_data = {
                'Count': lifecycle['album']['count'],
                'Avg Popularity': f"{lifecycle['album']['avg_popularity']:.2f}",
                'Avg Position': f"{lifecycle['album']['avg_position']:.1f}",
                'Popularity Std Dev': f"{lifecycle['album']['popularity_std']:.2f}",
                'Avg Total Tracks': f"{lifecycle['album']['avg_total_tracks']:.1f}"
            }
            for key, value in albums_data.items():
                st.metric(key, value)
    
    # Tab 3: Explicit Content
    with tab3:
        st.markdown("### Content Attributes Analysis")
        explicit = analysis.explicit_content_classification()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔞 Explicit Content")
            explicit_data = {
                'Count': explicit['explicit']['count'],
                'Avg Popularity': f"{explicit['explicit']['avg_popularity']:.2f}",
                'Avg Position': f"{explicit['explicit']['avg_position']:.1f}",
                'Avg Engagement': f"{explicit['explicit']['avg_engagement']:.3f}"
            }
            for key, value in explicit_data.items():
                st.metric(key, value)
        
        with col2:
            st.markdown("#### ✓ Non-Explicit Content")
            non_explicit_data = {
                'Count': explicit['non_explicit']['count'],
                'Avg Popularity': f"{explicit['non_explicit']['avg_popularity']:.2f}",
                'Avg Position': f"{explicit['non_explicit']['avg_position']:.1f}",
                'Avg Engagement': f"{explicit['non_explicit']['avg_engagement']:.3f}"
            }
            for key, value in non_explicit_data.items():
                st.metric(key, value)
    
    # Tab 4: Playlist Location
    with tab4:
        st.markdown("### Playlist Location Analysis")
        playlist = analysis.playlist_location_analysis()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Top 10")
            for key, value in playlist['Top 10'].items():
                if isinstance(value, float):
                    st.write(f"**{key}:** {value:.2f}")
                else:
                    st.write(f"**{key}:** {value}")
        
        with col2:
            st.markdown("#### Top 11-25")
            for key, value in playlist['Top 11-25'].items():
                if isinstance(value, float):
                    st.write(f"**{key}:** {value:.2f}")
                else:
                    st.write(f"**{key}:** {value}")
        
        with col3:
            st.markdown("#### Top 26-50")
            for key, value in playlist['Top 26-50'].items():
                if isinstance(value, float):
                    st.write(f"**{key}:** {value:.2f}")
                else:
                    st.write(f"**{key}:** {value}")
    
    # Tab 5: Popularity Stability
    with tab5:
        st.markdown("### Popularity Stability Analysis")
        stability = analysis.popularity_stability_analysis()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### High Popularity (≥85)")
            for key, value in stability['high_popularity'].items():
                if isinstance(value, float):
                    st.write(f"**{key}:** {value:.2f}")
                else:
                    st.write(f"**{key}:** {value}")
        
        with col2:
            st.markdown("#### Medium Popularity (70-84)")
            for key, value in stability['medium_popularity'].items():
                if isinstance(value, float):
                    st.write(f"**{key}:** {value:.2f}")
                else:
                    st.write(f"**{key}:** {value}")
        
        with col3:
            st.markdown("#### Lower Popularity (<70)")
            for key, value in stability['lower_popularity'].items():
                if isinstance(value, float):
                    st.write(f"**{key}:** {value:.2f}")
                else:
                    st.write(f"**{key}:** {value}")

# PAGE 4: DATA EXPLORER
elif page == "📋 Data Explorer":
    st.markdown("## 📋 Data Explorer")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        album_type_filter = st.multiselect(
            "Album Type",
            options=analysis.df['album_type'].unique(),
            default=analysis.df['album_type'].unique()
        )
    
    with col2:
        explicit_filter = st.multiselect(
            "Explicit Content",
            options=[True, False],
            default=[True, False],
            format_func=lambda x: "Explicit" if x else "Non-Explicit"
        )
    
    with col3:
        popularity_range = st.slider(
            "Popularity Range",
            min_value=int(analysis.df['popularity'].min()),
            max_value=int(analysis.df['popularity'].max()),
            value=(int(analysis.df['popularity'].min()), int(analysis.df['popularity'].max()))
        )
    
    # Apply filters
    filtered_df = analysis.df[
        (analysis.df['album_type'].isin(album_type_filter)) &
        (analysis.df['is_explicit'].isin(explicit_filter)) &
        (analysis.df['popularity'].between(popularity_range[0], popularity_range[1]))
    ].copy()
    
    # Display statistics
    st.markdown(f"### Filtered Results: {len(filtered_df)} songs")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Popularity", f"{filtered_df['popularity'].mean():.1f}")
    with col2:
        st.metric("Avg Duration", f"{(filtered_df['duration_ms'] / 60000).mean():.1f} min")
    with col3:
        st.metric("Explicit %", f"{(filtered_df['is_explicit'].sum() / len(filtered_df) * 100):.1f}%")
    with col4:
        st.metric("Avg Position", f"{filtered_df['position'].mean():.1f}")
    
    st.divider()
    
    # Display table
    st.markdown("### Data Table")
    display_df = filtered_df[['position', 'song', 'artist', 'popularity', 'duration_ms', 
                              'album_type', 'is_explicit', 'total_tracks']].copy()
    display_df['duration_min'] = (display_df['duration_ms'] / 60000).round(2)
    display_df = display_df.drop('duration_ms', axis=1)
    display_df.columns = ['Position', 'Song', 'Artist', 'Popularity', 'Album Type', 
                          'Explicit', 'Total Tracks', 'Duration (min)']
    
    st.dataframe(display_df, use_container_width=True, height=500)
    
    # Download options
    st.markdown("### Download Data")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="filtered_songs_analysis.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = filtered_df.to_json(orient="records", indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name="filtered_songs_analysis.json",
            mime="application/json"
        )

# Sidebar Info
st.sidebar.divider()
st.sidebar.markdown("### 📊 Data Info")
st.sidebar.metric("Total Songs", len(analysis.df))
st.sidebar.metric("Analysis Date", analysis.df['date'].max().strftime("%Y-%m-%d"))
st.sidebar.metric("Dataset Size", f"{len(analysis.df)} records")

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Quick Stats")
st.sidebar.write(f"""
- **Top Song**: {analysis.df.loc[analysis.df['popularity'].idxmax(), 'song']}
- **Most Popular Artist**: Most frequent top 50 artist
- **Chart Dominance**: {(analysis.df['is_explicit'].sum() / len(analysis.df) * 100):.1f}% explicit
""")
