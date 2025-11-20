import csv


class Validators():
    translation_table = dict.fromkeys(map(ord, '!,.'), None)
    with open('../static/profanity-list.txt') as f:
            reader = csv.reader(f, delimiter="\n")
            bad_word_list = sum(list(reader),[]) #this is because it imports the file as a list of 1 element lists like this: [['word'],['word']]
            #and that flattens it out

    def Validators(self):
        return self
    
    #----its in the name----#
    def is_word_profanity(self,word):
        if word in self.bad_word_list:
            return True
        else:
            return False 
        
    #----returns what specfic word in a piece of text is being flagged----#
    def what_word_in_text_is_profanity(self,text):
        text = text.translate(self.translation_table) #this removes some puncuality
        list_of_words = text.split()
        for word in list_of_words:
            if word in self.bad_word_list:
                return word
        return ''
    
    #----returns true/false of whether any word is a bad word----#
    def is_any_word_in_text_profanity(self,text):
        text = text.translate(self.translation_table) #this removes some puncuality
        list_of_words = text.split()
        for word in list_of_words:
            if word in self.bad_word_list:
                return True
        return False
    
    #----returns all words that are flagged as profanity----#
    def get_all_bad_words(self,text):
        text = text.translate(self.translation_table) #this removes some puncuality
        list_of_words = text.split()
        flagged_words = []
        for word in list_of_words:
            if word in self.bad_word_list:
                flagged_words.append(word)
        return flagged_words
    

#testing

test_1 = 'you are a bitch ass motherfucker, fucking bitch'

valid = Validators()
print(valid.is_word_profanity('fucker'))
print(valid.get_all_bad_words(test_1))