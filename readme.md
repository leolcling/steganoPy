# SteganoPy

Steganography is the art of hiding secret in plain sight. A message can be embedded into an image such that no one but the sender knows the existence of the message.

In this simple implementation, message is embedded in the least significant bits of the image. No encryption is supported yet. But because people won't even suspect that they are looking at a secret message, they won't even try to crack it.


## Usage

To hide message:
```shell
$ python steganoPy.py -m hide -i "path/to/image.png"
Enter the message you want to hide:
```
Specfic the message:
```shell
python steganoPy.py -m hide -i "path/to/image.png" -s "Secret message"

python steganoPy.py -m hide -i "path/to/image.png" -e "path/to/text/documents/to/hide.txt"
```

To reveal secret:
```shell
python steganoPy.py -m reveal -i "path/to/image.png" -d "path/to/output/secret.txt"
```

To see all options:
```shell
python steganoPy.py -help
```

