from Crypto.PublicKey import RSA
from Crypto import Random
import os

def encode_crypt(str_src):
    home = os.path.expanduser('~')
    f = open('%s/.ssh/id_rsa.pub'%(home),'r')
    key = RSA.importKey(f.read())
    s = key.encrypt(str_src,1L) 
    return s

def decode_crypt(str_src):
    home = os.path.expanduser('~')
    f = open('%s/.ssh/id_rsa'%(home),'r')
    r = f.read()
    key = RSA.importKey(r)
    s1 = key.decrypt(str_src) 
    return s1

