from os import walk

mypath = "./tagged_data"
tag_files = []
for (dirpath, dirnames, filenames) in walk(mypath):
    tag_files.extend(filenames)

t = len(tag_files)
c = 0
# print tag_files

for tag_file in tag_files:
    c += 1
    print "Cleaning Tags : " + "(" + str(c) + "/" + str(t) + ") " + tag_file
    f = open("./tagged_data/" + tag_file, 'r')
    data = f.read()
    f.close()

    f1 = open("./cleaned_tag_data/" + tag_file.replace("_cleaned.csv", ""), 'w')
    lines = data.split("\n")
    for line in lines:
        words = line.split(" ")
        for i in range(0, len(words)):
            if words[i] != "E" and words[i] != "H" and words[i] != "D" :
                words.pop(i)
        for i in range(0, len(words)):
            if words[i] == 'E':
                f1.write('E ')
            elif words[i] == 'H':
                f1.write('H ')
            # elif words[i] == 'N':
            #     if i == 0:
            #         if words[1] == 'H':
            #             f1.write('H ')
            #         elif words[1] == 'E':
            #             f1.write('E ')
            #     elif i == len(words):
            #         if words[i - 1] == 'H':
            #             f1.write('H ')
            #         elif words[i - 1] == 'E':
            #             f1.write('E ')
            #     elif words[i - 1] == 'H' and words[i + 1] == 'H':
            #         f1.write('H ')
            #     elif words[i - 1] == 'E' and words[i + 1] == 'E':
            #         f1.write('E ')
            elif words[i] == 'D':
                if i == len(words)-1:
                    if words[i - 1] == 'H':
                        f1.write('H ')
                    elif words[i - 1] == 'E':
                        f1.write('E ')
                    elif words[i - 1] == 'D':
                        # f1.write('D ')
                        pass
                elif i == 0:
                    if words[1] == 'H':
                        f1.write('H ')
                    elif words[1] == 'E':
                        f1.write('E ')
                    elif words[1] == 'D':
                        # f1.write('D ')
                        pass
                elif words[i - 1] == 'H' and words[i + 1] == 'H':
                    f1.write('H ')
                elif words[i - 1] == 'E' and words[i + 1] == 'E':
                    f1.write('E ')
        f1.write('\n')
    f1.close()

mypath = "./cleaned_tag_data"
tag_files = []
for (dirpath, dirnames, filenames) in walk(mypath):
    tag_files.extend(filenames)

t = len(tag_files)
index = 0
f1 = open("final.txt", 'w')
for tag_file in tag_files:
    index += 1
    print "Counting : " + "(" + str(index) + "/" + str(t) + ") " + tag_file
    f = open("./cleaned_tag_data/" + tag_file, 'r')
    data = f.read()
    f.close()

    lines = data.split("\n")
    H = 0
    E = 0
    mix = 0
    switch = 0
    other = 0
    total = len(lines)-2

    for line in lines:
        words = line.split(" ")
        h = h1 = 0
        e = e1 = 0
        d = d1 = 0
        if words[0] == 'H':
            h1 = h1 + 1
        elif words[0] == 'E':
            e1 = e1 + 1
        elif words[0] == 'D':
            d1 = d1 + 1
        if len(words) > 1:
            for i in range(1, len(words)):
                if words[i] == 'E':
                    e1 = e1 + 1
                    if words[i - 1] == 'H' and h1 > h:
                        h = h1
                    if words[i - 1] == 'D' and d1 > d:
                        d = d1
                    h1 = 0
                    d1 = 0
                elif words[i] == 'H':
                    h1 = h1 + 1
                    if words[i - 1] == 'E' and e1 > e:
                        e = e1
                    if words[i - 1] == 'D' and d1 > d:
                        d = d1
                    e1 = 0
                    d1 = 0
                elif words[i] == 'D':
                    d1 = d1 + 1
                    if words[i - 1] == 'E' and e1 > e:
                        e = e1
                    if words[i - 1] == 'H' and h1 > h:
                        h = h1
                    e1 = 0
                    h1 = 0
        if h1 > h:
            h = h1
        if e1 > e:
            e = e1
        if d1 > d:
            d = d1
        if h > 3 and e > 3:
            switch = switch + 1
        elif h > 3 and e == 0:
            H = H + 1
        elif e > 3 and h == 0:
            E = E + 1
        elif e > 0 and h > 0:
            mix = mix + 1
        elif d > 3:
            other = other + 1
    f1.write(tag_file.replace("_tags.txt", "") + " H " + str(H) + " E " + str(E) + " switch " + str(switch) + " mix " + str(mix) + " other " + str(other) + " total " + str(total) + "\n")
f1.close()
print "\nFinished."
