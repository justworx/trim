
# cline

The `trix.app.cline` module implements command line handling for 
trix features.

Each cline-based module implements a feature that supports the trix
package, helps with debugging, or provides information related to 
the use of trix (or, sometimes, python in general).


#### cline arguments

The argument format for calls to cline modules are consistent. All
cline calls can accept arguments, flags, and keyword arguments. 

 - Pass flags as a dash followed by one or more non-dash characters.
 - Pass kwargs as a keyword preceeded by two consequtive dashes and 
   followed by an equal sign .
 - Normal arguments, of course, require no dashes :)

The echo cline handler lets you see exactly how your input will be
interpreted - a useful development tool. 

```
python3 -m trix echo Hello, World!
python3 -m trix echo '"Foo Bar!"'

```


# cline modules

The following modules are currently available:

  * compenc  - encode/decode b64, b32, b16, zlib, etc...
  * echo     - print/display arg values - for dev/debugging.
  * http     - launch a webserver. (buggy - won't quit)
  * launch   - launch a Runner-based object in a new process
  * loc      - return locale info for alternate locales
  * portscan - scan for open ports
  * test     - run the trix test suite (such as it is)
  * version  - display trix version and related info


Several cline modules are subclasses of a `cix` module, which provides
the service of printing/displaying output, as well as interpreting
"compact" arguments - large json arguments that are zlib compressed.

The following cline modules are based on cix:
 * echo
 * loc

These cix subclasses automatically convert compact arguments and,
optionally, kwargs for internal use by the module. The following
flags are standard for cix-based cline modules:
 
 -i = expand "compact" input (args and optionally kwargs)
 -c = return data in JCompact format (with a minimum of whitespace)

```
python3 -m trix loc
python3 -m trix loc -c en_CA.UTF_8
python3 -m trix loc -cx

```


# the -ix flags

The i and x flags can be really useful, but the do require a bit of
explanation.

The -i flag tells `cix` subclasses (eg, loc and echo) to take the
command-line argument as "compact" data - that is, a json string
containing args, kwargs (and potentially other data) that is has been
compressed using the `util.cmpenc.compact` function.

When a cix subclass receives the -i flag, it "expands" the argument
and parses the resulting json then uses the data as appropriate.

```
python3 -m trix echo -i eJyrVkpUslLySM3JyddRCM8vyklRVKoFAEWJBoU=

```

By the output of the above, you can see that the rather lengthy
argument, when expanded, is a pair of argument strings: "Hello," and 
"World!".

Unfortunately, it's a bit tricky to generate such strings using the
compenc cline handler since the command line interpreter may do some
unexpected things to your arguments. It's probably best, if you need
to use this feature, to prepare your compact argument using the
`trix.formatter()` classmethod. Here's how I did it:

```
carg = trix.formatter(f="JCompact").compact({"a":"Hello, World!"})
p = trix.popen("python3 -m trix echo -i %s" % carg.decode())
p.stdout.read().decode()

```

The formatter uses compact json, passing it to the compact function 
(from compenc) to use zlib to compress data, and finally encodes the 
result to base64.

When a cix-based cline handler receives the -i flag, it will use the
reversal method (util.compenc.expand) to reverse the process and send
back the original object, in this case the dict {'a':"Hello, World!"}

If you'd like to receive the returned data in compact format, add the
-x flag to your command line. In cases where large amounts of data
are returned, this might be desirable.

