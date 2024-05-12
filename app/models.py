from datetime import datetime, timezone
from typing import List, Optional
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    user_id1_trades: so.Mapped['Trade'] = so.relationship(
        'Trade', foreign_keys="[Trade.user_id1]", back_populates='user1', lazy=True)
    
    user_id2_trades: so.Mapped['Trade'] = so.relationship(
        'Trade', foreign_keys="[Trade.user_id2]", back_populates='user2', lazy=True)

    inventory = so.relationship(
        'Pokemon', secondary='user_pokemon', back_populates='owners', lazy=True)

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def get_trades(self):   
        return Trade.query.filter((Trade.user_id1 == self.id) | (Trade.user_id2 == self.id)).all()
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

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

class Trade(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    # Define pokemon_id1 and pokemon_id2 as foreign keys
    pokemon_id1: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Pokemon.id, name='fk_trade_pokemon_id1'), index=True)
    pokemon_id2: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Pokemon.id, name='fk_trade_pokemon_id2'), index=True)
    
    # Define the relationship with Pokemon for pokemon_id1 and pokemon_id2
    pokemon1 = so.relationship('Pokemon', foreign_keys=[pokemon_id1])
    pokemon2 = so.relationship('Pokemon', foreign_keys=[pokemon_id2])

    # Define user_id1 and user_id2 as foreign keys
    user_id1: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id, name='fk_trade_user_id1'), index=True)
    user_id2: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(User.id, name='fk_trade_user_id2'), index=True)

    # Define the relationship with User for user_id1 and user_id2
    user1 = so.relationship('User', foreign_keys=[user_id1], back_populates='user_id1_trades')
    user2 = so.relationship('User', foreign_keys=[user_id2], back_populates='user_id2_trades')

    def __repr__(self):
        # Get usernames of the users involved in the trade
        user1_name = self.user1.username if self.user1 else 'Unknown User'
        user2_name = self.user2.username if self.user2 else 'Unknown User'

        # Get names of the Pokemon involved in the trade
        pokemon1_name = self.pokemon1.name if self.pokemon1 else 'Unknown Pokemon'
        pokemon2_name = self.pokemon2.name if self.pokemon2 else 'Unknown Pokemon'

        return '<Trade: {user1_name} traded {pokemon1_name} <-> {user2_name} traded {pokemon2_name}>'