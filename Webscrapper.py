import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_data():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Enter a valid URL")
        return

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Check if response is successful
        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting Data
        company_name = soup.title.string.strip() if soup.title else "Unknown"
        website = url

        # Regex Patterns
        phone_pattern = re.compile(r'\b\d{10}\b')  # 10-digit phone numbers
        email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

        phones = set(phone_pattern.findall(soup.get_text()))
        emails = set(email_pattern.findall(soup.get_text()))

        contact_info = ", ".join(emails) + (", " if emails and phones else "") + ", ".join(phones)
        phone_number = next(iter(phones), "N/A")  # First phone number found

        display_data(company_name, website, phone_number, contact_info)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to scrape: {e}")

def display_data(company_name, website, phone_number, contact_info):
    """Display data in the table"""
    table.delete(*table.get_children())  # Clear previous entries
    table.insert("", "end", values=(company_name, website, phone_number, contact_info))

def export_to_excel():
    """Export scraped data to an Excel file"""
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        data = [table.item(row)['values'] for row in table.get_children()]
        df = pd.DataFrame(data, columns=["Company Name", "Website", "Phone Number", "Contact Info"])
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Data exported successfully!")

# GUI Setup
root = tk.Tk()
root.title("Web Scraping Tool")
root.geometry("800x400")

tk.Label(root, text="Enter Website URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

scrape_btn = tk.Button(root, text="Scrape Website", command=scrape_data)
scrape_btn.pack(pady=5)

# Table
columns = ("Company Name", "Website", "Phone Number", "Contact Info")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=180)
table.pack(expand=True, fill="both", pady=5)

export_btn = tk.Button(root, text="Export to Excel", command=export_to_excel)
export_btn.pack(pady=5)

root.mainloop()
