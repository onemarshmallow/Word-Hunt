import os


class WordProcessor:
    @staticmethod
    def readWordsFile(file_name):
        assert os.path.exists(file_name), "Cannot find the words file: %s" % (file_name)
        file = open(file_name, "r")
        # A blank line signifies the end of the file.
        content = file.readlines() + ["\n"]
        file.close()

        accepted_words = {}
        words = []  # Will be turned into the keys for accepted_words
        scores = []  # Will be turned into the values for accepted_words

        for lineNum in range(len(content)):
            # Process each line that was in the level file.
            line = content[lineNum].rstrip("\n")

            if line == "":
                break

            if ";" in line:
                # Ignore the ; lines, treat it as a comment
                line = line[:line.find(";")]

            if line.isalpha():
                words.append(line)
            elif line.isnumeric():
                scores.append(int(line))

        # Processes words and scores into accepted_words dictionary.
        for i in range(len(words)):
            accepted_words[words[i]] = scores[i]

        return accepted_words

