from ScopusWp.config import Config, PATH, PROJECT_PATH
import pathlib
import json


ID_JSON_TEMPLATE = (
    '{\n'
    '"counter": 1,\n'
    '"used": [],\n'
    '"unused": []\n'
    '}'
)


class IDManagerInterface:

    def new(self):
        raise NotImplementedError()

    def delete(self, publication_id):
        raise NotImplementedError

    @property
    def all(self):
        raise NotImplementedError()

    @property
    def used(self):
        raise NotImplementedError()

    @property
    def unused(self):
        raise NotImplementedError()


class IDManager(IDManagerInterface):

    def __init__(self, name):
        self.name = name
        self.path = pathlib.Path(PROJECT_PATH) / 'id_{}.json'.format(self.name)

        self._dict = {}
        self.load()

        self.used_ids = self._dict['used']
        self.unused_ids = self._dict['unused']
        self.pointer = self._dict['counter']

    def exists(self):
        return self.path.exists() and self.path.is_file()

    def save(self):
        """
        Saves the the content dict, which contains the info about the used ids into a json file in the project folder

        :return: void
        """
        with self.path.open(mode='w') as file:
            content_dict = {
                'used': self.used_ids,
                'unused': self.unused_ids,
                'counter': self.pointer
            }
            json.dump(content_dict, file)

    def new(self):
        """
        Creates and returns a new id to use.

        Updates the created id into the list of used ids directly and increments the pointer, that indicates the amount
        of used ids.
        :return: The int id that has been created
        """
        self.pointer += 1
        self.used_ids.append(self.pointer)
        return self.pointer

    def delete(self, publication_id):
        if publication_id in self.used_ids:
            self.used_ids.remove(publication_id)
            self.unused_ids.append(publication_id)

    def load(self):
        """
        Loads the information about the used ids from the json file in the project folder.

        :return: the dict, that contains the list if used and unused ids as well as the pointer for the amount of ids
        """
        # First checking if the file already exists. If not creates a new one from the template and loads that
        if not self.exists():
            with self.path.open(mode='w+') as file:
                file.write(ID_JSON_TEMPLATE)
                file.flush()

        # Loading the content of the file as a single dict
        with self.path.open(mode='r') as file:
            self._dict = json.load(file)

    @property
    def all(self):
        return self.used_ids

    @property
    def used(self):
        return self.used_ids

    @property
    def unused(self):
        return self.unused_ids