#!/usr/bin/env python3
from cifl_auth_wrapper import cifl_auth

def main():
    credentials = cifl_auth.get_auth()
    print("Oauth Flow Complete, credentials successfully generated")
    print(credentials)


if __name__ == '__main__':
    main()
