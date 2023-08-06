import datetime

from ScopusWp.util import IDManager


class PublicationJournal:

    def __init__(self, name, volume):
        self.name = name
        self.volume = volume


class PublicationAuthor:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def index_name(self):
        return '{}. {}'.format(self.first_name[0].upper(), self.last_name)


class PublicationLink:

    def __init__(self, name, href):
        self.name = name
        self.href = href


class PublicationOrigin:

    def __init__(self, identifier, name, text):
        self.name = name
        self.identifier = identifier
        self.text = text


class GeneralPublication:

    _ID_MANAGER = IDManager('general_publication')

    def __init__(
            self,
            id,
            origin,
            title,
            description,
            date,
            doi,
            author_list,
            citation_list,
            tag_list,
            category_list,
            link_list,
            journal,
            volume
    ):
        self.id = id
        self.tags = tag_list
        self.categories = category_list
        self.title = title
        self.description = description
        self.date = date
        self.doi = doi
        self.authors = author_list
        self.journal = journal
        self.volume = volume
        self.origin = origin
        self.links = link_list
        self.citations = citation_list

    @property
    def published(self):
        return self.date

    @staticmethod
    def from_model(publication):
        try:
            general_publication = GeneralPublication(
                publication.publicationID,
                PublicationOrigin(
                    publication.origin.id,
                    publication.origin.type.name,
                    publication.origin.text
                ),
                publication.title,
                publication.description,
                publication.published,
                publication.doi,
                list(map(
                    lambda x: PublicationAuthor(
                        x.first_name,
                        x.last_name
                    ),
                    publication.authors
                )),
                list(map(
                    lambda x: GeneralPublication.from_model(x),
                    publication.citedby
                )),
                list(map(
                    lambda x: x.content,
                    publication.tags
                )),
                list(map(
                    lambda x: x.content,
                    publication.categories
                )),
                list(map(
                    lambda x: PublicationLink(
                        x.name,
                        x.href,
                    ),
                    publication.links
                )),
                publication.journal.name,
                publication.journal.volume
            )
        except Exception as e:
            raise e

        return general_publication

    @staticmethod
    def from_dict(publication_dict):
        try:
            publication_origin = PublicationOrigin(
                publication_dict['origin']['id'],
                publication_dict['origin']['type'],
                publication_dict['origin']['text']
            )

            publication_authors = list(map(
                lambda author_dict: PublicationAuthor(author_dict['first_name'], author_dict['last_name']),
                publication_dict['authors']
            ))

            publication_links = list(map(
                lambda link_dict: PublicationLink(link_dict['name'], link_dict['href']),
                publication_dict['links']
            ))

            general_publication = GeneralPublication(
                GeneralPublication._ID_MANAGER.new(),
                publication_origin,
                publication_dict['title'],
                publication_dict['description'],
                publication_dict['published'],
                publication_dict['doi'],
                publication_authors,
                publication_dict['tags'],
                publication_dict['categories'],
                publication_links,
                publication_dict['journal'],
                publication_dict['volume']
            )
            GeneralPublication._ID_MANAGER.save()
            return general_publication
        except Exception as e:
            print(e)
            print(type(e))
