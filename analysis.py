"""
Content Maturity, Release Lifecycle & Playlist Rotation Analysis
Spain Top 50 Songs Analysis Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

class SpanishChartsAnalysis:
    def __init__(self, csv_path):
        """Initialize the analysis with the CSV data"""
        self.df = pd.read_csv(csv_path)
        self.df['date'] = pd.to_datetime(self.df['date'], format='%d-%m-%Y')
        self.prepare_data()
        
    def prepare_data(self):
        """Prepare and normalize data for analysis"""
        # Convert duration to minutes
        self.df['duration_minutes'] = self.df['duration_ms'] / 60000
        
        # Normalize popularity score (0-1 scale)
        self.df['popularity_normalized'] = self.df['popularity'] / 100
        
        # Create engagement score (combination of popularity and position)
        self.df['engagement_score'] = (
            (100 - self.df['position']) / 50 * 0.5 +  # Position factor (inverse)
            self.df['popularity_normalized'] * 0.5  # Popularity factor
        )
        
        # Create content maturity indicator
        self.df['maturity_level'] = self.df.apply(self._calculate_maturity, axis=1)
        
        print("Data prepared successfully")
        print(f"Total records: {len(self.df)}")
        print(f"Date range: {self.df['date'].min()} to {self.df['date'].max()}")
    
    def _calculate_maturity(self, row):
        """Calculate content maturity based on attributes"""
        # Explicit content increases maturity
        explicit_factor = 0.3 if row['is_explicit'] else 0
        
        # Duration factor (longer songs suggest more mature content)
        duration_factor = min(row['duration_minutes'] / 10, 0.2)
        
        # Position factor (top songs might target broader audience)
        position_factor = (100 - row['position']) / 100 * 0.1
        
        maturity = explicit_factor + duration_factor + position_factor
        return min(maturity, 1.0)
    
    def calculate_kpis(self):
        """Calculate Key Performance Indicators"""
        kpis = {
            'average_popularity': self.df['popularity'].mean(),
            'median_popularity': self.df['popularity'].median(),
            'explicit_percentage': (self.df['is_explicit'].sum() / len(self.df)) * 100,
            'average_duration_minutes': self.df['duration_minutes'].mean(),
            'average_engagement_score': self.df['engagement_score'].mean(),
            'single_percentage': (self.df['album_type'] == 'single').sum() / len(self.df) * 100,
            'album_percentage': (self.df['album_type'] == 'album').sum() / len(self.df) * 100,
            'average_maturity_level': self.df['maturity_level'].mean(),
        }
        
        return kpis
    
    def lifecycle_construction_analysis(self):
        """Analyze release lifecycle patterns"""
        lifecycle_data = {
            'single': self.df[self.df['album_type'] == 'single'],
            'album': self.df[self.df['album_type'] == 'album']
        }
        
        lifecycle_analysis = {}
        for album_type, group in lifecycle_data.items():
            lifecycle_analysis[album_type] = {
                'count': len(group),
                'avg_popularity': group['popularity'].mean(),
                'avg_position': group['position'].mean(),
                'popularity_std': group['popularity'].std(),
                'avg_total_tracks': group['total_tracks'].mean(),
            }
        
        return lifecycle_analysis
    
    def explicit_content_classification(self):
        """Classify content attributes on lifecycle"""
        classification = {
            'explicit': {
                'count': self.df['is_explicit'].sum(),
                'avg_popularity': self.df[self.df['is_explicit']]['popularity'].mean(),
                'avg_position': self.df[self.df['is_explicit']]['position'].mean(),
                'avg_engagement': self.df[self.df['is_explicit']]['engagement_score'].mean(),
            },
            'non_explicit': {
                'count': (~self.df['is_explicit']).sum(),
                'avg_popularity': self.df[~self.df['is_explicit']]['popularity'].mean(),
                'avg_position': self.df[~self.df['is_explicit']]['position'].mean(),
                'avg_engagement': self.df[~self.df['is_explicit']]['engagement_score'].mean(),
            }
        }
        
        return classification
    
    def playlist_location_analysis(self):
        """Analyze playlist position and chart patterns"""
        # Divide into groups: Top 10, 11-25, 26-50
        self.df['chart_segment'] = pd.cut(self.df['position'], 
                                          bins=[0, 10, 25, 50],
                                          labels=['Top 10', 'Top 11-25', 'Top 26-50'])
        
        playlist_analysis = {}
        for segment in ['Top 10', 'Top 11-25', 'Top 26-50']:
            segment_data = self.df[self.df['chart_segment'] == segment]
            playlist_analysis[segment] = {
                'count': len(segment_data),
                'avg_popularity': segment_data['popularity'].mean(),
                'avg_duration': segment_data['duration_minutes'].mean(),
                'explicit_count': segment_data['is_explicit'].sum(),
                'avg_engagement': segment_data['engagement_score'].mean(),
            }
        
        return playlist_analysis
    
    def popularity_stability_analysis(self):
        """Analyze popularity vs lifecycle stability"""
        # Create stability score based on consistency of popularity
        self.df['popularity_stability'] = abs(self.df['popularity'] - 
                                              self.df['popularity'].mean()) / self.df['popularity'].std()
        
        stability_metrics = {
            'high_popularity': {
                'threshold': 85,
                'count': len(self.df[self.df['popularity'] >= 85]),
                'avg_position': self.df[self.df['popularity'] >= 85]['position'].mean(),
                'avg_stability': self.df[self.df['popularity'] >= 85]['popularity_stability'].mean(),
            },
            'medium_popularity': {
                'threshold': '70-84',
                'count': len(self.df[(self.df['popularity'] >= 70) & (self.df['popularity'] < 85)]),
                'avg_position': self.df[(self.df['popularity'] >= 70) & (self.df['popularity'] < 85)]['position'].mean(),
                'avg_stability': self.df[(self.df['popularity'] >= 70) & (self.df['popularity'] < 85)]['popularity_stability'].mean(),
            },
            'lower_popularity': {
                'threshold': '<70',
                'count': len(self.df[self.df['popularity'] < 70]),
                'avg_position': self.df[self.df['popularity'] < 70]['position'].mean(),
                'avg_stability': self.df[self.df['popularity'] < 70]['popularity_stability'].mean(),
            }
        }
        
        return stability_metrics
    
    def create_visualizations(self, output_dir='./visualizations'):
        """Create all required visualizations"""
        Path(output_dir).mkdir(exist_ok=True)
        
        # 1. Popularity Distribution
        plt.figure(figsize=(12, 6))
        plt.hist(self.df['popularity'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
        plt.xlabel('Popularity Score')
        plt.ylabel('Number of Songs')
        plt.title('Distribution of Popularity Scores - Spain Top 50')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/01_popularity_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Position vs Popularity Scatter
        plt.figure(figsize=(12, 7))
        scatter = plt.scatter(self.df['position'], self.df['popularity'], 
                            c=self.df['maturity_level'], cmap='coolwarm', 
                            s=200, alpha=0.6, edgecolors='black')
        plt.colorbar(scatter, label='Maturity Level')
        plt.xlabel('Chart Position')
        plt.ylabel('Popularity Score')
        plt.title('Position vs Popularity (colored by Maturity Level)')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/02_position_vs_popularity.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Album Type Distribution
        plt.figure(figsize=(10, 6))
        album_counts = self.df['album_type'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']
        plt.pie(album_counts, labels=album_counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90, textprops={'fontsize': 12})
        plt.title('Distribution of Album Types (Singles vs Albums)')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/03_album_type_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Explicit Content Analysis
        plt.figure(figsize=(12, 6))
        explicit_data = self.df['is_explicit'].value_counts()
        explicit_labels = ['Non-Explicit', 'Explicit'] if False in explicit_data.index else ['Explicit']
        colors_explicit = ['#95E1D3', '#F38181']
        bars = plt.bar(range(len(explicit_data)), explicit_data.values, color=colors_explicit[:len(explicit_data)])
        plt.xticks(range(len(explicit_data)), [explicit_labels[0] if not i else explicit_labels[1] for i in range(len(explicit_data))])
        plt.ylabel('Number of Songs')
        plt.title('Explicit vs Non-Explicit Content Distribution')
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}\n({height/len(self.df)*100:.1f}%)',
                    ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/04_explicit_content.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Duration Analysis
        plt.figure(figsize=(12, 6))
        plt.scatter(self.df['duration_minutes'], self.df['popularity'], 
                   s=self.df['position']*3, alpha=0.6, c=self.df['position'], 
                   cmap='viridis', edgecolors='black')
        plt.colorbar(label='Chart Position')
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Popularity Score')
        plt.title('Song Duration vs Popularity (bubble size = position)')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/05_duration_vs_popularity.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 6. Chart Segment Analysis
        plt.figure(figsize=(12, 6))
        segment_stats = self.df.groupby('chart_segment')['popularity'].agg(['mean', 'std', 'count'])
        x_pos = np.arange(len(segment_stats))
        plt.bar(x_pos, segment_stats['mean'], yerr=segment_stats['std'], 
               capsize=5, alpha=0.7, color=['#FFD93D', '#6BCB77', '#4D96FF'])
        plt.xticks(x_pos, segment_stats.index)
        plt.ylabel('Average Popularity')
        plt.title('Average Popularity by Chart Segment')
        for i, v in enumerate(segment_stats['mean']):
            plt.text(i, v + 2, f'{v:.1f}', ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/06_chart_segments.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 7. Maturity Level Distribution
        plt.figure(figsize=(12, 6))
        plt.hist(self.df['maturity_level'], bins=20, color='coral', edgecolor='black', alpha=0.7)
        plt.xlabel('Maturity Level')
        plt.ylabel('Number of Songs')
        plt.title('Distribution of Content Maturity Levels')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/07_maturity_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 8. Engagement Score vs Position
        plt.figure(figsize=(12, 6))
        plt.scatter(self.df['position'], self.df['engagement_score'], 
                   s=100, alpha=0.6, c=self.df['popularity'], cmap='plasma', 
                   edgecolors='black')
        plt.colorbar(label='Popularity')
        plt.xlabel('Chart Position')
        plt.ylabel('Engagement Score')
        plt.title('Chart Position vs Engagement Score')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/08_engagement_score.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualizations saved to {output_dir}/")
    
    def generate_report(self, output_path='./analysis_report.json'):
        """Generate comprehensive analysis report"""
        report = {
            'metadata': {
                'title': 'Content Maturity, Release Lifecycle & Playlist Rotation Analysis',
                'subtitle': 'Spain Top 50 Songs Analysis',
                'generated_date': datetime.now().isoformat(),
                'data_source': 'Atlantic_Spain.csv',
                'total_songs_analyzed': len(self.df)
            },
            'key_performance_indicators': self.calculate_kpis(),
            'lifecycle_analysis': self.lifecycle_construction_analysis(),
            'explicit_content_analysis': self.explicit_content_classification(),
            'playlist_location_analysis': self.playlist_location_analysis(),
            'popularity_stability_analysis': self.popularity_stability_analysis(),
            'top_10_songs': self.df.nlargest(10, 'popularity')[
                ['position', 'song', 'artist', 'popularity', 'is_explicit', 'album_type']
            ].to_dict('records'),
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Report saved to {output_path}")
        return report

def main():
    # Initialize analysis
    analysis = SpanishChartsAnalysis('Atlantic_Spain.csv')
    
    # Generate visualizations
    analysis.create_visualizations()
    
    # Generate report
    report = analysis.generate_report()
    
    # Print summary
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE - KEY FINDINGS")
    print("="*60)
    kpis = report['key_performance_indicators']
    print(f"\nKey Performance Indicators:")
    print(f"  - Average Popularity: {kpis['average_popularity']:.2f}")
    print(f"  - Explicit Content: {kpis['explicit_percentage']:.1f}%")
    print(f"  - Average Duration: {kpis['average_duration_minutes']:.2f} minutes")
    print(f"  - Average Engagement Score: {kpis['average_engagement_score']:.3f}")
    
    lifecycle = report['lifecycle_analysis']
    print(f"\nLifecycle Analysis:")
    for album_type, data in lifecycle.items():
        print(f"  {album_type.upper()}:")
        print(f"    - Count: {data['count']}")
        print(f"    - Avg Popularity: {data['avg_popularity']:.2f}")
        print(f"    - Avg Position: {data['avg_position']:.1f}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
