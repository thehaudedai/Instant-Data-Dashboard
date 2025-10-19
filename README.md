# Instant Data Dashboard (Name WIP)

A Streamlit dashboard that lets users upload datasets, clean and explore data, and generate visualizations without coding.

- Designed to simplify early-stage analysis and allow export of cleaned data and visualization code.
- Built with Python, pandas, and Streamlit.

---

## 🚧 Project Features Roadmap & Implementation Checklist

This is a living checklist of planned features and components grouped by functionality. Use it to track progress and stay focused on the scope.

---

### ✅ 1. Data Preprocessing

#### 📂 Dataset Handling

- [x] Upload CSV / Excel / JSON
- [x] View raw data (with pagination)
- [x] View raw data Info
- [ ] Filter and View Certain Columns
- [ ] Filter and View Certain Rows via Index or Conditions
- [ ] Save/load project sessions _(optional)_

#### 🧼 Data Cleaning

- [x] Rename columns
- [x] Remove columns
- [x] Reorder columns
- [x] Drop duplicates
- [ ] Remove rows
  - [x] Remove Rows by Filtering
  - [ ] Remove Rows by Indexing
- [ ] Change data types (int, float, string, datetime, categorical)
- [ ] Handle missing values:
  - [ ] Drop rows/columns with NaNs
  - [ ] Fill NaNs with:
    - [ ] Mean
    - [ ] Median
    - [ ] Mode
    - [ ] Forward Fill
    - [ ] Backward Fill
    - [ ] Custom value
- [ ] Replace values (via mapping or custom)
- [ ] Edit specific cells via GUI
- [ ] Strip whitespaces
- [ ] Convert strings to datetime
- [ ] Convert categorical to numerical:
  - [ ] Label Encoding
  - [ ] One-Hot Encoding
- [ ] Normalize / Standardize columns
- [ ] Transpose data
- [ ] Pivot / Unpivot (Melt) data
- [ ] Filter rows (based on conditions)
- [ ] Sort data by columns
- [ ] Create new columns (via formula or presets)
- [ ] Group by operations with aggregation (sum, mean, count, etc.)
- [ ] Merge/Join datasets _(optional for v2)_
- [ ] Download cleaned data

---

### 📊 2. Data Analysis

#### 📋 Summary Statistics

- [ ] Dataset overview:
  - [ ] Number of rows/columns
  - [ ] Missing value count
  - [ ] Data types
- [ ] Column-level statistics:
  - [ ] Mean, Median, Mode
  - [ ] Min, Max
  - [ ] Std Deviation
  - [ ] Unique values
  - [ ] Value counts (for categoricals)
- [ ] Correlation matrix (with heatmap)
- [ ] Covariance matrix
- [ ] Skewness / Kurtosis _(optional)_
- [ ] Outlier detection (IQR / Z-score)
- [ ] Feature-target relationship summaries _(for supervised ML)_

---

### 📈 3. Data Visualization

#### 📊 Chart Types

- [ ] Bar Chart
- [ ] Line Chart
- [ ] Pie Chart
- [ ] Scatter Plot
- [ ] Histogram
- [ ] Box Plot
- [ ] Area Chart
- [ ] Heatmap
- [ ] Violin Plot _(optional)_
- [ ] Pair Plot _(optional)_

#### 🧩 Customization Options

- [ ] Select X and Y axis
- [ ] Group by / Hue support
- [ ] Filters on visualized data
- [ ] Chart titles and axis labels
- [ ] Toggle grid, legends, tooltips
- [ ] Color customization
- [ ] Export chart as image
- [ ] Export chart as Python code (Matplotlib / Seaborn / Plotly)

#### 📁 Dashboarding _(Optional for v2)_

- [ ] Combine visuals into a dashboard layout
- [ ] Save/load dashboards

---

### 🤖 4. Model Training (Sklearn)

#### 📄 Data Selection

- [ ] Choose target column
- [ ] Select features
- [ ] Train/Test split (with slider)
- [ ] Cross-validation setup _(optional)_

#### 📚 Model Selection

**Classification:**

- [ ] Logistic Regression
- [ ] Random Forest
- [ ] Decision Tree
- [ ] KNN
- [ ] SVM

**Regression:**

- [ ] Linear Regression
- [ ] Ridge / Lasso
- [ ] Random Forest Regressor
- [ ] SVR

- [ ] Clustering (KMeans) _(optional for v2)_

#### ⚙️ Model Configuration

- [ ] Hyperparameter tuning (via sliders/dropdowns)
- [ ] Random seed config
- [ ] Feature scaling:
  - [ ] StandardScaler
  - [ ] MinMaxScaler

#### 📈 Model Evaluation

**Classification:**

- [ ] Accuracy
- [ ] Precision, Recall, F1-score
- [ ] Confusion matrix
- [ ] ROC Curve

**Regression:**

- [ ] MAE, MSE, RMSE
- [ ] R² Score
- [ ] Prediction vs Actual plot

#### 📦 Model Export

- [ ] Download trained model (Pickle / Joblib)
- [ ] Export training code _(optional)_

#### 🧪 Prediction Interface

- [ ] Single row prediction (via form input)
- [ ] Batch prediction (CSV upload)

---

### 🚀 Optional / Advanced Features (Future Roadmap)

- [ ] User accounts and saved sessions
- [ ] Upload from cloud (Google Drive, Dropbox)
- [ ] AutoML (TPOT / AutoSklearn)
- [ ] NLP module (tokenization, stemming, etc.)
- [ ] Time series tools (decomposition, lag features)
- [ ] Collaborative mode (real-time editing)

---

### 🧭 Suggested UI Navigation

- **Upload** → **Clean** → **Analyze** → **Visualize** → **Model**

Use sidebar navigation with collapsible panels and modal windows for advanced operations.

---

### 💡 Contributing

This is currently a personal project, but contributions and feedback are welcome once the MVP is released.

---

### 📄 License

To be added.
