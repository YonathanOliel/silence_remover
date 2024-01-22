from wave_file_manager import*
from exclude_silence_processing import*
import matplotlib.pyplot as plt
import sys
from os import path


def check_input_file(file_name):
    if len(file_name) < 5:
        return "Invalid file name"

    input_split = file_name.split(".")
    if input_split == 1:
        return "The file has no extension"

    if input_split[-1] != "wav":
        return "The system only accepts wav files"

    if not path.exists(file_name):
        return "The file does not exist"
       
    return None


print("arg:", sys.argv)
if len(sys.argv) < 2:
    print("Please insert an audio file")
    exit(0)

input_file_name = sys.argv[1]
input_file_name_error = check_input_file(input_file_name)
if input_file_name_error != None:
    print("ERROR:", input_file_name_error)
    exit(0)


wave_samples = wave_file_read_samples(input_file_name)
if wave_samples == None:
    print("Error: No symbols found in the file")
    exit(0)

wave_samples_norm = normalize_samples(wave_samples, 1000)
silences_points = get_silences_points(wave_samples_norm, SILENCES_THRESHOLD, GLITCH_MAX_LEN, SILENCES_MIN_LEN, MARGIN_START, MARGIN_END)
wave_samples_without_silences = get_amples_without_silences(wave_samples, silences_points)

output_file_name = input_file_name[:-4] + "_out.wav"
print("output fille name:", output_file_name)
wave_file_write_samples(output_file_name, wave_samples_without_silences)


# ----------------- matplotlib ------------------

plt.plot(wave_samples_norm)
plt.axhline(y = SILENCES_THRESHOLD, color = "r")

for p in silences_points:
    plt.axvline(x = p[0], color = "y")
    plt.axvline(x = p[1], color = "r")

plt.show()

# ------------------------------------------------
