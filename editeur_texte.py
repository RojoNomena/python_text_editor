"""
Éditeur de Texte Simple en Python avec Tkinter
Ce programme implémente un éditeur de texte basique avec les fonctionnalités essentielles :
- Création/ouverture/enregistrement de fichiers
- Opérations d'édition de base (copier/coller/annuler)
- Raccourcis clavier
"""

# Importation des modules nécessaires
import tkinter as tk  # Pour l'interface graphique
from tkinter import filedialog  # Pour les dialogues d'ouverture/enregistrement
from tkinter import messagebox  # Pour les boîtes de message


class EditeurTexte:
    def __init__(self, root):
        """
        Initialise l'éditeur de texte avec la fenêtre principale
        :param root: La fenêtre principale Tkinter
        """
        self.root = root
        # Configuration de la fenêtre principale
        self.root.title("Éditeur de Texte Simple")  # Titre de la fenêtre
        self.root.geometry("800x600")  # Taille par défaut (largeur x hauteur)

        # ========== CRÉATION DU MENU PRINCIPAL ==========
        self.menu_bar = tk.Menu(root)  # Barre de menu principale

        # ------ Menu Fichier ------
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)  # tearoff=0 empêche le détachement
        # Ajout des commandes avec raccourcis clavier
        self.file_menu.add_command(
            label="Nouveau",
            command=self.nouveau_fichier,
            accelerator="Ctrl+N"  # Affiche le raccourci dans le menu
        )
        self.file_menu.add_command(
            label="Ouvrir",
            command=self.ouvrir_fichier,
            accelerator="Ctrl+O"
        )
        self.file_menu.add_command(
            label="Enregistrer",
            command=self.enregistrer_fichier,
            accelerator="Ctrl+S"
        )
        self.file_menu.add_separator()  # Ligne de séparation
        self.file_menu.add_command(label="Quitter", command=self.quitter)
        # Ajout du menu Fichier à la barre de menu
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)

        # ------ Menu Édition ------
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        # Commandes d'édition avec raccourcis
        self.edit_menu.add_command(
            label="Annuler",
            command=self.annuler,
            accelerator="Ctrl+Z"
        )
        self.edit_menu.add_command(
            label="Rétablir",
            command=self.retablir,
            accelerator="Ctrl+Y"
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Couper",
            command=self.couper,
            accelerator="Ctrl+X"
        )
        self.edit_menu.add_command(
            label="Copier",
            command=self.copier,
            accelerator="Ctrl+C"
        )
        self.edit_menu.add_command(
            label="Coller",
            command=self.coller,
            accelerator="Ctrl+V"
        )
        # Ajout du menu Édition à la barre de menu
        self.menu_bar.add_cascade(label="Édition", menu=self.edit_menu)

        # Configuration de la barre de menu dans la fenêtre
        root.config(menu=self.menu_bar)

        # ========== ZONE DE TEXTE PRINCIPALE ==========
        # Barre de défilement verticale
        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Position à droite

        # Widget Text principal pour l'édition
        self.zone_texte = tk.Text(
            root,
            yscrollcommand=self.scrollbar.set,  # Lie à la scrollbar
            wrap=tk.WORD,  # Retour à la ligne par mots entiers
            undo=True,  # Active la fonctionnalité d'annulation
            autoseparators=True,  # Séparateurs automatiques pour undo
            maxundo=-1  # Nombre illimité d'annulations
        )
        # Placement qui remplit tout l'espace disponible
        self.zone_texte.pack(expand=True, fill=tk.BOTH)
        # Configuration de la scrollbar pour contrôler la zone de texte
        self.scrollbar.config(command=self.zone_texte.yview)

        # ========== CONFIGURATION DES RACCOURCIS CLAVIER ==========
        # Lie les combinaisons de touches aux méthodes correspondantes
        self.zone_texte.bind("<Control-n>", lambda event: self.nouveau_fichier())
        self.zone_texte.bind("<Control-o>", lambda event: self.ouvrir_fichier())
        self.zone_texte.bind("<Control-s>", lambda event: self.enregistrer_fichier())
        self.zone_texte.bind("<Control-z>", lambda event: self.annuler())
        self.zone_texte.bind("<Control-y>", lambda event: self.retablir())
        self.zone_texte.bind("<Control-x>", lambda event: self.couper())
        self.zone_texte.bind("<Control-c>", lambda event: self.copier())
        self.zone_texte.bind("<Control-v>", lambda event: self.coller())

        # Variable pour suivre le fichier actuellement ouvert
        self.fichier_courant = None

    # ========== MÉTHODES DE GESTION DES FICHIERS ==========

    def nouveau_fichier(self):
        """Crée un nouveau document vide en effaçant le contenu actuel"""
        self.zone_texte.delete(1.0, tk.END)  # Efface du début (ligne 1, colonne 0) à la fin
        self.fichier_courant = None  # Réinitialise le fichier courant

    def ouvrir_fichier(self):
        """
        Ouvre un fichier existant via un dialogue et charge son contenu
        dans la zone de texte
        """
        # Ouvre le dialogue de sélection de fichier
        fichier = filedialog.askopenfilename(
            defaultextension=".txt",  # Extension par défaut
            filetypes=[
                ("Fichiers texte", "*.txt"),  # Filtre pour les fichiers texte
                ("Tous les fichiers", "*.*")  # Option pour tous les fichiers
            ]
        )

        if fichier:  # Si un fichier a été sélectionné (pas d'annulation)
            try:
                # Ouverture en mode lecture
                with open(fichier, "r", encoding='utf-8') as f:
                    contenu = f.read()  # Lecture du contenu

                # Remplacement du contenu actuel
                self.zone_texte.delete(1.0, tk.END)
                self.zone_texte.insert(1.0, contenu)
                self.fichier_courant = fichier  # Mémorise le fichier ouvert
            except Exception as e:
                # Affichage d'une erreur en cas de problème
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'ouvrir le fichier:\n{str(e)}"
                )

    def enregistrer_fichier(self):
        """
        Enregistre le contenu dans le fichier courant.
        Si aucun fichier n'est ouvert, appelle enregistrer_sous()
        """
        if self.fichier_courant:  # Si un fichier est déjà ouvert
            try:
                # Ouverture en mode écriture
                with open(self.fichier_courant, "w", encoding='utf-8') as f:
                    # Écrit tout le contenu (de 1.0 = début à END = fin)
                    f.write(self.zone_texte.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'enregistrer le fichier:\n{str(e)}"
                )
        else:  # Si nouveau fichier non encore enregistré
            self.enregistrer_sous()  # Ouvre le dialogue "Enregistrer sous"

    def enregistrer_sous(self):
        """
        Ouvre un dialogue pour enregistrer sous un nouveau nom
        :return: True si l'enregistrement a réussi, False sinon
        """
        # Ouvre le dialogue de sauvegarde
        fichier = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Fichiers texte", "*.txt"),
                ("Tous les fichiers", "*.*")
            ]
        )

        if fichier:  # Si un emplacement a été choisi
            try:
                with open(fichier, "w", encoding='utf-8') as f:
                    f.write(self.zone_texte.get(1.0, tk.END))
                self.fichier_courant = fichier  # Mémorise le nouveau fichier
                return True
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'enregistrer le fichier:\n{str(e)}"
                )
                return False
        return False  # Si l'utilisateur a annulé

    def quitter(self):
        """Demande confirmation avant de quitter l'application"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            self.root.destroy()  # Ferme la fenêtre principale

    # ========== MÉTHODES D'ÉDITION ==========

    def annuler(self):
        """Annule la dernière action dans la zone de texte"""
        try:
            self.zone_texte.edit_undo()  # Utilise le système undo intégré à Tkinter
        except:
            pass  # Ignore les erreurs (par exemple si rien à annuler)

    def retablir(self):
        """Rétablit la dernière action annulée"""
        try:
            self.zone_texte.edit_redo()  # Utilise le système redo intégré
        except:
            pass  # Ignore les erreurs

    def couper(self):
        """Coupe le texte sélectionné dans le presse-papier"""
        self.zone_texte.event_generate("<<Cut>>")  # Génère l'événement de coupe

    def copier(self):
        """Copie le texte sélectionné dans le presse-papier"""
        self.zone_texte.event_generate("<<Copy>>")  # Génère l'événement de copie

    def coller(self):
        """Colle le texte du presse-papier à la position du curseur"""
        self.zone_texte.event_generate("<<Paste>>")  # Génère l'événement de collage


# Point d'entrée principal du programme
if __name__ == "__main__":
    root = tk.Tk()  # Crée la fenêtre principale
    editeur = EditeurTexte(root)  # Crée l'instance de l'éditeur
    root.mainloop()  # Lance la boucle principale de l'interface