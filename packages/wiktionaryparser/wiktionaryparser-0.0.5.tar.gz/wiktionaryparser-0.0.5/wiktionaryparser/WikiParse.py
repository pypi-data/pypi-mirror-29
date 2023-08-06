"""
Final code for wiktionary parser.
"""
from __future__ import unicode_literals
from __future__ import absolute_import
import re, requests
from wiktionaryparser.utils import WordData, Definition, RelatedWord
from bs4 import BeautifulSoup

PARTS_OF_SPEECH = [
    "noun", "verb", "adjective", "adverb", "determiner",
    "article", "preposition", "conjunction", "proper noun",
    "letter", "character", "phrase", "proverb", "idiom",
    "symbol", "syllable", "numeral", "initialism", "interjection", "definitions"
]

RELATIONS = [
    "synonyms", "antonyms", "hypernyms", "hyponyms",
    "meronyms", "holonyms", "troponyms", "related terms",
    "derived terms", "coordinate terms",
]

UNWANTED_LIST = [
    'External links', 'Compounds', 'translations'
    'Anagrams', 'References', 'Statistics', 
    'See also', 'Usage notes',
]


class WiktionaryParser(object):
    """
    Final class for Wiktionary parser.
    """

    def __init__(self):
        self.url = "https://en.wiktionary.org/wiki/"
        self.soup = None
        self.session = requests.Session()
        self.session.mount(
            "http://",
            requests.adapters.HTTPAdapter(max_retries=2)
        )
        self.session.mount(
            "https://",
            requests.adapters.HTTPAdapter(max_retries=2)
        )
        self.language = 'english'
        self.current_word = None

    def set_default_language(self, language=None):
        """
        Sets the default language of the parser object.
        """
        if language is not None:
            self.language = language.lower()
        return

    def get_default_language(self):
        """
        returns the default language of the object.
        """
        return self.language

    def get_id_list(self, contents, content_type):
        """
        Returns a list of IDs relating to the specific content type.
        Text can be obtained by parsing the text within span tags
        having those IDs.
        """
        if content_type == 'etymologies':
            checklist = ['etymology']
        elif content_type == 'pronunciation':
            checklist = ['pronunciation']
        elif content_type == 'definitions':
            checklist = list(PARTS_OF_SPEECH)
            if self.language == 'chinese':
                checklist += self.current_word
        elif content_type == 'related':
            checklist = RELATIONS
        else:
            return None
        id_list = []
        for content_tag in contents:
            content_index = content_tag.find_previous().text
            text_to_check = ''.join(i for i in content_tag.text
                                    if not i.isdigit()).strip().lower()
            if text_to_check in checklist:
                content_id = content_tag.parent['href'].replace('#', '')
                id_list.append((content_index, content_id, text_to_check))
        return id_list

    def get_word_data(self, language):
        """
        Match language, get previous tag, get starting number.
        """
        try:
            self.soup.find('div',{'class': 'sister-wikipedia sister-project noprint floatright'}).decompose()   
        except:
            pass
        contents = self.soup.find_all('span', {'class': 'toctext'})
        language_contents = []
        start_index = None
        for content in contents:
            if content.text.lower() == language:
                start_index = content.find_previous().text + '.'
        if start_index is None:
            return []
        for content in contents:
            index = content.find_previous().text
            if index.startswith(start_index):
                language_contents.append(content)
        word_contents = []
        for content in language_contents:
            if content.text not in UNWANTED_LIST:
                word_contents.append(content)
        word_data = {
            'definitions': self.parse_definitions(word_contents),
            'examples': self.parse_examples(word_contents),
            'etymologies': self.parse_etymologies(word_contents),
            'related': self.parse_related_words(word_contents),
            'pronunciations': self.parse_pronunciations(word_contents)
        }
        json_obj_list = self.make_class(word_data)
        return json_obj_list

    def parse_pronunciations(self, word_contents):
        """
        Parse pronunciations from their IDs.
        clear supertext tags first.
        separate audio links.
        """
        pronunciation_id_list = self.get_id_list(word_contents, 'pronunciation')
        pronunciation_list = []
        for pronunciation_index, pronunciation_id, _ in pronunciation_id_list:
            span_tag = self.soup.find_all('span', {'id': pronunciation_id})[0]
            list_tag = span_tag.parent
            while list_tag.name not in ['ul', 'p']:
                list_tag = list_tag.find_next_sibling()
                if list_tag.name == 'div' and 'mw-collapsible' in list_tag['class']:
                    break
            for super_tag in list_tag.find_all('sup'):
                super_tag.clear()
            audio_links = []
            pronunciation_text = []
            tag_to_search = 'li'
            if list_tag.name == 'p': tag_to_search = 'span'
            for list_element in list_tag.find_all(tag_to_search):
                for audio_tag in list_element.find_all(
                        'div', {'class': 'mediaContainer'}):
                    audio_links.append(audio_tag.find('source')['src'])
                    list_element.clear()
                if list_element.text:
                    try:
                        if 'IPA' in list_element['class']:
                            pronunciation_text.append(list_element.text)
                    except:
                        pronunciation_text.append(list_element.text)
            pronunciation_list.append(
                (pronunciation_index, pronunciation_text, audio_links))
        return pronunciation_list

    def parse_definitions(self, word_contents):
        """
        Definitions are ordered lists
        Look for the first <ol> tag
        The tag right before the <ol> tag has tenses.
        """
        definition_id_list = self.get_id_list(word_contents, 'definitions')
        definition_list = []
        for def_index, def_id, def_type in definition_id_list:
            span_tag = self.soup.find_all('span', {'id': def_id})[0]
            table = span_tag.parent
            definition_tag = None
            while table.name != 'ol':
                definition_tag = table
                table = table.find_next_sibling()
            for examples in table.find_all('ul'):
                examples.decompose()
            definition_text = definition_tag.text + '\n'
            for element in table.find_all('li'):
                definition_text += re.sub('(\\n+)', '',
                    element.text.strip()) + '\n'
            if def_type == 'definitions':
                def_type = ''
            definition_list.append((
                def_index,
                definition_text,
                def_type
            ))
        return definition_list

    def parse_examples(self, word_contents):
        """
        look for <dd> tags inside <ol> tags.
        remove data in <ul> tags.
        """
        definition_id_list = self.get_id_list(word_contents, 'definitions')
        example_list = []
        for def_index, def_id, def_type in definition_id_list:
            span_tag = self.soup.find_all('span', {'id': def_id})[0]
            table = span_tag.parent
            while table.name != 'ol':
                table = table.find_next_sibling()
            # for element in table.find_all('ul'):
            #     element.clear()
            examples = []
            for element in table.find_all('dd'):
                example_text = element.text.strip()
                examples.append(example_text)
                #element.clear()
            example_list.append((def_index, examples, def_type))
        return example_list

    def parse_etymologies(self, word_contents):
        """
        Word etymology is either a para or a list.
        move forward till you find either.
        """
        etymology_id_list = self.get_id_list(word_contents, 'etymologies')
        etymology_list = []
        for etymology_index, etymology_id, _ in etymology_id_list:
            span_tag = self.soup.find_all('span', {'id': etymology_id})[0]
            etymology_tag = None
            next_tag = span_tag.parent.find_next_sibling()
            while next_tag.name not in ['h3', 'h4', 'div']:
                etymology_tag = next_tag
                next_tag = next_tag.find_next_sibling()
            if etymology_tag is None:
                etymology_text = ''
            elif etymology_tag.name == 'p':
                etymology_text = etymology_tag.text
            else:
                etymology_text = ''
                for list_tag in etymology_tag.find_all('li'):
                    etymology_text += list_tag.text + '\n'
            etymology_list.append(
                (etymology_index, etymology_text))
        return etymology_list

    def parse_related_words(self, word_contents):
        """
        Look for parent tags with <li> tags, those are related words.
        <li> tags can either be in tables or lists.
        """
        relation_id_list = self.get_id_list(word_contents, 'related')
        related_words_list = []
        for related_index, related_id, relation_type in relation_id_list:
            words = []
            span_tag = self.soup.find_all('span', {'id': related_id})[0]
            parent_tag = span_tag.parent
            while not parent_tag.find_all('li'):
                parent_tag = parent_tag.find_next_sibling()
            for list_tag in parent_tag.find_all('li'):
                words.append(list_tag.text)
            related_words_list.append((related_index, words, relation_type))
        return related_words_list

    def make_class(self, word_data):
        """
        Takes all the data and makes classes.
        """
        json_obj_list = []
        if not word_data['etymologies']:
            word_data['etymologies'] = [('', '')]
        for etymology_index, etymology_text in word_data['etymologies']:
            data_obj = WordData()
            data_obj.etymology = etymology_text
            for pronunciation_index, text, audio_links in word_data['pronunciations']:
                if pronunciation_index.startswith(etymology_index) \
                or pronunciation_index.count('.') == etymology_index.count('.'):
                    data_obj.pronunciations = text
                    data_obj.audio_links = audio_links
            for definition_index, definition_text, definition_type in word_data['definitions']:
                if definition_index.startswith(etymology_index) \
                or definition_index.count('.') == etymology_index.count('.'):
                    def_obj = Definition()
                    def_obj.text = definition_text
                    def_obj.part_of_speech = definition_type
                    for example_index, examples, _ in word_data['examples']:
                        if example_index.startswith(definition_index):
                            def_obj.example_uses = examples
                    for related_word_index, related_words, relation_type in word_data['related']:
                        if related_word_index.startswith(definition_index) \
                        or (related_word_index.startswith(etymology_index) \
                        and related_word_index.count('.') == definition_index.count('.')):
                            words = None
                            try:
                                words = next(
                                    item.words for item in def_obj.related_words
                                    if item.relationship_type == relation_type
                                )
                            except StopIteration:
                                pass  
                            if words is not None:
                                words += related_words
                                break
                            related_word_obj = RelatedWord()
                            related_word_obj.words = related_words
                            related_word_obj.relationship_type = relation_type
                            def_obj.related_words.append(related_word_obj)
                    data_obj.definition_list.append(def_obj)
            json_obj_list.append(data_obj.to_json())
        return json_obj_list

    def fetch(self, word, language=None):
        """
        main function.
        subject to change.
        """
        language = self.language if not language else language
        response = self.session.get(self.url + word + '?printable=yes')
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.current_word = word
        return self.get_word_data(language.lower())
