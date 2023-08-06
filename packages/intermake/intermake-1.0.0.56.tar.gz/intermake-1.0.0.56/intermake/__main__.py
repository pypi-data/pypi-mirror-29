"""
INTERMAKE is a library, not an application.

This is a sample intermake application contained entirely in one file.

It doesn't have any features beyond the intermake core commands.

But it's well documented so you can use it as a template for your own applications.
"""


def main() -> None:
    """
    Entry point.
    """
    print( __doc__ )
    
    # Setup intermake
    # - Normally we'd put the following in __init__.py, so if we're importing
    #   this as a library, we'd still set up our environment correctly
    #   However, as we're self contained, we do it here.
    
    # First we import intermake!
    import intermake
    
    # Now we define our environment
    # - set the name (title bar)
    # - and the short-name (prompt, folder names, etc)
    # - and set the version (we just use Intermake's own version here, you should define your own)
    intermake.MENV.configure( name = "INTERMAKE SAMPLE APPLICATION",
                              abv_name = "INTERMAKE",
                              version = intermake.__version__ )
    
    
    # If we were a proper application, we'd import our own modules here, which
    # would define some `@command` decorated functions, but as we're stand-alone
    # we'll just define one here
    @intermake.command
    def say_hello( times: int = 1 ) -> None:
        """
        Says hello.
        :param times: Number of times to say hello.
        """
        for _ in range( times ):
            intermake.MCMD.print( "hello" )
    
    
    # Finally, launch the UI.
    intermake.start()


# Standard Python boilerplate code follows
# This allows the `main` function to run if the user types `python -m intermake`
# instead of `intermake`, but stops it running if someone, for some reason, typed
# `from intermake import __main__`
if __name__ == "__main__":
    main()
