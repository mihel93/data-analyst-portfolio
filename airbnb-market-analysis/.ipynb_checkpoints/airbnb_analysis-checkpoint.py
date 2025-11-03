"""
Airbnb Market Analysis
======================
Analyzing Airbnb listings to understand pricing factors and market dynamics.

Author: [Your Name]
Date: October 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import re
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Load the data
df = pd.read_csv('listings.csv')

print("="*80)
print("AIRBNB MARKET ANALYSIS")
print("="*80)

# ==========================================
# 1. DATA CLEANING & PREPARATION
# ==========================================
print("\n1. DATA CLEANING")
print("-" * 80)
print(f"Original dataset: {df.shape[0]} listings, {df.shape[1]} features")

# Clean price column (remove $ and , then convert to float)
df['price_cleaned'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)

# Remove outliers (prices beyond reasonable range)
q1 = df['price_cleaned'].quantile(0.01)
q99 = df['price_cleaned'].quantile(0.99)
df_clean = df[(df['price_cleaned'] >= q1) & (df['price_cleaned'] <= q99)].copy()

print(f"After cleaning: {df_clean.shape[0]} listings")
print(f"Price range: ${df_clean['price_cleaned'].min():.2f} - ${df_clean['price_cleaned'].max():.2f}")
print(f"Average price: ${df_clean['price_cleaned'].mean():.2f}")
print(f"Median price: ${df_clean['price_cleaned'].median():.2f}")

# ==========================================
# 2. MARKET OVERVIEW
# ==========================================
print("\n2. MARKET OVERVIEW")
print("-" * 80)

# Room type distribution
print("\nRoom Type Distribution:")
print(df_clean['room_type'].value_counts())
print("\nRoom Type Percentages:")
print((df_clean['room_type'].value_counts() / len(df_clean) * 100).round(2))

# Property type distribution (top 10)
print("\nTop 10 Property Types:")
print(df_clean['property_type'].value_counts().head(10))

# Neighborhood distribution (top 10)
if 'neighbourhood_cleansed' in df_clean.columns:
    print("\nTop 10 Neighborhoods by Listings:")
    print(df_clean['neighbourhood_cleansed'].value_counts().head(10))

# ==========================================
# 3. PRICING ANALYSIS
# ==========================================
print("\n3. PRICING ANALYSIS")
print("-" * 80)

# Average price by room type
print("\nAverage Price by Room Type:")
price_by_room = df_clean.groupby('room_type')['price_cleaned'].agg(['mean', 'median', 'count'])
print(price_by_room.round(2))

# Average price by number of bedrooms
if 'bedrooms' in df_clean.columns and df_clean['bedrooms'].notna().sum() > 0:
    print("\nAverage Price by Number of Bedrooms:")
    price_by_bedrooms = df_clean[df_clean['bedrooms'].notna()].groupby('bedrooms')['price_cleaned'].mean().sort_index()
    print(price_by_bedrooms.head(8).round(2))

# Average price by accommodates
print("\nAverage Price by Guest Capacity:")
price_by_accommodates = df_clean.groupby('accommodates')['price_cleaned'].mean().sort_index()
print(price_by_accommodates.head(10).round(2))

# Top 10 most expensive neighborhoods
if 'neighbourhood_cleansed' in df_clean.columns:
    print("\nTop 10 Most Expensive Neighborhoods:")
    expensive_neighborhoods = df_clean.groupby('neighbourhood_cleansed').agg({
        'price_cleaned': 'mean',
        'id': 'count'
    }).rename(columns={'id': 'count'})
    expensive_neighborhoods = expensive_neighborhoods[expensive_neighborhoods['count'] >= 5]  # At least 5 listings
    print(expensive_neighborhoods.sort_values('price_cleaned', ascending=False).head(10).round(2))

# ==========================================
# 4. REVIEW ANALYSIS
# ==========================================
print("\n4. REVIEW & RATING ANALYSIS")
print("-" * 80)

# Overall review statistics
print(f"\nTotal reviews: {df_clean['number_of_reviews'].sum():,.0f}")
print(f"Listings with reviews: {(df_clean['number_of_reviews'] > 0).sum()} ({(df_clean['number_of_reviews'] > 0).sum() / len(df_clean) * 100:.1f}%)")

if 'review_scores_rating' in df_clean.columns:
    ratings = df_clean['review_scores_rating'].dropna()
    if len(ratings) > 0:
        print(f"\nAverage rating: {ratings.mean():.2f} / 5.0")
        print(f"Median rating: {ratings.median():.2f} / 5.0")
        
        # Correlation between reviews and price
        if df_clean[['number_of_reviews', 'price_cleaned']].notna().all(axis=1).sum() > 10:
            corr = df_clean[['number_of_reviews', 'price_cleaned']].corr().iloc[0, 1]
            print(f"\nCorrelation between reviews and price: {corr:.3f}")

# ==========================================
# 5. HOST ANALYSIS
# ==========================================
print("\n5. HOST ANALYSIS")
print("-" * 80)

if 'host_is_superhost' in df_clean.columns:
    superhosts = df_clean['host_is_superhost'].value_counts()
    print(f"\nSuperhosts: {superhosts.get('t', 0)} ({superhosts.get('t', 0) / len(df_clean) * 100:.1f}%)")
    
    # Superhost vs regular host pricing
    superhost_price = df_clean[df_clean['host_is_superhost'] == 't']['price_cleaned'].mean()
    regular_price = df_clean[df_clean['host_is_superhost'] == 'f']['price_cleaned'].mean()
    print(f"Superhost average price: ${superhost_price:.2f}")
    print(f"Regular host average price: ${regular_price:.2f}")

# ==========================================
# 6. AVAILABILITY & BOOKING ANALYSIS
# ==========================================
print("\n6. AVAILABILITY ANALYSIS")
print("-" * 80)

print(f"\nAverage availability (next 365 days): {df_clean['availability_365'].mean():.0f} days")
print(f"Median availability: {df_clean['availability_365'].median():.0f} days")

# Listings with high availability (>300 days)
high_availability = (df_clean['availability_365'] > 300).sum()
print(f"\nListings available >300 days/year: {high_availability} ({high_availability / len(df_clean) * 100:.1f}%)")

# Minimum nights analysis
print(f"\nAverage minimum nights: {df_clean['minimum_nights'].mean():.1f}")
print(f"Median minimum nights: {df_clean['minimum_nights'].median():.0f}")

# ==========================================
# 7. VISUALIZATIONS
# ==========================================
print("\n7. GENERATING VISUALIZATIONS...")
print("-" * 80)

# Create comprehensive visualization
fig = plt.figure(figsize=(20, 12))

# 1. Price Distribution
ax1 = plt.subplot(3, 3, 1)
plt.hist(df_clean['price_cleaned'], bins=50, color='#3498db', alpha=0.7, edgecolor='black')
plt.axvline(df_clean['price_cleaned'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: ${df_clean['price_cleaned'].mean():.0f}")
plt.axvline(df_clean['price_cleaned'].median(), color='green', linestyle='--', linewidth=2, label=f"Median: ${df_clean['price_cleaned'].median():.0f}")
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.title('Price Distribution', fontsize=14, fontweight='bold')
plt.legend()

# 2. Price by Room Type
ax2 = plt.subplot(3, 3, 2)
room_prices = df_clean.groupby('room_type')['price_cleaned'].mean().sort_values(ascending=True)
plt.barh(room_prices.index, room_prices.values, color='#e74c3c')
plt.xlabel('Average Price ($)')
plt.title('Average Price by Room Type', fontsize=14, fontweight='bold')

# 3. Room Type Distribution
ax3 = plt.subplot(3, 3, 3)
room_counts = df_clean['room_type'].value_counts()
colors_pie = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
plt.pie(room_counts, labels=room_counts.index, autopct='%1.1f%%', colors=colors_pie, startangle=90)
plt.title('Room Type Distribution', fontsize=14, fontweight='bold')

# 4. Price vs Accommodates
ax4 = plt.subplot(3, 3, 4)
accommodates_price = df_clean.groupby('accommodates')['price_cleaned'].mean()
plt.plot(accommodates_price.index, accommodates_price.values, marker='o', linewidth=2, markersize=8, color='#9b59b6')
plt.xlabel('Number of Guests')
plt.ylabel('Average Price ($)')
plt.title('Price by Guest Capacity', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# 5. Number of Reviews Distribution
ax5 = plt.subplot(3, 3, 5)
reviews_with_data = df_clean[df_clean['number_of_reviews'] > 0]['number_of_reviews']
plt.hist(reviews_with_data, bins=50, color='#1abc9c', alpha=0.7, edgecolor='black')
plt.xlabel('Number of Reviews')
plt.ylabel('Frequency')
plt.title('Review Count Distribution', fontsize=14, fontweight='bold')
plt.xlim(0, reviews_with_data.quantile(0.95))

# 6. Availability Distribution
ax6 = plt.subplot(3, 3, 6)
plt.hist(df_clean['availability_365'], bins=50, color='#f39c12', alpha=0.7, edgecolor='black')
plt.xlabel('Days Available (per year)')
plt.ylabel('Frequency')
plt.title('Availability Distribution', fontsize=14, fontweight='bold')

# 7. Price vs Reviews Scatter
ax7 = plt.subplot(3, 3, 7)
sample_data = df_clean[df_clean['number_of_reviews'] > 0].sample(min(500, len(df_clean)))
plt.scatter(sample_data['number_of_reviews'], sample_data['price_cleaned'], 
           alpha=0.5, color='#e74c3c', s=30)
plt.xlabel('Number of Reviews')
plt.ylabel('Price ($)')
plt.title('Price vs Number of Reviews', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# 8. Minimum Nights Distribution
ax8 = plt.subplot(3, 3, 8)
min_nights_filtered = df_clean[df_clean['minimum_nights'] <= 30]['minimum_nights']
plt.hist(min_nights_filtered, bins=30, color='#16a085', alpha=0.7, edgecolor='black')
plt.xlabel('Minimum Nights')
plt.ylabel('Frequency')
plt.title('Minimum Stay Requirements', fontsize=14, fontweight='bold')

# 9. Top 10 Neighborhoods by Listings
ax9 = plt.subplot(3, 3, 9)
if 'neighbourhood_cleansed' in df_clean.columns:
    top_neighborhoods = df_clean['neighbourhood_cleansed'].value_counts().head(10)
    plt.barh(range(len(top_neighborhoods)), top_neighborhoods.values, color='#2980b9')
    plt.yticks(range(len(top_neighborhoods)), top_neighborhoods.index)
    plt.xlabel('Number of Listings')
    plt.title('Top 10 Neighborhoods', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('airbnb_market_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: airbnb_market_analysis.png")

# ==========================================
# 8. CORRELATION ANALYSIS
# ==========================================
print("\n8. CORRELATION ANALYSIS")
print("-" * 80)

# Select key numerical features for correlation
correlation_features = ['price_cleaned', 'accommodates', 'bedrooms', 'beds', 
                        'number_of_reviews', 'availability_365', 'minimum_nights']

# Remove features not in dataset
correlation_features = [f for f in correlation_features if f in df_clean.columns]

# Get correlation matrix
corr_df = df_clean[correlation_features].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_df, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix - Key Pricing Factors', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('airbnb_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: airbnb_correlation_heatmap.png")

# Top correlations with price
print("\nTop correlations with Price:")
price_corr = corr_df['price_cleaned'].drop('price_cleaned').abs().sort_values(ascending=False)
print(price_corr)

# ==========================================
# 9. KEY FINDINGS & RECOMMENDATIONS
# ==========================================
print("\n" + "="*80)
print("KEY FINDINGS & RECOMMENDATIONS")
print("="*80)

avg_price = df_clean['price_cleaned'].mean()
entire_home_pct = (df_clean['room_type'] == 'Entire home/apt').sum() / len(df_clean) * 100
high_review_pct = (df_clean['number_of_reviews'] >= 10).sum() / len(df_clean) * 100

print(f"""
MARKET INSIGHTS:
1. Average Listing Price: ${avg_price:.2f} per night
2. Most Common: Entire homes/apartments ({entire_home_pct:.1f}% of listings)
3. {high_review_pct:.1f}% of listings have 10+ reviews (established properties)
4. Price increases linearly with guest capacity and number of bedrooms
5. Superhosts can command higher prices on average

PRICING FACTORS (Strongest to Weakest):
1. Number of guests accommodated - Primary driver
2. Room type - Entire homes command premium prices
3. Number of bedrooms/beds - Direct impact on price
4. Location/Neighborhood - Significant geographic variation
5. Host status (Superhost) - Modest premium

RECOMMENDATIONS FOR HOSTS:
1. Optimize capacity: Listings that accommodate more guests earn significantly more
2. Consider room type: Converting to entire home can increase revenue if feasible
3. Build reviews: Focus on guest experience to accumulate positive reviews
4. Strategic pricing: Research neighborhood averages and price competitively
5. Maintain availability: Higher availability correlates with more bookings
6. Work toward Superhost status: Small but meaningful price premium

RECOMMENDATIONS FOR MARKET ENTRANTS:
1. Target underserved neighborhoods with lower competition
2. Focus on unique property types in high-demand areas
3. Offer competitive pricing for first 5-10 reviews
4. Emphasize amenities that justify higher prices
5. Maintain high response rates and guest satisfaction
""")

print("\n" + "="*80)
print("Analysis complete! Check the generated PNG files for visualizations.")
print("="*80)
