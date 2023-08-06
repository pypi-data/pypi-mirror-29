Simple blocking AMI client (0.1.0b0)
====================================


For install with pip:
---------------------

.. code-block:: shell
    
    pip install ami


Event subscription API:
-----------------------
Subscription is supported for both one and several events.
It is possible to bind predicates through logical AND, and also through logical OR.

If you want to link conditions with AND, then you need to use one `dict`: `manager.event.when({'Event': 'Dial', 'SubEvent': 'Begin'})`

If you want to link conditions with OR, then you need to use multiple `dict`:`manager.event.when({'Event': 'Dial'}, {'SubEvent': 'Begin'})`


Usecases for event subscription:
--------------------------------

.. code-block:: python
   
    import ami

    host = 'localhost'
    port = 5038
    user = 'user'
    secret = 'secret'


    if __name__ == '__main__':
        manager = ami.Manager(host, port, user, secret)

        @manager.event.when({'Event': 'Dial'})
        def on_event_with_plain_predicat(event):
            print(event)

        @manager.event.when({
            'Event': 'Dial',
            'SubEvent': 'Begin'
        })
        def on_event_with_and_predicat(event):
            print(event)

        @manager.event.when(
            {'Event': 'Dial'},
            {'SubEvent': 'Begin'}
        )
        def on_event_with_or_predicat(event):
            print(event)

        # NOTE: will block current thread
        manager.serve_forever()
