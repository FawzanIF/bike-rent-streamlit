import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Membaca file CSV
hour_df = pd.read_csv('hour.csv')
day_df = pd.read_csv('day.csv')

# Disable the warning about deprecated use of pyplot
st.set_option('deprecation.showPyplotGlobalUse', False)

# Fungsi untuk mengatur format angka dengan pemisah ribuan
def format_millions(x, pos):
    return f'{x/1e6:.1f} jt'

# Membuat aplikasi Streamlit
st.title('Analisis Data dengan Streamlit')

# Grafik Jumlah Peminjaman per Musim
# Grafik Jumlah Peminjaman per Musim
st.subheader('Grafik Jumlah Peminjaman per Musim')
season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
day_df['season'] = day_df['season'].map(season_map)
seasonly_rentals = day_df.groupby('season')['cnt'].sum().reset_index()
seasonly_rentals = seasonly_rentals.sort_values(by='cnt', ascending=False)
colors = ['skyblue', 'salmon', 'lightgreen', 'orange']

plt.figure(figsize=(8, 6))
plt.bar(seasonly_rentals['season'], seasonly_rentals['cnt'], alpha=0.7, color=colors)
plt.xlabel('Musim')
plt.ylabel('Jumlah Peminjaman')
y_format = mticker.FuncFormatter(format_millions)
plt.gca().yaxis.set_major_formatter(y_format)
plt.title('Jumlah Peminjaman per Musim')
st.pyplot()

hour_df_cleaned = pd.read_csv('hour_cleaned.csv')
day_df_cleaned = pd.read_csv('day_cleaned.csv')

# Grafik Rata-rata Suhu per Musim
st.subheader('Grafik Rata-rata Suhu per Musim')
season_avg_temp = hour_df_cleaned.groupby('season')['atemp'].mean()
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
avg_temps = season_avg_temp.values

plt.figure(figsize=(8, 6))
plt.bar(seasons, avg_temps, color='b')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Suhu (temp)')
plt.title('Rata-rata Suhu (temp) di Setiap Musim')
plt.ylim(0, max(avg_temps) + 0.1)
plt.grid(axis='y')

for i, temp in enumerate(avg_temps):
    plt.text(i, temp + 0.02, f'{temp:.2f}', ha='center', va='bottom')

st.pyplot()

# Grafik Total Jumlah Peminjam Casual vs Registered
st.subheader('Grafik Total Jumlah Peminjam Casual vs Registered')
total_casual = hour_df_cleaned['casual'].sum()
total_registered = hour_df_cleaned['registered'].sum()

labels = ['Casual', 'Registered']
sizes = [total_casual, total_registered]
colors = ['skyblue', 'salmon']
formatted_total_casual = f'{total_casual:,}'
formatted_total_registered = f'{total_registered:,}'
casual_label = f'Casual: \n{formatted_total_casual}'
registered_label = f'Registered: \n{formatted_total_registered}'

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=[casual_label, registered_label], colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Total Jumlah Peminjam Casual vs Registered')
plt.axis('equal')
st.pyplot()

# Grafik Perbandingan Transaksi di Setiap Sesi
st.subheader('Grafik Perbandingan Transaksi di Setiap Sesi')
grouped_data = hour_df_cleaned.groupby(['workingday', 'holiday', 'hr'])['cnt'].mean().reset_index()
hours = range(24)

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
weekday_data = grouped_data[(grouped_data['workingday'] == 1) & (grouped_data['holiday'] == 0)]
weekday_counts = weekday_data['cnt']
plt.plot(hours, weekday_counts, marker='o', linestyle='-', label='Weekday', color='skyblue')
plt.ylabel('Rata-rata Jumlah Transaksi (cnt)')
plt.title('Perbandingan Transaksi di Setiap Sesi')
plt.xticks(hours)
plt.legend()

plt.subplot(3, 1, 2)
weekend_data = grouped_data[(grouped_data['workingday'] == 0) & (grouped_data['holiday'] == 0)]
weekend_counts = weekend_data['cnt']
plt.plot(hours, weekend_counts, marker='o', linestyle='-', label='Weekend', color='salmon')
plt.ylabel('Rata-rata Jumlah Transaksi (cnt)')
plt.xticks(hours)
plt.legend()

plt.subplot(3, 1, 3)
holiday_data = grouped_data[grouped_data['holiday'] == 1]
holiday_counts = holiday_data['cnt']
plt.plot(hours, holiday_counts, marker='o', linestyle='-', label='Holiday', color='lightgreen')
plt.xlabel('Jam (Hour)')
plt.ylabel('Rata-rata Jumlah Transaksi (cnt)')
plt.xticks(hours)
plt.legend()

plt.tight_layout()
st.pyplot()

st.subheader('Grafik Total Jumlah Transaksi pada Sesisi Weekday, Weekend, dan Holiday')
grouped_data = hour_df_cleaned.groupby(['workingday', 'holiday'])['cnt'].sum().reset_index()
weekday_total = grouped_data[(grouped_data['workingday'] == 1) & (grouped_data['holiday'] == 0)]['cnt'].values[0]
weekend_total = grouped_data[(grouped_data['workingday'] == 0) & (grouped_data['holiday'] == 0)]['cnt'].values[0]
holiday_total = grouped_data[grouped_data['holiday'] == 1]['cnt'].values[0]
total_counts = [weekday_total, weekend_total, holiday_total]
sessions = ['Weekday', 'Weekend', 'Holiday']
colors = ['skyblue', 'salmon', 'lightgreen']

plt.figure(figsize=(8, 6))
plt.bar(sessions, total_counts, color=colors)
plt.xlabel('Sesi')
plt.ylabel('Total Jumlah Transaksi (cnt)')

for i, total in enumerate(total_counts):
    plt.text(i, total + 1000, f'{total}', ha='center', va='bottom')

y_format = mticker.FuncFormatter(format_millions)
plt.gca().yaxis.set_major_formatter(y_format)
plt.title(f'Total Jumlah Transaksi (cnt) pada Sesisi Weekday, Weekend, dan Holiday')
st.pyplot()

st.subheader('Grafik Pertumbuhan Konsumen dari Waktu ke Waktu (per bulan)')
day_df['dteday'] = pd.to_datetime(day_df_cleaned['dteday'])
monthly_counts = day_df.groupby(day_df_cleaned['dteday'].dt.to_period('M'))['cnt'].sum()
months = monthly_counts.index.strftime('%b %Y')
counts = monthly_counts.values

plt.figure(figsize=(12, 6))
plt.plot(months, counts, marker='o', linestyle='-', color='b')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Total Transaksi (cnt)')
plt.title('Pertumbuhan Konsumen dari Waktu ke Waktu (per bulan)')
plt.xticks(rotation=45)

st.pyplot()

st.subheader('Grafik Distribusi Feeling Temperature (atemp)')
atemp_normalized = hour_df_cleaned['atemp']
cnt = hour_df_cleaned['cnt']
atemp_celsius = atemp_normalized * 50.0

plt.figure(figsize=(10, 6))
plt.hist(atemp_celsius, bins=30, alpha=0.5, color='b', edgecolor='black')
plt.xlabel('Feeling Temperature (atemp) (°C)')
plt.ylabel('Frekuensi')
plt.title('Distribusi Feeling Temperature (atemp) (°C) terhadap Minat Konsumen dalam Melakukan Transaksi')
plt.grid(True)

st.pyplot()
