import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import webbrowser

def scrape_github():
    github_link = github_link_entry.get()

    try:
        response = requests.get(github_link)
        soup = BeautifulSoup(response.content, "html.parser")
        img_element = soup.find("img", class_="avatar-user")
        if img_element:
            image_url = img_element["src"]
            image_url = image_url.replace("?s=64", "?")
            photo_link_entry.delete(0, tk.END)
            photo_link_entry.insert(tk.END, image_url)
            follow_button.config(state=tk.NORMAL)
            download_button.config(state=tk.NORMAL)
        else:
            photo_link_entry.delete(0, tk.END)
            photo_link_entry.insert(tk.END, "Failed to retrieve the GitHub profile photo.")
    except Exception as e:
        photo_link_entry.delete(0, tk.END)
        photo_link_entry.insert(tk.END, f"Error: {str(e)}")
        follow_button.config(state=tk.DISABLED)
        download_button.config(state=tk.DISABLED)

def follow_link():
    photo_link = photo_link_entry.get()
    webbrowser.open_new(photo_link)

def download_photo():
    photo_link = photo_link_entry.get()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG Image", "*.jpg"), ("All Files", "*.*")],
    )

    if file_path:
        try:
            response = requests.get(photo_link)
            with open(file_path, "wb") as file:
                file.write(response.content)
            messagebox.showinfo("Download Complete", "Profile photo downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Download Error", f"An error occurred during the download: {str(e)}")
    else:
        messagebox.showwarning("Download Cancelled", "Download cancelled by user.")

window = tk.Tk()
window.title("Web Scraper")
window.geometry("500x350")
window.configure(bg="#f0f0f0")

heading_label = tk.Label(window, text="Web Scraper", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333")
heading_label.pack(pady=10)

github_link_label = tk.Label(window, text="Enter GitHub Profile Link:", font=("Arial", 10), bg="#f0f0f0", fg="#333333")
github_link_label.pack()

github_link_entry = tk.Entry(window, width=40, font=("Arial", 10))
github_link_entry.pack(pady=5)

submit_button = tk.Button(window, text="Submit", command=scrape_github, bg="#4287f5", fg="white")
submit_button.pack(pady=10)

photo_link_label = tk.Label(window, text="Profile Photo Link:", font=("Arial", 10), bg="#f0f0f0", fg="#333333")
photo_link_label.pack()

photo_link_entry = tk.Entry(window, width=40, font=("Arial", 10))
photo_link_entry.pack(pady=5)

follow_button = tk.Button(window, text="Follow Link", command=follow_link, state=tk.DISABLED, bg="#4287f5", fg="white")
follow_button.pack(pady=5)

download_button = tk.Button(window, text="Download Photo", command=download_photo, state=tk.DISABLED, bg="#4287f5", fg="white")
download_button.pack(pady=5)

window.mainloop()
