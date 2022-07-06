import random
import string

def PasswordGenerator():

    lower_letters =  list(string.ascii_lowercase)
    upper_letters = list(string.ascii_uppercase)
    nums = list(string.digits)
    Special_Characters = ['!','@','#','$','%','^','&']

    all_characters = lower_letters + upper_letters + nums + Special_Characters

    random_letter = random.choice(lower_letters)
    random_upper = random.choice(upper_letters)
    random_num = random.choice(nums)
    random_special = random.choice(Special_Characters)
    
    passwd = [random_letter ,random_upper ,random_num ,random_special]

    for i in range(6):
        passwd.append(random.choice(all_characters))

    password = ''

    return password.join(passwd)



