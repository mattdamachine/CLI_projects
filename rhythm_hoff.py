''' Program that uses the sound of a metronome to help guide the user through
    a breath-work session based on Wim Hof
    Steps are as follows:
    1. 30 deep breaths in (at 40bpm)
    2. Exhale and hold breath for 60 or 90 seconds (depending on round #)
    3. Breathe in and hold for 15 seconds
    4. Repeat steps 2-4 for x number of rounds '''

import simpleaudio, time

strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')  # inhale sound
weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')  # exhale sound

def breathe():
    ''' Perform 30 large breaths at 40bpm '''
    curr_click_count = 0  # number of current clicks
    click_limit = 61  # determined by inhales and exhales
    breath_count = 1  # number of breaths
    
    while curr_click_count < click_limit:
        curr_click_count += 1
        if curr_click_count % 2 != 0:  # inhale
            strong_beat.play()
            print('IN ' + str(breath_count))
            breath_count += 1
        else:  # exhale
            weak_beat.play()  
            print('OUT')
        
        time.sleep(1.5)

def breath_hold(seconds, in_or_out: str):
    ''' Hold your breath in or out for a specified number of seconds '''
    if in_or_out == 'IN':
        print(f'Breathe in fully and hold for {seconds} seconds...')
    elif in_or_out == 'OUT':
        print(f'Breathe out fully and hold for {seconds} seconds...')

    time.sleep(2)

    # Count and play a click each second
    current_second = 0
    while current_second < seconds:
        current_second += 1
        print(current_second)
        strong_beat.play()
        time.sleep(1)

    if in_or_out == 'IN':
        print('Exhale...')
    elif in_or_out == 'OUT':
        print('Deep breath in...')

def main():
    print('\nWelcome to the Wim Hof Rhythmic Breathing Practice.')
    num_of_rounds = 0
    while num_of_rounds <= 0:  # prompt user for number of rounds
        num_of_rounds = int(input('Enter how many rounds you\'d like to do:  '))

    for x in range(num_of_rounds):
        print(f'Round number {x + 1}')
        print('Breathe in and out to the pace of the clicks...')
        time.sleep(1)

        breathe()  # 30 deep breaths in

        if (x + 1) == 1:  
            breath_hold(60, 'OUT')  # 60 sec breath hold on first round
        else:
            breath_hold(90, 'OUT')  # 90 sec breath hold on every round after first
        time.sleep(2)

        breath_hold(15, 'IN')  # Recovery breath in for 15 seconds
        time.sleep(3)

    print('Great job! Enjoy the rest of your day...')

if __name__ == '__main__':
    main()
