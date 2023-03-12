import pypokedex

# helper for pypoke

pokemon_name = 'Garbodor'

try: 
    pokemon = pypokedex.get(name=pokemon_name)
    print(pokemon.name)
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