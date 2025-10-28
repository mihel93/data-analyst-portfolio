"""
HR Employee Attrition Analysis
===============================
Analyzing factors that influence employee attrition to help HR make data-driven decisions.

Author: [Your Name]
Date: October 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load the data
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

print("="*80)
print("HR EMPLOYEE ATTRITION ANALYSIS")
print("="*80)

# ==========================================
# 1. DATA OVERVIEW
# ==========================================
print("\n1. DATA OVERVIEW")
print("-" * 80)
print(f"Dataset shape: {df.shape[0]} employees, {df.shape[1]} features")
print(f"Attrition rate: {(df['Attrition']=='Yes').sum() / len(df) * 100:.2f}%")
print(f"Missing values: {df.isnull().sum().sum()}")

# ==========================================
# 2. EXPLORATORY DATA ANALYSIS
# ==========================================
print("\n2. ATTRITION BREAKDOWN")
print("-" * 80)

# Attrition by Department
print("\nAttrition by Department:")
attrition_dept = pd.crosstab(df['Department'], df['Attrition'], normalize='index') * 100
print(attrition_dept.round(2))

# Attrition by Job Role
print("\nAttrition by Job Role:")
attrition_role = df.groupby('JobRole')['Attrition'].apply(lambda x: (x=='Yes').sum() / len(x) * 100).sort_values(ascending=False)
print(attrition_role.round(2))

# Attrition by Age Group
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 100], labels=['<30', '30-40', '40-50', '50+'])
print("\nAttrition by Age Group:")
attrition_age = df.groupby('AgeGroup')['Attrition'].apply(lambda x: (x=='Yes').sum() / len(x) * 100)
print(attrition_age.round(2))

# ==========================================
# 3. KEY INSIGHTS - NUMERICAL FEATURES
# ==========================================
print("\n3. NUMERICAL ANALYSIS")
print("-" * 80)

# Compare key metrics between employees who left vs stayed
numerical_cols = ['MonthlyIncome', 'Age', 'YearsAtCompany', 'DistanceFromHome', 
                  'TotalWorkingYears', 'YearsSinceLastPromotion']

comparison = df.groupby('Attrition')[numerical_cols].mean()
print("\nAverage values by Attrition status:")
print(comparison.round(2))

# Statistical significance testing
print("\n\nStatistical Significance (t-test p-values):")
for col in numerical_cols:
    left = df[df['Attrition'] == 'Yes'][col]
    stayed = df[df['Attrition'] == 'No'][col]
    t_stat, p_value = stats.ttest_ind(left, stayed)
    significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
    print(f"{col:30s}: p={p_value:.4f} {significance}")

# ==========================================
# 4. CATEGORICAL FEATURES ANALYSIS
# ==========================================
print("\n4. CATEGORICAL FEATURES IMPACT")
print("-" * 80)

categorical_features = ['OverTime', 'JobSatisfaction', 'WorkLifeBalance', 
                       'EnvironmentSatisfaction', 'JobInvolvement']

for feature in categorical_features:
    attrition_rate = df.groupby(feature)['Attrition'].apply(lambda x: (x=='Yes').sum() / len(x) * 100)
    print(f"\n{feature}:")
    print(attrition_rate.round(2))

# ==========================================
# 5. VISUALIZATIONS
# ==========================================
print("\n5. GENERATING VISUALIZATIONS...")
print("-" * 80)

# Create a figure with multiple subplots
fig = plt.figure(figsize=(20, 12))

# 1. Attrition Overview
ax1 = plt.subplot(3, 3, 1)
attrition_counts = df['Attrition'].value_counts()
colors = ['#2ecc71', '#e74c3c']
plt.pie(attrition_counts, labels=['Stayed', 'Left'], autopct='%1.1f%%', 
        colors=colors, startangle=90)
plt.title('Overall Attrition Rate', fontsize=14, fontweight='bold')

# 2. Attrition by Department
ax2 = plt.subplot(3, 3, 2)
dept_attrition = df[df['Attrition']=='Yes']['Department'].value_counts()
plt.barh(dept_attrition.index, dept_attrition.values, color='#e74c3c')
plt.xlabel('Number of Employees Left')
plt.title('Attrition by Department', fontsize=14, fontweight='bold')
plt.tight_layout()

# 3. Attrition by Age Group
ax3 = plt.subplot(3, 3, 3)
age_data = df.groupby('AgeGroup')['Attrition'].apply(lambda x: (x=='Yes').sum() / len(x) * 100)
plt.bar(age_data.index, age_data.values, color='#3498db')
plt.ylabel('Attrition Rate (%)')
plt.title('Attrition Rate by Age Group', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)

# 4. Monthly Income Distribution
ax4 = plt.subplot(3, 3, 4)
plt.hist([df[df['Attrition']=='No']['MonthlyIncome'], 
          df[df['Attrition']=='Yes']['MonthlyIncome']], 
         label=['Stayed', 'Left'], bins=30, alpha=0.7, color=['#2ecc71', '#e74c3c'])
plt.xlabel('Monthly Income')
plt.ylabel('Frequency')
plt.title('Income Distribution by Attrition', fontsize=14, fontweight='bold')
plt.legend()

# 5. Years at Company
ax5 = plt.subplot(3, 3, 5)
plt.hist([df[df['Attrition']=='No']['YearsAtCompany'], 
          df[df['Attrition']=='Yes']['YearsAtCompany']], 
         label=['Stayed', 'Left'], bins=20, alpha=0.7, color=['#2ecc71', '#e74c3c'])
plt.xlabel('Years at Company')
plt.ylabel('Frequency')
plt.title('Tenure Distribution by Attrition', fontsize=14, fontweight='bold')
plt.legend()

# 6. Distance from Home
ax6 = plt.subplot(3, 3, 6)
plt.hist([df[df['Attrition']=='No']['DistanceFromHome'], 
          df[df['Attrition']=='Yes']['DistanceFromHome']], 
         label=['Stayed', 'Left'], bins=20, alpha=0.7, color=['#2ecc71', '#e74c3c'])
plt.xlabel('Distance from Home (km)')
plt.ylabel('Frequency')
plt.title('Distance from Home by Attrition', fontsize=14, fontweight='bold')
plt.legend()

# 7. Overtime Impact
ax7 = plt.subplot(3, 3, 7)
overtime_data = pd.crosstab(df['OverTime'], df['Attrition'], normalize='index') * 100
overtime_data.plot(kind='bar', ax=ax7, color=['#2ecc71', '#e74c3c'])
plt.ylabel('Percentage (%)')
plt.title('Attrition by Overtime Status', fontsize=14, fontweight='bold')
plt.xticks(rotation=0)
plt.legend(title='Attrition', labels=['Stayed', 'Left'])

# 8. Job Satisfaction
ax8 = plt.subplot(3, 3, 8)
satisfaction_data = df.groupby('JobSatisfaction')['Attrition'].apply(lambda x: (x=='Yes').sum() / len(x) * 100)
plt.plot(satisfaction_data.index, satisfaction_data.values, marker='o', linewidth=2, markersize=8, color='#e74c3c')
plt.xlabel('Job Satisfaction Level (1-4)')
plt.ylabel('Attrition Rate (%)')
plt.title('Attrition Rate by Job Satisfaction', fontsize=14, fontweight='bold')
plt.xticks([1, 2, 3, 4])
plt.grid(True, alpha=0.3)

# 9. Work-Life Balance
ax9 = plt.subplot(3, 3, 9)
balance_data = df.groupby('WorkLifeBalance')['Attrition'].apply(lambda x: (x=='Yes').sum() / len(x) * 100)
plt.plot(balance_data.index, balance_data.values, marker='s', linewidth=2, markersize=8, color='#9b59b6')
plt.xlabel('Work-Life Balance (1-4)')
plt.ylabel('Attrition Rate (%)')
plt.title('Attrition Rate by Work-Life Balance', fontsize=14, fontweight='bold')
plt.xticks([1, 2, 3, 4])
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('hr_attrition_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: hr_attrition_analysis.png")

# ==========================================
# 6. CORRELATION ANALYSIS
# ==========================================
print("\n6. CORRELATION ANALYSIS")
print("-" * 80)

# Create binary attrition column
df['Attrition_Binary'] = (df['Attrition'] == 'Yes').astype(int)

# Select numerical columns for correlation
numerical_features = ['Age', 'MonthlyIncome', 'DistanceFromHome', 'TotalWorkingYears',
                     'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
                     'JobSatisfaction', 'WorkLifeBalance', 'EnvironmentSatisfaction',
                     'JobInvolvement', 'Attrition_Binary']

correlation_matrix = df[numerical_features].corr()

# Plot correlation heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix - Key Features', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: correlation_heatmap.png")

# Top correlations with attrition
print("\nTop correlations with Attrition:")
attrition_corr = correlation_matrix['Attrition_Binary'].drop('Attrition_Binary').abs().sort_values(ascending=False)
print(attrition_corr.head(10))

# ==========================================
# 7. KEY FINDINGS & RECOMMENDATIONS
# ==========================================
print("\n" + "="*80)
print("KEY FINDINGS & RECOMMENDATIONS")
print("="*80)

print("""
TOP ATTRITION DRIVERS:
1. Overtime: Employees working overtime have significantly higher attrition
2. Job Satisfaction: Lower satisfaction correlates with higher turnover
3. Work-Life Balance: Poor balance increases likelihood of leaving
4. Distance from Home: Longer commutes associated with higher attrition
5. Years at Company: New employees (<2 years) have highest attrition risk

RECOMMENDATIONS:
1. Review and optimize overtime policies to prevent burnout
2. Implement regular satisfaction surveys and address concerns promptly
3. Offer flexible work arrangements to improve work-life balance
4. Consider remote work options for employees with long commutes
5. Strengthen onboarding and mentorship programs for new hires
6. Focus retention efforts on Sales Representatives and Laboratory Technicians
7. Monitor younger employees (<30) more closely for early warning signs
""")

print("\n" + "="*80)
print("Analysis complete! Check the generated PNG files for visualizations.")
print("="*80)
