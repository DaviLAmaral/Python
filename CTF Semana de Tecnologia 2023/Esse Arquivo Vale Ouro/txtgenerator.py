import os
import sys
import itertools

# Characters that can be used in the unknown positions
possible_characters = '0123456789'

# Number of unknown characters
n = 4

# Name of the file where the combinations will be saved
path = f"{os.path.dirname(sys.argv[0])}"
file_name = f'{path}/passwordlist.txt'

# Open the file for writing
with open(file_name, 'w') as file:
    for combination in itertools.product(possible_characters, repeat=n):
        # Generate the string by replacing the unknown characters
        new_string = f'{"".join(combination)}'
        # Write the string to the file
        file.write(new_string + '\n')

print(f'All combinations have been saved in {file_name}')
