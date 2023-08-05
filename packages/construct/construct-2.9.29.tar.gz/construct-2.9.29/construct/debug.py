import sys, traceback, pdb, inspect
from construct import *
from construct.lib import *


class Probe(Construct):
    r"""
    A probe: dumps the context, stack frames, and stream content (peek) to the screen to aid the debugging process.

    :param show_stream: optional, bool, whether or not to show stream contents (peek), default is True
    :param show_context: optional, bool, whether or not to show the context, default is True
    :param stream_lookahead: optional, integer, number of bytes to dump when show_stack is set, default is 128
    
    Example::

        >>> d = Struct("count"/Byte, "items"/Byte[this.count], Probe())
        >>> d.parse(b"\x05abcde")
        ================================================================================
        Probe <unnamed 3>
        EOF reached
        Container: 
            count = 5
            items = ListContainer: 
                97
                98
                99
                100
                101
        ================================================================================
        Container(count=5)(items=[97, 98, 99, 100, 101])

    ::

        >>> d = (Byte >> Probe())
        >>> d.parse(b"?")
        ================================================================================
        Probe <unnamed 1>
        EOF reached
        Container: 
            0 = 63
        ================================================================================
        [63, None]
    """
    __slots__ = ["show_stream", "show_context", "stream_lookahead", "func"]
    
    def __init__(self, show_stream=True, show_context=True, stream_lookahead=128, func=None):
        super(Probe, self).__init__()
        self.flagbuildnone = True
        self.show_stream = show_stream
        self.show_context = show_context
        self.stream_lookahead = stream_lookahead
        self.func = func

    def __repr__(self):
        return "<%s>" % (self.__class__.__name__, )

    def _parse(self, stream, context, path):
        self.printout(stream, context, path)

    def _build(self, obj, stream, context, path):
        self.printout(stream, context, path)

    def _sizeof(self, context, path):
        self.printout(None, context, path)
        return 0

    def _emitparse(self, code):
        return "print(%r)" % (self.func,) if self.func else "print(this)"

    def printout(self, stream, context, path):
        print("================================================================================")
        print("Probe, path is %s, func is %s" % (path, self.func))

        if self.show_stream and stream is not None:
            fallback = stream.tell()
            datafollows = stream.read(self.stream_lookahead)
            stream.seek(fallback)
            if not datafollows:
                print("EOF reached")
            else:
                print(hexdump(datafollows, 32))
        
        if self.show_context and context is not None:
            if self.func:
                try:
                    context = self.func(context)
                    print(context)
                except Exception:
                    print("Failed to compute `%r` on the context" % self.func)
            else:
                print(context)
        print("================================================================================")


def ProbeInto(func):
    r"""
    ProbeInto looks inside the context and extracts a (sub)key out of it using a lambda for printing. See :class:`~construct.debug.Probe` .

    :param func: context lambda, see example

    Example::

        >>> st = "junk"/RepeatUntil(obj_ == 0,Byte) + "num"/Byte + ProbeInto(this.num)
        >>> st.parse(b"xcnzxmbjskahuiwerhquiehnsdjk\x00\xff")
        ================================================================================
        Probe <unnamed 6>
        path is parsing
        EOF reached
        255
        ================================================================================
        Container(junk=[120, 99, 110, 122, 120, 109, 98, 106, 115, 107, 97, 104, 117, 105, 119, 101, 114, 104, 113, 117, 105, 101, 104, 110, 115, 100, 106, 107, 0])(num=255)
    """
    return Probe(func=func)


class Debugger(Subconstruct):
    r"""
    A pdb-based debugger. When an exception occurs in the subcon, a debugger will appear and allow you to debug the error (and even fix it on-the-fly).
    
    :param subcon: Construct instance, subcon to debug
    
    Example::
    
        >>> Debugger(Byte[3]).build([])
        ================================================================================
        Debugging exception of <Range: None>:
          File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/debug.py", line 116, in _build
            obj.stack.append(a)
          File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 1069, in _build
            raise RangeError("expected from %d to %d elements, found %d" % (self.min, self.max, len(obj)))
        construct.core.RangeError: expected from 3 to 3 elements, found 0

        > /home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py(1069)_build()
        -> raise RangeError("expected from %d to %d elements, found %d" % (self.min, self.max, len(obj)))
        (Pdb) 
        ================================================================================

    ::

        >>> st = Struct(
        ...     "spam" / Debugger(Enum(Byte, A=1, B=2, C=3)),
        ... )
        >>> st.parse(b"\xff")
        ================================================================================
        Debugging exception of <Mapping: None>:
          File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 2578, in _decode
            return self.decoding[obj]
        KeyError: 255

        During handling of the above exception, another exception occurred:

        Traceback (most recent call last):
          File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/debug.py", line 127, in _parse
            return self.subcon._parse(stream, context)
          File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 308, in _parse
            return self._decode(self.subcon._parse(stream, context), context)
          File "/home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py", line 2583, in _decode
            raise MappingError("no decoding mapping for %r" % (obj,))
        construct.core.MappingError: no decoding mapping for 255

        (you can set the value of 'self.retval', which will be returned)
        > /home/arkadiusz/Dokumenty/GitHub/construct/construct/core.py(2583)_decode()
        -> raise MappingError("no decoding mapping for %r" % (obj,))
        (Pdb) self.retval = "???"
        (Pdb) q
    """
    __slots__ = ["retval"]

    def _parse(self, stream, context, path):
        try:
            return self.subcon._parse(stream, context, path)
        except Exception:
            self.retval = NotImplemented
            self.handle_exc(path, msg="(you can set the value of 'self.retval', which will be returned)")
            if self.retval is NotImplemented:
                raise
            else:
                return self.retval

    def _build(self, obj, stream, context, path):
        try:
            self.subcon._build(obj, stream, context, path)
        except Exception:
            self.handle_exc(path)

    def _sizeof(self, context, path):
        try:
            self.subcon._sizeof(context, path)
        except Exception:
            self.handle_exc(path)

    def handle_exc(self, path, msg=None):
        print("================================================================================")
        print("Debugging exception of %s:" % self.subcon)
        print("path is %s" % path)
        print("".join(traceback.format_exception(*sys.exc_info())[1:]))
        if msg:
            print(msg)
        pdb.post_mortem(sys.exc_info()[2])
        print("================================================================================")
