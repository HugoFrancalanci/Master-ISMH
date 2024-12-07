import os
import glob
import kineticstoolkit.lab as ktk

def reconstruct_c3d(input_dir, output_dir, clusters_info):
    # Obtenir la liste de tous les fichiers c3d dans le dossier d'origine
    input_files = glob.glob(os.path.join(input_dir, "*.c3d"))

    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Traiter chaque fichier c3d
    for input_file in input_files:
        try:
            # Charger les données
            original_markers = ktk.read_c3d(input_file)["Points"]
            markers = original_markers.copy()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {input_file}: {e}")
            continue

        # Créer un dictionnaire pour stocker les clusters
        clusters = {}

        # Créer un cluster pour chaque ensemble de marqueurs
        for cluster_name, marker_names in clusters_info.items():
            try:
                # Sélectionner les marqueurs d'intérêt
                cluster_markers = markers.get_subset(marker_names)

                # Vérifier que les marqueurs existent
                if not all(marker in markers.data for marker in marker_names):
                    print(f"Le cluster {cluster_name} n'a pas de marqueurs valides dans {input_file}.")
                    continue

                # Créer un cluster de marqueurs
                cluster = ktk.kinematics.create_cluster(cluster_markers, marker_names)

                # Ajouter le cluster au dictionnaire
                clusters[cluster_name] = cluster
            except Exception as e:
                print(f"Erreur lors de la création du cluster {cluster_name}: {e}")
                continue

        # Reconstituer les marqueurs manquants pour chaque cluster
        for cluster_name, cluster in clusters.items():
            try:
                reconstructed_markers = ktk.kinematics.track_cluster(markers, cluster)

                # Mettre à jour les marqueurs avec les marqueurs reconstruits
                for marker_name in clusters_info[cluster_name]:
                    markers.data[marker_name] = reconstructed_markers.data[marker_name]
            except Exception as e:
                print(f"Erreur lors de la reconstruction du cluster {cluster_name}: {e}")
                continue

        # Créer le nom du nouveau fichier
        base_name, ext = os.path.splitext(os.path.basename(input_file))
        new_file_path = os.path.join(output_dir, base_name + "_reconstructed" + ext)

        try:
            # Enregistrer les marqueurs reconstruits dans le nouveau fichier
            ktk.write_c3d(new_file_path, markers)
            print(f"Les marqueurs reconstruits de {input_file} ont été enregistrés.")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier {new_file_path}: {e}")

# Définir les marqueurs pour chaque cluster
clusters_info = {
    "Tronc": ["C7", "XYP", "MAN", "EPSD", "EPSG", "EASG", "EASD", "ACD", "ACG"],
    "Haut_Bras_D": ["ACD", "CLD", "CMD", "MTBD"],
    "Haut_Bras_G": ["ACG", "CLG", "CMG", "MTBG"],
    "Bas_bras_D": ["CLD", "CMD", "MTABG", "PSRD", "PSUD"],
    "Bas_bras_G": ["CLG", "CMG", "MTABG", "PSRG", "PSUG"],
    "Haut_Jambe_D": ["GLD", "GMD", "EASD"],
    "Haut_Jambe_G": ["GLG", "GMG", "EASG"],
    "Bas_Jambe_D": ["GLD", "GMD", "TIBD", "MMD", "MLD"],
    "Bas_Jambe_G": ["GLG", "GMG", "TIBG", "MMG", "MLG"],
    "Pied_D": ["MLD", "MMD", "CALD", "MT5D"],
    "Pied_G": ["MLG", "MMG", "CALG", "MT5G"],
    "Main_D": ["PSRD", "PSUD", "MC2D", "MC5D"],
    "Main_G": ["PSRG", "PSUG", "MC2G", "MC5G"],
}

input_dir = r"D:\QUALISYS\final"
output_dir = r"D:\QUALISYS\FINAL_re"
reconstruct_c3d(input_dir, output_dir, clusters_info)
