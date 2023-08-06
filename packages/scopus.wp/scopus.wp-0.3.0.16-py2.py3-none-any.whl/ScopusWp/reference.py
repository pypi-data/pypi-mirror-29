from ScopusWp.config import PATH, PROJECT_PATH
from ScopusWp.config import Config

from ScopusWp.database import MySQLDatabaseAccess

from ScopusWp.dat import GeneralPublication
from ScopusWp.util import IDManager

import datetime

import json
import pathlib

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from ScopusWp.database import MySQLDatabase, get_or_create
from ScopusWp.util import IDManager

Base = declarative_base()


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class PublicationReference(Base):

    __tablename__ = 'publication_reference'

    id = Column(BigInteger, primary_key=True)
    wordpress_id = Column(BigInteger)
    scopus_id = Column(BigInteger)
    update_datetime = Column(DATETIME)
    post_datetime = Column(DATETIME)


class CommentReference(Base):

    __tablename__ = 'comment_reference'

    id = Column(BigInteger, primary_key=True)
    wordpress_post_id = Column(BigInteger)
    wordpress_comment_id = Column(BigInteger)
    external_id = Column(BigInteger)
    type = Column(Integer)
    posted_datetime = Column(DATETIME)


class ReferenceType(Base):

    __tablename__ = 'reference_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))


class ReferenceController:

    def __init__(self):

        self.publication_reference_id_manager = IDManager('reference')
        self.session = MySQLDatabase.get_session()  # type: Session

    def select_reference(self, internal_id):
        return self.session.query(PublicationReference).filter(PublicationReference.id == internal_id)[0]

    def select_all_references(self):
        """
        Returns a list of tuples, where each tuple represents one entry in the reference database, with the first
        item being the internal id for the publication, the second being the wordpress id and the third being the
        scopus id for the publication.

        :return: A list of tuples with three items each
        """
        return list(self.session.query(PublicationReference).all())

    def insert_reference(self, internal_id, wordpress_id, scopus_id):
        ref = get_or_create(
            self.session,
            PublicationReference,
            id=internal_id,
            wordpress_id=wordpress_id,
            scopus_id=scopus_id,
            update_datetime=datetime.datetime.strptime('0001-01-01', '%Y-%M-%d'),
            post_datetime=datetime.datetime.now()
        )
        self.session.commit()

    def insert_comment_reference(self, internal_id, wordpress_post_id, wordpress_comment_id, scopus_id):
        """
        Inserts a new comment reference into the comment reference database

        :param internal_id: The internally created id for the post
        :param wordpress_post_id: The id of the wordpress post, the comment is added to
        :param wordpress_comment_id: The comment id specifically
        :param scopus_id: The scopus id of the publication on which the comment is based on
        :return: void
        """
        ref = get_or_create(
            self.session,
            CommentReference,
            id=internal_id,
            wordpress_post_id=wordpress_post_id,
            wordpress_comment_id=wordpress_comment_id,
            external_id=scopus_id,
            type=1,
            posted_datetime=datetime.datetime.now()
        )
        self.session.commit()

    def select_comment_reference_list_py_post(self, wordpress_post_id):
        """
        Gets a list of all the comment references for the post specified by the wordpress id

        :param wordpress_post_id: The int id of the wordpress post
        :return: [(internal id, post id, comment id, scopus id)]
        """
        return list(self.session.query(CommentReference).filter(CommentReference.wordpress_post_id==wordpress_post_id))

    def insert_publication(self, publication, wordpress_id, scopus_id):
        assert isinstance(publication, GeneralPublication)

        self.insert_reference(publication.id, wordpress_id, scopus_id)

    # TODO: This is not separation of concerns, what is this doing here
    def publication_from_scopus(self, scopus_publication):
        # Getting an id from the id manager
        publication_id = self.publication_reference_id_manager.new()

        # Creating the publication object
        publication = GeneralPublication.from_scopus_publication(scopus_publication, publication_id)
        return publication

    def select_post_reference_by_scopus(self, scopus_id):
        """
        Select the reference by the scopus id.

        :param scopus_id: The int scopus id
        :return: (internal id, wordpress id, scopus id)
        """
        return list(
            self.session.query(PublicationReference).filter(
                PublicationReference.scopus_id == scopus_id
            )
        )

    def select_post_reference_by_wordpress(self, wordpress_post_id):
        """
        Select the reference by the wordpress id of the post.

        :param wordpress_post_id: The int wordpress id
        :return: (internal id, wordpress id, scopus id)
        """
        return list(
            self.session.query(PublicationReference).filter(
                PublicationReference.wordpress_id == wordpress_post_id
            )
        )

    def wipe(self):
        self.session.query(PublicationReference).delete()
        self.session.query(CommentReference).delete()
        self.session.commit()

    def close(self):
        self.publication_reference_id_manager.save()