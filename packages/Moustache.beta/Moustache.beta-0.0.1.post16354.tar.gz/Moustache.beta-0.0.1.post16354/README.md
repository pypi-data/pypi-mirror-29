# Moustache

Moustache est un module de fusion documentaire ODT.


## Installation

### Docker 

 `docker run -p 5000:5000 gitlab.libriciel.fr:4567/libriciel/hackathon-2018-01/moustache:master`

### Ubuntu

Sur une distribution Ubuntu 16.04 LTS, voici la procédure à suivre :

```bash
apt update -y
apt install -y libreoffice libreoffice-script-provider-python curl libmagickwand-dev

curl https://bootstrap.pypa.io/get-pip.py | python3

pip3 install moustache
```

## Lancement

Avant tout lancement de Moustache, il faut lancer libreoffice en mode headless, sur le port 2002 :
```bash
soffice --headless --invisible --nologo --nodefault --nocrashreport --nolockcheck --norestore --nofirststartwizard --accept="socket,host=0,port=2002;urp;" &
```

Puis il suffira de lancer la commande :
```bash
moustache
```

Moustache sera ensuite accessible sur le port 5000.