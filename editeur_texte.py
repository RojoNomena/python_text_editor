import tkinter as tk
from tkinter import (
    filedialog,
    messagebox,
    simpledialog,
    colorchooser
)


class EditeurTexte:
    def __init__(self, root):
        self.root = root
        self.root.title("Éditeur de Texte Avancé")
        self.root.geometry("900x600")

        self.fichier_courant = None
        self.taille_police = 12
        self.mode_sombre_actif = False
        self.couleur_police = "black"

        #création des menus
        self.menu_bar = tk.Menu(root)

        #menu fichier
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Nouveau", command=self.nouveau_fichier, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Ouvrir", command=self.ouvrir_fichier, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Enregistrer", command=self.enregistrer_fichier, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Enregistrer sous", command=self.enregistrer_sous)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.quitter)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)

        #menu édition
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Annuler", command=self.annuler, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Rétablir", command=self.retablir, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Couper", command=self.couper, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copier", command=self.copier, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Coller", command=self.coller, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Rechercher", command=self.rechercher, accelerator="Ctrl+F")
        self.menu_bar.add_cascade(label="Édition", menu=self.edit_menu)

        #menu affichage
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Changer taille de police", command=self.changer_police)
        self.view_menu.add_command(label="Changer couleur de police", command=self.changer_couleur_police)
        self.view_menu.add_command(label="Mode sombre", command=self.mode_sombre)
        self.menu_bar.add_cascade(label="Affichage", menu=self.view_menu)

        root.config(menu=self.menu_bar)

        #zone de texte
        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.zone_texte = tk.Text(
            root,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", self.taille_police),
            fg=self.couleur_police,
            yscrollcommand=self.scrollbar.set
        )
        self.zone_texte.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.zone_texte.yview)

        #barre d'état
        self.status_bar = tk.Label(root, text="Ligne 1, Colonne 1", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        #raccourci
        self.zone_texte.bind("<Control-n>", lambda e: self.nouveau_fichier())
        self.zone_texte.bind("<Control-o>", lambda e: self.ouvrir_fichier())
        self.zone_texte.bind("<Control-s>", lambda e: self.enregistrer_fichier())
        self.zone_texte.bind("<Control-f>", lambda e: self.rechercher())
        self.zone_texte.bind("<KeyRelease>", self.mettre_a_jour_status)
        self.zone_texte.bind("<ButtonRelease>", self.mettre_a_jour_status)
        self.zone_texte.bind("<<Modified>>", self.fichier_modifie)

    #fichiers
    def nouveau_fichier(self):
        self.zone_texte.delete(1.0, tk.END)
        self.fichier_courant = None
        self.root.title("Éditeur de Texte Avancé")

    def ouvrir_fichier(self):
        fichier = filedialog.askopenfilename(
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if fichier:
            with open(fichier, "r", encoding="utf-8") as f:
                self.zone_texte.delete(1.0, tk.END)
                self.zone_texte.insert(1.0, f.read())
            self.fichier_courant = fichier
            self.root.title(f"Éditeur de Texte - {fichier}")

    def enregistrer_fichier(self):
        if self.fichier_courant:
            with open(self.fichier_courant, "w", encoding="utf-8") as f:
                f.write(self.zone_texte.get(1.0, tk.END))
        else:
            self.enregistrer_sous()

    def enregistrer_sous(self):
        fichier = filedialog.asksaveasfilename(defaultextension=".txt")
        if fichier:
            with open(fichier, "w", encoding="utf-8") as f:
                f.write(self.zone_texte.get(1.0, tk.END))
            self.fichier_courant = fichier
            self.root.title(f"Éditeur de Texte - {fichier}")

    def quitter(self):
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            self.root.destroy()

    #édition
    def annuler(self):
        try:
            self.zone_texte.edit_undo()
        except:
            pass

    def retablir(self):
        try:
            self.zone_texte.edit_redo()
        except:
            pass

    def couper(self):
        self.zone_texte.event_generate("<<Cut>>")

    def copier(self):
        self.zone_texte.event_generate("<<Copy>>")

    def coller(self):
        self.zone_texte.event_generate("<<Paste>>")

    #outils
    def rechercher(self):
        mot = simpledialog.askstring("Rechercher", "Mot à chercher :")
        if not mot:
            return

        self.zone_texte.tag_remove("highlight", "1.0", tk.END)
        index = "1.0"

        while True:
            index = self.zone_texte.search(mot, index, tk.END)
            if not index:
                break
            fin = f"{index}+{len(mot)}c"
            self.zone_texte.tag_add("highlight", index, fin)
            index = fin

        self.zone_texte.tag_config("highlight", background="yellow")

    def changer_police(self):
        taille = simpledialog.askinteger(
            "Police",
            "Taille de police :",
            minvalue=8,
            maxvalue=40
        )
        if taille:
            self.taille_police = taille
            self.zone_texte.config(font=("Consolas", self.taille_police))

    def changer_couleur_police(self):
        couleur = colorchooser.askcolor(title="Choisir la couleur du texte")
        if couleur[1]:
            self.couleur_police = couleur[1]
            self.zone_texte.config(fg=self.couleur_police)

    def mode_sombre(self):
        if not self.mode_sombre_actif:
            self.zone_texte.config(
                bg="#1e1e1e",
                fg=self.couleur_police,
                insertbackground="white"
            )
            self.mode_sombre_actif = True
        else:
            self.zone_texte.config(
                bg="white",
                fg=self.couleur_police,
                insertbackground="black"
            )
            self.mode_sombre_actif = False

    #barre d'état
    def mettre_a_jour_status(self, event=None):
        ligne, colonne = self.zone_texte.index(tk.INSERT).split(".")
        self.status_bar.config(
            text=f"Ligne {ligne}, Colonne {int(colonne)+1}"
        )

    def fichier_modifie(self, event=None):
        self.zone_texte.edit_modified(False)
        titre = "Éditeur de Texte"
        if self.fichier_courant:
            titre += f" - {self.fichier_courant}"
        self.root.title(titre + " *")


    #lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = EditeurTexte(root)
    root.mainloop()
