# reverse-shell-WordPress-pugin
Generates a wordpress plugin that will grant you a reverse shell once uploaded and navigated to. I loved wetw0rk's script (https://github.com/wetw0rk/malicious-wordpress-plugin), but I didn't want to use Meterpreter during my time preparing for the OSCP exam so I modified his to generate a reverse shell instead. Props go to wetw0rk. Not sure if the Windows functionality is there but it definitely works against Linux.
NOTE: For this to work, you must have Pentest monkey's PHP reverse shell in the /usr/share/webshells/php directory. Further, it needs to be named php-reverse-shell-unix.py.
