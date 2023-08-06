from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME, BigInteger, Table, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from ScopusWp.database import MySQLDatabase, get_or_create
from ScopusWp.util import IDManager

from jutil.database import sqlalchemy_many_list_tuple, sqlalchemy_add_children
from jutil.processing import DictQuery

from ScopusWp.dat import GeneralPublication, PublicationAuthor, PublicationJournal, PublicationLink, PublicationOrigin
import datetime

from ScopusWp.database import BASE

from pprint import pprint


publication_author_junction = Table(
    'publication_author_junction',
    BASE.metadata,
    Column('authorID', BigInteger, ForeignKey('author.authorID'), primary_key=True),
    Column('publicationID', BigInteger, ForeignKey('publication.publicationID'), primary_key=True)
)

publication_tag_junction = Table(
    'publication_tag_junction',
    BASE.metadata,
    Column('publicationID', BigInteger, ForeignKey('publication.publicationID'), primary_key=True),
    Column('tagID', BigInteger, ForeignKey('tag.tagID'), primary_key=True)
)

publication_category_junction = Table(
    'publication_category_junction',
    BASE.metadata,
    Column('publicationID', BigInteger, ForeignKey('publication.publicationID'), primary_key=True),
    Column('CategoryID', BigInteger, ForeignKey('category.categoryID'), primary_key=True)
)

publication_citation_junction = Table(
    'publication_citation_junction',
    BASE.metadata,
    Column('publicationID', BigInteger, ForeignKey('publication.publicationID'), primary_key=True),
    Column('citationID', BigInteger, ForeignKey('publication.publicationID'), primary_key=True)
)


class Publication(BASE):

    __tablename__ = 'publication'

    publicationID = Column(BigInteger, primary_key=True)
    doi = Column(String(200))
    title = Column(String(500))
    description = Column(Text)
    published = Column(DATETIME)
    originID = Column(BigInteger, ForeignKey('origin.originID'))
    journalID = Column(BigInteger, ForeignKey('journal.journalID'))

    origin = relationship(
        'Origin',
        uselist=False,
        back_populates='publication'
    )
    journal = relationship(
        'Journal',
        uselist=False,
        back_populates='publications'
    )
    links = relationship(
        'Link',
        back_populates='publication'
    )
    authors = relationship(
        "Author",
        secondary=publication_author_junction,
        back_populates='publications'
    )
    categories = relationship(
        'Category',
        secondary=publication_category_junction,
        back_populates='publications'
    )
    tags = relationship(
        'Tag',
        secondary=publication_tag_junction,
        back_populates='publications'
    )
    citedby = relationship(
        'Publication',
        secondary=publication_citation_junction,
        primaryjoin='Publication.publicationID == publication_citation_junction.c.publicationID',
        secondaryjoin='Publication.publicationID == publication_citation_junction.c.citationID'
    )

    def add_citation(self, publication):
        if publication not in self.citedby:
            self.citedby.append(publication)


class Author(BASE):

    __tablename__ = 'author'

    authorID = Column(BigInteger, index=True, primary_key=True)
    first_name = Column(String(500))
    last_name = Column(String(500))

    publications = relationship(
        'Publication',
        secondary=publication_author_junction,
        back_populates='authors'
    )


class Tag(BASE):

    __tablename__ = 'tag'

    tagID = Column(BigInteger, primary_key=True)
    content = Column(String(500))

    publications = relationship(
        'Publication',
        secondary=publication_tag_junction,
        back_populates='tags'
    )


class Journal(BASE):

    __tablename__ = 'journal'

    journalID = Column(BigInteger, primary_key=True)
    name = Column(String(200))
    volume = Column(String(200))

    publications = relationship(
        'Publication',
        back_populates='journal'
    )


class Category(BASE):

    __tablename__ = 'category'

    categoryID = Column(BigInteger, primary_key=True)
    content = Column(String(500))

    publications = relationship(
        'Publication',
        secondary=publication_category_junction,
        back_populates='categories'
    )


class Origin(BASE):

    __tablename__ = 'origin'

    originID = Column(BigInteger, primary_key=True)
    id = Column(String(100))
    typeID = Column(Integer, ForeignKey('type.typeID'))
    text = Column(Text)

    publication = relationship(
        'Publication',
        back_populates='origin'
    )
    type = relationship(
        'OriginType',
        back_populates='origins'
    )


class Link(BASE):

    __tablename__ = 'link'

    linkID = Column(BigInteger, primary_key=True)
    name = Column(String(200))
    href = Column(String(200))
    publicationID = Column(BigInteger, ForeignKey('publication.publicationID'))

    publication = relationship(
        'Publication',
        back_populates='links'
    )


class OriginType(BASE):

    __tablename__ = 'type'

    typeID = Column(Integer, primary_key=True)
    name = Column(String(100))

    origins = relationship(
        'Origin',
        back_populates='type'
    )


class PublicationRegister:

    def __init__(self):

        """
        self.id_managers = {
            'origin': IDManager('origin'),
            'publication': IDManager('publication'),
            'author': IDManager('author'),
            'link': IDManager('link'),
            'tag': IDManager('tag'),
            'category': IDManager('category'),
        }
        """

        self.session = MySQLDatabase.get_session()

        self.publication_id_manager = IDManager('general_publication')
        self.remaining_citations = {}

        self.publication_processor = PublicationInserter(self)

    def insert(self, publication_dict):

        self.publication_processor.set(publication_dict)
        publication, remaining_citations = self.publication_processor.process()
        self.remaining_citations.update(remaining_citations)

        self.session.add(publication)
        self.session.commit()

    def contains_publication(self, publication_dict):
        query = self.session.query(Publication)\
                    .join(Publication.origin, aliased=True).filter_by(id=publication_dict['origin']['id'])\
                    .join(Origin.type).filter_by(name=publication_dict['origin']['name'])
        return len(list(query)) != 0

    def select(self, publication_id):
        publication = self.session.query(Publication).get(publication_id)
        return GeneralPublication.from_model(publication)

    def select_origin(self, name, text=None):
        if text is None:
            query = self.session.query(Publication)\
                        .join(Publication.origin)\
                        .join(OriginType).filter_by(name=name)
        else:
            query = self.session.query(Publication) \
                .join(Publication.origin).filter_by(text=text) \
                .join(OriginType).filter_by(name=name)
        publications = list(query)
        return list(map(lambda x: GeneralPublication.from_model(x), publications))

    def query(self, model_class, filter_statement):
        return list(self.session.query(model_class).filter(filter_statement))

    def wipe(self):
        self.session.query(Link).delete()
        self.session.execute('TRUNCATE TABLE publication_author_junction')
        self.session.execute('TRUNCATE TABLE publication_category_junction')
        self.session.execute('TRUNCATE TABLE publication_tag_junction')
        self.session.execute('TRUNCATE TABLE publication_citation_junction')
        self.session.query(Publication).delete()
        self.session.query(Tag).delete()
        self.session.query(Category).delete()
        self.session.query(Author).delete()
        self.session.query(Origin).delete()
        self.session.query(Journal).delete()
        self.session.commit()


class PublicationInserter(DictQuery):

    def __init__(self, register):
        DictQuery.__init__(self)
        self.session = register.session
        self.id_manager = register.publication_id_manager
        self.publication = None

        self.remaining_citations = {}

    def query_exception(self, query, query_dict, default):
        return default

    def process(self):
        self.publication = Publication(
            publicationID=self.id_manager.new(),
            doi=self.query_dict('doi', ''),
            title=self.query_dict('title', ''),
            description=self.query_dict('description', ''),
            published=self.query_dict('published', datetime.datetime.now())
        )

        self.publication.origin = self.origin()
        self.publication.journal = self.journal()
        self.publication.links = self.links()
        sqlalchemy_add_children(self.publication.tags, self.tags())
        sqlalchemy_add_children(self.publication.authors, self.authors())
        sqlalchemy_add_children(self.publication.categories, self.categories())
        for publication in self.citations():
            print(publication.origin.id)
            self.publication.add_citation(publication)

        self.id_manager.save()

        return self.publication, self.remaining_citations

    def origin(self):
        # Getting the origin type
        origin_type = self.session.query(OriginType).filter(
            OriginType.name == self.query_dict('origin/name', '')
        ).first()
        return Origin(
            id=self.query_dict('origin/id', 0),
            text=self.query_dict('origin/text', ''),
            type=origin_type
        )

    def journal(self):

        journal_tuple = (
            self.query_dict('journal', ''),
            self.query_dict('volume', '')
        )

        # The many list tuple function returns a tuple, of which the first item is a list with all the model objects
        # corresponding to the parameter list given (in this cae only the one constructed tuple) either by getting
        # them from the db or constructing a new Model object
        return sqlalchemy_many_list_tuple(
            self.session,
            Journal,
            [journal_tuple],
            lambda x: and_(Journal.name == x[0], Journal.volume == x[1]),
            lambda x: Journal(name=x[0], volume=x[1])
        )[0][0]  # The corresponding model object to the one constructed above must be the first item of this first list

    def links(self):
        # The links are unique to each publication, which means they all have to be constructed from scratch.
        # Each item of the links list is a dict again with the info about the link name and the actual url
        return list(map(
            lambda link: Link(
                name=link['name'],
                href=link['href']
            ),
            self.query_dict('links', [])
        ))

    def authors(self):
        authors, authors_remaining = sqlalchemy_many_list_tuple(
            self.session,
            Author,
            self.query_dict('authors', []),
            lambda author: and_(
                Author.first_name == author['first_name'],
                Author.last_name == author['last_name']
            ),
            lambda author: Author(
                first_name=author['first_name'],
                last_name=author['last_name']
            )
        )
        return authors

    def tags(self):
        tags, tags_remaining = sqlalchemy_many_list_tuple(
            self.session,
            Tag,
            self.query_dict('tags', []),
            lambda tag: Tag.content == tag,
            lambda tag: Tag(content=tag)
        )
        return tags

    def categories(self):
        categories, categories_remaining = sqlalchemy_many_list_tuple(
            self.session,
            Category,
            self.query_dict('categories', []),
            lambda category: Category.content == category,
            lambda category: Category(content=category)
        )
        return categories

    def citations(self):
        citations, remaining_publications = sqlalchemy_many_list_tuple(
            self.session,
            Publication,
            self.query_dict('citations', []),
            lambda origin_dict: self.citations_filter_function(origin_dict),
            lambda origin_dict: {(origin_dict['id'], origin_dict['name']): self.publication.publicationID}
        )
        for item in remaining_publications:
            self.remaining_citations.update(item)
        return list(filter(lambda x: not isinstance(x, dict), citations))

    @staticmethod
    def citations_filter_function(origin_dict):
        return and_(
            Publication.origin.has(id=origin_dict['id']),
            Origin.type.has(name=origin_dict['name'])
        )


if __name__ == '__main__':
    r = PublicationRegister()
    BASE.metadata.drop_all(MySQLDatabase._engine)
    MySQLDatabase.create_database(BASE)

