import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# ==========================================
# 1. AŞAMA: VERİYİ YÜKLEME VE TANIMA (EDA)
# ==========================================
df = pd.read_csv(r'C:\Users\user\Downloads\netflix_customer_churn.csv')

print("=== Veri Seti Boyutu ===")
print(df.shape)

print("\n=== Hedef Değişken (churned) Dağılımı ===")
print(df['churned'].value_counts())
print("\nYüzdesel Dağılım (%):")
print(df['churned'].value_counts(normalize=True) * 100)

# ==========================================
# 2. AŞAMA: VERİ TEMİZLEME VE ÖN İŞLEME
# ==========================================
df_cleaned = df.drop(columns=['customer_id'])
categorical_cols = ['gender', 'subscription_type', 'region', 'device', 'payment_method', 'favorite_genre']
df_cleaned = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True, dtype=int)

# ==========================================
# 3. AŞAMA: GÖRSELLEŞTİRME (5 GRAFİK)
# ==========================================
sns.set_theme(style="whitegrid")

# Grafik 1: Churn Dağılımı
plt.figure(figsize=(6, 4))
sns.countplot(x='churned', data=df, palette='Set2')
plt.title('Grafik 1: Abonelik Durumu Dağılımı (Churn)')
plt.xlabel('Abonelik Durumu (0: Kaldı, 1: Ayrıldı)')
plt.ylabel('Müşteri Sayısı')
plt.tight_layout()
plt.savefig(r'C:\Users\user\Downloads\grafik1_churn.png')
plt.show()

# Grafik 2: Yaş vs Churn
plt.figure(figsize=(6, 4))
sns.boxplot(x='churned', y='age', data=df, palette='Set2')
plt.title('Grafik 2: Yaş Gruplarına Göre Churn')
plt.xlabel('Abonelik Durumu (0: Kaldı, 1: Ayrıldı)')
plt.ylabel('Yaş')
plt.tight_layout()
plt.savefig(r'C:\Users\user\Downloads\grafik2_yas.png')
plt.show()

# Grafik 3: Cihaz Türü vs Churn
plt.figure(figsize=(7, 4))
sns.countplot(x='device', hue='churned', data=df, palette='Set1')
plt.title('Grafik 3: Cihaz Türüne Göre Churn')
plt.xlabel('Cihaz Türü')
plt.ylabel('Müşteri Sayısı')
plt.tight_layout()
plt.savefig(r'C:\Users\user\Downloads\grafik3_cihaz.png')
plt.show()

# Grafik 4: Son Giriş Gün Sayısı Yoğunluğu
plt.figure(figsize=(7, 4))
sns.kdeplot(data=df, x='last_login_days', hue='churned', fill=True, palette='Set2')
plt.title('Grafik 4: Son Giriş Gün Sayısı Dağılımı')
plt.xlabel('Son Girişten Bu Yana Geçen Gün')
plt.ylabel('Yoğunluk')
plt.tight_layout()
plt.savefig(r'C:\Users\user\Downloads\grafik4_son_giris.png')
plt.show()

# Grafik 5: Sayısal Değişkenlerin Korelasyon Matrisi
plt.figure(figsize=(8, 6))
numeric_cols = df.select_dtypes(include=['int64', 'float64'])
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Grafik 5: Korelasyon Isı Haritası')
plt.tight_layout()
plt.savefig(r'C:\Users\user\Downloads\grafik5_korelasyon.png')
plt.show()

# ==========================================
# 4. VE 5. AŞAMA: MODEL KURULUMU VE EVALUATION
# ==========================================
X = df_cleaned.drop(columns=['churned'])
y = df_cleaned['churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

# Ölçekleme (StandardScaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model 1: Logistic Regression
log_model = LogisticRegression(random_state=42)
log_model.fit(X_train_scaled, y_train)
y_pred_log = log_model.predict(X_test_scaled)

# Model 2: Decision Tree
tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model.fit(X_train, y_train)
y_pred_tree = tree_model.predict(X_test)

# Model Karşılaştırma Tablosu
results_df = pd.DataFrame({
    'Model': ['Logistic Regression', 'Decision Tree'],
    'Accuracy': [accuracy_score(y_test, y_pred_log), accuracy_score(y_test, y_pred_tree)],
    'Precision': [precision_score(y_test, y_pred_log), precision_score(y_test, y_pred_tree)],
    'Recall': [recall_score(y_test, y_pred_log), recall_score(y_test, y_pred_tree)]
})

print("\n=== MODEL KARŞILAŞTIRMA TABLOSU ===")
print(results_df)

print("\n=== LOGISTIC REGRESSION CONFUSION MATRIX ===")
print(confusion_matrix(y_test, y_pred_log))

print("\n=== DECISION TREE CONFUSION MATRIX ===")
print(confusion_matrix(y_test, y_pred_tree))
