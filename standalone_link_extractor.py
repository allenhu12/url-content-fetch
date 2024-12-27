import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import requests
import time
import sys
import os

class LinkExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Extractor")
        self.root.geometry("600x500")
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input HTML file selection
        ttk.Label(main_frame, text="Input HTML File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        # URL file selection with Load and Save options
        ttk.Label(main_frame, text="URL File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_file_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.url_file_path, width=50).grid(row=1, column=1, pady=5)
        
        # URL file buttons frame
        url_buttons_frame = ttk.Frame(main_frame)
        url_buttons_frame.grid(row=1, column=2, padx=5)
        ttk.Button(url_buttons_frame, text="Load", command=self.load_url_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(url_buttons_frame, text="Save As", command=self.save_url_file).pack(side=tk.LEFT, padx=2)
        
        # Content file selection
        ttk.Label(main_frame, text="Content File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.content_file_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.content_file_path, width=50).grid(row=2, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_content_file).grid(row=2, column=2, padx=5, pady=5)
        
        # API Key input
        ttk.Label(main_frame, text="API Key:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.api_key = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.api_key, width=50).grid(row=3, column=1, pady=5)
        
        # Operation selection
        ttk.Label(main_frame, text="Operations:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.extract_urls = tk.BooleanVar(value=True)
        self.fetch_content = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Extract URLs", variable=self.extract_urls).grid(row=4, column=1, sticky=tk.W)
        ttk.Checkbutton(main_frame, text="Fetch Content", variable=self.fetch_content).grid(row=4, column=1, sticky=tk.E)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=3, pady=5)
        
        # Log area
        self.log_text = tk.Text(main_frame, height=12, width=60)
        self.log_text.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Scrollbar for log area
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=6, column=3, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Run button
        ttk.Button(main_frame, text="Run", command=self.run_extraction).grid(row=7, column=0, columnspan=3, pady=10)

        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

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
            # Suggest URL file name
            suggested_url_file = os.path.splitext(filename)[0] + "_urls.txt"
            self.url_file_path.set(suggested_url_file)
            # Suggest content file name
            suggested_content_file = os.path.splitext(filename)[0] + "_content.txt"
            self.content_file_path.set(suggested_content_file)

    def load_url_file(self):
        """Load existing URL file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Load URL File"
        )
        if filename:
            self.url_file_path.set(filename)
            # Suggest content file name based on URL file
            suggested_content_file = os.path.splitext(filename)[0] + "_content.txt"
            self.content_file_path.set(suggested_content_file)
            # Set fetch content as default operation when loading URL file
            self.extract_urls.set(False)
            self.fetch_content.set(True)
            self.log_message(f"Loaded URL file: {filename}")
            
            # Preview URLs
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    urls = [line.strip() for line in file if line.strip()]
                    self.log_message(f"Found {len(urls)} URLs in file")
                    if urls:
                        self.log_message("First few URLs:")
                        for url in urls[:3]:  # Show first 3 URLs
                            self.log_message(f"- {url}")
                        if len(urls) > 3:
                            self.log_message("...")
            except Exception as e:
                self.log_message(f"Error reading URL file: {e}")

    def save_url_file(self):
        """Save URL file with new location"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save URL File As"
        )
        if filename:
            self.url_file_path.set(filename)

    def browse_content_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.content_file_path.set(filename)

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
            # Extract URLs if selected
            if self.extract_urls.get():
                if not self.input_path.get():
                    raise ValueError("Input HTML file is required for URL extraction")
                if not self.url_file_path.get():
                    raise ValueError("Please specify a path to save the extracted URLs")
                
                self.status_var.set("Reading HTML file...")
                self.log_message("Reading HTML file...")
                with open(self.input_path.get(), 'r', encoding='utf-8') as file:
                    html_content = file.read()

                self.status_var.set("Extracting links...")
                self.log_message("Extracting links...")
                links = self.extract_links(html_content)

                self.status_var.set("Saving links...")
                self.log_message("Saving links...")
                with open(self.url_file_path.get(), 'w', encoding='utf-8') as file:
                    for link in sorted(links):
                        file.write(f"{link}\n")
                self.log_message(f"Saved {len(links)} URLs to {self.url_file_path.get()}")

            # Fetch content if selected
            if self.fetch_content.get():
                if not self.url_file_path.get():
                    raise ValueError("Please select a URL file for content fetching")
                if not self.content_file_path.get():
                    raise ValueError("Please specify where to save the fetched content")
                if not self.api_key.get():
                    raise ValueError("API Key is required for content fetching")
                if not os.path.exists(self.url_file_path.get()):
                    raise ValueError("URL file does not exist. Please load a valid URL file.")

                self.status_var.set("Reading URLs...")
                self.log_message("Reading URLs from file...")
                
                # Read URLs from file
                with open(self.url_file_path.get(), 'r', encoding='utf-8') as file:
                    urls = [line.strip() for line in file if line.strip()]
                
                if not urls:
                    raise ValueError("No URLs found in the URL file")
                
                self.status_var.set("Fetching content...")
                self.log_message("Fetching content...")
                
                with open(self.content_file_path.get(), 'w', encoding='utf-8') as f:
                    for i, url in enumerate(urls, 1):
                        self.log_message(f"Processing URL {i}/{len(urls)}: {url}")
                        divider = f"\n{'='*80}\nURL {i}: {url}\n{'='*80}\n"
                        f.write(divider)
                        content = self.fetch_url_content(url)
                        f.write(content + "\n")
                        time.sleep(1)  # Delay to avoid overwhelming the API
                
                self.log_message(f"Saved content to {self.content_file_path.get()}")

            self.status_var.set("Completed!")
            self.log_message("Task completed successfully!")
            messagebox.showinfo("Success", "Operations completed successfully!")

        except Exception as e:
            self.status_var.set("Error occurred!")
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def run_extraction(self):
        # Validate operations based on selected mode
        if self.extract_urls.get() and not self.input_path.get():
            messagebox.showerror("Error", "Please select an input HTML file for URL extraction")
            return
            
        if self.fetch_content.get() and not self.url_file_path.get():
            messagebox.showerror("Error", "Please select a URL file for content fetching")
            return
            
        if not self.extract_urls.get() and not self.fetch_content.get():
            messagebox.showerror("Error", "Please select at least one operation (Extract URLs or Fetch Content)")
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