NATS wrapper for fast scanner development
=======================

----
Some instructions for add a new instance of scanner.
----


from scanner_api.wrappers import scanner_wrapper

Define the worker function which takes two argumentw (source, data).
    source - infromation about publisher (e.g. nmap.reporter.masscan - this can catch only in 'nmap.**')
    data - dict with JSON data for scanner, which NATS scheduler send
worker returns a list with data to be sent to next scanner or reporter. (each element of list will be sent as separate message)

You can redefine log format according logging module.

def worker(source, data):
    result = []
    result = processing...(data)
    logging.info("i do work")
    logging.warning("i warn you")
    logging.error("i made a mistake")
    return result


Make a wrapper with define scanner name. The data will be collected from NATS by this name. (e.g. name.***.*** or name). 
Also name its a queue name.

Define NATS host addr.

wrapper = scanner_wrapper(
    nats=["nats://127.0.0.1:4222"],
    name="reporter"
)


Run by passing an argument worker function. This is blocking call!

wrapper.run(worker)



LOG FORMAT:
Connected to nats.
Started module named '{name}'
Received from '{subject}': {data}
Starting '{name}'
Result: {result} \n Was sent to '{pipeline}'

Here:
    {name} - scanner name
    {subject} - queue name
    {data} - json from NATS
    {result} - out data from worker function
    {pipeline} - new addr in NATS queue


