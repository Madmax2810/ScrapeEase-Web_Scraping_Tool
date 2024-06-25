import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, Menu
import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def scrap_web():
    url = url_entry.get()
    selector = element_selector_entry.get()

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        result_text = ""

        if selector:
            selected_elements = soup.select(selector)
            result_text += "Selected Text Content:\n"
            for element in selected_elements:
                result_text += element.get_text() + '\n'
        else:
            result_text += "Whole HTML Code:\n" + str(soup)

        res_txt.config(state='normal')
        res_txt.delete(1.0, tk.END)
        res_txt.insert(tk.END, result_text)
        res_txt.config(state='disabled')

    except requests.exceptions.RequestException as e:
        res_txt.config(state='normal')
        res_txt.delete(1.0, tk.END)
        res_txt.insert(tk.END, f"Error: {e}")
        res_txt.config(state='disabled')


def export_results(format):
    data = res_txt.get(1.0, tk.END)

    save_dir = filedialog.askdirectory()

    if save_dir:
        save_file_path = filedialog.asksaveasfilename(
            defaultextension="." + format.lower(),
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt")
            ],
            initialdir=save_dir
        )

        if save_file_path:
            if format == "PDF" and save_file_path.endswith('.pdf'):
                generate_pdf(save_file_path, data)
            elif format == "CSV" and save_file_path.endswith('.csv'):
                with open(save_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    csvfile.write(data)
            elif format == "TXT" and save_file_path.endswith('.txt'):
                with open(save_file_path, 'w', encoding='utf-8') as txtfile:
                    txtfile.write(data)


def generate_pdf(file_path, data):
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    x = 100
    y = 750
    lines = data.strip().split('\n')
    for line in lines:
        if y < 50:
            c.showPage()
            y = 750
        c.drawString(x, y, line)
        y -= 20
    c.save()


def instructions():
    instructions_window = tk.Toplevel(app)
    instructions_window.title("Instructions")
    instructions_text = """
    Instructions:
    1. Enter the URL of the website you want to scrape in the text field.
    2. (Optional) Enter a data selector (e.g., p, h1, .my-class) to extract specific text content.
    3. Click the 'Scrape' button to retrieve content from the webpage.
    4. Click 'Export' in the File menu to save the scraped content in the selected format(s).
    """
    instructions_label = tk.Label(instructions_window, text=instructions_text, justify=tk.LEFT)
    instructions_label.pack(padx=10, pady=10)


app = tk.Tk()
app.title("Web Scraper with GUI")

app.minsize(width=500, height=400)
app.maxsize(width=500, height=400)

padding = 10

style = ttk.Style()
style.configure("TButton", padding=(10, 5))

url_label = ttk.Label(app, text="Enter URL:")
url_label.grid(row=0, column=0, padx=padding, pady=padding, sticky="w")
url_entry = ttk.Entry(app, width=35)
url_entry.grid(row=0, column=1, padx=padding, pady=padding, columnspan=2)

element_selector_label = ttk.Label(app, text="Element Selector:")
element_selector_label.grid(row=1, column=0, padx=padding, pady=padding, sticky="w")
element_selector_entry = ttk.Entry(app, width=30)
element_selector_entry.grid(row=1, column=1, padx=padding, pady=padding, columnspan=2)

scr_but = ttk.Button(app, text="Scrape", command=scrap_web)
scr_but.grid(row=2, column=0, columnspan=3, pady=(0, padding))

res_txt = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=10)
res_txt.config(state='disabled')
res_txt.grid(row=3, column=0, columnspan=3, padx=padding, pady=padding)

menubar = Menu(app)
app.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
export_menu = Menu(file_menu, tearoff=0)
export_menu.add_command(label="Export to PDF...", command=lambda: export_results("PDF"))
export_menu.add_command(label="Export to CSV...", command=lambda: export_results("CSV"))
export_menu.add_command(label="Export to TXT...", command=lambda: export_results("TXT"))
file_menu.add_cascade(label="Export", menu=export_menu)
menubar.add_cascade(label="File", menu=file_menu)

about_menu = Menu(menubar, tearoff=0)
about_menu.add_command(label="Instructions", command=instructions)
menubar.add_cascade(label="About", menu=about_menu)

app.mainloop()
