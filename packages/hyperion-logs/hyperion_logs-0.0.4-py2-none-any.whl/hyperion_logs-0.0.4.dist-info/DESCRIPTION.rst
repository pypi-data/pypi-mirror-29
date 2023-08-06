===========
Hyperion V0.0.3
===========

Hyperion provides an intuitive and efficient way to store logs from python into AWS CloudWatch.


Typical Usage:


    #import the package
    import hyperion


    #This will return the HyperionLogger Object which included additional built in functions.
    log = hyperion.get_logger()

    #add the handler with a unique stream name and log group name.
    #Note: You can do this anywhere in your code so if the stream_name has to be generated in code.
    #Bigger NOTE: If you do not add a handler it will not log to cloud watch!
    log.add_handler(stream_name,log_group)

    #There is also a set_level function to set the level for the logger.
    log.set_level(debug,info,warning, etc.)

    #In order to start logging do the following:
    log.info('message')
    log.debug('message')
    log.error(dict(foo='bar',details={'user_name':'user123','password':'password1'}))


