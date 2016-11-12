import csv
from nltk.corpus import wordnet
from os import walk

# print wordnet.synsets("mi")

# BINARY SEARCH FUNCTION


def word_search(corpus, word):
    first = 0
    last = len(corpus)
    while first < last:
        mid = (first + last) / 2
        m_word = corpus[mid]
        if m_word < word:
            first = mid + 1
        elif m_word > word:
            last = mid
        elif m_word == word:
            return mid
    return -1

# HINDI CORPUS SETUP
f = open("hindi_words.txt", 'r')
data = f.read()
f.close()
data = data.replace(" H", "").replace(" N", "").replace(" ", "")
lines = data.split("\n")

# ENGLISH CORPUS SETUP
f_eng = open("english_words.txt", 'r')
data_eng = f_eng.read()
f_eng.close()
data_eng = data_eng.replace(" ", "")
lines_eng = data_eng.split("\n")

# READING ALL THE FILES IN THE DIRECTORY "DATA" (CONTAINS "_cleaned.csv" FILES)
mypath = "./cleaned_data"
cleaned_files = []
for (dirpath, dirnames, filenames) in walk(mypath):
    cleaned_files.extend(filenames)

# INDICES SETUP
i = 0
total_files = len(cleaned_files)

# TAGGING START
for cleaned_file in cleaned_files:
    i += 1
    print "Generating Tags : " + "(" + str(i) + "/" + str(total_files) + ") " + cleaned_file

    tag_writer = open("./tagged_data/" + cleaned_file.replace("_cleaned.csv", "") + "_tags.txt", 'w')

    with open("./cleaned_data/" + cleaned_file, 'rb') as f:

        reader = csv.reader(f)

        try:
            reader.next()
        except Exception as e:
            pass

        # PICK UP A SINGLE TWEET
        for row in reader:
            col = row[3]
            words = col.split(" ")

            for word in words:
                # SEARCH HINDI WORD IN OUR CORPUS
                flag = 1  # DEFAULT FLAG
                hin_ret = word_search(lines, word)
                if hin_ret != -1:
                    tag_writer.write("H ")
                    flag = 0  # HINDI FLAG

                if flag == 1:
                    # SEARCH ENGLISH WORD IN WORDNET CORPUS
                    if wordnet.synsets(word):
                        tag_writer.write("E ")
                        flag = 2  # ENGLISH FLAG
                    else:
                        # SEARCH ENGLISH WORD IN OUR CORPUS
                        eng_ret = word_search(lines_eng, word)
                        if eng_ret != -1:
                            tag_writer.write("E ")
                            flag = 2

                        # UNKNOWN WORDS
                        if flag == 1:
                            tag_writer.write("D ")

            # WRITING SINGLE TWEET COMPLETED
            tag_writer.write("\n")
    # WRITING TAGS FOR SINGLE USER COMPLETE
    tag_writer.close()
