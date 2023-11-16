def count_word_frequency(filename):
    word_frequency = {}

    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        words = text.split()

        for word in words:
            word = word.strip('.,!?()[]{}"\'').lower()

            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1

    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_frequency

filename = 'text_1_var_36'
output_filename = 'result_1.txt'

word_frequency = count_word_frequency(filename)

with open(output_filename, 'w', encoding='utf-8') as outfile:
    for word, frequency in word_frequency:
        outfile.write(f"{word}:{frequency}\n")