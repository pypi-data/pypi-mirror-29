# -*- coding: utf-8 -*-
# :Project:   PatchDB -- Main Makefile
# :Created:   mar 03 giu 2014 17:33:11 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2014, 2015, 2016, 2017 Lele Gaifax
#

.PHONY: all
all: test

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	-@find src tests -name '*~' -print0 | xargs -r0 rm

include Makefile.i18n
include Makefile.release
