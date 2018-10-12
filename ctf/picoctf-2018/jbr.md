### James Brahm Returns
*Cryptography - 700*

#### Problem Statement
Dr. Xernon has finally approved an update to James Brahm's spy terminal. (Someone finally told them that ECB isn't secure.) Fortunately, CBC mode is safe! Right? Connect with `nc 2018shell1.picoctf.com 22666`. 
[source](https://2018shell1.picoctf.com/static/7858d9aeeba4938ed586cbef2931d6a9/source.py)

Hint: What killed SSL3?

#### Research

Googling the hint, we come across the POODLE attack. Apparently, this problem uses a weak form of encryption (AES CBC) that we can exploit to get the flag. However, there wasn't good literature on exactly how to implement this attack.

Eventually, I came across this [article](https://www.voidsecurity.in/2014/12/the-padding-oracle-in-poodle.html) which detailed the attack in more depth. The following explanation is derived from this article.

#### Attack
First to understand this exploit, its important to understand how CBC (Cipher Block Chaining) works. 

![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)

The value of the previous ciphertext is xored with our plaintext before AES. Thus, when decrypting, we get something that looks like this.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/CBC_decryption.svg/601px-CBC_decryption.svg.png)

There are two parts to our attack. First, we must align the blocks such that there is one full block of padding. Next, we replace our padding block with one of our previous ciphertext blocks that we want to decode.

<img src="data:image/png;base64,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" />
*Red is padding block, blue is block we want to decode*

Crucial to our exploit is `verify_mac(message)`. 
The only way this function verifies our message is if the original padding scheme remains, where 16 bytes are removed. If 16 bytes are removed, we know that the last byte of our decrypted text is going to be `10 = 0x1` because of how `check_padding` works.

We also know the value of the last byte of the ciphertext that is xored with the plaintext. It's the last byte in the 2nd to last block! Thus, the output of our decrypted blue block should be `0x1 ^ blocks[-2][-1]`. Remember that we're not done! This value still needs to be xored one more time. To finish, we xor this value with the last value of the block behind our blue block to arrive at plaintext.

Overall, we extract plaintext by calculating `0x1 ^ blocks[-2][-1] ^ prevBlock[-1]`. By shifting around the padding, we can extract more and more characters. 

Note that we can only extract plaintext when `verify_mac` returns true. Because IV is randomized, there is a 1/256 chance that this attack works everytime. By brute forcing, we can eventually extract the entire plaintext.