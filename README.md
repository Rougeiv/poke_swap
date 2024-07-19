# CITS3403 Project

## Team Members

- @AarifLamat (Aarif Lamat) 23628374
- @Rougeiv (Nicholas Mulyawan) 23044774
- @HeathenH (Harrsion Harun) 23347644
- @ricccooo (Enrico Tionandra ) 23732436


### Frontend

- [Bootstrap](https://getbootstrap.com/) for responsive styling

#### Backend

- [alembic] for database migrations
- [unittest] for unit tests

## Database

- To generate a migration run `flask db migrate -m "<message>"`.
- To initialise and apply migrations to the database run `flask db upgrade`.

## How To Run

Create a virtual environment using 
``` 
python3 -m venv poke-venv
 ```

Activate the virtual environment using the following command depending on your OS

Linux: 
``` source poke-venv/bin/activate ```
Windows cmd: 
``` poke-venv\Scripts\activate ```
Windows PowerShell: 
``` poke-venv\Scripts\Activate.ps1 ```

Once in the virtual environment run: 
``` 
pip install -r requirements.txt
 ```

Create the database using: 
``` 
flask db upgrade
 ```

Create a .env file that contains 
``` SECRET_KEY=example-secret-key ```

### Setting up the Database
For the application to function the db requires a little set up.

run:
``` $ flask shell ```

once in the shell run the following:
```
 original_pokemon_data = [
    {"pokedex_num": 1, "name": "Bulbasaur", "shiny": False, "sprite_path": "path_to_bulbasaur_sprite.png"},
    {"pokedex_num": 2, "name": "Ivysaur", "shiny": False, "sprite_path": "path_to_ivysaur_sprite.png"},
    {"pokedex_num": 3, "name": "Venusaur", "shiny": False, "sprite_path": "path_to_venusaur_sprite.png"},
    {"pokedex_num": 4, "name": "Charmander", "shiny": False, "sprite_path": "path_to_charmander_sprite.png"},
    {"pokedex_num": 5, "name": "Charmeleon", "shiny": False, "sprite_path": "path_to_charmeleon_sprite.png"},
    {"pokedex_num": 6, "name": "Charizard", "shiny": False, "sprite_path": "path_to_charizard_sprite.png"},
    {"pokedex_num": 7, "name": "Squirtle", "shiny": False, "sprite_path": "path_to_squirtle_sprite.png"},
    {"pokedex_num": 8, "name": "Wartortle", "shiny": False, "sprite_path": "path_to_wartortle_sprite.png"},
    {"pokedex_num": 9, "name": "Blastoise", "shiny": False, "sprite_path": "path_to_blastoise_sprite.png"},
    {"pokedex_num": 10, "name": "Caterpie", "shiny": False, "sprite_path": "path_to_caterpie_sprite.png"},
    {"pokedex_num": 11, "name": "Metapod", "shiny": False, "sprite_path": "path_to_metapod_sprite.png"},
    {"pokedex_num": 12, "name": "Butterfree", "shiny": False, "sprite_path": "path_to_butterfree_sprite.png"},
    {"pokedex_num": 13, "name": "Weedle", "shiny": False, "sprite_path": "path_to_weedle_sprite.png"},
    {"pokedex_num": 14, "name": "Kakuna", "shiny": False, "sprite_path": "path_to_kakuna_sprite.png"},
    {"pokedex_num": 15, "name": "Beedrill", "shiny": False, "sprite_path": "path_to_beedrill_sprite.png"},
    {"pokedex_num": 16, "name": "Pidgey", "shiny": False, "sprite_path": "path_to_pidgey_sprite.png"},
    {"pokedex_num": 17, "name": "Pidgeotto", "shiny": False, "sprite_path": "path_to_pidgeotto_sprite.png"},
    {"pokedex_num": 18, "name": "Pidgeot", "shiny": False, "sprite_path": "path_to_pidgeot_sprite.png"},
    {"pokedex_num": 19, "name": "Rattata", "shiny": False, "sprite_path": "path_to_rattata_sprite.png"},
    {"pokedex_num": 20, "name": "Raticate", "shiny": False, "sprite_path": "path_to_raticate_sprite.png"},
    {"pokedex_num": 21, "name": "Spearow", "shiny": False, "sprite_path": "path_to_spearow_sprite.png"},
    {"pokedex_num": 22, "name": "Fearow", "shiny": False, "sprite_path": "path_to_fearow_sprite.png"},
    {"pokedex_num": 23, "name": "Ekans", "shiny": False, "sprite_path": "path_to_ekans_sprite.png"},
    {"pokedex_num": 24, "name": "Arbok", "shiny": False, "sprite_path": "path_to_arbok_sprite.png"},
    {"pokedex_num": 25, "name": "Pikachu", "shiny": False, "sprite_path": "path_to_pikachu_sprite.png"},
    {"pokedex_num": 26, "name": "Raichu", "shiny": False, "sprite_path": "path_to_raichu_sprite.png"},
    {"pokedex_num": 27, "name": "Sandshrew", "shiny": False, "sprite_path": "path_to_sandshrew_sprite.png"},
    {"pokedex_num": 28, "name": "Sandslash", "shiny": False, "sprite_path": "path_to_sandslash_sprite.png"},
    {"pokedex_num": 29, "name": "Nidoran-f", "shiny": False, "sprite_path": "path_to_nidoran_female_sprite.png"},
    {"pokedex_num": 30, "name": "Nidorina", "shiny": False, "sprite_path": "path_to_nidorina_sprite.png"},
    {"pokedex_num": 31, "name": "Nidoqueen", "shiny": False, "sprite_path": "path_to_nidoqueen_sprite.png"},
    {"pokedex_num": 32, "name": "Nidoran-m", "shiny": False, "sprite_path": "path_to_nidoran_male_sprite.png"},
    {"pokedex_num": 33, "name": "Nidorino", "shiny": False, "sprite_path": "path_to_nidorino_sprite.png"},
    {"pokedex_num": 34, "name": "Nidoking", "shiny": False, "sprite_path": "path_to_nidoking_sprite.png"},
    {"pokedex_num": 35, "name": "Clefairy", "shiny": False, "sprite_path": "path_to_clefairy_sprite.png"},
    {"pokedex_num": 36, "name": "Clefable", "shiny": False, "sprite_path": "path_to_clefable_sprite.png"},
    {"pokedex_num": 37, "name": "Vulpix", "shiny": False, "sprite_path": "path_to_vulpix_sprite.png"},
    {"pokedex_num": 38, "name": "Ninetales", "shiny": False, "sprite_path": "path_to_ninetales_sprite.png"},
    {"pokedex_num": 39, "name": "Jigglypuff", "shiny": False, "sprite_path": "path_to_jigglypuff_sprite.png"},
    {"pokedex_num": 40, "name": "Wigglytuff", "shiny": False, "sprite_path": "path_to_wigglytuff_sprite.png"},
    {"pokedex_num": 41, "name": "Zubat", "shiny": False, "sprite_path": "path_to_zubat_sprite.png"},
    {"pokedex_num": 42, "name": "Golbat", "shiny": False, "sprite_path": "path_to_golbat_sprite.png"},
    {"pokedex_num": 43, "name": "Oddish", "shiny": False, "sprite_path": "path_to_oddish_sprite.png"},
    {"pokedex_num": 44, "name": "Gloom", "shiny": False, "sprite_path": "path_to_gloom_sprite.png"},
    {"pokedex_num": 45, "name": "Vileplume", "shiny": False, "sprite_path": "path_to_vileplume_sprite.png"},
    {"pokedex_num": 46, "name": "Paras", "shiny": False, "sprite_path": "path_to_paras_sprite.png"},
    {"pokedex_num": 47, "name": "Parasect", "shiny": False, "sprite_path": "path_to_parasect_sprite.png"},
    {"pokedex_num": 48, "name": "Venonat", "shiny": False, "sprite_path": "path_to_venonat_sprite.png"},
    {"pokedex_num": 49, "name": "Venomoth", "shiny": False, "sprite_path": "path_to_venomoth_sprite.png"},
    {"pokedex_num": 50, "name": "Diglett", "shiny": False, "sprite_path": "path_to_diglett_sprite.png"},
    {"pokedex_num": 51, "name": "Dugtrio", "shiny": False, "sprite_path": "path_to_dugtrio_sprite.png"},
    {"pokedex_num": 52, "name": "Meowth", "shiny": False, "sprite_path": "path_to_meowth_sprite.png"},
    {"pokedex_num": 53, "name": "Persian", "shiny": False, "sprite_path": "path_to_persian_sprite.png"},
    {"pokedex_num": 54, "name": "Psyduck", "shiny": False, "sprite_path": "path_to_psyduck_sprite.png"},
    {"pokedex_num": 55, "name": "Golduck", "shiny": False, "sprite_path": "path_to_golduck_sprite.png"},
    {"pokedex_num": 56, "name": "Mankey", "shiny": False, "sprite_path": "path_to_mankey_sprite.png"},
    {"pokedex_num": 57, "name": "Primeape", "shiny": False, "sprite_path": "path_to_primeape_sprite.png"},
    {"pokedex_num": 58, "name": "Growlithe", "shiny": False, "sprite_path": "path_to_growlithe_sprite.png"},
    {"pokedex_num": 59, "name": "Arcanine", "shiny": False, "sprite_path": "path_to_arcanine_sprite.png"},
    {"pokedex_num": 60, "name": "Poliwag", "shiny": False, "sprite_path": "path_to_poliwag_sprite.png"},
    {"pokedex_num": 61, "name": "Poliwhirl", "shiny": False, "sprite_path": "path_to_poliwhirl_sprite.png"},
    {"pokedex_num": 62, "name": "Poliwrath", "shiny": False, "sprite_path": "path_to_poliwrath_sprite.png"},
    {"pokedex_num": 63, "name": "Abra", "shiny": False, "sprite_path": "path_to_abra_sprite.png"},
    {"pokedex_num": 64, "name": "Kadabra", "shiny": False, "sprite_path": "path_to_kadabra_sprite.png"},
    {"pokedex_num": 65, "name": "Alakazam", "shiny": False, "sprite_path": "path_to_alakazam_sprite.png"},
    {"pokedex_num": 66, "name": "Machop", "shiny": False, "sprite_path": "path_to_machop_sprite.png"},
    {"pokedex_num": 67, "name": "Machoke", "shiny": False, "sprite_path": "path_to_machoke_sprite.png"},
    {"pokedex_num": 68, "name": "Machamp", "shiny": False, "sprite_path": "path_to_machamp_sprite.png"},
    {"pokedex_num": 69, "name": "Bellsprout", "shiny": False, "sprite_path": "path_to_bellsprout_sprite.png"},
    {"pokedex_num": 70, "name": "Weepinbell", "shiny": False, "sprite_path": "path_to_weepinbell_sprite.png"},
    {"pokedex_num": 71, "name": "Victreebel", "shiny": False, "sprite_path": "path_to_victreebel_sprite.png"},
    {"pokedex_num": 72, "name": "Tentacool", "shiny": False, "sprite_path": "path_to_tentacool_sprite.png"},
    {"pokedex_num": 73, "name": "Tentacruel", "shiny": False, "sprite_path": "path_to_tentacruel_sprite.png"},
    {"pokedex_num": 74, "name": "Geodude", "shiny": False, "sprite_path": "path_to_geodude_sprite.png"},
    {"pokedex_num": 75, "name": "Graveler", "shiny": False, "sprite_path": "path_to_graveler_sprite.png"},
    {"pokedex_num": 76, "name": "Golem", "shiny": False, "sprite_path": "path_to_golem_sprite.png"},
    {"pokedex_num": 77, "name": "Ponyta", "shiny": False, "sprite_path": "path_to_ponyta_sprite.png"},
    {"pokedex_num": 78, "name": "Rapidash", "shiny": False, "sprite_path": "path_to_rapidash_sprite.png"},
    {"pokedex_num": 79, "name": "Slowpoke", "shiny": False, "sprite_path": "path_to_slowpoke_sprite.png"},
    {"pokedex_num": 80, "name": "Slowbro", "shiny": False, "sprite_path": "path_to_slowbro_sprite.png"},
    {"pokedex_num": 81, "name": "Magnemite", "shiny": False, "sprite_path": "path_to_magnemite_sprite.png"},
    {"pokedex_num": 82, "name": "Magneton", "shiny": False, "sprite_path": "path_to_magneton_sprite.png"},
    {"pokedex_num": 83, "name": "Farfetchd", "shiny": False, "sprite_path": "path_to_farfetchd_sprite.png"},
    {"pokedex_num": 84, "name": "Doduo", "shiny": False, "sprite_path": "path_to_doduo_sprite.png"},
    {"pokedex_num": 85, "name": "Dodrio", "shiny": False, "sprite_path": "path_to_dodrio_sprite.png"},
    {"pokedex_num": 86, "name": "Seel", "shiny": False, "sprite_path": "path_to_seel_sprite.png"},
    {"pokedex_num": 87, "name": "Dewgong", "shiny": False, "sprite_path": "path_to_dewgong_sprite.png"},
    {"pokedex_num": 88, "name": "Grimer", "shiny": False, "sprite_path": "path_to_grimer_sprite.png"},
    {"pokedex_num": 89, "name": "Muk", "shiny": False, "sprite_path": "path_to_muk_sprite.png"},
    {"pokedex_num": 90, "name": "Shellder", "shiny": False, "sprite_path": "path_to_shellder_sprite.png"},
    {"pokedex_num": 91, "name": "Cloyster", "shiny": False, "sprite_path": "path_to_cloyster_sprite.png"},
    {"pokedex_num": 92, "name": "Gastly", "shiny": False, "sprite_path": "path_to_gastly_sprite.png"},
    {"pokedex_num": 93, "name": "Haunter", "shiny": False, "sprite_path": "path_to_haunter_sprite.png"},
    {"pokedex_num": 94, "name": "Gengar", "shiny": False, "sprite_path": "path_to_gengar_sprite.png"},
    {"pokedex_num": 95, "name": "Onix", "shiny": False, "sprite_path": "path_to_onix_sprite.png"},
    {"pokedex_num": 96, "name": "Drowzee", "shiny": False, "sprite_path": "path_to_drowzee_sprite.png"},
    {"pokedex_num": 97, "name": "Hypno", "shiny": False, "sprite_path": "path_to_hypno_sprite.png"},
    {"pokedex_num": 98, "name": "Krabby", "shiny": False, "sprite_path": "path_to_krabby_sprite.png"},
    {"pokedex_num": 99, "name": "Kingler", "shiny": False, "sprite_path": "path_to_kingler_sprite.png"},
    {"pokedex_num": 100, "name": "Voltorb", "shiny": False, "sprite_path": "path_to_voltorb_sprite.png"},
    {"pokedex_num": 101, "name": "Electrode", "shiny": False, "sprite_path": "path_to_electrode_sprite.png"},
    {"pokedex_num": 102, "name": "Exeggcute", "shiny": False, "sprite_path": "path_to_exeggcute_sprite.png"},
    {"pokedex_num": 103, "name": "Exeggutor", "shiny": False, "sprite_path": "path_to_exeggutor_sprite.png"},
    {"pokedex_num": 104, "name": "Cubone", "shiny": False, "sprite_path": "path_to_cubone_sprite.png"},
    {"pokedex_num": 105, "name": "Marowak", "shiny": False, "sprite_path": "path_to_marowak_sprite.png"},
    {"pokedex_num": 106, "name": "Hitmonlee", "shiny": False, "sprite_path": "path_to_hitmonlee_sprite.png"},
    {"pokedex_num": 107, "name": "Hitmonchan", "shiny": False, "sprite_path": "path_to_hitmonchan_sprite.png"},
    {"pokedex_num": 108, "name": "Lickitung", "shiny": False, "sprite_path": "path_to_lickitung_sprite.png"},
    {"pokedex_num": 109, "name": "Koffing", "shiny": False, "sprite_path": "path_to_koffing_sprite.png"},
    {"pokedex_num": 110, "name": "Weezing", "shiny": False, "sprite_path": "path_to_weezing_sprite.png"},
    {"pokedex_num": 111, "name": "Rhyhorn", "shiny": False, "sprite_path": "path_to_rhyhorn_sprite.png"},
    {"pokedex_num": 112, "name": "Rhydon", "shiny": False, "sprite_path": "path_to_rhydon_sprite.png"},
    {"pokedex_num": 113, "name": "Chansey", "shiny": False, "sprite_path": "path_to_chansey_sprite.png"},
    {"pokedex_num": 114, "name": "Tangela", "shiny": False, "sprite_path": "path_to_tangela_sprite.png"},
    {"pokedex_num": 115, "name": "Kangaskhan", "shiny": False, "sprite_path": "path_to_kangaskhan_sprite.png"},
    {"pokedex_num": 116, "name": "Horsea", "shiny": False, "sprite_path": "path_to_horsea_sprite.png"},
    {"pokedex_num": 117, "name": "Seadra", "shiny": False, "sprite_path": "path_to_seadra_sprite.png"},
    {"pokedex_num": 118, "name": "Goldeen", "shiny": False, "sprite_path": "path_to_goldeen_sprite.png"},
    {"pokedex_num": 119, "name": "Seaking", "shiny": False, "sprite_path": "path_to_seaking_sprite.png"},
    {"pokedex_num": 120, "name": "Staryu", "shiny": False, "sprite_path": "path_to_staryu_sprite.png"},
    {"pokedex_num": 121, "name": "Starmie", "shiny": False, "sprite_path": "path_to_starmie_sprite.png"},
    {"pokedex_num": 122, "name": "Mr-Mime", "shiny": False, "sprite_path": "path_to_mr_mime_sprite.png"},
    {"pokedex_num": 123, "name": "Scyther", "shiny": False, "sprite_path": "path_to_scyther_sprite.png"},
    {"pokedex_num": 124, "name": "Jynx", "shiny": False, "sprite_path": "path_to_jynx_sprite.png"},
    {"pokedex_num": 125, "name": "Electabuzz", "shiny": False, "sprite_path": "path_to_electabuzz_sprite.png"},
    {"pokedex_num": 126, "name": "Magmar", "shiny": False, "sprite_path": "path_to_magmar_sprite.png"},
    {"pokedex_num": 127, "name": "Pinsir", "shiny": False, "sprite_path": "path_to_pinsir_sprite.png"},
    {"pokedex_num": 128, "name": "Tauros", "shiny": False, "sprite_path": "path_to_tauros_sprite.png"},
    {"pokedex_num": 129, "name": "Magikarp", "shiny": False, "sprite_path": "path_to_magikarp_sprite.png"},
    {"pokedex_num": 130, "name": "Gyarados", "shiny": False, "sprite_path": "path_to_gyarados_sprite.png"},
    {"pokedex_num": 131, "name": "Lapras", "shiny": False, "sprite_path": "path_to_lapras_sprite.png"},
    {"pokedex_num": 132, "name": "Ditto", "shiny": False, "sprite_path": "path_to_ditto_sprite.png"},
    {"pokedex_num": 133, "name": "Eevee", "shiny": False, "sprite_path": "path_to_eevee_sprite.png"},
    {"pokedex_num": 134, "name": "Vaporeon", "shiny": False, "sprite_path": "path_to_vaporeon_sprite.png"},
    {"pokedex_num": 135, "name": "Jolteon", "shiny": False, "sprite_path": "path_to_jolteon_sprite.png"},
    {"pokedex_num": 136, "name": "Flareon", "shiny": False, "sprite_path": "path_to_flareon_sprite.png"},
    {"pokedex_num": 137, "name": "Porygon", "shiny": False, "sprite_path": "path_to_porygon_sprite.png"},
    {"pokedex_num": 138, "name": "Omanyte", "shiny": False, "sprite_path": "path_to_omanyte_sprite.png"},
    {"pokedex_num": 139, "name": "Omastar", "shiny": False, "sprite_path": "path_to_omastar_sprite.png"},
    {"pokedex_num": 140, "name": "Kabuto", "shiny": False, "sprite_path": "path_to_kabuto_sprite.png"},
    {"pokedex_num": 141, "name": "Kabutops", "shiny": False, "sprite_path": "path_to_kabutops_sprite.png"},
    {"pokedex_num": 142, "name": "Aerodactyl", "shiny": False, "sprite_path": "path_to_aerodactyl_sprite.png"},
    {"pokedex_num": 143, "name": "Snorlax", "shiny": False, "sprite_path": "path_to_snorlax_sprite.png"},
    {"pokedex_num": 144, "name": "Articuno", "shiny": False, "sprite_path": "path_to_articuno_sprite.png"},
    {"pokedex_num": 145, "name": "Zapdos", "shiny": False, "sprite_path": "path_to_zapdos_sprite.png"},
    {"pokedex_num": 146, "name": "Moltres", "shiny": False, "sprite_path": "path_to_moltres_sprite.png"},
    {"pokedex_num": 147, "name": "Dratini", "shiny": False, "sprite_path": "path_to_dratini_sprite.png"},
    {"pokedex_num": 148, "name": "Dragonair", "shiny": False, "sprite_path": "path_to_dragonair_sprite.png"},
    {"pokedex_num": 149, "name": "Dragonite", "shiny": False, "sprite_path": "path_to_dragonite_sprite.png"},
    {"pokedex_num": 150, "name": "Mewtwo", "shiny": False, "sprite_path": "path_to_mewtwo_sprite.png"},
    {"pokedex_num": 151, "name": "Mew", "shiny": False, "sprite_path": "path_to_mew_sprite.png"}
]
```
```
for pokemon_data in original_pokemon_data:
    pokemon = Pokemon(
        pokedex_num=pokemon_data['pokedex_num'],
        name=pokemon_data['name'],
        shiny=pokemon_data['shiny'],
        sprite_path=pokemon_data['sprite_path']
    )
    db.session.add(pokemon)
db.session.commit()
```

## Running tests
for unit tests:
```
python tests/unit.py
```
for selenium tests:
```
python test.py`
```
