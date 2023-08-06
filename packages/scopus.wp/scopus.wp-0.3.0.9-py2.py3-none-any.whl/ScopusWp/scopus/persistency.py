from ScopusWp.database import MySQLDatabaseAccess

from ScopusWp.scopus.data import ScopusPublication, ScopusAuthorProfile, ScopusAuthor
from ScopusWp.scopus.data import from_dict, to_dict

from ScopusWp.config import PATH, Config

import json
import pathlib

import pickle
import os
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME, BigInteger, Table, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from ScopusWp.database import MySQLDatabase, get_or_create
from ScopusWp.util import IDManager

from jutil.database import *

BASE = declarative_base()


class ScopusMySQLDatabase(mysql_database_singleton(
    Config.get_instance()['MYSQL']['username'],
    Config.get_instance()['MYSQL']['password'],
    Config.get_instance()['MYSQL']['host'],
    '__scopus'
)):
    pass


publication_snapshot_junction = Table(
    'publication_snapshot_junction',
    BASE.metadata,
    Column('authorID', BigInteger, ForeignKey('author_snapshot.snapshotID'), primary_key=True),
    Column('scopusID', BigInteger, ForeignKey('publication.scopusID'), primary_key=True)
)


class Author(BASE):

    __tablename__ = 'author'

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(500))
    last_name = Column(String(500))
    h_index = Column(Integer)
    citation_count = Column(Integer)
    publications = Column(Text)
    document_count = Column(Integer)
    affiliation_country = Column(String(100))
    affiliation_city = Column(String(100))
    affiliation_name = Column(String(300))


class AuthorSnapshot(BASE):

    __tablename__ = 'author_snapshot'

    snapshotID = Column(BigInteger, primary_key=True)
    author_id = Column(BigInteger)
    first_name = Column(String(500))
    last_name = Column(String(500))
    affiliations = Column(Text)
    type = Column(String(100))

    publications = relationship(
        'Publication',
        secondary=publication_snapshot_junction,
        back_populates='authors'
    )


class Publication(BASE):

    __tablename__ = 'publication'

    scopusID = Column(BigInteger, primary_key=True)
    eid = Column(String(100))
    doi = Column(String(100))
    creator_id = Column(BigInteger, ForeignKey('author_snapshot.snapshotID'))
    title = Column(Text)
    description = Column(Text)
    journal = Column(String(500))
    volume = Column(String(100))
    date = Column(DATETIME)
    keywords = Column(Text)
    citations = Column(Text)

    creator = relationship(
        'AuthorSnapshot',
        uselist=False,
    )

    authors = relationship(
        'AuthorSnapshot',
        secondary=publication_snapshot_junction,
        back_populates='publications'
    )


class ScopusDatabaseController:

    def __init__(self):

        self.session = ScopusMySQLDatabase.get_session()  # type: Session

        self.author_id_manager = IDManager('author_snapshot')

    def insert_author_profile(self, author_profile):
        author = get_or_create(
            self.session,
            Author,
            id=author_profile.id,
            first_name=author_profile.first_name,
            last_name=author_profile.last_name,
            h_index=author_profile.h_index,
            citation_count=author_profile.citation_count,
            publications=json.dumps(author_profile.publications),
            document_count=author_profile.document_count,
            affiliation_country="",
            affiliation_city="",
            affiliation_name=""
        )
        self.session.commit()

    def contains_author_profile(self, author):
        return len(list(self.session.query(Author).filter(Author.id == int(author)))) != 0

    def select_author_profile(self, author_id):
        results = self.session.query(Author).filter(Author.id == int(author_id))
        author = results[0]

        author_profile = ScopusAuthorProfile(
            author.id,
            author.first_name,
            author.last_name,
            author.h_index,
            author.citation_count,
            author.document_count,
            json.loads(author.publications)
        )

        return author_profile

    def select_all_author_profiles(self):
        return self.session.query(Author).all()

    def insert_publication(self, publication):

        pub = Publication(
            scopusID=publication.id,
            eid=publication.eid,
            doi=publication.doi,
            title=publication.title,
            description=publication.description,
            journal=publication.journal,
            volume=publication.volume,
            date=datetime.datetime.strptime(publication.date, '%Y-%M-%d'),
            keywords=json.dumps(publication.keywords),
            citations=json.dumps(publication.citations)
        )

        creator_snapshot = get_or_create(
            self.session,
            AuthorSnapshot,
            author_id=publication.creator.id,
            first_name=publication.creator.first_name,
            last_name=publication.creator.last_name,
            affiliations=json.dumps(sorted(publication.creator.affiliations)),
            type='ScopusAuthor'
        )
        pub.creator = creator_snapshot

        author_snapshots, author_snapshots_remaining = sqlalchemy_many_list_tuple(
            self.session,
            AuthorSnapshot,
            publication.authors,
            lambda author: and_(AuthorSnapshot.author_id == int(author),
                                AuthorSnapshot.affiliations == json.dumps(sorted(author.affiliations))),
            lambda author: AuthorSnapshot(
                author_id=author.id,
                first_name=author.first_name,
                last_name=author.last_name,
                affiliations=json.dumps(sorted(author.affiliations)),
                type='ScopusAuthor'
            )
        )

        pub.authors = author_snapshots
        self.session.add(pub)

        self.session.commit()

    def _insert_author_snapshot(self, author):

        author_snapshot_id = self.author_id_manager.new()
        author_snapshot = get_or_create(
            self.session,
            AuthorSnapshot,
            id=author_snapshot_id,
            author_id=author.id,
            first_name=author.first_name,
            last_name=author.last_name,
            affiliations=json.dumps(sorted(author.affiliations)),
            type='ScopusAuthor'
        )

        return author_snapshot_id

    def _select_author_snapshot(self, snapshot_id):
        results = self.session.query(AuthorSnapshot).filter(AuthorSnapshot.snapshotID == snapshot_id)
        # Creating the actual ScopusAuthor object from that
        snapshot = results[0]  # type: AuthorSnapshot
        scopus_author = ScopusAuthor(
            snapshot.first_name,
            snapshot.last_name,
            snapshot.snapshotID,
            json.loads(snapshot.affiliations)
        )
        return scopus_author

    def insert_multiple_publications(self, publication_list):
        for publication in publication_list:
            self.insert_publication(publication)

    def contains_publication(self, publication):
        return len(list(self.session.query(Publication).filter(Publication.scopusID == int(publication))))

    def _scopus_author_from_snapshot(self, author_snapshot):
        return ScopusAuthor(
            author_snapshot.first_name,
            author_snapshot.last_name,
            author_snapshot.snapshotID,
            json.loads(author_snapshot.affiliations)
        )

    def select_publication(self, scopus_id):
        results = self.session.query(Publication).filter(Publication.scopusID == int(scopus_id))
        publication = results[0]
        # Loading the creator and the authors list from the snapshots database

        creator = self._scopus_author_from_snapshot(publication.creator)
        author_list = list(map(
            lambda x: self._scopus_author_from_snapshot(x),
            publication.authors
        ))

        # Creating an actual ScopusPublication object from that
        scopus_publication = ScopusPublication(
            publication.scopusID,
            publication.eid,
            publication.doi,
            publication.title,
            publication.description,
            publication.date,
            creator,
            author_list,
            json.loads(publication.citations),
            json.loads(publication.keywords),
            publication.journal,
            publication.volume
        )
        return scopus_publication

    def wipe(self):
        #self.session.query(Author).delete()
        self.session.execute('TRUNCATE TABLE publication_snapshot_junction')
        self.session.query(Publication).delete()
        self.session.query(AuthorSnapshot).delete()
        self.session.commit()

    def select_multiple_publications(self, scopus_id_list):
        publication_list = []
        for scopus_id in scopus_id_list:
            publication = self.select_publication(scopus_id)
            publication_list.append(publication)
        return publication_list

    def select_all_publications(self):
        return self.session.query(Publication).all()

    def select_all_publication_ids(self):
        return self.session.query(Publication.scopusID).all()

    def select_all_author_ids(self):
        return self.session.query(Author.id).all()

    def save(self):
        self.session.commit()
        self.author_id_manager.save()

if __name__ == '__main__':
    session = ScopusMySQLDatabase.get_session()
    BASE.metadata.drop_all(ScopusMySQLDatabase._engine)
    BASE.metadata.create_all(ScopusMySQLDatabase._engine)
