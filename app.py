import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

from threading import Thread

from ocr import (
    extract_text,
    save_as_docx,
    save_as_pdf,
    save_as_txt
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("Image OCR Converter")

app.geometry("800x600")

app.resizable(False, False)

selected_image = None


def select_image():

    global selected_image

    file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            (
                "Images",
                "*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp"
            )
        ]
    )

    if file:

        selected_image = file

        file_label.configure(
            text=f"Selected:\n{file}"
        )


def convert_worker():

    try:

        status_label.configure(
            text="Reading image..."
        )

        text = extract_text(
            selected_image
        )

        if not text.strip():

            messagebox.showwarning(
                "No Text",
                "No text found in image."
            )

            status_label.configure(
                text="No text found"
            )

            return

        preview_box.delete(
            "1.0",
            "end"
        )

        preview_box.insert(
            "1.0",
            text
        )

        output_format = format_var.get()

        if output_format == "DOCX":

            save_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[
                    (
                        "Word Document",
                        "*.docx"
                    )
                ]
            )

            if save_path:
                save_as_docx(
                    text,
                    save_path
                )

        elif output_format == "PDF":

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[
                    (
                        "PDF File",
                        "*.pdf"
                    )
                ]
            )

            if save_path:
                save_as_pdf(
                    text,
                    save_path
                )

        else:

            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    (
                        "Text File",
                        "*.txt"
                    )
                ]
            )

            if save_path:
                save_as_txt(
                    text,
                    save_path
                )

        status_label.configure(
            text="Completed ✓"
        )

        messagebox.showinfo(
            "Success",
            "Conversion completed."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        status_label.configure(
            text="Failed"
        )


def start_conversion():

    if not selected_image:

        messagebox.showwarning(
            "Select Image",
            "Please select an image."
        )

        return

    Thread(
        target=convert_worker,
        daemon=True
    ).start()


title = ctk.CTkLabel(
    app,
    text="📝 Image OCR Converter",
    font=("Arial", 30, "bold")
)

title.pack(
    pady=20
)

select_btn = ctk.CTkButton(
    app,
    text="Select Image",
    width=250,
    height=40,
    command=select_image
)

select_btn.pack(
    pady=10
)

file_label = ctk.CTkLabel(
    app,
    text="No image selected",
    wraplength=700
)

file_label.pack()

frame = ctk.CTkFrame(
    app
)

frame.pack(
    pady=15
)

ctk.CTkLabel(
    frame,
    text="Output Format:"
).pack(
    side="left",
    padx=10
)

format_var = ctk.StringVar(
    value="DOCX"
)

format_menu = ctk.CTkOptionMenu(
    frame,
    values=[
        "DOCX",
        "PDF",
        "TXT"
    ],
    variable=format_var
)

format_menu.pack(
    side="left",
    padx=10
)

convert_btn = ctk.CTkButton(
    app,
    text="Convert",
    width=250,
    height=45,
    command=start_conversion
)

convert_btn.pack(
    pady=15
)

preview_label = ctk.CTkLabel(
    app,
    text="OCR Preview"
)

preview_label.pack()

preview_box = ctk.CTkTextbox(
    app,
    width=700,
    height=250
)

preview_box.pack(
    pady=10
)

status_label = ctk.CTkLabel(
    app,
    text="Ready"
)

status_label.pack(
    pady=10
)

app.mainloop()