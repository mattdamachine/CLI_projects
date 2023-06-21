""" Have the user define a target tempo and a folder of songs.
    Calculate the tempo of each one, keep the songs that fall within a close proximity to the target tempo 
    (target tempo - 10 <= song <= target tempo + 10),
    display them back to the user, and allow them to choose one to play."""
import os
import sys
import tkinter as tk
from tkinter import filedialog
import librosa
import simpleaudio as sa

def get_song_files(file_path: str) -> list:
    """Return a list of song file names from a file path."""

    try:
        os.chdir(file_path)
    except FileNotFoundError:
        sys.exit("Error: Please enter a valid file path...")
        

    return os.listdir()

def choose_directory() -> str:
    """Allow the user to choose a song directory."""
    root = tk.Tk()
    root.withdraw()

    # Open the directory selection dialog
    selected_directory = filedialog.askdirectory(title="Select a folder of Wav files")

    return selected_directory

def choose_target_tempo() -> int:
    """Allow the user to define a target tempo to use."""
    target_tempo = ""
    while True:
        try:
            target_tempo = int(input("Enter the desired tempo to search with: "))
            if isinstance(target_tempo, int) and target_tempo > 0:
                break
            else:
                print("Target tempo must be greater than 0")
        except ValueError:
            print("Target tempo must be an integer value")

    return target_tempo


def calculate_tempo(file_path: str, file_name: str) -> int:
    """Use librosa to load in each song and calculate its tempo."""

    full_file_path = os.path.join(file_path, file_name)
    
    # Load the audio as a waveform 'y', store the sampling rate as 'sr'
    y, sr = librosa.load(full_file_path)

    # Run the default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    return tempo.round(2)

    # beat_times = librosa.frames_to_time(beat_frames, sr=sr)

def choose_song(song_list: list) -> int:
    """Print the songs and allow the user to choose a song from the list."""
    print("Here are the songs that fit within the tempo range...")

    if song_list:
        for i, song in enumerate(song_list):
            print(f"{i}) {song}")

        # Grab the user's choice of song 
        song_choice = int(input("Enter the number of the song you'd like to play: "))

        return song_choice
    else:
        raise IndexError("No songs fall within the specified tempo range")

def play_song(song_list: list, song_index: int):
    """Play the user-selected song."""

    wave_object = sa.WaveObject.from_wave_file(song_list[song_index])
    print(f"Playing song {song_index}...")

    play_object = wave_object.play()
    play_object.wait_done()

def main():
    # Get target tempo from user
    target_tempo = choose_target_tempo()
        
    # Get the song directory from user
    print("Choose a directory of songs to use...")
    file_path = choose_directory()

    # Get the song files from the chosen directory
    song_files = get_song_files(file_path)

    # key = song file name: str. value = tempo: float
    song_tempos = {}

    print(f"Searching for songs between {target_tempo - 10}bpm and {target_tempo + 10}bpm...")

    # Calculate the tempos of each song in the song array
    for song in song_files:
        estimated_tempo = calculate_tempo(file_path, song)
        song_tempos[song] = estimated_tempo

    # print(song_tempos)

    # Filter the songs to only keep the ones that fall within the tempo range
    target_songs = [song for song in song_tempos 
                    if (target_tempo - 10) <= song_tempos[song] <= (target_tempo + 10)]
    
    # Print out each one of the songs and choose a song from the list
    song_choice = choose_song(target_songs)

    # Play the chosen song
    play_song(target_songs, song_choice)


if __name__ == "__main__":
    main()