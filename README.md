# 📱 Top-Selling Phones by Company — Year-wise Analytics Dashboard

A Streamlit dashboard that analyzes phone sales by company across years, with a
simple built-in forecast for next year's sales.

## What's in this folder
- `generate_data.py` — creates the synthetic dataset (`phone_sales.csv`)
- `app.py` — the dashboard itself
- `requirements.txt` — the Python packages needed
- `phone_sales.csv` — the generated dataset (already included, but you can regenerate it)

---

## PART A: Run it on your own computer

### Step 1 — Install Python
If you don't have Python yet, download it from https://www.python.org/downloads/
(Get version 3.10 or higher. During install on Windows, tick "Add Python to PATH".)

### Step 2 — Open a terminal in this folder
- **Windows:** open the folder in File Explorer, click the address bar, type `cmd`, hit Enter.
- **Mac:** open Terminal, type `cd ` (with a space), then drag this folder into the terminal window, hit Enter.

### Step 3 — Install the required packages
```
pip install -r requirements.txt
```
Wait for it to finish (this downloads Streamlit, Pandas, NumPy, Plotly).

### Step 4 — Generate the data (only needed once, or whenever you want fresh random data)
```
python generate_data.py
```
You should see a message like `Done! 'phone_sales.csv' created with 56 rows.`

### Step 5 — Run the dashboard
```
streamlit run app.py
```
Your browser will automatically open to something like `http://localhost:8501`
showing the live dashboard. Use the sidebar to filter by year and company.

To stop it, go back to the terminal and press `Ctrl + C`.

---

## PART B: Deploy it online for free (Streamlit Community Cloud)

### Step 1 — Create a GitHub account
If you don't have one: https://github.com/join

### Step 2 — Create a new repository
1. Go to https://github.com/new
2. Name it something like `phone-sales-dashboard`
3. Set it to **Public**
4. Click **Create repository**

### Step 3 — Upload your files
On the new repo's page, click **"uploading an existing file"** and drag in:
- `app.py`
- `generate_data.py`
- `requirements.txt`
- `phone_sales.csv`

Click **Commit changes**.

### Step 4 — Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"Create app"** → choose **"From an existing repo"**
4. Select your `phone-sales-dashboard` repo, branch `main`, and set the main file to `app.py`
5. Click **Deploy**

Wait 1-2 minutes. You'll get a public link like:
`https://your-username-phone-sales-dashboard.streamlit.app`

That link is now live — share it on your resume, LinkedIn, or with recruiters.

---

## How the prediction works
The dashboard fits a straight line (linear trend) through each company's
historical `units_sold` per year, then projects it one year forward. This is
intentionally simple so it runs instantly with no extra setup — it's a
reasonable v1 forecast for a portfolio project. You can later upgrade it to
a more advanced model (e.g., Facebook Prophet) once the basic app is deployed
and working.

## Customizing
- Want real-looking numbers? Open `generate_data.py` and adjust the
  `base_units`, `growth`, and `base_price` ranges to match numbers you've
  seen in public market reports (Counterpoint, IDC, Statista).
- Want different companies? Edit the `companies` list at the top of
  `generate_data.py`.
