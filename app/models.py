from datetime import datetime, timezone
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    trades: so.WriteOnlyMapped[List['Trade']] = so.relationship(
        backref='user', lazy=True)
    
    inventory: so.Mapped[List['Pokemon']] = so.relationship(
        'Pokemon', backref='owner', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Trade(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    pokemon1: so.Mapped[str] = so.mapped_column(sa.String(32))
    pokemon2: so.Mapped[str] = so.mapped_column(sa.String(32))
    
    # Define user_id1 and user_id2 as foreign keys
    user_id1: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    user_id2: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return '<Trade {} gave {} <-> {} given by {}>'.format(self.user_id1).format(self.pokemon1).format(self.pokemon2).format(self.user_id2)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# one User can have many pokemon and each pokemon is unique to a user
class Pokemon(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    pokedex_num: so.Mapped[int] = so.mapped_column(sa.Integer)
    name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True,
                                                unique=True)
    shiny: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"))

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))