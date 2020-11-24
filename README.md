# password-manager-app
Simple password manager app developed using python.
App UI is built using kivy module and cryptography module is being used for storing passwords.
Buildozer packaged all python files to .apk file.

**Huge thanks to kivy, cryptography and buildozer developers and contributers**

About app:
Included functions: add password, edit login details, backup passwords, change encryption keys.
All passwords are locally saved in /data folder. No internet access needed.
Passwords are encrypted using fernet recipe and key derivation function is scrypt included in cryptography module.
