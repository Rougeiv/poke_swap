from datetime import datetime, timezone
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from hashlib import md5

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    user_id1_trades: so.Mapped[List['Trade']] = so.relationship(
        'Trade', foreign_keys="[Trade.user_id1]", back_populates='user', lazy=True)
    
    user_id2_trades: so.Mapped[List['Trade']] = so.relationship(
        'Trade', foreign_keys="[Trade.user_id2]", back_populates='user', lazy=True)

    inventory = so.relationship(
        'Pokemon', secondary='user_pokemon', back_populates='owners', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def get_trades(self):
        return Trade.query.filter((Trade.user_id1 == self.id) | (Trade.user_id2 == self.id)).all()
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class Trade(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    pokemon1: so.Mapped[str] = so.mapped_column(sa.String(32))
    pokemon2: so.Mapped[str] = so.mapped_column(sa.String(32))
    
    # Define user_id1 and user_id2 as foreign keys
    user_id1: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    user_id2: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)

    # Define the relationship with User for user_id1 and user_id2
    user1 = so.relationship('User', foreign_keys=[user_id1], back_populates='user_id1_trades')
    user2 = so.relationship('User', foreign_keys=[user_id2], back_populates='user_id2_trades')
    
    def __repr__(self):
        return '<Trade: {} gave {} <-> {} given by {}>'.format(self.user_id1, self.pokemon1, self.pokemon2, self.user_id2)

class Pokemon(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    pokedex_num: so.Mapped[int] = so.mapped_column(sa.Integer)
    name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True,
                                                unique=True)
    shiny: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    owners = so.relationship('User', secondary='user_pokemon', back_populates='inventory', lazy=True)
    def __repr__(self):
        return '<Pokemon {} {}>'.format(self.pokedex_num, self.name)

# association table to track which pokemon belong to which users
user_pokemon: so.Mapped[sa.Table] = db.Table('user_pokemon',
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('pokemon_id', sa.Integer, sa.ForeignKey('pokemon.id'), primary_key=True)
)