from datetime import datetime, timezone
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

# # Define association table for the many-to-many relationship
# trade_association_table = db.Table(
#     'trade_association',
#     db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
#     db.Column('trade_id', db.ForeignKey('trade.id'), primary_key=True),
#     sa.UniqueConstraint('trade_id', 'user_id')  # Constraint for exactly 2 users per trade
# )

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    inventory: so.Mapped[List['Pokemon']] = so.relationship()

    trades: so.WriteOnlyMapped[List['Trade']] = so.relationship(
        back_populates='user_id1')

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

    # Define relationships with the User table
    user1: so.Mapped[User] = so.relationship('User', foreign_keys=[user_id1], back_populates='trades')
    user2: so.Mapped[User] = so.relationship('User', foreign_keys=[user_id2], back_populates='trades')

    def __repr__(self):
        return '<Trade {} <-> {}>'.format(self.gave).format(self.received)

# one User can have many pokemon and each pokemon is unique to a user
class Pokemon(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    pokedex_num: so.Mapped[int] = so.mapped_column(sa.Integer)
    name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True,
                                                unique=True)
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"))

