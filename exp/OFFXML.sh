curl -v \
-H "SOAPAction: "urn:Belkin:service:basicevent:1#SetBinaryState"" \
-H "Content-Type: text/xml"
-data @OFF.xml \
-X POST http://192.168.1.115:49153/