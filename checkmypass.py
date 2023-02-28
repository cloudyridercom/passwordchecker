import requests
import hashlib
import sys


def request_api_data(query_char):
    #Passing first 5 Characters from Password Hash to the API
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check the API try again.")
    return res

def get_password_leaks_count(hashes, hash_to_check):
    #Splitting the response into lines, separate hash value from count and check the tail of hash
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:  #check tail of the hash
            return count    #returns how many times password was hacked
    return 0            

def pwned_api_check(password):
    #Hashing the password and splitting the first 5 characters
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return get_password_leaks_count(response, tail)
    

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times, Change password')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'

if __name__ == '__main__': 
    sys.exit(main(sys.argv[1:])) #sys.exit in case sth. don't work to bring back to CommandLine
