import pypokedex

# helper for pypokedex

pokemon_name = ' Glalie  '

try: 
    pokemon = pypokedex.get(name=pokemon_name.strip())
    print(pokemon.name.capitalize())
    print(pokemon.types)
    print(pokemon.abilities)
    print(pokemon.weight)
    print(pokemon.base_stats)
except:
    print("not a pokemon")


move_name = 'Sludge Bomb'
try:
    move = pypokedex.get(name=move_name)
    print(move.name)
    print(move.type)
    print(move.power)
    print(move.accuracy)
    print(move.pp)
except:
    print("not a move")