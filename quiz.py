from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do? ## there you go, problem solved.
message = b'gAAAAABcmQWIgyomS-18ntnb8O_1O_HTV240Y_hXIwct4KJkKsv' \
          b'ukUU5E0W6XTnMjM7fkRcm6hoZ20yYevs0_i_QXILePYExDockhyJw9NZy' \
          b'RoUrxZllTlYmPmkutcQoKiwB1Aedgwq7COEoyfJCqgHlWcZoClqJLsESGBMOAbD' \
          b'Vo3wkoH166F2W1Np_o6cOsCg-aNKaBWIU'


def main():
    print('test')
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ != "__main__":
    main()
