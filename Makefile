SRCDIR:=${CURDIR}
INSTDIR:=/usr/local/src/RestXMPP
CONFDIR:=/etc/xmpp
SERVDIR:=/usr/lib/systemd/system
SERVFILE:=restxmpp.service


install:
	@echo ${SRCDIR}
	@mkdir -p ${INSTDIR}
	@cp -rf ${SRCDIR}/* ${INSTDIR}
	chmod -R 755 ${INSTDIR}/bin
	@mkdir -p -m 755 ${CONFDIR}
	@mkdir -p ${SERVDIR}
	@cp -rf ${INSTDIR}/promiscuous/${SERVFILE} ${SERVDIR}
	@rm -rf ${INSTDIR}/promiscuous

clean:
	rm -rf ${INSTDIR}
	@rm -rf ${SERVDIR}/${SERVFILE}

