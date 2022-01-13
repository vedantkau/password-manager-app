# password-manager-app

**Huge thanks to kivy, cryptography and buildozer developers and contributers**

Simple password manager app developed using python. App UI is built using kivy module and cryptography module is being used for encrypting username-password data. Buildozer packaged all python files to .apk file.
**The app is in development phase.**  

**App functions:**  
Add/Store username-password 
Edit login details  
Backup username-password data  
Change encryption keys   
Quickly add/store username-password

Username-passowrd data is encrypted using AES algorithm and Scrpt is key derivation method. As Scrypt is CPU intensive, it takes some time to login. Username-password can be quickly added without login to app (master password is still required for this).   
Encrypted data is locally saved in /data folder. No internet access needed.
