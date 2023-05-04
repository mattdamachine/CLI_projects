'''Use Markov Chain analysis to compose a new list of chords from 
   a given starting chord. The training corpus will be based off of 
   a text file of chords that the user can specify.'''
import sys
from collections import Counter
import numpy as np

# keys with diatonic chords
MAJOR_KEYS = {'C' : ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim'],
              'D' : ['D', 'Em', 'F#m', 'G', 'A', 'Bm', 'C#dim'],
              'E' : ['E', 'F#m', 'Gm', 'Ab', 'Bb', 'C#m', 'D#dim'],
              'F' : ['F', 'Gm', 'Am', 'Bb', 'C', 'Dm', 'Edim'],
              'G' : ['G', 'Am', 'Bm', 'C', 'D', 'Em', 'F#dim'],
              'A' : ['A', 'Bm', 'C#m', 'D', 'E', 'F#m', 'G#dim'],
              'B' : ['B', 'C#m', 'D#m', 'E', 'F#', 'G#m', 'A#dim']}

def load_chords(file):
    '''Return a list of chords from a text file'''
    try:
        with open(file) as in_file:
            loaded_chords = in_file.read().split('\n')
            return loaded_chords
    except IOError as e:
        print(f'{e}\nError opening {file}. Terminating program.')
        sys.exit(1)

def create_bigrams(chords_list):
    '''Create a list of bigrams from chord list (ex. ('1', '4'))'''
    bigrams = []
    for i in range(len(chords_list) - 1):
        bigrams.append(chords_list[i] + ' ' + chords_list[i + 1])
    return bigrams

def get_chord(chords):
    '''Prompt the user to enter a starting chord and
       check that it exists in the chord list'''
    starting_chord = input('Enter the chord degree to start with: ')
    while starting_chord not in chords:
        print('Chord does not exist in chord list. Choose another...')
        starting_chord = input('Enter the chord degree to start with: ')
    return starting_chord

def get_key():
    '''Prompt the user to enter a key to use and check
       that it exists in the MAJOR_KEYS dict'''
    key = input('Enter a key to use: ').upper()
    while key not in MAJOR_KEYS.keys():
        print("Key cannot be used. Key must be a major key...")
        key = input('Enter a key to use: ').upper()
    return key

def predict_next_state(chord, bigrams):
    '''Return next chord in sequence based on current state.'''

    # create list of bigrams that start with current chord
    bigrams_current_chord = [bigram for bigram in bigrams if bigram.split(' ')[0] == chord]

    # count occurance of each bigram
    count_appearance = dict(Counter(bigrams_current_chord))

    # change appearance counts into decimal probabilities
    for bigram in count_appearance.keys():
        count_appearance[bigram] = count_appearance[bigram]/len(bigrams_current_chord)

    # create list of possible options for the next chord
    options = []
    for chord in count_appearance.keys():
        options.append(chord.split(' ')[1])
    # create list of probabilities
    probabilities = [prob for prob in count_appearance.values()]

    # make random prediction
    return np.random.choice(options, p=probabilities)

def generate_sequence(chord, bigrams, length, key):
    '''Return sequence of diatonic chords of user-defined length.'''
    chords = []  # create list to store return chords
    current_key = MAJOR_KEYS[key]  # set key to work in

    for x in range(length):
        # append next chord to the list
        new_chord_degree = predict_next_state(chord, bigrams)
        chords.append(current_key[int(new_chord_degree) - 1])
        # use last chord to predict the next chord
        chord = new_chord_degree

    return chords

def write_to_file(starting_chord, key, final_chords):
    '''Write the final chord sequence to a text file for safe-keeping.'''
    with open('user_chords.txt', 'a') as file:
        file.write(f'\nkey: {key}\n')
        file.write(f'starting chord: {starting_chord}\n')
        file.write(f'generated markov sequence: {final_chords}\n')
    
    print(f'Successfully written to text file...')

def main():
    ''' Load in chords from txt file, create bigrams, choose starting chord & key,
        set number of chords to be generated.'''
    # USER INPUT: file name 
    file_name = input('Enter the name of the chord file to be used: ')
    chords = load_chords(file_name)
    # chords = load_chords('/Users/Mattdamachine/Code/impractical_projects/extra_projects/chord_degrees.txt')

    # populate bigrams 
    bigrams = create_bigrams(chords)
    
    # USER INPUT: starting chord (must be a non-negative integer in chord_set)
    chord_set = set(chords)
    starting_chord = get_chord(chord_set)

    # USER INPUT: key (must be major (& no sharps or flats) right now)
    key = get_key()

    # USER INPUT: number of chords to be printed
    num_of_chords = int(input('Enter the number of chords to generate: '))

    final_chords = generate_sequence(starting_chord, bigrams, num_of_chords, key)

    # write chord, key, and final sequence to a txt file
    write_to_file(starting_chord, key, final_chords)

if __name__ == '__main__':
    main()