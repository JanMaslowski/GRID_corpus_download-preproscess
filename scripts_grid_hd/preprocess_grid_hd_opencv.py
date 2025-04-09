import os
import shutil
import cv2

# Ustawienia
main_folder = 'gridcorpus_hd/video'
overwrite = True  # Jeśli True, to istniejące foldery zostaną usunięte i utworzone na nowo

def remove_video_dir(path):
    video_dir_path = os.path.join(path, 'video')
    
    if os.path.exists(video_dir_path) and os.path.isdir(video_dir_path):
        shutil.rmtree(video_dir_path)
        print(f'Usunięto katalog "video": {video_dir_path}')
    else:
        print(f'Katalog "video" nie istnieje w ścieżce: {path}')

# Przenoszenie plików .mpg do głównych podfolderów
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    if os.path.isdir(subfolder_path):
        for root, _, files in os.walk(subfolder_path):
            for file in files:
                if file.endswith('.mpg'):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(subfolder_path, file)

                    if source_path != destination_path:
                        shutil.move(source_path, destination_path)
                        print(f'Przeniesiono {source_path} do {destination_path}')

        remove_video_dir(subfolder_path)

print("Wszystkie pliki .mpg zostały przeniesione do odpowiednich głównych podfolderów.")

# Przetwarzanie plików .mpg
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    if os.path.isdir(subfolder_path):
        # Jeśli istnieje zagnieżdżony folder o tej samej nazwie, przenieś jego zawartość i usuń go
        nested_folder_path = os.path.join(subfolder_path, subfolder)
        if os.path.isdir(nested_folder_path):
            for file in os.listdir(nested_folder_path):
                shutil.move(os.path.join(nested_folder_path, file), subfolder_path)
            os.rmdir(nested_folder_path)
        
        # Przetwarzanie plików .mpg
        for file in os.listdir(subfolder_path):
            if file.endswith('.mpg'):
                video_path = os.path.join(subfolder_path, file)
                file_name = os.path.splitext(file)[0]
                output_folder = os.path.join(subfolder_path, file_name)

                # Jeśli folder już istnieje, zachowaj logikę zależnie od parametru overwrite
                if os.path.exists(output_folder):
                    if overwrite:
                        shutil.rmtree(output_folder)
                        print(f'Folder {output_folder} usunięty (overwrite=True).')
                    else:
                        print(f'Folder {output_folder} już istnieje, pomijam przetwarzanie pliku {file}')
                        continue

                os.makedirs(output_folder, exist_ok=True)
                
                cap = cv2.VideoCapture(video_path)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                # Próba odczytania pierwszej klatki, aby sprawdzić, czy plik nie jest uszkodzony
                ret, first_frame = cap.read()
                if not ret:
                    with open("damaged_files.txt", "a") as log_file:
                        log_file.write(f"{video_path} - nie udało się odczytać pierwszej klatki\n")
                    print(f"Plik {file} jest uszkodzony (brak pierwszej klatki). Usuwam plik.")
                    cap.release()
                    os.remove(video_path)
                    continue

                # Zapis pierwszej klatki
                frame_count = 0
                frame_filename = os.path.join(output_folder, f'frame_{frame_count:03d}.jpg')
                cv2.imwrite(frame_filename, first_frame)
                frame_count += 1

                success = True
                while success:
                    success, frame = cap.read()
                    if success:
                        frame_filename = os.path.join(output_folder, f'frame_{frame_count:03d}.jpg')
                        cv2.imwrite(frame_filename, frame)
                        frame_count += 1
                
                cap.release()
                
                # Sprawdzenie, czy odczytano wszystkie klatki (może się zdarzyć, że plik jest uszkodzony)
                if frame_count < total_frames:
                    with open("damaged_files.txt", "a") as log_file:
                        log_file.write(f"{video_path} - odczytano {frame_count} z {total_frames} klatek\n")
                    print(f"Plik {file} jest uszkodzony (odczytano {frame_count} z {total_frames} klatek). Usuwam plik oraz folder {output_folder}.")
                    shutil.rmtree(output_folder)
                    os.remove(video_path)
                else:
                    print(f'Przetworzono plik: {file}, klatki zapisane w: {output_folder}')

print("Przetwarzanie zakończone.")
