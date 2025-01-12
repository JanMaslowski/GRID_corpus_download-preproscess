import os
import zipfile
import subprocess
import tarfile

os.makedirs("gridcorpus_hd/raw/audio", exist_ok=True)
os.makedirs("gridcorpus_hd/raw/video", exist_ok=True)
os.makedirs("gridcorpus_hd/audio", exist_ok=True)
os.makedirs("gridcorpus_hd/video", exist_ok=True)

start_speaker = int(input("Enter the starting speaker number: "))
end_speaker = int(input("Enter the ending speaker number: "))
extract_files = input("Do you want to extract files after downloading? (y/n): ")

for i in range(start_speaker, end_speaker + 1):

    if i == 21:
        print(f"\n\n------------------------- Skipping {i}th speaker -------------------------\n\n")
        continue
    print(f"\n\n------------------------- Downloading {i}th speaker -------------------------\n\n")

    # Download audio tar file
    subprocess.run(["curl", f"https://spandh.dcs.shef.ac.uk/gridcorpus/s{i}/audio/s{i}.tar", "-o", f"gridcorpus_hd/raw/audio/s{i}.tar"])
    
    # Download HD video zip file
    subprocess.run(["curl", f"https://spandh.dcs.shef.ac.uk/gridcorpus/s{i}/video/s{i}.mpg_6000.part1.tar", "-o", f"gridcorpus_hd/raw/video/s{i}p1.tar"])
    subprocess.run(["curl", f"https://spandh.dcs.shef.ac.uk/gridcorpus/s{i}/video/s{i}.mpg_6000.part2.tar", "-o", f"gridcorpus_hd/raw/video/s{i}p2.tar"])
    if extract_files.lower() == "y":
        # Extract video zip file
        with tarfile.open(f"gridcorpus_hd/raw/video/s{i}p1.tar", 'r') as tar_ref:
            tar_ref.extractall(f"gridcorpus_hd/video/")
        with tarfile.open(f"gridcorpus_hd/raw/video/s{i}p2.tar", 'r') as tar_ref:
            tar_ref.extractall(f"gridcorpus_hd/video/")
        
        # Extract audio tar file
        with tarfile.open(f"gridcorpus_hd/raw/audio/s{i}.tar", 'r') as tar_ref:
            tar_ref.extractall(f"gridcorpus_hd/audio/s{i}")

print("Download completed.")
