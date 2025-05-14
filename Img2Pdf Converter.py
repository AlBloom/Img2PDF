import tkinter as tk
from tkinter import filedialog, ttk
from reportlab.pdfgen import canvas
from PIL import Image
import os 

class Img_to_pdf_Coverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.status_label = tk.Label(root, text="", fg="gray")

        self.initialize_ui()

    def initialize_ui(self):
        title_lable = tk.Label(self.root, text="Image to PDF Convreter", font=("Helvetica", 16, "bold"))
        title_lable.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0,10))

        self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)

        lable = tk.Label(self.root, text="Enter PDF name: ")
        lable.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        self.progress_bar.pack(pady=10)
        self.status_label.pack()

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_to_pdf)
        convert_button.pack(pady=(20,40))
    
    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)

        for image_path in self.image_paths:
            _, image_path = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_path)

    def convert_to_pdf(self):
        if not self.image_paths:
            return

        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    
        # Create output path
        pdf_name = self.output_pdf_name.get() or 'output'
        output_pdf_path = os.path.join(desktop_path, f"{pdf_name}.pdf")

        total_images = len(self.image_paths)
        self.progress_bar['value'] = 0
        self.status_label.config(text="Starting conversion...")
        self.root.update_idletasks()

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for index, images_path in enumerate(self.image_paths):

            img = Image.open(images_path)
            available_width = 548
            available_height = 720
            scale_factor = min(available_width /  img.width, available_height / img.height)           
            
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width)/2
            y_centered = (792 - new_height)/2

            pdf.setFillColorRGB(255,255,255)
            pdf.rect(0,0,612,792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        progress = (index + 1) / total_images * 100
        self.progress_bar['value'] = progress
        self.status_label.config(text=f"Processing image {index + 1} of {total_images}")
        self.root.update_idletasks()
        
        pdf.save()

        self.progress_bar['value'] = 100
        self.status_label.config(text="Conversion complete!")
        self.root.after(2000, lambda: self.status_label.config(text=""))

def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = Img_to_pdf_Coverter(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()