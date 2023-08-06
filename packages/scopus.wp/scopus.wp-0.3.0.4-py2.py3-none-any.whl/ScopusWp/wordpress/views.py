from ScopusWp.dat import GeneralPublication

from ScopusWp.wordpress.config import PATH

from jinja2 import Template

import pathlib


class PublicationCommentView:

    def __init__(self, general_publication):
        self.publication = general_publication  # type: GeneralPublication
        self.templates_path = pathlib.Path(PATH) / 'templates'

    def date(self):
        return self.publication.published

    def content(self):
        with (self.templates_path / 'comment.html').open(mode='r') as file:
            template_string = file.read()
            template = Template(template_string)
            a = template.render(
                authors=self.publication.authors,
                title=self.publication.title,
                journal=self.publication.journal,
                volume=self.publication.volume,
                year=self.publication.published.year,
            )
            return a


class PublicationPostView:

    def __init__(self, general_publication):
        self.publication = general_publication  # type: GeneralPublication
        self.templates_path = pathlib.Path(PATH) / 'templates'
        self.author_limit = 20

    def title(self):
        return self.publication.title.encode('utf-8')

    def date(self):
        return self.publication.published

    def slug(self):
        return str(self.publication.id)

    def content(self):
        with (self.templates_path / 'post.html').open(mode='r') as file:
            template_string = file.read()
            template = Template(template_string)
            return template.render(
                authors=self._authors(),
                journal=self.publication.journal,
                volume=self.publication.volume,
                year=self.publication.published.year,
                doi=self.publication.doi,
                description=self.publication.description,
                links=self._links()
            )

    def excerpt(self):
        return u''

    def tags(self):
        return self.publication.tags

    def categories(self):
        return self.publication.categories

    def _authors(self):
        author_list = []
        for author in self.publication.authors:
            try:
                author_list.append(author.index_name)
            # In case there is a index error, that means the first name of the author does not even contain a single
            # character in which case it is useless to even add this string to the list of authors
            except IndexError:
                continue
        if len(author_list) >= self.author_limit:
            author_list = author_list[:self.author_limit]
        return ', '.join(author_list)

    def _links(self):
        with (self.templates_path / 'button.html').open(mode='r') as file:
            template = Template(file.read())
            return template.render(
                doi=self.publication.doi
            )
