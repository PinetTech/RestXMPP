# RestXMPP - Restful XMPP Client

## The Purpose of RestXMPP

RestXMPP is a http restful XMPP client that aims to provide these functions:

1. Login XMPP server using the configured jabber name and password
2. Auto allow any friend requests
3. Register a new Jabber user if requested
4. Provide a set of rest api to provde the roster and message functions of XMPP
5. Provide a callback mechanism to callback certain script when message arrived (should be a customized iq element) 

## Before Start

You should have these configurations setup to run this client:

1. An XMPP server running
2. A work jabber id or let XMPP server to create a new jabber user
3. Configure RestXMPP to connect to the ip and port to the XMPP server
4. Configure the host and port that RestXMPP http service to listen to
5. Configure the control port that RestXMPP listen(to control the server)

## Management

To start the client, you just need to run command:
    
    ./bin/xmpp start

To stop the client, this command:
    
    ./bin/xmpp stop

To view the status, this command:

    ./bin/xmpp status
