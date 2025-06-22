Usage
=====

Basic Usage
----------

Here's a simple example of how to use Langpify:

.. code-block:: python

    from langpify import example

    # Using a function
    result = example.hello_world()
    print(result)  # Outputs: Hello, World!

    # Using a class
    obj = example.Example(name="Python")
    greeting = obj.greet()
    print(greeting)  # Outputs: Hello, Python!

    # Processing data
    data = [
        {"name": "John", "age": 30},
        {"name": "Jane", "age": 25, "city": "New York"},
        {"city": "Boston", "country": "USA"},
    ]
    result = example.Example.process_data(data)
    print(result)  # Outputs: {'name': 2, 'age': 2, 'city': 2, 'country': 1}

Advanced Usage
-------------

More advanced examples will be added as the library develops.
