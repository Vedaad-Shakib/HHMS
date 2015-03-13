##########HHMS Setup##########

###Installing Dependencies###
mkdir ./temp;

#Installing Python#
hdiutil mount python-2.7.8-macosx10.6.dmg;
cp /Volumes/Python\ 2.7.8/Python.mpkg/ ./temp;
hdiutilunmount"/Volumes/Python 2.7.8"
open ./temp/Python.mpkg;

#Installing Pip#
sudo python get-pip.py;

#Installing PycURL#
pip install pycurl;

#Installing Beautiful Soup 4#
pip install beautifulsoup4;

#Installing Django#
pip install Django==1.7.6;

#Installing django_extensions#
pip install django-extensions;

#Installing Homebrew#
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)";

#Installing MySQL#
brew install mysql;
unset TMPDIR;
mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp;
sudo mv /usr/local/opt/mysql/my-new.cnf /usr/local/opt/mysql/my.cnf;
cp `brew --prefix mysql`/homebrew.mxcl.mysql.plist ~/Library/LaunchAgents/;
launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist;

rm -rf ./temp