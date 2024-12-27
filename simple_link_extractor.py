import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import requests
import time

class LinkExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Extractor")
        self.root.geometry("600x400")
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input file selection
        ttk.Label(main_frame, text="Input HTML File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        
        # API Key input
        ttk.Label(main_frame, text="API Key:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.api_key = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.api_key, width=50).grid(row=2, column=1, pady=5)
        
        # Fetch content checkbox
        self.fetch_content = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Fetch Content", variable=self.fetch_content).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=3, pady=5)
        
        # Log area
        self.log_text = tk.Text(main_frame, height=10, width=60)
        self.log_text.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Scrollbar for log area
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=5, column=3, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Run button
        ttk.Button(main_frame, text="Run", command=self.run_extraction).grid(row=6, column=0, columnspan=3, pady=10)

    def log_message(self, message):
        """Add message to log area"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)

    def extract_links(self, html_content):
        """Extract links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href:
                links.add(href)
        return links

    def fetch_url_content(self, url):
        """Fetch content from URL using the Jina API"""
        try:
            jina_url = f'https://r.jina.ai/{url}'
            headers = {'Authorization': f'Bearer {self.api_key.get()}'}
            response = requests.get(jina_url, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return f"Error fetching URL: {str(e)}"

    def process_extraction(self):
        try:
            # Read HTML file
            self.status_var.set("Reading HTML file...")
            self.log_message("Reading HTML file...")
            with open(self.input_path.get(), 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Extract links
            self.status_var.set("Extracting links...")
            self.log_message("Extracting links...")
            links = self.extract_links(html_content)

            # Save links
            self.status_var.set("Saving links...")
            self.log_message("Saving links...")
            with open(self.output_path.get(), 'w', encoding='utf-8') as file:
                for link in sorted(links):
                    file.write(f"{link}\n")

            # Fetch content if requested
            if self.fetch_content.get():
                content_file = self.output_path.get().replace('.txt', '_content.txt')
                self.status_var.set("Fetching content...")
                self.log_message("Fetching content...")
                
                with open(content_file, 'w', encoding='utf-8') as f:
                    for i, url in enumerate(links, 1):
                        self.log_message(f"Processing URL {i}/{len(links)}: {url}")
                        divider = f"\n{'='*80}\nURL {i}: {url}\n{'='*80}\n"
                        f.write(divider)
                        content = self.fetch_url_content(url)
                        f.write(content + "\n")
                        time.sleep(1)  # Delay to avoid overwhelming the API

            self.status_var.set("Completed!")
            self.log_message("Task completed successfully!")
            messagebox.showinfo("Success", "Link extraction completed successfully!")

        except Exception as e:
            self.status_var.set("Error occurred!")
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def run_extraction(self):
        # Validate inputs
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("Error", "Please select input and output files")
            return
        
        if self.fetch_content.get() and not self.api_key.get():
            messagebox.showerror("Error", "API Key is required for content fetching")
            return

        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Run in separate thread
        thread = threading.Thread(target=self.process_extraction)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = LinkExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 