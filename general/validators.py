import csv
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

class Validators():
    #\\\\\\\\\\\\\\
    #note that some methods are have the static tag because for form validators 
    #django cant handle it having a 'self' arg, so we have to make sure it doesnt have that
    #\\\\\\\\\\\\\\

    translation_table = dict.fromkeys(map(ord, '!,.'), None) 
    with open('static/profanity-list.txt') as f:
            reader = csv.reader(f, delimiter="\n")
            bad_word_list = sum(list(reader),[])
             #this is because it imports the file as a list of 1 element lists like this: [['word'],['word']]
            #and that flattens it out

    def Validators(self):
        return self
    
    #----its in the name----#
    @staticmethod
    def is_word_profanity(value):
        translation_table = dict.fromkeys(map(ord, '!,.'), None) 
        with open('static/profanity-list.txt') as f:
            reader = csv.reader(f, delimiter="\n")
            bad_word_list = sum(list(reader),[])

        if value in bad_word_list:
            raise ValidationError(_(f"You cant have bad words in your message"), code="invalid")
    
        
    #----returns what specfic word in a piece of text is being flagged----#
    def what_word_in_text_is_profanity(self,text):
        text = text.translate(self.translation_table) #this removes some puncuality
        list_of_words = text.split()
        for word in list_of_words:
            if word in self.bad_word_list:
                return word
    
    #----returns true/false of whether any word is a bad word----#
    @staticmethod
    def is_any_word_in_text_profanity(value):
        translation_table = dict.fromkeys(map(ord, '!,.'), None) 
        with open('static/profanity-list.txt') as f:
            reader = csv.reader(f, delimiter="\n")
            bad_word_list = sum(list(reader),[])


        text = value.translate(translation_table) #this removes some puncuality
        list_of_words = text.split()
        for word in list_of_words:
            if word in bad_word_list:
                raise ValidationError(_(f"You cant have bad words in your message"), code="invalid")
    
    #----returns all words that are flagged as profanity----#
    def get_all_bad_words(self,text):
        text = text.translate(self.translation_table) #this removes some puncuality
        list_of_words = text.split()
        flagged_words = []
        for word in list_of_words:
            if word in self.bad_word_list:
                flagged_words.append(word)
        return flagged_words
    
