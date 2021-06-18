import requests
from bs4 import BeautifulSoup
import re


class Dytionary:
    def __init__(self, word):
        self.name = word

    # Only works with the words the dictionary can return an actual defenition not suggested defenitions
    # For example "apples" won't work but "apple" will
    def definition(self):

        # Main Method To Check For Definition
        # Some Words Like "Apples" not supported in first check
        try:
            # Storing Original Text From Website that's unfiltered
            UrlToGet = "https://www.merriam-webster.com/dictionary/" + self.name
            r = requests.get(UrlToGet)

            # Parsing and Turning into string for string Manipulation
            rawString = str(BeautifulSoup(r.content, 'html.parser'))

            # Getting Beginning and End of the section where the String is stored
            newString = rawString[int(rawString.index("</script>")):int(
                rawString.index("… See the full definition\" property=\"og:description\">"))]

            # Second Round Of Processing Getting Rid of junk from the beginning string
            finalString = newString[
                          int(newString.index("property=\"og:url\">") + len("property=\"og:url\"> <meta content=\"")):]

            return finalString

        # Trying to get definition for words that might have trouble from above.
        # Checks Method above first since it's faster
        except:
            # Storing Original Text From Website that's unfiltered
            UrlToGet = "https://www.merriam-webster.com/dictionary/" + self.name
            r = requests.get(UrlToGet)

            # Parsing and Turning into string for string Manipulation
            rawString = str(BeautifulSoup(r.content, 'html.parser'))

            # Reducing String Just To The Core With Some Extra Text

            # Getting Position Of "<div id=\"dictionary-entry-1\">"
            wordToLocate = "<div id=\"dictionary-entry-1\">"
            hLocation = []
            for i in range(len(rawString) - len(wordToLocate)):
                if rawString[i:i + len(wordToLocate)] == wordToLocate:
                    hLocation.append(i)

            # Getting Position Of "</div> </div></div></div></div></div></div></div></div></body></html>"
            wordToLocate = "</div> </div></div></div></div></div></div></div></div></body></html>"
            divLocation = []
            for i in range(len(rawString) - len(wordToLocate)):
                if rawString[i:i + len(wordToLocate)] == wordToLocate:
                    divLocation.append(i)

            # Getting Rid Of Useless Text
            textBox = rawString[hLocation[0]:divLocation[0]]

            # Using regex to get rid of html elements
            cleantext = re.sub(re.compile('<.*?>'), '', textBox).replace("\n", "")

            # Putting It Into A final String
            sentence = ""
            for i in range(len(cleantext)):
                sentence += cleantext[i]

            # Adding Space Between Also and word before since it gets cleared above
            sentence = sentence[:sentence.find("also:")] + " " + sentence[sentence.find("also:"):]

            return sentence

    def synonym(self):
        # Storing Original Text From Website that's unfiltered
        UrlToGet = "https://www.thesaurus.com/browse/" + self.name
        r = requests.get(UrlToGet)

        # Parsing and Turning into string for string Manipulation
        rawString = str(BeautifulSoup(r.content, 'html.parser'))
        newString = str(rawString[int(
            rawString.index("<script>window.INITIAL_STATE") + len("<script>window.INITIAL_STATE = ")):int(
            rawString.index("<script>window.emotionIds=")) - len(";</script>") - 1])

        # For loop to check all the possible terms
        positions = [i for i in range(len(newString)) if newString.startswith('"targetTerm":"', i)]
        output = []
        for i in range(len(positions)):
            # Removing Funky Strings From Definition
            try:
                phrase = newString[positions[i]:positions[i] + 50]
                words = phrase[len("\"targetTerm\":\""):phrase.index("\",\"targetSlug\":")]
                output.append(words)
            except:
                # These Terms Are In A heading And do not contribute
                pass

        return output

    def ant(self):
        # Storing Original Text From Website that's unfiltered
        UrlToGet = "https://www.antonym.com/synonyms/" + self.name
        r = requests.get(UrlToGet)

        # Parsing and Turning into string for string Manipulation
        rawString = str(BeautifulSoup(r.content, 'html.parser'))

        # Saving Positions Of Where breakers are at
        antLocation = []
        synLocation = []

        # Getting Position Of "Antonym"
        wordToLocate = "Antonyms"
        for i in range(len(rawString) - len(wordToLocate)):
            if rawString[i:i + len(wordToLocate)] == wordToLocate:
                antLocation.append(i)

        # Getting Position Of "Synonyms"
        wordToLocate = "Synonyms"
        for i in range(len(rawString) - len(wordToLocate)):
            if rawString[i:i + len(wordToLocate)] == wordToLocate:
                synLocation.append(i)

        word = ""

        # Running i amount of times for each antonyms section
        for i in range(len(antLocation)):
            # Getting The Section For The Antonym
            wordToApppend = rawString[antLocation[i]:synLocation[i]]
            word = word + wordToApppend

        # Breaking Apart At Every New Line
        splitted = word.split("\n")

        # Fancy List Comprehension to get rid of useless statements
        # Credit: https://stackoverflow.com/a/3416473/11521629
        # [:-1] is added to get rid of last element that cannot be filtered
        divSorted = [x for x in splitted if
                     "</div>" not in x and "<div" not in x and "</a>" not in x and "<a" not in x and "Antonyms" not in x][
                    :-1]

        # Saving To Final Output List
        output = []

        # Removing Extra Spaces, Is Always 12 Spaces at front
        for i in range(len(divSorted)):
            output.append(divSorted[i][12:])

        print(output)

    def pos(self):
        # Checks by which position of sentence word shows up the most on the website
        # Storing Original Text From Website that's unfiltered
        UrlToGet = "https://www.dictionary.com/browse/" + self.name
        r = requests.get(UrlToGet)

        # Parsing and Turning into string for string Manipulation
        rawString = str(BeautifulSoup(r.content, 'html.parser')).lower()

        # (noun, pronoun, verb, adjective, adverb, preposition, conjunction, and interjection)
        words = []

        # Counts how many possibilities there are
        for i in range(rawString.count("<span class=\"luna-pos\">")):
            # Finding the tag in-between where the words are stored
            rawString = rawString[rawString.find("<span class=\"luna-pos\">") + len("<span class=\"luna-pos\">"):]

            # Because the word is already at the begining we know it ends at the span tag so we find the word in between
            words.append(rawString[:rawString.find("</span>")])

        # Removing Duplicates
        res = []
        for i in words:
            if i not in res:
                res.append(i)

        return res
