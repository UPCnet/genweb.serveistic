#|/bin/bash
EXCLUDE="bin build develop-eggs eggs include lib local parts"
cd ../../..
~/bin/i18ndude rebuild-pot --pot genweb/serveistic/locales/genweb.serveistic.pot --create genweb.serveistic . --exclude "$EXCLUDE"

cd genweb/serveistic/locales/ca/LC_MESSAGES
~/bin/i18ndude sync --pot ../../genweb.serveistic.pot genweb.serveistic.po

cd ../../en/LC_MESSAGES
~/bin/i18ndude sync --pot ../../genweb.serveistic.pot genweb.serveistic.po

cd ../../es/LC_MESSAGES
~/bin/i18ndude sync --pot ../../genweb.serveistic.pot genweb.serveistic.po
