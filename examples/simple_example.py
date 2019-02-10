from api_base import APIBase


class Cats(APIBase):
    """
    This class inherits from APIBase and creates a wrapper around the "Cat Facts" API
    """

    def __init__(self):
        """
        Initialize the class. This calls the init method of the APIBase class and passes through the API root URL.
        """
        super().__init__(root='https://cat-fact.herokuapp.com/')

    def get_facts(self):
        """
        Returns facts about cats

        :return: Cat facts in JSON form
        """
        return self._get('facts')


# Instantiate class
cats = Cats()

# Get facts
facts = cats.get_facts()

# Print first fact
print(facts['all'][0]['text'])
