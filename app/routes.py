from urllib.parse import urlsplit
from flask import flash, render_template, request, redirect, session, jsonify, url_for, current_app
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from datetime import datetime, timezone
from app.models import User, Pokemon, Trade
from app.forms import EditProfileForm, LoginForm, SignUpForm
from sqlalchemy.sql.expression import func
import sqlalchemy.orm as orm
from flask_wtf import CSRFProtect
from datetime import datetime, timedelta
import os
from app.blueprints import main
from app import db


@main.route('/')
@main.route('/index')
# @login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    offset = (page - 1) * per_page

    # Aliases for Pokemon to use in joins
    Pokemon1 = orm.aliased(Pokemon)
    Pokemon2 = orm.aliased(Pokemon)

    # Query for trading data with proper joins, now with ascending order
    trades_query = db.session.query(
        Trade.id,
        Trade.timestamp,
        Pokemon1.name.label('pokemon1_name'),
        Pokemon2.name.label('pokemon2_name')
    ).join(
        Pokemon1, Trade.pokemon_id1 == Pokemon1.id
    ).join(
        Pokemon2, Trade.pokemon_id2 == Pokemon2.id
    ).filter(
        Trade.user_id2 == None
    ).order_by(Trade.timestamp.asc())

    # Manual pagination handling
    total_count = trades_query.count()
    trades = trades_query.offset(offset).limit(per_page).all()
    total_pages = (total_count + per_page - 1) // per_page

    trade_offers = [{
        'trade_id': trade.id,
        'timestamp': trade.timestamp.strftime('%Y-%m-%d %H:%M'),
        'pokemon1_name': trade.pokemon1_name.lower(),
        'pokemon2_name': trade.pokemon2_name.lower()
    } for trade in trades]

    return render_template('index.html', trade_offers=trade_offers, page=page, total_pages=total_pages)



@main.route('/trade/<int:trade_id>')
@login_required
def trade(trade_id):
    # Fetch the trade details from the database using the trade_id
    Pokemon1 = orm.aliased(Pokemon)
    Pokemon2 = orm.aliased(Pokemon)

    trade = db.session.query(
        Trade.id,
        Trade.timestamp,
        User.username.label('user1'),
        Trade.user_id1,
        Pokemon1.name.label('pokemon1_name'),
        Pokemon2.name.label('pokemon2_name')
    ).join(
        Pokemon1, Trade.pokemon_id1 == Pokemon1.id
    ).join(
        Pokemon2, Trade.pokemon_id2 == Pokemon2.id
    ).join(
        User, Trade.user_id1 == User.id
    ).filter(
        Trade.id == trade_id
    ).first()

    if not trade:
        flash('Trade not found.')
        return redirect(url_for('index'))

    return render_template('trade.html', trade=trade)


@main.route('/accept_trade/<int:trade_id>', methods=['POST'])
@login_required
def accept_trade(trade_id):
    trade = db.session.query(Trade).filter_by(id=trade_id).first()
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    # Check if the current user owns the requested Pokémon
    requested_pokemon = db.session.query(Pokemon).filter_by(id=trade.pokemon_id2).first()
    if requested_pokemon not in current_user.inventory:
        return jsonify({'error': 'You do not own the Pokémon the user is requesting'}), 403
    
    try:
        # Add the current user as user_id2 in the trade
        trade.user_id2 = current_user.id
        
        # Update the inventory of both users
        user1 = db.session.query(User).filter_by(id=trade.user_id1).first()
        user2 = current_user
        
        # User1 gets Pokemon2 and loses Pokemon1
        if trade.pokemon1 in user1.inventory:
            user1.inventory.remove(trade.pokemon1)
        if trade.pokemon2 not in user1.inventory:
            user1.inventory.append(trade.pokemon2)
        
        # User2 gets Pokemon1 and loses Pokemon2
        if trade.pokemon2 in user2.inventory:
            user2.inventory.remove(trade.pokemon2)
        if trade.pokemon1 not in user2.inventory:
            user2.inventory.append(trade.pokemon1)
        
        db.session.commit()
        return jsonify({'success': 'Trade accepted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(location=url_for('main.index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(location=url_for('main.login'))
    return render_template('signup.html', title='SignUp', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(location=url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)

        # Check for expired trades
        three_days_ago = datetime.now() - timedelta(days=3)
        expired_trades = db.session.query(Trade).filter(
            Trade.user_id1 == user.id,
            Trade.user_id2 == None,
            Trade.timestamp < three_days_ago
        ).all()

        expired_count = 0
        for trade in expired_trades:
            offered_pokemon = db.session.query(Pokemon).filter_by(id=trade.pokemon_id1).first()
            if offered_pokemon:
                if offered_pokemon not in user.inventory:
                    user.inventory.append(offered_pokemon)
                db.session.delete(trade)
                expired_count += 1

        db.session.commit()

        if expired_count > 0:
            flash(f'{expired_count} expired trade(s) were deleted and Pokémon returned to your inventory.', 'info')

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(location=url_for('main.index'))

@main.route('/catch')
def catch():
    # Check if user is logged in
    if current_user.is_anonymous:
        return redirect(location=url_for('main.login'))
    return render_template('catch.html')

@main.route('/gacha_one_pull', methods=['POST'])
def gacha_one_pull():
    try:
        if current_user.coins >= 3:
            # first get pokemon already owned by user
            # owned_pokemon_ids = [pokemon.id for pokemon in current_user.inventory]
            # .filter(sa.not_(Pokemon.id.in_(owned_pokemon_ids)))
            pquery = sa.select(Pokemon).order_by(func.random()).limit(1)
            random_pokemon = db.session.scalar(pquery)
            if random_pokemon is None:
                return jsonify({'error': 'No Pokémon found'}), 404, {'Content-Type': 'application/json'}

            pokemon_data = {
            'id': random_pokemon.id,
            'pokemon_id': random_pokemon.pokedex_num,
            'name': random_pokemon.name
            }

            # first check if the user already has the pokemon
            if random_pokemon in current_user.inventory:
                main.logger.debug('User %s already has Pokémon %s', current_user.username, random_pokemon.name)
                # take 1 coin away from the user
                current_user.coins -= 1
            else:
                # Assign the Pokémon to the user's inventory
                current_user.inventory.append(random_pokemon)
                main.logger.debug('Assigned Pokémon %s to user %s', random_pokemon.name, current_user.username)
                main.logger.debug('Response Data: %s', jsonify({'pokemon_data': pokemon_data}))
                # take 3 coins away from the user
                current_user.coins -= 3
            db.session.commit()

            # Generate the URL for the Pokémon image
            pokemon_image_url = f'/static/images/pokemon_gen4_sprites/{random_pokemon.name.lower()}.png'

            # return jsonify(pokemon_data), 200, {'Content-Type': 'application/json'}
            return jsonify({'coins': current_user.coins, 'pokemon_name': random_pokemon.name, 'pokemon_image_url': pokemon_image_url}), 200, {'Content-Type': 'application/json'}
        else:
            # Return an error response if the user doesn't have enough coins
            return jsonify({'error': 'Insufficient coins'}), 403, {'Content-Type': 'application/json'}
    except Exception as e:
        main.logger.error('An error occurred: %s', str(e))
        return jsonify({'error': str(e)}), 500, {'Content-Type': 'application/json'}
    
@main.route('/gacha_ten_pull', methods=['POST'])
def gacha_ten_pull():
    try:
        if current_user.coins >= 10:
            # first get pokemon already owned by user
            # owned_pokemon_ids = [pokemon.id for pokemon in current_user.inventory]
            # randomly select 10 pokemon that the user doesnt own already
            # .filter(sa.not_(Pokemon.id.in_(owned_pokemon_ids)))
            pquery = sa.select(Pokemon).order_by(func.random()).limit(10)
            random_pokemon = db.session.execute(pquery)
            if random_pokemon is None:
                return jsonify({'error': 'No Pokémon found'}), 404, {'Content-Type': 'application/json'}
            
            # Prepare a list to hold the random Pokémon data
            random_pokemon_list = []

            # Loop through each randomly selected Pokémon
            for tuple_entry in random_pokemon:
                pokemon = tuple_entry[0]
                pokemon_data = {
                    'id': pokemon.id,
                    'pokedex_num': pokemon.pokedex_num,
                    'name': pokemon.name
                }
                random_pokemon_list.append(pokemon_data)
                
                # first check if the user already has the pokemon
                if pokemon in current_user.inventory:
                    current_app.logger.debug('User %s already has Pokémon %s', current_user.username, pokemon.name)
                else:
                    # Assign the Pokémon to the user's inventory
                    current_user.inventory.append(pokemon)
                    current_app.logger.debug('Assigned Pokémon %s to user %s', pokemon.name, current_user.username)
                    current_app.logger.debug('Response Data: %s', jsonify({'pokemon_list': random_pokemon_list}))
            # take 10 coins away from the user
            current_user.coins -= 10
            # Commit the changes to the database
            db.session.commit()
            # Return the list of randomly selected Pokémon as JSON
            return jsonify({'coins': current_user.coins, 'pokemon_list': random_pokemon_list}), 200, {'Content-Type': 'application/json'}
     
        else:
            # Return an error response if the user doesn't have enough coins
            return jsonify({'error': 'Insufficient coins'}), 403, {'Content-Type': 'application/json'}
    except Exception as e:
        # return jsonify({'error exception': str(e)}), 500, {'Content-Type': 'application/json'}
        current_app.logger.error('An error occurred: %s', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@main.route('/my_trades', methods=['GET'])
def my_trades():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    offset = (page - 1) * per_page

    Pokemon1 = orm.aliased(Pokemon)
    Pokemon2 = orm.aliased(Pokemon)

    # Query for active trades
    active_trades_query = db.session.query(
        Trade.id,
        Trade.timestamp,
        Pokemon1.name.label('pokemon1_name'),
        Pokemon2.name.label('pokemon2_name')
    ).join(
        Pokemon1, Trade.pokemon_id1 == Pokemon1.id
    ).join(
        Pokemon2, Trade.pokemon_id2 == Pokemon2.id
    ).filter(
        Trade.user_id1 == current_user.id,
        Trade.user_id2 == None
    ).order_by(Trade.timestamp.asc())

    active_trades = [{
        'trade_id': trade.id, 
        'timestamp': trade.timestamp.strftime('%Y-%m-%d %H:%M'), 
        'pokemon1_name': trade.pokemon1_name.lower(), 
        'pokemon2_name': trade.pokemon2_name.lower()
    } for trade in active_trades_query.all()]

    # Query for completed trades with pagination
    past_trades_query = db.session.query(
        Trade.id,
        Trade.timestamp,
        Pokemon1.name.label('pokemon1_name'),
        Pokemon2.name.label('pokemon2_name')
    ).join(
        Pokemon1, Trade.pokemon_id1 == Pokemon1.id
    ).join(
        Pokemon2, Trade.pokemon_id2 == Pokemon2.id
    ).filter(
        Trade.user_id1 == current_user.id,
        Trade.user_id2 != None
    ).order_by(Trade.timestamp.asc())

    total_count = past_trades_query.count()
    past_trades = [{
        'trade_id': trade.id, 
        'timestamp': trade.timestamp.strftime('%Y-%m-%d %H:%M'), 
        'pokemon1_name': trade.pokemon1_name.lower(), 
        'pokemon2_name': trade.pokemon2_name.lower()
    } for trade in past_trades_query.offset(offset).limit(per_page).all()]

    total_pages = (total_count + per_page - 1) // per_page

    return render_template('my_trades.html', active_trades=active_trades, past_trades=past_trades, page=page, total_pages=total_pages)

@main.route('/delete_trade/<int:trade_id>', methods=['POST'])
@login_required
def delete_trade(trade_id):
    try:
        # Fetch the trade to be deleted
        trade = db.session.query(Trade).filter_by(id=trade_id, user_id1=current_user.id, user_id2=None).first()
        if not trade:
            flash('Trade not found or already completed.', 'danger')
            return redirect(url_for('my_trades'))

        # Fetch the Pokémon being offered
        offered_pokemon = db.session.query(Pokemon).filter_by(id=trade.pokemon_id1).first()
        
        if not offered_pokemon:
            flash('Offered Pokémon not found.', 'danger')
            return redirect(url_for('my_trades'))

        # Check if the user already owns the Pokémon
        if offered_pokemon not in current_user.inventory:
            # Add the Pokémon back to the user's inventory
            current_user.inventory.append(offered_pokemon)

        # Delete the trade
        db.session.delete(trade)
        db.session.commit()

        flash('Trade offer deleted and Pokémon returned to your inventory.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')
    
    return redirect(url_for('my_trades'))


@login_required
@main.route('/trade_offer', methods=['POST', 'GET'])
def trade_offer():
    # Using SQLAlchemy ORM to fetch Pokémon names owned by the logged-in user
    if current_user.is_authenticated:
        try:
            sprite_folder = os.path.join(current_app.static_folder, 'images', 'pokemon_gen4_sprites')

            # Ensure the sprite folder exists
            if not os.path.exists(sprite_folder):
                current_app.logger.error(f"Sprite folder does not exist: {sprite_folder}")
                flash(f"error: Sprite folder does not exist: {sprite_folder}")
                pokemon_sprites = []
            else:
                pokemon_sprites = [f[:-4] for f in os.listdir(sprite_folder) if f.endswith('.png')]  # Removes '.png'
                # app.logger.info(f"Loaded Pokémon sprites: {pokemon_sprites}")
        except Exception as e:
            current_app.logger.error(f"Failed to load Pokémon sprites: {e}")
            pokemon_sprites = []
        # Fetch the Pokémon IDs for the logged-in user
        inventory_pokemon = current_user.inventory

        pokemon_names = [pokemon.name.lower() for pokemon in inventory_pokemon]

        return render_template('trade_offer.html', pokemon_sprites=pokemon_sprites, pokemon_owned=pokemon_names, current_user_id=current_user.id)
    else:
        return redirect(location=url_for('main.login'))

@main.route('/post_trade', methods=['POST'])
@login_required
def post_trade():
    pokemon_name1 = request.form.get('pokemon_name1')
    pokemon_name2 = request.form.get('pokemon_name2')
    timestamp = datetime.now()  # Uses the datetime object directly

    try:
        # Check the number of active trades for the user
        active_trades_count = db.session.query(Trade).filter_by(user_id1=current_user.id, user_id2=None).count()
        
        if active_trades_count >= 3:
            return jsonify({'error': 'You have reached the maximum number of active trades.'}), 403

        # Resolve Pokémon names to IDs using SQLAlchemy
        pokemon1 = Pokemon.query.filter_by(name=pokemon_name1).first()
        pokemon2 = Pokemon.query.filter_by(name=pokemon_name2).first()

        if not pokemon1 or not pokemon2:
            return jsonify({'error': 'One or both Pokémon names are invalid.'}), 404

        print("Received names:", pokemon_name1, pokemon_name2)

        # Ensure the user owns the Pokémon they are offering
        if pokemon1 not in current_user.inventory:
            return jsonify({'error': 'You do not own the Pokémon you are offering.'}), 403

        # Remove the offered Pokémon from the user's inventory
        current_user.inventory.remove(pokemon1)

        # Insert the new trade into the trade table
        new_trade = Trade(
            timestamp=timestamp,
            user_id1=current_user.id,
            user_id2=None,  # Assuming this is an offer waiting for another user to accept
            pokemon_id1=pokemon1.id,
            pokemon_id2=pokemon2.id
        )

        db.session.add(new_trade)

        # when a user posts a trade, they get +3 coins
        current_user.coins += 3
        
        db.session.commit()
        flash('Your post is now live!')
        return jsonify({'success': 'Trade posted successfully!'}), 200
        # return redirect(url_for('main.index'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/update_sprite_selection', methods=['POST'])
def update_sprite_selection():
    sprite_src = request.form['sprite']
    # Update session or database with the new sprite selection
    # e.g., session['selected_sprite'] = sprite_src
    return jsonify(success=True)


@main.route('/how_to_play')
def how_to_play():
    return render_template('how_to_play.html')
# user profile page route
@main.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    trades = [
        {'pokemon1': 'Pikachu', 'pokemon2': 'Charmander', 'timestamp': '2021-01-01', 'user_id1': 1, 'user_id2': 2},
        {'pokemon1': 'Bulbasaur', 'pokemon2': 'Squirtle', 'timestamp': '2021-01-02', 'user_id1': 1, 'user_id2': 2}
        ]
    return render_template('user.html', user=user, trades=trades)

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(location=url_for('main.user', username=form.username.data))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500