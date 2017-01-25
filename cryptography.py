def ord2(character,case):
    if case=='upper':
        beginning=ord('A')
    else:
        beginning=ord('a')
    return ord(character)-beginning

def chr2(number,case):
    if case=='upper':
        beginning=ord('A')
    else:
        beginning=ord('a')
    return chr(beginning+number)

def caeser_cipher(string,key):
    encrypted_string=""
    for character in string:
        if ord2(character,'upper')>=0 and ord2(character,'upper')<=25 or ord2(character,'lower')>=0 and ord2(character,'lower')<=25:
            if character.isupper():
                case='upper'
            else:
                case='lower'
            character=ord2(character,case)+key
            character%=26
            encrypted_string+=chr2(character,case)
        else:
            encrypted_string+=character
    return encrypted_string
                                  

            
