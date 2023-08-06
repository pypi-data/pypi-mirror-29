#########
decent.py
#########

**decent.py** is a Python library that makes creating `Decent`_ clients and bots easy. ::

    import decent

    server = decent.Server("https://meta.decent.chat", "my_username", "my_password")
    server.connect()


    @server.event
    def on_message(message):
        print("New message from {}: {}".format(message.author, message.text))
        message.channel.send("Received a message")


    while True:
        server.mainloop()

.. _Decent: https://github.com/decent-chat/decent
