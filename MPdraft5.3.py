import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import requests
from bs4 import BeautifulSoup
import csv
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


#============================================================================================= SCRAPER =====================================================================================================

def scrap_web():
    url = url_entry.get()
    selector = element_selector_entry.get()  
    scrape_text = text_var.get()  
    scrape_links = links_var.get()  

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        result_text = ""

        if scrape_text:
            if selector:
                selected_elements = soup.select(selector)
                result_text += "Selected Text Content:\n"
                for element in selected_elements:
                    result_text += element.get_text() + '\n'
            else:
                result_text += "Whole HTML Code:\n" + str(soup)

        if scrape_links:
            link_elements = soup.find_all('a', href=True)
            result_text += "Links:\n"
            for link in link_elements:
                result_text += link['href'] + '\n'

        res_txt.config(state='normal')
        res_txt.delete(1.0, tk.END)
        res_txt.insert(tk.END, result_text)
        res_txt.config(state='disabled')

    except requests.exceptions.RequestException as e:
        res_txt.config(state='normal')
        res_txt.delete(1.0, tk.END)
        res_txt.insert(tk.END, f"Error: {e}")
        res_txt.config(state='disabled')

#=========================================================================================== EXPORT RESULTS =============================================================================================

def export_results():
    data = res_txt.get(1.0, tk.END)
    selected_formats = []

    if pdf_var.get():
        selected_formats.append("PDF")
    if csv_var.get():
        selected_formats.append("CSV")
    if json_var.get():
        selected_formats.append("JSON")

    save_dir = filedialog.askdirectory()

    if save_dir and selected_formats:
        for format in selected_formats:
            save_file_path = filedialog.asksaveasfilename(
                defaultextension="." + format.lower(),
                filetypes=[
                    ("PDF Files", "*.pdf"),
                    ("CSV Files", "*.csv"),
                    ("JSON Files", "*.json")
                ],
                initialdir=save_dir
            )

            if save_file_path:
                if format == "PDF" and save_file_path.endswith('.pdf'):
                    generate_pdf(save_file_path, data)
                elif format == "CSV" and save_file_path.endswith('.csv'):
                    with open(save_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        csvfile.write(data)
                elif format == "JSON" and save_file_path.endswith('.json'):
                    # You need to parse the text content as JSON data
                    data_dict = {'text_content': data}
                    with open(save_file_path, 'w', encoding='utf-8') as jsonfile:
                        json.dump(data_dict, jsonfile)



#================================================================================================= GENERATE PDF ============================================================================================

def generate_pdf(file_path, data):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

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

#============================================================================================= INSTRUCTIONS ==================================================================================================

def instructions():
    instructions_window = tk.Toplevel(app)
    instructions_window.title("Instructions")
    instructions_text = """
    Instructions:
    1. Enter the URL of the website you want to scrape in the text field.
    2. (Optional) Enter a data selector (e.g., p, h1, .my-class) to extract specific text content.
    3. Check the options for what you want to scrape (Text, Links).
    4. Click the 'Scrape' button to retrieve content from the webpage.
    5. Check the export format(s) you want (PDF, CSV, JSON).
    6. Click 'Export Results' to save the scraped content in the selected format(s).
    """
    instructions_label = tk.Label(instructions_window, text=instructions_text, justify=tk.LEFT)
    instructions_label.pack(padx=10, pady=10)

#========================================================================================== GUI ==============================================================================================================

app = tk.Tk()
app.title("Web Scraper with GUI")


pdf_var = tk.IntVar()
csv_var = tk.IntVar()
json_var = tk.IntVar()


text_var = tk.IntVar()
links_var = tk.IntVar()

padding = 10

style = ttk.Style()
style.configure("TButton", padding=(10, 5))

url_label = ttk.Label(app, text="Enter URL:")
url_label.grid(row=0, column=0, padx=padding, pady=padding, sticky="w")
url_entry = ttk.Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=padding, pady=padding, columnspan=2)

element_selector_label = ttk.Label(app, text="Element Selector:")
element_selector_label.grid(row=1, column=0, padx=padding, pady=padding, sticky="w")
element_selector_entry = ttk.Entry(app, width=30)
element_selector_entry.grid(row=1, column=1, padx=padding, pady=padding, columnspan=2)

text_chkbox = ttk.Checkbutton(app, text="Text", variable=text_var)
text_chkbox.grid(row=2, column=0, padx=padding, pady=5)
links_chkbox = ttk.Checkbutton(app, text="Links", variable=links_var)
links_chkbox.grid(row=2, column=1, padx=padding, pady=5)

scr_but = ttk.Button(app, text="Scrape", command=scrap_web)
scr_but.grid(row=3, column=0, columnspan=3, pady=(0, padding))

res_txt = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=10)
res_txt.config(state='disabled')
res_txt.grid(row=4, column=0, columnspan=3, padx=padding, pady=padding)

export_formats_frame = ttk.Frame(app)
export_formats_frame.grid(row=5, column=0, columnspan=3, pady=(0, padding))

pdf_chkbox = ttk.Checkbutton(export_formats_frame, text="PDF", variable=pdf_var)
pdf_chkbox.grid(row=0, column=0, padx=padding, pady=5)
csv_chkbox = ttk.Checkbutton(export_formats_frame, text="CSV", variable=csv_var)
csv_chkbox.grid(row=0, column=1, padx=padding, pady=5)
json_chkbox = ttk.Checkbutton(export_formats_frame, text="JSON", variable=json_var)
json_chkbox.grid(row=0, column=2, padx=padding, pady=5)

exp_but = ttk.Button(app, text="Export Results", command=export_results)
exp_but.grid(row=6, column=0, columnspan=3, pady=padding)

instrct_but = ttk.Button(app, text="Instructions", command=instructions)
instrct_but.grid(row=7, column=0, columnspan=3, pady=padding)

app.mainloop()
