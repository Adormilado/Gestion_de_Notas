import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk


class NotesApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Notas")
        self.root.geometry("650x500")

        # Archivo para guardar las notas (Persistencia)
        self.filename = "notes_data.json"
        self.notes = []
        self.selected_index = None

        # Estilo de interfaz
        style = ttk.Style()
        style.theme_use("clam")

        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        # Panel izquierdo: Lista de notas y botones principales
        left_panel = ttk.Frame(self.root, padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        ttk.Label(
            left_panel, text="Mis Notas", font=("Helvetica", 12, "bold")
        ).pack(anchor="w")

        self.notes_listbox = tk.Listbox(
            left_panel, width=25, font=("Helvetica", 10)
        )
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.notes_listbox.bind("<<ListboxSelect>>", self.on_select_note)

        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Nueva Nota", command=self.clear_editor
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            btn_frame, text="Eliminar", command=self.delete_note
        ).pack(fill=tk.X, pady=2)

        # Panel derecho: Editor de texto
        right_panel = ttk.Frame(self.root, padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_panel, text="Título:").pack(anchor="w")
        self.title_entry = ttk.Entry(
            right_panel, font=("Helvetica", 11)
        )
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(right_panel, text="Contenido:").pack(anchor="w")
        self.content_text = tk.Text(
            right_panel, font=("Helvetica", 10), wrap=tk.WORD
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Etiqueta para mostrar fecha de creación (Bonus Feature)
        self.date_label = ttk.Label(
            right_panel,
            text="",
            font=("Helvetica", 8, "italic"),
            foreground="gray",
        )
        self.date_label.pack(anchor="w", pady=(0, 5))

        ttk.Button(
            right_panel, text="Guardar / Actualizar", command=self.save_note
        ).pack(anchor="e")

    # --- Persistencia de Datos ---
    def load_notes(self):
        """Carga las notas guardadas en el archivo JSON."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.notes = json.load(file)
                    self.refresh_listbox()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudieron cargar las notas: {e}"
                )

    def save_to_disk(self):
        """Guarda la lista actual de notas en el archivo JSON."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.notes, file, ensure_ascii=False, indent=4)

    # --- Operaciones CRUD ---
    def refresh_listbox(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes:
            self.notes_listbox.insert(tk.END, note["title"])

    def clear_editor(self):
        self.selected_index = None
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.date_label.config(text="")
        self.notes_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showwarning("Atención", "La nota debe tener un título.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Editar nota existente
        if self.selected_index is not None:
            self.notes[self.selected_index]["title"] = title
            self.notes[self.selected_index]["content"] = content
        # Crear nueva nota
        else:
            new_note = {"title": title, "content": content, "created_at": now}
            self.notes.append(new_note)

        self.save_to_disk()
        self.refresh_listbox()
        self.clear_editor()

    def on_select_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            note = self.notes[self.selected_index]

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note["title"])

            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", note["content"])

            created_at = note.get("created_at", "Fecha no disponible")
            self.date_label.config(text=f"Creado el: {created_at}")

    def delete_note(self):
        if self.selected_index is not None:
            confirm = messagebox.askyesno(
                "Confirmar", "¿Seguro que deseas eliminar esta nota?"
            )
            if confirm:
                del self.notes[self.selected_index]
                self.save_to_disk()
                self.refresh_listbox()
                self.clear_editor()
        else:
            messagebox.showwarning(
                "Atención", "Selecciona una nota para eliminar."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()