from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os.path

def decrypt_rsa(cpvt_key, spub_key, esym_key, sign):
    pkey_rsa = RSA.importKey(cpvt_key.decode('base64'))
    cipher = PKCS1_OAEP.new(pkey_rsa)
    symkey = cipher.decrypt(esym_key.decode('base64'))

    #Verify the signature
    pkey_rsa = RSA.importKey(spub_key.decode('base64'))
    hash_val = SHA256.new(esym_key)
    verifier = PKCS1_v1_5.new(pkey_rsa)
    if verifier.verify(hash_val, sign.decode('base64')):
        return symkey

    print 'Verification Check Failed: Please update the RSA Private Key'
    return None

def add_pad(msg):
    BLOCK_SIZE = 16
    msgLen = len(msg)
    modLen = BLOCK_SIZE - (msgLen%16)
    padChar = str(modLen)
    if(msgLen%16==0):
        padChar='0'

    if(modLen==10):
        padChar='a'
    elif(modLen==11):
        padChar='b'
    elif(modLen==12):
        padChar='c'
    elif(modLen==13):
        padChar='d'
    elif(modLen==14):
        padChar='e'
    elif(modLen==15):
        padChar='f'

    pad = modLen*padChar
    newMsg = msg+pad
    return newMsg

def remove_pad(msg):
    msgLen=len(msg)
    rmLen=msg[msgLen-1]
    if(msg[msgLen-1]=='a'):
        rmLen=10
    elif(msg[msgLen-1]=='b'):
        rmLen=11
    elif(msg[msgLen-1]=='c'):
        rmLen=12
    elif(msg[msgLen-1]=='d'):
        rmLen=13
    elif(msg[msgLen-1]=='e'):
        rmLen=14
    elif(msg[msgLen-1]=='f'):
        rmLen=15
    else:
        rmLen=int(msg[msgLen-1])

    if(rmLen==0):
        rmLen=16
    newMsg= msg[:(len(msg)-rmLen)]
    return newMsg

def sym_encrypt_query(symkey, qs):
    padded_text = add_pad(qs)

    #encrypt message
    aes_obj = AES.new(symkey.decode('base64'), AES.MODE_ECB)
    ciph = aes_obj.encrypt(padded_text)
    enc_qs = ciph.encode('base64').rstrip()
    return enc_qs

def sym_decrypt_resp(symkey, enc_res):
    aes_obj = AES.new(symkey.decode('base64'), AES.MODE_ECB)
    dec = aes_obj.decrypt(enc_res.decode('base64'))
    response = remove_pad(dec)
    return response
