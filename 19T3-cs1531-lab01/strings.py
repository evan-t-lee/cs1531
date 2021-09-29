'''
TODO Complete this file by following the instructions in the lab exercise.
'''

strings = ['This', 'list', 'is', 'now', 'all', 'together']
sentence = ''
for word in strings:
	sentence += word + ' '
sentence = sentence[:-1]
print(sentence)
print(' '.join(strings))
