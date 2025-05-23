import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import date

# --- Konfigurasi Aplikasi ---
st.set_page_config(page_title="Devi's Reminder", layout="wide")

# --- CSS Tampilan Lucu dan Full Width ---
st.markdown("""
    <style>
    .stApp {
        background-color: #fff0f5;
        font-family: 'Comic Sans MS', cursive;
    }
    h1, h2, h3 {
        color: #d63384;
    }
    .main {
        max-width: none !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Menu ---
with st.sidebar:
    st.title("🌸 Devi's Reminder")
    selected = option_menu(
        menu_title="Main Menu",
        options=["🏠 Beranda", "📅 Jadwal Kuliah", "📘 Tugas Kuliah", "👩‍💼 Organisasi", "📝 To-Do List"],
        icons=["house", "calendar", "book", "people", "check2-square"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "5px", "background-color": "#ffcce6"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {"color": "black", "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#d63384", "color": "white"},
        }
    )

# --- Fungsi bantu ---
def hapus_data(df, file, label):
    st.write(f"### ❌ Hapus {label}")
    opsi_hapus = df.apply(lambda row: " - ".join(map(str, row)), axis=1)
    pilihan = st.selectbox(f"Pilih {label.lower()} yang ingin dihapus:", opsi_hapus)
    if st.button(f"Hapus {label}"):
        index_hapus = opsi_hapus[opsi_hapus == pilihan].index[0]
        df.drop(index=index_hapus, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(file, index=False)
        st.success(f"{label} berhasil dihapus!")
        st.experimental_rerun()

# --- Halaman Beranda ---
# --- Halaman Beranda ---
if selected == "🏠 Beranda":
    # CSS tambahan untuk tombol dan tampilan lucu
    st.markdown("""
        <style>
        .custom-button {
            background-color: #ffb6c1;
            color: black;
            border: none;
            padding: 0.6rem 1.5rem;
            margin: 0.5rem;
            font-size: 1rem;
            border-radius: 10px;
            cursor: pointer;
        }
        .custom-button:hover {
            background-color: #ff69b4;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout dua kolom
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("<h1 style='color:#ff4db8;'>Welcome Devi’s Reminder </h1>", unsafe_allow_html=True)
        st.markdown("""
            <p style='font-size:18px; color:#555;'>A simple, smart way to manage your day — <br>
            <i>because every moment counts.</i></p>
        """, unsafe_allow_html=True)

        # Tombol Horizontal
        st.markdown("""
            <div style='display:flex; flex-wrap:wrap; gap:10px; margin-top:20px;'>
                <button class='custom-button'>Cute</button>
                <button class='custom-button'>Smile</button>
                <button class='custom-button'>Happy</button>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("2.png", caption=None, use_column_width=True)

    # Deskripsi bawah
    st.markdown("""
        <div style='background-color:#ffe6f2; padding: 20px 30px; border-radius: 15px; margin-top: 40px;'>
            <h3 style='color:#d63384;'>With Devi’s Reminder, every task finds its time</h3>
            <p style='font-size:16px; color:#444;'>Start your day with peace of mind knowing that Devi’s Reminder is here to support you. 
            From big goals to tiny tasks, we’ll help you stay on track every step of the way.</p>
        </div>
    """, unsafe_allow_html=True)



# --- Halaman Jadwal Kuliah ---
elif selected == "📅 Jadwal Kuliah":
    st.header("📅 Jadwal Kuliah")
    file = "jadwal_kuliah.csv"
    df = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=["Hari", "Mata Kuliah", "Jam"])

    with st.expander("➕ Tambah Jadwal Kuliah"):
        hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])
        mk = st.text_input("Mata Kuliah")
        jam = st.text_input("Jam (contoh: 08.00 - 10.00)")
        if st.button("Tambah Jadwal"):
            if mk and jam:
                new_row = pd.DataFrame({"Hari": [hari], "Mata Kuliah": [mk], "Jam": [jam]})
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(file, index=False)
                st.success("Jadwal berhasil ditambahkan!")
            else:
                st.warning("Harap isi semua kolom!")

    st.write("### 📋 Daftar Jadwal Kuliah")
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        hapus_data(df, file, "Jadwal")

# --- Halaman Tugas Kuliah ---
elif selected == "📘 Tugas Kuliah":
    st.header("📘 Tugas Mata Kuliah")
    file = "tugas_kuliah.csv"
    df = pd.read_csv(file, parse_dates=["Deadline"]) if os.path.exists(file) else pd.DataFrame(columns=["Mata Kuliah", "Deskripsi", "Deadline"])

    mk = st.text_input("Mata Kuliah")
    desk = st.text_area("Deskripsi Tugas")
    deadline = st.date_input("Deadline")

    if st.button("Tambah Tugas"):
        if mk and desk:
            new_row = pd.DataFrame({"Mata Kuliah": [mk], "Deskripsi": [desk], "Deadline": [deadline]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file, index=False)
            st.success("Tugas berhasil ditambahkan!")
        else:
            st.warning("Harap isi semua kolom!")

    st.write("### 📋 Daftar Tugas")
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        hapus_data(df, file, "Tugas")

# --- Halaman Organisasi ---
elif selected == "👩‍💼 Organisasi":
    st.header("👩‍💼 Agenda Organisasi")
    file = "organisasi.csv"
    df = pd.read_csv(file, parse_dates=["Tanggal"]) if os.path.exists(file) else pd.DataFrame(columns=["Agenda", "Tanggal", "Tempat"])

    agenda = st.text_input("Nama Agenda")
    tanggal = st.date_input("Tanggal Agenda")
    tempat = st.text_input("Tempat")

    if st.button("Tambah Agenda"):
        if agenda and tempat:
            new_row = pd.DataFrame({"Agenda": [agenda], "Tanggal": [tanggal], "Tempat": [tempat]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file, index=False)
            st.success("Agenda berhasil ditambahkan!")
        else:
            st.warning("Harap isi semua kolom!")

    st.write("### 📋 Daftar Agenda")
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        hapus_data(df, file, "Agenda")

# --- Halaman To-Do List ---
elif selected == "📝 To-Do List":
    st.header("📝 To-Do List Harian")
    file = "todo.csv"
    df = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=["Tanggal", "Kegiatan"])
    tanggal = str(date.today())
    kegiatan = st.text_input("Apa yang harus dilakukan hari ini?")

    if st.button("Tambah Kegiatan"):
        if kegiatan:
            new_row = pd.DataFrame({"Tanggal": [tanggal], "Kegiatan": [kegiatan]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file, index=False)
            st.success("Kegiatan berhasil ditambahkan!")
        else:
            st.warning("Isi kegiatan tidak boleh kosong!")

    st.write("### 📋 Daftar To-Do Hari Ini")
    st.dataframe(df[df["Tanggal"] == tanggal], use_container_width=True)
    if not df.empty:
        hapus_data(df, file, "Kegiatan")
