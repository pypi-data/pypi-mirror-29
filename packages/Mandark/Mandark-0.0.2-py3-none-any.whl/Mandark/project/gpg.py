import os
import gnupg
from pprint import pprint

class GPG:
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.gpghome = basedir
        self.gpg = gnupg.GPG(gnupghome=self.gpghome)
        self.email = 'test@test.com'
        self.password = 'test12345'

    def generate_key(self):
        input_data = self.gpg.gen_key_input(name_emil=self.email,
                                       passphrase=self.password)
        key = self.gpg.gen_key(input_data)
        return key

    def export_keys(self, key):
        ascii_armored_public_keys = self.gpg.export_keys(key)
        ascii_armored_private_keys = self.gpg.export_keys(key, True)
        with open(f'{self.email}.asc', 'w') as f:
            f.write(ascii_armored_public_keys)
            f.write(ascii_armored_private_keys)

    def import_keys(self, keyfile=f'{self.email}.asc'):
        key_data = open(keyfile).read()
        import_result = self.gpg.import_keys(key_data)
        pprint(import_result)

    def list_keys(self):
        public_keys = self.gpg.list_keys()
        private_keys = self.gpg.list_keys(True)
        print('public keys:')
        pprint(public_keys)
        print('private keys:')
        pprint(private_keys)

    def encrypt_string(self, unencrypted_string='Who are you? How did you get in my mind?'):  # noqa
        encrypted_data = self.gpg.encrypt(unencrypted_string, self.email)
        encrypted_string = str(encrypted_data)
        print('ok: ', encrypted_data.ok)
        print('status: ', encrypted_data.status)
        print('stderr: ', encrypted_data.stderr)
        print('unencrypted_string: ', unencrypted_string)
        print('encrypted_string: ', encrypted_string)
        return encrypted_string

    def decrypt_string(self, encrypted_string):
        unencrypted_string = 'Who are you? How did you get in my house?'
        encrypted_data = self.gpg.encrypt(unencrypted_string, self.email)
        encrypted_string = str(encrypted_data)
        decrypted_data = self.gpg.decrypt(encrypted_string,
                                          passphrase=self.password)
        print('ok: ', decrypted_data.ok)
        print('status: ', decrypted_data.status)
        print('stderr: ', decrypted_data.stderr)
        print('decrypted string: ', decrypted_data.data)
        return decrypted_data.data

    def encrypt_file(self, file='my-unencrypted.txt'):
        open(file, 'w').write('You need to Google Venn diagram.')
        with open('my-unencrypted.txt', 'rb') as f:
            status = self.gpg.encrypt_file(
                f, recipients=[self.email],
                output='my-encrypted.txt.gpg')

        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)
        return status.ok

    def decrypt_file(self, file='my-unencrypted.txt'):
        with open(file, 'rb') as f:
            status = self.gpg.decrypt_file(f, passphrase=self.password,
                                           output='my-decrypted.txt')

        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)
