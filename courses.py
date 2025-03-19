import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from tkinter.font import Font

class GestionnaireCoursesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Courses")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        self.courses = []
        self.charger_courses()

        # Polices
        self.title_font = Font(family="Helvetica", size=16, weight="bold")
        self.label_font = Font(family="Helvetica", size=12)
        self.button_font = Font(family="Helvetica", size=10, weight="bold")

        # Titre
        self.title_label = tk.Label(root, text="Gestionnaire de Courses", font=self.title_font, bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        # Liste de courses
        self.list_frame = tk.Frame(root, bg="#f0f0f0")
        self.list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.list_frame, width=60, height=10, font=self.label_font, bg="#fff", fg="#333", selectbackground="#0078d7")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Formulaire pour ajouter/modifier un article
        self.form_frame = tk.Frame(root, bg="#f0f0f0")
        self.form_frame.pack(pady=10, padx=20, fill=tk.X)

        self.entry_nom = tk.Entry(self.form_frame, font=self.label_font, width=20, bg="#fff", fg="#333")
        self.entry_nom.grid(row=0, column=0, padx=5, pady=5)

        self.entry_quantite = tk.Entry(self.form_frame, font=self.label_font, width=5, bg="#fff", fg="#333")
        self.entry_quantite.grid(row=0, column=1, padx=5, pady=5)

        self.categories = ["Fruits", "Légumes", "Produits laitiers", "Viandes", "Boissons", "Divers"]
        self.combo_categorie = ttk.Combobox(self.form_frame, values=self.categories, font=self.label_font, state="readonly")
        self.combo_categorie.grid(row=0, column=2, padx=5, pady=5)
        self.combo_categorie.set("Fruits")

        self.important_var = tk.BooleanVar()
        self.check_important = tk.Checkbutton(self.form_frame, text="Important", variable=self.important_var, font=self.label_font, bg="#f0f0f0")
        self.check_important.grid(row=0, column=3, padx=5, pady=5)

        # Boutons
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=10, padx=20, fill=tk.X)

        self.add_button = tk.Button(self.button_frame, text="➕ Ajouter", command=self.ajouter_article, font=self.button_font, bg="#0078d7", fg="#fff")
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = tk.Button(self.button_frame, text="✏️ Modifier", command=self.modifier_article, font=self.button_font, bg="#ff9800", fg="#fff")
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="🗑️ Supprimer", command=self.supprimer_article, font=self.button_font, bg="#f44336", fg="#fff")
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        self.mark_button = tk.Button(self.button_frame, text="✅ Acheté", command=self.marquer_achete, font=self.button_font, bg="#4caf50", fg="#fff")
        self.mark_button.grid(row=0, column=3, padx=5, pady=5)

        self.export_button = tk.Button(self.button_frame, text="📤 Exporter", command=self.exporter_liste, font=self.button_font, bg="#9c27b0", fg="#fff")
        self.export_button.grid(row=0, column=4, padx=5, pady=5)

        # Filtres
        self.filter_frame = tk.Frame(root, bg="#f0f0f0")
        self.filter_frame.pack(pady=10, padx=20, fill=tk.X)

        self.filter_categorie = ttk.Combobox(self.filter_frame, values=["Toutes"] + self.categories, font=self.label_font, state="readonly")
        self.filter_categorie.grid(row=0, column=0, padx=5, pady=5)
        self.filter_categorie.set("Toutes")

        self.filter_statut = ttk.Combobox(self.filter_frame, values=["Tous", "Achetés", "Non achetés"], font=self.label_font, state="readonly")
        self.filter_statut.grid(row=0, column=1, padx=5, pady=5)
        self.filter_statut.set("Tous")

        self.filter_button = tk.Button(self.filter_frame, text="🔍 Filtrer", command=self.afficher_courses, font=self.button_font, bg="#607d8b", fg="#fff")
        self.filter_button.grid(row=0, column=2, padx=5, pady=5)

        self.afficher_courses()
        self.verifier_articles_importants()

    def ajouter_article(self):
        nom = self.entry_nom.get()
        quantite = self.entry_quantite.get()
        categorie = self.combo_categorie.get()
        important = self.important_var.get()

        if nom:
            quantite = int(quantite) if quantite.isdigit() else 1
            self.courses.append({
                "nom": nom,
                "quantite": quantite,
                "categorie": categorie,
                "achete": False,
                "important": important
            })
            self.sauvegarder_courses()
            self.afficher_courses()
            self.entry_nom.delete(0, tk.END)
            self.entry_quantite.delete(0, tk.END)
            self.important_var.set(False)
        else:
            messagebox.showwarning("Attention", "Veuillez entrer un nom d'article.")

    def modifier_article(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            nom = self.entry_nom.get()
            quantite = self.entry_quantite.get()
            categorie = self.combo_categorie.get()
            important = self.important_var.get()

            if nom:
                quantite = int(quantite) if quantite.isdigit() else 1
                self.courses[index] = {
                    "nom": nom,
                    "quantite": quantite,
                    "categorie": categorie,
                    "achete": self.courses[index]["achete"],
                    "important": important
                }
                self.sauvegarder_courses()
                self.afficher_courses()
                self.entry_nom.delete(0, tk.END)
                self.entry_quantite.delete(0, tk.END)
                self.important_var.set(False)
            else:
                messagebox.showwarning("Attention", "Veuillez entrer un nom d'article.")
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article.")

    def supprimer_article(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            del self.courses[index]
            self.sauvegarder_courses()
            self.afficher_courses()
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article.")

    def marquer_achete(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.courses[index]["achete"] = True
            self.sauvegarder_courses()
            self.afficher_courses()
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article.")

    def afficher_courses(self):
        self.listbox.delete(0, tk.END)
        categorie_filtre = self.filter_categorie.get()
        statut_filtre = self.filter_statut.get()

        for article in self.courses:
            # Filtre par catégorie
            if categorie_filtre != "Toutes" and article["categorie"] != categorie_filtre:
                continue
            # Filtre par statut
            if statut_filtre == "Achetés" and not article["achete"]:
                continue
            if statut_filtre == "Non achetés" and article["achete"]:
                continue

            statut = "✓" if article["achete"] else "✗"
            important = "⭐" if article["important"] else ""
            self.listbox.insert(tk.END, f"[{statut}] {important} {article['nom']} ({article['quantite']}) - {article['categorie']}")

    def exporter_liste(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for article in self.courses:
                    statut = "Acheté" if article["achete"] else "Non acheté"
                    important = " (Important)" if article["important"] else ""
                    f.write(f"{article['nom']} ({article['quantite']}) - {article['categorie']} - {statut}{important}\n")
            messagebox.showinfo("Succès", "La liste de courses a été exportée avec succès.")

    def verifier_articles_importants(self):
        articles_importants_non_achetes = [article for article in self.courses if article["important"] and not article["achete"]]
        if articles_importants_non_achetes:
            messagebox.showwarning("Articles importants", "Attention, certains articles importants ne sont pas encore achetés !")

    def sauvegarder_courses(self):
        with open("courses.json", "w") as f:
            json.dump(self.courses, f)

    def charger_courses(self):
        try:
            with open("courses.json", "r") as f:
                self.courses = json.load(f)
        except FileNotFoundError:
            self.courses = []

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireCoursesApp(root)
    root.mainloop()