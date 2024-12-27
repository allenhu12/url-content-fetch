import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from link_extractor import read_html_file, extract_links, save_links, process_links_file
import logging

class LinkExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Extractor")
        self.root.geometry("600x400")
        
        # Create main frame
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
        
        # Progress
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=4, column=0, columnspan=3, pady=10)
        
        # Log area
        self.log_text = tk.Text(main_frame, height=10, width=60)
        self.log_text.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Run button
        ttk.Button(main_frame, text="Run", command=self.run_extraction).grid(row=6, column=0, columnspan=3, pady=10)
        
        # Configure logging
        self.setup_logging()

    def setup_logging(self):
        """Configure logging to both file and GUI"""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)

        # Clear existing handlers
        logging.getLogger().handlers = []
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Add text handler
        text_handler = TextHandler(self.log_text)
        logging.getLogger().addHandler(text_handler)

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

    def run_extraction(self):
        # Validate inputs
        if not self.input_path.get() or not self.output_path.get() or not self.api_key.get():
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.process_extraction)
        thread.daemon = True
        thread.start()

    def process_extraction(self):
        try:
            self.progress_var.set("Reading HTML file...")
            html_content = read_html_file(self.input_path.get())
            
            self.progress_var.set("Extracting links...")
            links = extract_links(html_content)
            
            self.progress_var.set("Saving links...")
            save_links(links, self.output_path.get())
            
            if self.fetch_content.get():
                self.progress_var.set("Fetching content...")
                fetched_content_file = self.output_path.get().replace('.txt', '_content.txt')
                process_links_file(self.output_path.get(), fetched_content_file, self.api_key.get())
            
            self.progress_var.set("Completed!")
            messagebox.showinfo("Success", "Link extraction completed successfully!")
            
        except Exception as e:
            self.progress_var.set("Error occurred!")
            messagebox.showerror("Error", str(e))
            logging.error(f"Error: {e}")

def main():
    root = tk.Tk()
    app = LinkExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 