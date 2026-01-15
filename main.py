from generateBlumPrimes import generate_aes_key
from encryption import AESEncryption
import click

@click.group()
def cli():
    pass

@cli.command(name="key-gen")
def key_gen():

    key = generate_aes_key()
    click.echo(f"Your key in hexidecimal: {key.hex()}")


@cli.command(name="encrypt")
@click.argument("key")
@click.argument("input_file", metavar="input-file")
@click.argument("output_dir", metavar="output-dir")
def encrypt(key, input_file, output_dir):

    aes = AESEncryption(bytes.fromhex(key))
    aes.encrypt(input_file, output_dir)

@cli.command(name="decrypt")
@click.argument("key")
@click.argument("input_file", metavar="input-file")
@click.argument("output_dir", metavar="output-dir")
def decrypt(key, input_file, output_dir):

    aes = AESEncryption(bytes.fromhex(key))
    aes.decrypt(input_file, output_dir)


if __name__=="__main__":

    cli()
