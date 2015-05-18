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

## Dependencies

RestXMPP depends below libraries to provde the function:

1. [cement](http://builtoncement.com/): This awesome framework provides a very nice(indeeded) cli application development foundation
2. [sleekxmpp](https://github.com/fritzy/SleekXMPP): This framework provdes the foundations of XMPP services
3. [requests](http://docs.python-requests.org/en/latest/index.html): This framework provids the http requests apis
4. [pydns](http://pydns.sourceforge.net/): The dns resolving library used by [sleekxmpp](https://github.com/fritzy/SleekXMPP)

You can use pip to install all of these depenencies by using this command
    
    pip install cement xmpppy requests

## Management

To start the client, you just need to run command:
    
    ./bin/xmpp start

To stop the client, this command:
    
    ./bin/xmpp stop

To view the status, this command:

    ./bin/xmpp status
