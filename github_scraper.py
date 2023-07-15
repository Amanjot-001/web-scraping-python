import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import webbrowser
from tkinter import messagebox

def scrape_github():
    github_link = github_link_entry.get()

    try:
        response = requests.get(github_link)
        soup = BeautifulSoup(response.content, "html.parser")
        img_element = soup.find("img", class_="avatar-user")
        if img_element:
            image_url = img_element["src"]
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
window.title("Web Scraping")

window.configure(bg="#331D2C")

window.geometry("500x400")
window.update_idletasks()
window_height = window.winfo_height()
screen_height = window.winfo_screenheight()
y_offset = (screen_height - window_height) // 2
window.geometry(f"500x400+{window.winfo_x()}+{y_offset}")

container_frame = tk.Frame(window, bg="#331D2C")
container_frame.pack(expand=True)

heading_label = tk.Label(
    container_frame,
    text="Web Scraping",
    font=("Arial", 48),
    fg="#97FEED",
    bg="#331D2C",
)
heading_label.pack(pady=(50, 20))

form_frame = tk.Frame(container_frame, bg="#331D2C")
form_frame.pack()

github_link_label = tk.Label(
    form_frame,
    text="Enter the Github user link:",
    font=("Arial", 16),
    fg="#068FFF",
    bg="#331D2C",
)
github_link_label.grid(row=0, column=0, padx=10, pady=(0, 10))

github_link_entry = tk.Entry(form_frame, width=50, font=("Arial", 12))
github_link_entry.grid(row=0, column=1, padx=10, pady=(0, 10))

scrape_button = tk.Button(
    form_frame,
    text="Submit",
    font=("Arial", 12),
    bg="black",
    fg="white",
    relief=tk.FLAT,
    command=scrape_github,
)
scrape_button.grid(row=0, column=2, padx=10, pady=(0, 10))

result_frame = tk.Frame(container_frame, bg="#331D2C")
result_frame.pack(pady=(20, 50))

photo_link_label = tk.Label(
    result_frame,
    text="Github profile photo link:",
    font=("Arial", 16),
    fg="#068FFF",
    bg="#331D2C",
)
photo_link_label.grid(row=0, column=0, padx=10, pady=(0, 10))

photo_link_entry = tk.Entry(result_frame, width=50, font=("Arial", 12))
photo_link_entry.grid(row=0, column=1, padx=10, pady=(0, 10))

follow_button = tk.Button(
    result_frame,
    text="Follow Link",
    font=("Arial", 12),
    bg="black",
    fg="white",
    relief=tk.FLAT,
    state=tk.DISABLED,
    command=follow_link,
)
follow_button.grid(row=0, column=2, padx=10, pady=(0, 10))

download_button = tk.Button(
    result_frame,
    text="Download",
    font=("Arial", 12),
    bg="black",
    fg="white",
    relief=tk.FLAT,
    state=tk.DISABLED,
    command=download_photo,
)
download_button.grid(row=0, column=3, padx=10, pady=(0, 10))

form_frame.columnconfigure(0, weight=1)
form_frame.columnconfigure(1, weight=2)
form_frame.columnconfigure(2, weight=1)

result_frame.columnconfigure(0, weight=1)
result_frame.columnconfigure(1, weight=2)
result_frame.columnconfigure(2, weight=1)
result_frame.columnconfigure(3, weight=1)

form_frame.grid_rowconfigure(0, pad=10)
result_frame.grid_rowconfigure(0, pad=10)

window.mainloop()
