#embedsignature=True
#*****************************
# Colibri Core
#   by Maarten van Gompel
#   Centre for Language Studies
#   Radboud University Nijmegen
#
#   http://proycon.github.io/colibri-core
#
#   Licensed under GPLv3
#****************************/
from libcpp.string cimport string
from libcpp cimport bool
from libcpp.vector cimport vector
from cython.operator cimport dereference as deref, preincrement as inc
from cython import address
from colibricore_classes cimport ClassEncoder as cClassEncoder, ClassDecoder as cClassDecoder, Pattern as cPattern, PatternPointer as cPatternPointer, IndexedData as cIndexedData, IndexReference as cIndexReference, PatternMap as cPatternMap, HashOrderedPatternMap as cHashOrderedPatternMap, PatternSet as cPatternSet, PatternModelOptions as cPatternModelOptions, PatternSetModel as cPatternSetModel, PatternModel as cPatternModel,IndexedPatternModel as cIndexedPatternModel, IndexedDataHandler as cIndexedDataHandler, BaseValueHandler as cBaseValueHandler, cout, IndexedCorpus as cIndexedCorpus, SKIPPATTERN as cSKIPPATTERN, FLEXPATTERN as cFLEXPATTERN, UNKPATTERN as cUNKPATTERN, BOUNDARYPATTERN as cBOUNDARYPATTERN, AlignedPatternMap as cAlignedPatternMap, PatternModelInterface as cPatternModelInterface, PatternVector as cPatternVector, PatternFeatureVector as cPatternFeatureVector, PatternFeatureVectorMap as cPatternFeatureVectorMap, PatternAlignmentModel as cPatternAlignmentModel, BasicPatternAlignmentModel as cBasicPatternAlignmentModel, patternfromfile as cpatternfromfile, t_relationmap, t_relationmap_double, t_relationmap_iterator, t_relationmap_double_iterator, istream
from unordered_map cimport unordered_map
from unordered_set cimport unordered_set
from libc.stdint cimport *
from libcpp.map cimport map as stdmap
from libcpp.utility cimport pair
import os.path
from collections import Counter
from sys import version



PYTHON2=(version[0] == '2')
if PYTHON2:
    FileNotFoundError = IOError

def encode(s):
    if PYTHON2:
        if isinstance(s, unicode):
            return s.encode('utf-8')
        else:
            return s #assume already encoded
    else:
        return s.encode('utf-8')


class Category:
    """Pattern Category"""
    NGRAM=1
    SKIPGRAM=2
    FLEXGRAM=3

cdef class ClassEncoder:
    """The class encoder allows patterns to be built from their string representation. Load in a class file and invoke the ``buildpattern()`` method"""

    cdef cClassEncoder data
    cdef str _filename
    cdef unordered_map[string,unsigned int] freqlist
    cdef int minlength
    cdef int maxlength

    def __init__(self, str filename=None, int minlength=0, int maxlength=0):
        self.minlength = minlength
        self.maxlength = maxlength
        if filename:
            self._filename = filename
            if os.path.exists(filename):
                self.data.load(encode(filename), minlength, maxlength)
            else:
                raise FileNotFoundError("File " + filename + " does not exist")
        else:
            self._filename = ""

    def filename(self):
        return self._filename

    def __len__(self):
        """Returns the total number of classes"""
        return self.data.size()

    def buildpattern(self, str text, bool allowunknown=True, bool autoaddunknown=False):
        """Builds a pattern: converts a string representation into a Pattern

        :param text: The actual text of the pattern
        :type text: str
        :param allowunknown: Encode unknown classes as 'unknown', a single class for all, rather than failing with an exception if a word type is unseen (bool, default=False)
        :type allowunknown: bool
        :param autoaddunknown: Automatically add unknown classes to the model (bool, default=False)
        :type autoaddunknown: bool
        :rtype: Pattern
        """

        cdef cPattern cpattern = self.data.buildpattern(encode(text), allowunknown, autoaddunknown)
        pattern = Pattern()
        pattern.bind(cpattern)
        return pattern


    def processcorpus(self, str filename): #build a class from this dataset
        """Process a corpus, call buildclasses() when finished with all corpora"""
        if os.path.exists(filename):
            self.data.processcorpus(encode(filename), self.freqlist)

    def buildclasses(self):
        """Build classes, call after processing all corpora with processcorpus()"""
        self.data.buildclasses(self.freqlist)

    def build(self, str filename): #build a class from this dataset
        """Builds a class encoder from a plain-text corpus (utf-8). Equivalent to a call to processcorpus() followed by buildclasses()"""
        if os.path.exists(filename):
            self.data.build(encode(filename))
        else:
            raise FileNotFoundError("File " + filename + " does not exist")

    def encodefile(self, str sourcefile, str targetfile, bool allowunknown=True, bool addunknown=False, bool append=False, bool ignorenewlines=False): #apply the encoder to a file
        """Encodes the specified sourcefile according to the classer (as targetfile)

        :param sourcefile: Source filename
        :type sourcefile: str
        :param targetfile: Target filename
        :type sourcefile: str
        :param allowunknown: Encode unknown classes as 'unknown', a single class for all, rather than failing with an exception if a word type is unseen (bool, default=False)
        :type allowunknown: bool
        :param addunknown: Add unknown classes to the class encoder (bool, default=False)
        :type addunknown: bool
        :param append: Append to file (bool, default=False)
        :type append: bool
        """
        if os.path.exists(sourcefile):
            self.data.encodefile(encode(sourcefile), encode(targetfile),allowunknown, addunknown, append, ignorenewlines, True)
        else:
            raise FileNotFoundError("File " + sourcefile + " does not exist")

    def save(self, str filename):
        if not self.filename:
            self.filename = filename
        self.data.save(encode(filename))


cdef class ClassDecoder:
    """The Class Decoder allows Patterns to be decoded back to their string representation. An instance of ClassDecoder is passed to Pattern.tostring()"""

    cdef cClassDecoder data #it's not actually a pointer anymore..
    cdef str _filename

    def __init__(self, str filename=None):
        if filename:
            self._filename = filename
            if os.path.exists(filename):
                self.data.load(encode(filename))
            else:
                raise FileNotFoundError("No such file: " + filename)
        else:
            self._filename = ""

    def __len__(self):
        """Returns the total number of classes"""
        return self.data.size()


    def decodefile(self, str filename):
        if os.path.exists(filename):
            if PYTHON2:
                return self.data.decodefiletostring(encode(filename))
            else:
                return self.data.decodefiletostring(encode(filename)).decode('utf-8') #bytes to str (python3)
        else:
            raise FileNotFoundError("File " + filename + " does not exist")

    def filename(self):
        return self._filename

def patternfromfile(str filename):
    """Builds a single pattern from corpus data, will ignore any newlines. You may want to use IndexedCorpus instead."""
    cdef cPattern cpattern = cpatternfromfile(encode(filename))
    pattern = Pattern()
    pattern.bind(cpattern)
    return pattern

cdef class Pattern:
    """The Pattern class contains an ngram, skipgram or flexgram, and allows a wide variety of actions to be performed on it. It is stored in a memory-efficient fashion and facilitating fast operation and comparison. Use ClassEncoder.buildpattern to build a pattern."""

    cdef cPattern cpattern

    cdef cPattern getcpattern(self):
        return self.cpattern

    cdef bind(self, cPattern& cpattern):
        self.cpattern = cpattern

    def bindunk(self):
        self.cpattern = cUNKPATTERN

    def bindskip(self):
        self.cpattern = cSKIPPATTERN

    def bindflex(self):
        self.cpattern = cFLEXPATTERN

    def bindboundary(self):
        self.cpattern = cBOUNDARYPATTERN

    def tostring(self, ClassDecoder decoder):
        """Convert a Pattern back to a str

        :param decoder: the class decoder to use
        :type decoder: ClassDecoder
        :rtype: str
        """

        if PYTHON2:
            return unicode(self.cpattern.tostring(decoder.data),'utf-8')
        else:
            return str(self.cpattern.tostring(decoder.data),'utf-8')

    def unknown(self):
        return self.cpattern.unknown()

    def __contains__(self, Pattern pattern):
        """Check if the specified pattern occurs within this larger pattern.

        :param pattern: the subpattern to look for
        :type pattern: Pattern
        :rtype: bool

        Example::

            subpattern in pattern
        """
        cdef bool r
        r = self.cpattern.contains(pattern.cpattern)
        return r


    def __bool__(self):
        return self.cpattern.n() > 0

    def __len__(self):
        """Returns the length of the pattern in words/tokens::

            len(pattern)
        """
        return self.cpattern.n()

    def __copy__(self):
        """Produces a copy of the pattern (deep)::

            pattern2 = copy(pattern)
        """
        cdef cPattern c_pattern
        c_pattern = cPattern(self.cpattern) #copy constructor
        newpattern = Pattern()
        newpattern.bind(c_pattern)
        return newpattern

    def __deepcopy__(self):
        """Produces a copy of the pattern (deep)::

            pattern2 = copy(pattern)
        """
        cdef cPattern c_pattern
        c_pattern = cPattern(self.cpattern) #copy constructor
        newpattern = Pattern()
        newpattern.bind(c_pattern)
        return newpattern

    def concat(self, Pattern pattern):
        cdef cPattern newcpattern = self.cpattern + pattern.cpattern
        newpattern = Pattern()
        newpattern.bind(newcpattern)
        return newpattern

    def __add__(self, Pattern other):
        """Concatenate two patterns together, forming a larger one::

                pattern3 = pattern1 + pattern2
        """
        return self.concat(other)

    def __getitem__(self, item):
        """Retrieves a word/token from the pattern::

            unigram = pattern[index]

        Or retrieves a subpattern::

            subpattern = pattern[begin:end]


        :param item: an index or slice
        :rtype: a Pattern instance
        """

        cdef int start
        cdef int stop
        cdef cPattern c_pattern

        newpattern = Pattern()
        if isinstance(item, slice):
            start = item.start
            stop = item.stop
            if not stop:
                stop = len(self)
            if not start:
                start = 0
            c_pattern = cPattern(self.cpattern, start, stop - start)
            newpattern.bind(c_pattern)
            return newpattern
        else:
            if item < 0:
                start = len(self) + item
            else:
                start = item
            c_pattern = cPattern(self.cpattern, start, 1)
            newpattern.bind(c_pattern)
            return newpattern

    def __iter__(self):
        """Iterates over all words/tokens in this pattern"""
        for i in range(0, len(self)):
            yield self[i]

    def bytesize(self):
        """Returns the number of bytes used to encode this pattern in memory"""
        return self.cpattern.bytesize()

    def skipcount(self):
        """Returns the number of gaps in this pattern"""
        return self.cpattern.skipcount()

    def category(self):
        """Returns the category of this pattern
        :rtype: Category.NGRAM (1), Category.SKIPGRAM (2), or Category.FLEXGRAM (3)
        """
        return self.cpattern.category()

    def __hash__(self):
        """Returns the hashed value for this pattern"""
        return self.cpattern.hash()

    def __richcmp__(Pattern self, Pattern other, int op):
        """Allows comparisons of two patterns using the usual operators, <, > , <=, <=, =="""
        if op == 2: # ==
            return self.cpattern == other.cpattern
        elif op == 0: #<
            return self.cpattern < other.cpattern
        elif op == 4: #>
            return self.cpattern > other.cpattern
        elif op == 3: #!=
            return not( self.cpattern == other.cpattern)
        elif op == 1: #<=
            return (self.cpattern == other.cpattern) or (self.cpattern < other.cpattern)
        elif op == 5: #>=
            return (self.cpattern == other.cpattern) or (self.cpattern > other.cpattern)


    def reverse(self):
        """Reverse the pattern (all the words will be in reverse order)"""
        cdef cPattern newcpattern = self.cpattern.reverse()
        newpattern = Pattern()
        newpattern.bind(newcpattern)
        return newpattern

    cdef Pattern add(Pattern self, Pattern other):
        cdef cPattern newcpattern = self.cpattern + other.cpattern
        newpattern = Pattern()
        newpattern.bind(newcpattern)
        return newpattern

    def ngrams(self,int n=0, int maxn=0 ):
        """Generator iterating over all ngrams of a particular size (or range thereof) that are enclosed within this pattern. Despite the name, this may also return skipgrams!

        :param n: The desired size to obtain, if unspecified (0), will extract all ngrams
        :type n: int
        :param maxn: If larger than n, will extract ngrams in the specified n range
        :type maxn: int
        :rtype: generator over Pattern instances
        """

        if n == 0:
            return self.subngrams()
        elif maxn >= n:
            return self.subngrams(n,maxn)
        else:
            return self._ngrams_aux(n)

    def _ngrams_aux(self,int n):
        cdef vector[cPattern] result
        self.cpattern.ngrams(result, n)
        cdef cPattern cngram
        cdef vector[cPattern].iterator it = result.begin()
        cdef vector[cPattern].iterator it_end = result.end()
        while it != it_end:
            cngram  = deref(it)
            ngram = Pattern()
            ngram.bind(cngram)
            yield ngram
            inc(it)

    def parts(self):
        """Generating iterating over the consecutive non-gappy parts in a skipgram of flexgram

        :rtype: generator over Pattern instances
        """
        cdef vector[cPattern] result
        self.cpattern.parts(result)
        cdef cPattern cngram
        cdef vector[cPattern].iterator it = result.begin()
        cdef vector[cPattern].iterator it_end = result.end()
        while it != it_end:
            cngram  = deref(it)
            ngram = Pattern()
            ngram.bind(cngram)
            yield ngram
            inc(it)

    def gaps(self):
        """Generator iterating over the gaps in a skipgram or flexgram, return a tuple (begin,length) for each. For flexgrams, the minimum length (1) is always returned.

        :rtype: generator over (begin, length) tuples
        """
        cdef vector[pair[int,int]] result
        self.cpattern.gaps(result)
        cdef vector[pair[int,int]].iterator it = result.begin()
        cdef vector[pair[int,int]].iterator it_end = result.end()
        cdef pair[int,int] p
        while it != it_end:
            p  = deref(it)
            yield (p.first, p.second)
            inc(it)

    def toflexgram(self):
        """Converts a skipgram to a flexgram

        :rtype: Pattern
        """
        cdef cPattern newcpattern = self.cpattern.toflexgram()
        newpattern = Pattern()
        newpattern.bind(newcpattern)
        return newpattern

    def subngrams(self,int minn=1,int maxn=99):
        """Generator iterating over all ngrams of all sizes that are enclosed within this pattern. Despite the name, this may also return skipgrams!
        :param minn: minimum length (default 1)
        :type minn: int
        :param maxn: maximum length (default unlimited)
        :type maxn: int
        :rtype: generator over Pattern instances
        """
        minn = max(1,minn)
        maxn = min(maxn, len(self) -1 )
        for n in range(minn,maxn+1):
            for pattern in self.ngrams(n):
                yield pattern

    def tolist(self):
        """Returns a list representing the raw classes in the pattern"""
        cdef vector[unsigned int] state = self.cpattern.tovector()
        return state

    def __bytes__(self):
        cdef int s = self.bytesize()
        cdef bytes b = self.cpattern.data[:s]
        return b

    def __getstate__(self):
        cdef int s = self.bytesize()
        cdef bytes b = self.cpattern.data[:s]
        return b

    def __setstate__(self, bytes byterep):
        cdef unsigned char * cdata = byterep
        self.cpattern.set(cdata, len(byterep))

    def isgap(self, int index):
        return self.cpattern.isgap(index)

    def isskipgram(self):
        return self.cpattern.isskipgram()

    def isflexgram(self):
        return self.cpattern.isflexgram()

    def instanceof(self, Pattern skipgram):
        """Is this an instantiation of the skipgram/flexgram? Instantiation is not necessarily full, aka: A ? B C is also an instantiation of A ? ? C"""
        return self.cpattern.instanceof(skipgram.cpattern.getpointer())


cdef class IndexedData:
    """IndexedData is essentially a set of indexes in the form of (sentence,token) tuples, sentence is generally 1-indexed, token is always 0-indexed. It is used by Indexed Pattern Models to keep track of exact occurrences of all the patterns. Use len() to if you're merely interested in the number of occurrences, rather than their exact wherabouts."""

    cdef cIndexedData data

    cdef bind(self, cIndexedData cdata):
        self.data = cdata


    def __contains__(self, item):
        """Tests if the specified (sentence,token) tuple is in the set"""
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("Item should be a 2-tuple (sentence,token)")
        cdef cIndexReference ref = cIndexReference(item[0], item[1])
        return self.data.has(ref)

    def __iter__(self):
        """Iterate over all (sentence,token) tuples in the set"""
        cdef cIndexReference ref
        cdef cIndexedData.iterator it = self.data.begin()
        cdef cIndexedData.iterator it_end = self.data.end()
        while it != it_end:
            ref  = deref(it)
            yield (ref.sentence, ref.token)
            inc(it)

    def __len__(self):
        """Returns the number of occurrences, i.e. the length of the set"""
        return self.data.size()

    def __bool__(self):
        return self.data.size() > 0

    def __int__(self):
        return self.data.size()


cdef class PatternSet:
    """This is a simple low-level set that contains Pattern instances"""
    cdef cPatternSet[uint] data
    cdef cPatternSet[uint].iterator it
    cdef cPatternSet[uint].iterator it_end

    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, pattern):
        """Test if the pattern is in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: bool
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it)
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def add(self, Pattern pattern):
        """Adds a pattern to the set
    
        :param pattern: The pattern to add
        :type pattern: Pattern
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        self.data.insert(pattern.cpattern)
    
    #cdef getdatapointer(self):
    #    return address(self.data)


cdef class PatternDict_int32: #maps Patterns to uint32
    """This is a simple low-level dictionary that takes Pattern instances as keys, and integer (max 32 bit, unsigned) as value. For complete pattern models, use IndexedPatternModel or UnindexPatternModel instead."""

    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t] data
    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it
    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it_end
    cdef uint32_t value

    
    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, Pattern pattern):
        """Test if the pattern is in the dictionary"""
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __getitem__(self, Pattern pattern):
        """Retrieve the value for a pattern in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        """
        return self.data[pattern.cpattern]
    
    
    
    def items(self):
        """Iterate over all patterns and their values in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    
    def read(self, str filename):
        if os.path.exists(filename):
            self.data.read(encode(filename))
        else:
            raise IOError
    
    def write(self, str filename):
        self.data.write(encode(filename))

    def __setitem__(self, Pattern pattern, uint32_t v):
        """Set the value for a pattern in the dictionary

        :param pattern: the pattern
        :param value: its value
        """
        self.data[pattern.cpattern] = v

    cdef bind(self, cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t]& newdata):
        self.data = newdata



cdef class SmallPatternDict_int32: #maps Patterns to uint32
    """This is a simple low-level dictionary that takes Pattern instances as keys, and integer (max 32 bit, unsigned) as value. For complete pattern models, use IndexedPatternModel or UnindexPatternModel instead. This is a Small version taht allows at most 65536 patterns."""

    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint16_t] data
    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint16_t].iterator it
    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint16_t].iterator it_end
    cdef uint32_t value

    
    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, Pattern pattern):
        """Test if the pattern is in the dictionary"""
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __getitem__(self, Pattern pattern):
        """Retrieve the value for a pattern in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        """
        return self.data[pattern.cpattern]
    
    
    
    def items(self):
        """Iterate over all patterns and their values in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    
    def read(self, str filename):
        if os.path.exists(filename):
            self.data.read(encode(filename))
        else:
            raise IOError
    
    def write(self, str filename):
        self.data.write(encode(filename))

    def __setitem__(self, Pattern pattern, uint32_t v):
        """Set the value for a pattern in the dictionary

        :param pattern: the pattern
        :param value: its value
        """
        self.data[pattern.cpattern] = v

    cdef bind(self, cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint16_t]& newdata):
        self.data = newdata


cdef class TinyPatternDict_int32: #maps Patterns to uint32
    """This is a simple low-level dictionary that takes Pattern instances as keys, and integer (max 32 bit, unsigned) as value. For complete pattern models, use IndexedPatternModel or UnindexPatternModel instead. This is a tiny version that allow only up to 256 patterns."""

    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint8_t] data
    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint8_t].iterator it
    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint8_t].iterator it_end
    cdef uint32_t value

    
    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, Pattern pattern):
        """Test if the pattern is in the dictionary"""
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __getitem__(self, Pattern pattern):
        """Retrieve the value for a pattern in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        """
        return self.data[pattern.cpattern]
    
    
    
    def items(self):
        """Iterate over all patterns and their values in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    
    def read(self, str filename):
        if os.path.exists(filename):
            self.data.read(encode(filename))
        else:
            raise IOError
    
    def write(self, str filename):
        self.data.write(encode(filename))

    def __setitem__(self, Pattern pattern, uint32_t v):
        """Set the value for a pattern in the dictionary

        :param pattern: the pattern
        :param value: its value
        """
        self.data[pattern.cpattern] = v

    cdef bind(self, cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint8_t]& newdata):
        self.data = newdata

cdef class PatternDict_int: #maps Patterns to uint64
    """This is a simple low-level dictionary that takes Pattern instances as keys, and integer (unsigned 64 bit) as value. For complete pattern models, use IndexedPatternModel or UnindexPatternModel instead."""

    cdef cPatternMap[uint,cBaseValueHandler[uint],uint32_t] data
    cdef cPatternMap[uint,cBaseValueHandler[uint],uint32_t].iterator it
    cdef cPatternMap[uint,cBaseValueHandler[uint],uint32_t].iterator it_end
    cdef int value

    
    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, Pattern pattern):
        """Test if the pattern is in the dictionary"""
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __getitem__(self, Pattern pattern):
        """Retrieve the value for a pattern in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        """
        return self.data[pattern.cpattern]
    
    
    
    def items(self):
        """Iterate over all patterns and their values in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    
    def read(self, str filename):
        if os.path.exists(filename):
            self.data.read(encode(filename))
        else:
            raise IOError
    
    def write(self, str filename):
        self.data.write(encode(filename))

    def __setitem__(self, Pattern pattern, int v):
        """Set the value for a pattern in the dictionary

        :param pattern: the pattern
        :param value: its value
        """
        self.data[pattern.cpattern] = v

cdef class PatternDict_float: #maps Patterns to float
    """This is a simple low-level dictionary that takes Pattern instances as keys, and float (double) as value. For complete pattern models, use IndexedPatternModel or UnindexPatternModel instead."""

    cdef cPatternMap[float,cBaseValueHandler[float],uint32_t] data
    cdef cPatternMap[float,cBaseValueHandler[float],uint32_t].iterator it
    cdef cPatternMap[float,cBaseValueHandler[float],uint32_t].iterator it_end
    cdef float value

    
    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, Pattern pattern):
        """Test if the pattern is in the dictionary"""
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __getitem__(self, Pattern pattern):
        """Retrieve the value for a pattern in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        """
        return self.data[pattern.cpattern]
    
    
    
    def items(self):
        """Iterate over all patterns and their values in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    
    def read(self, str filename):
        if os.path.exists(filename):
            self.data.read(encode(filename))
        else:
            raise IOError
    
    def write(self, str filename):
        self.data.write(encode(filename))

    def __setitem__(self, Pattern pattern, float v):
        """Set the value for a pattern in the dictionary

        :param pattern: the pattern
        :param value: its value
        """
        self.data[pattern.cpattern] = v


cdef class AlignedPatternDict_int32: #maps Patterns to Patterns to uint32 (nested dicts)
    """This is a simple low-level dictionary that takes Pattern instances as keys, and integer (unsigned 64 bit) as value. For complete pattern models, use IndexedPatternModel or UnindexPatternModel instead."""

    cdef cAlignedPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t] data
    cdef cAlignedPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it
    cdef cAlignedPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it_end


    def __len__(self):
        """Return the total number of patterns in the dictionary. If you want the length for a particular pattern, use childcount(pattern)"""
        return self.data.size()

    def childcount(self, Pattern pattern):
        """Returns the number of children for the specified pattern. Use children(pattern) to iterate over them."""
        return self.data[pattern.cpattern].size()

    cpdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)

    cpdef haspair(self, Pattern pattern, Pattern pattern2):
        if not self.data.has(pattern.cpattern):
            return False
        else:
            return self.data[pattern.cpattern].has(pattern2.cpattern)

    def __contains__(self, item):
        """Test if the pattern or the combination of patterns is in the aligned dictionary::

                pattern in aligneddict

            Or:

                (pattern1,pattern2) in aligneddict

            """
        if isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError("Expected instance of Pattern or two-tuple of Patterns")
            elif not isinstance(item[0], Pattern) or not isinstance(item[1], Pattern):
                raise ValueError("Expected instance of Pattern or two-tuple of Patterns")
            return self.haspair(item[0], item[1])
        elif not isinstance(item, Pattern):
            raise ValueError("Expected instance of Pattern or two-tuple of Patterns")
            return self.has(item)

    def __iter__(self):
        """Iterate over all patterns in the dictionary. If you want to iterate over pattern pairs, use pairs() instead, to iterate over the children for a specific pattern, use children()"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)


    def children(self, Pattern pattern):
        """Iterate over all patterns in the dictionary. If you want to iterate over pattern pairs, use pairs() instead"""
        cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it2
        cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it2_end
        cdef cPattern cpattern
        it2 = self.data[pattern.cpattern].begin()
        it2_end = self.data[pattern.cpattern].end()
        while it2 != it2_end:
            cpattern = deref(it2).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it2)


    def items(self):
        """Iterate over all pattern pairs and their values in the dictionary. Yields (pattern1,pattern2,value) tuples"""
        cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it2
        cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t].iterator it2end
        cdef int value
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            it2 = self.data[pattern.cpattern].begin()
            it2end = self.data[pattern.cpattern].end()
            while it2 != it2end:
                cpattern = deref(it2).first
                pattern2 = Pattern()
                pattern2.bind(cpattern)
                value = deref(it2).second
                yield pattern, pattern2, value
                inc(it2)
            inc(it)

    cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t] * getmap(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")

        if not self.has(pattern):
           self.data[pattern.cpattern]

        cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t] * m = &(self.data[pattern.cpattern])
        return m




    cpdef getpair(self, Pattern pattern, Pattern pattern2):
        return self.data[pattern.cpattern][pattern2.cpattern]

    cpdef setpair(self, Pattern pattern, Pattern pattern2, uint32_t value):
        self.data[pattern.cpattern][pattern2.cpattern] = value

    def __getitem__(self, item):
        """Retrieve the item, item is a two-tuple of Pattern instances.

             aligneddict[(pattern1,pattern2)]


        :param item: A two tuple of Pattern instances
        """
        cdef cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint32_t] * mapdata

        if isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError("Expected instance of Pattern or two-tuple of Patterns")
            elif not isinstance(item[0], Pattern) or not isinstance(item[1], Pattern):
                raise ValueError("Expected instance of Pattern or two-tuple of Patterns")
            return self.getpair(item[0], item[1])
        elif isinstance(item, Pattern):
            mapdata = self.getmap(item[0])
            d = PatternDict_int32()
            d.bind(deref(mapdata))
            return d
        else:
            raise ValueError("Expected instance of Pattern or two-tuple of Patterns")

    def __setitem__(self, item, value):
        if isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError("Expected two-tuple of Patterns")
            elif not isinstance(item[0], Pattern) or not isinstance(item[1], Pattern):
                raise ValueError("Expected two-tuple of Patterns")
            self.setpair(item[0], item[1], value)
        else:
            raise ValueError("Expected two-tuple of Patterns")


    def read(self, str filename):
        if os.path.exists(filename):
            self.data.read(encode(filename))
        else:
            raise FileNotFoundError

    def write(self, str filename):
        self.data.write(encode(filename))


cdef class IndexedPatternModel:
    """Indexed Pattern Model. Implemented using a hash map (dictionary)"""

    cdef cIndexedPatternModel[cPatternMap[cIndexedData,cIndexedDataHandler,uint64_t]] data
    cdef cPatternModel[cIndexedData,cIndexedDataHandler,cPatternMap[cIndexedData,cIndexedDataHandler,uint64_t]].iterator it

    cdef object corpus
    
    def __len__(self):
        """Returns the total number of distinct patterns in the model"""
        return self.data.size()
    
    def __bool__(self):
        return self.data.size() > 0
    
    def types(self):
        """Returns the total number of distinct word types in the training data"""
        return self.data.types()
    
    def tokens(self):
        """Returns the total number of tokens in the training data"""
        return self.data.tokens()
    
    def minlength(self):
        """Returns the minimum pattern length in the model"""
        return self.data.minlength()
    
    def maxlength(self):
        """Returns the maximum pattern length in the model"""
        return self.data.maxlength()
    
    def type(self):
        """Returns the model type (10 = UNINDEXED, 20 = INDEXED)"""
        return self.data.type()
    
    def version(self):
        """Return the version of the model type"""
        return self.data.version()
    
    def occurrencecount(self, Pattern pattern):
        """Returns the number of times the specified pattern occurs in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.occurrencecount(pattern.cpattern)
    
    def coveragecount(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coveragecount(pattern.cpattern)
    
    def coverage(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data, as a fraction of the total amount of tokens
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coverage(pattern.cpattern)
    
    def frequency(self, Pattern pattern):
        """Returns the frequency of the pattern within its category (ngram/skipgram/flexgram) and exact size class. For a bigram it will thus return the bigram frequency.
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.frequency(pattern.cpattern)
    
    
    def totaloccurrencesingroup(self, int category=0, int n=0):
        """Returns the total number of occurrences in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total occurrence count over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaloccurrencesingroup(category,n)
    
    def totalpatternsingroup(self, int category=0, int n=0):
        """Returns the total number of distinct patterns in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of distrinct skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totalpatternsingroup(category,n)
    
    def totaltokensingroup(self, int category=0, int n=0):
        """Returns the total number of covered tokens in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered tokens over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
    
    def totalwordtypesingroup(self, int category=0, int n=0):
        """Returns the total number of covered word types (unigram types) in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered word types over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
        return self.data.totalwordtypesingroup(category,n)
    
    cdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, pattern):
        """Tests if a pattern is in the model:
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: bool
    
        Example::
    
            pattern in patternmodel
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.has(pattern)
    
    def __getitem__(self, pattern):
        """Retrieves the value for the pattern
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int (for Unindexed Models), IndexData (for Indexed models)
    
        Example (unindexed model)::
    
            occurrences = model[pattern]
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.getdata(pattern)
    
    
    
    def __iter__(self):
        """Iterates over all patterns in the model. Also consider using the filter() or top() methods if they suit your needs, as they will be faster than doing it manually.
    
        Example::
    
            for pattern in model:
                print(pattern.tostring(classdecoder))
    
        """
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __init__(self, str filename = "",PatternModelOptions options = None, constrainmodel = None, reverseindex = None):
        """Initialise a pattern model. Either an empty one or loading from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A model to be used as a constraint, only patterns occuring in this constraint model will be loaded/trained
        :type constrainmodel: IndexedPatternModel, UnindexedPatternModel or None (default)
        :param reverseindex: Corpus data to use as reverse index. On indexed models, this is required for various operations, including computation of skipgrams
        :type reverseindex: IndexedCorpus or None
        """
    
        self.corpus = None
        if reverseindex:
            self.loadreverseindex(reverseindex)
    
        if filename:
            if not options:
                options = PatternModelOptions()
            if filename and not os.path.exists(filename):
                raise FileNotFoundError(filename)
            self.load(filename,options, constrainmodel)
    
    def load(self, str filename, PatternModelOptions options=None, constrainmodel = None):
        """Load a patternmodel from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if not options:
            options = PatternModelOptions()
    
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
    
        if isinstance(constrainmodel, IndexedPatternModel):
            self.loadconstrainedbyindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbyunindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbysetmodel(filename,options, constrainmodel)
        else:
            self.data.load(encode(filename), options.coptions, NULL)
    
    def loadreverseindex(self, IndexedCorpus reverseindex):
        self.data.reverseindex = reverseindex.data
        self.corpus = reverseindex #so python doesn't garbage collect the python object
    
    
    cpdef loadconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbysetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)
    
    cpdef write(self, str filename):
        """Write a patternmodel to file
    
        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))
    
    cpdef printmodel(self,ClassDecoder decoder):
        """Print the entire pattern model to stdout, a detailed overview
    
        :param decoder: The class decoder
        :type decoder: ClassDecoder
        """
        self.data.printmodel(&cout, decoder.data )
    
    cpdef train(self, str filename, PatternModelOptions options, constrainmodel = None):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A patternmodel or patternsetmodel to constrain training (default None)
        :type constrainmodel: None, UnindexedPatternModel, IndexedPatternModel, PatternSetModel
        """
    
        if self.data.reverseindex != NULL:
            filename = ""
        if isinstance(self, IndexedPatternModel) and self.data.reverseindex == NULL and options.DOSKIPGRAMS:
            raise ValueError("No reversindex was specified but you are requesting to train skipgrams, set reverseindex to an IndexedCorpus instance upon model construction")
    
    
        if constrainmodel:
            assert len(constrainmodel) >= 0
            if isinstance(constrainmodel, IndexedPatternModel):
                self.trainconstrainedbyindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, UnindexedPatternModel):
                self.trainconstrainedbyunindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternSetModel):
                self.trainconstrainedbypatternsetmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternAlignmentModel_float):
                self.trainconstrainedbyalignmodel(filename, options, constrainmodel)
            else:
                raise ValueError("Invalid type for constrainmodel") #TODO: build patternmodel on the fly from an iterable of patterns or lower level patternstorage
        elif filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, NULL)
    
    cpdef train_filtered(self, str filename, PatternModelOptions options, PatternSet filterset):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param filterset: An instance of PatternSet. A limited set of skipgrams/flexgrams to use as a filter, patterns will only be included if they are an instance of a skipgram in this list (i.e. disjunctive). Ngrams can also be included as filters, if a pattern subsumes one of the ngrams in the filter, it counts as a match (or if it matches it exactly).
        """
        cdef cPatternSet[uint] * cfilterset = address(filterset.data)
    
        if filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, cfilterset)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, cfilterset)
    
    
    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()
    
    cpdef trainconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbypatternsetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyalignmodel(self, str filename, PatternModelOptions options, PatternAlignmentModel_float constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*>  NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef report(self):
        """Print a detailed statistical report to stdout"""
        self.data.report(&cout)
    
    cpdef printhistogram(self):
        """Print a histogram to stdout"""
        self.data.histogram(&cout)
    
    
    
    cpdef prune(self, int threshold, int n=0):
        """Prune all patterns occurring below the threshold.
    
        :param threshold: the threshold value (minimum number of occurrences)
        :type threshold: int
        :param n: prune only patterns of the specified size, use 0 (default) for no size limitation
        :type n: int
        """
        self.data.prune(threshold, n)
    
    
    def reverseindex(self):
        """Returns the reverseindex associated with the model, this will be an instance of IndexedCorpus. Use getreverseindex( (sentence, token) ) instead if you want to query the reverse index."""
        return self.corpus
    
    
    def getreverseindex(self, indexreference):
        """Generator over all patterns occurring at the specified index reference
    
        :param indexreference: a (sentence, tokenoffset) tuple
        """
    
        if not isinstance(indexreference, tuple) or not len(indexreference) == 2:
            raise ValueError("Expected tuple")
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef int sentence = indexreference[0]
        cdef int token = indexreference[1]
        cdef cIndexReference ref = cIndexReference(sentence, token)
        cdef unordered_set[cPatternPointer] results = self.data.getreverseindex(ref)
        cdef unordered_set[cPatternPointer].iterator resit = results.begin()
        cdef cPattern cpattern
        while resit != results.end():
            cpattern = deref(resit).pattern()
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(resit)
    
    def getreverseindex_bysentence(self, int sentence):
        """Generator over all patterns occurring in the specified sentence
    
        :param sentence: a sentence number
        """
    
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef vector[pair[cIndexReference,cPatternPointer]] results = self.data.getreverseindex_bysentence(sentence)
        cdef vector[pair[cIndexReference,cPatternPointer]].iterator resit = results.begin()
        cdef pair[cIndexReference,cPatternPointer] p
        cdef cPattern cpattern
        while resit != results.end():
            p = deref(resit)
            pattern = Pattern()
            cpattern = p.second.pattern()
            pattern.bind(cpattern)
            yield (p.first.sentence, p.first.token), pattern
            inc(resit)
    
    
    def histogram(self, unsigned int threshold=0, unsigned int cap=0, int category = 0, int size = 0):
        """Generator over a histogram of occurrence count data, produces (occurrencecount, frequency) tuples. A minimum threshold may be configured, or a cap on total number of occurrences may be specified (to get only the top occurrences). The histogram can be constrained by category and/or pattern size (if set to >0 values)"""
        cdef stdmap[unsigned int,unsigned int] hist
        cdef stdmap[unsigned int,unsigned int].iterator it
        self.data.histogram(hist,threshold,cap, category, size)
        it = hist.begin()
        while it != hist.end():
            yield deref(it).first, deref(it).second
            inc(it)
    
    
    def top(self, int amount, int category = 0, int size = 0):
        """Generator over the top [amount] most occurring patterns (of specified category and size if set to values above 0). This is faster than iterating manually! Will return (pattern, occurrencecount) tuples (unsorted). Note that this may return less than the specified amount of patterns if there are multiple patterns with the same occurrence count in its tail. """
    
        cdef unsigned int smallest = self.data.topthreshold(amount, category, size)
        return self.filter(smallest, category, size)
    
    
    
    def filter(self, unsigned int threshold, int category = 0, int size = 0):
        """Generator over patterns occurring over the set occurrence threshold (and of specified category and size if set to values above 0). This is faster than iterating and filtering manually! Will return (pattern, occurrencecount) tuples (unsorted)"""
        cdef unsigned int count
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            inc(it)
            if ((category > 0) and (cpattern.category() != category)) or (size > 0) and (size != cpattern.n()):
                continue
            count = self.data.occurrencecount(cpattern)
            if count >= threshold:
                pattern = Pattern()
                pattern.bind(cpattern)
                yield pattern, count
    
    def getinstance(self, tuple pos, Pattern pattern):
        """Gets a specific instance of a pattern (skipgram or flexgram), at the specified position. Raises a KeyError when not found."""
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
        return self.corpus.getinstance(pos, pattern)
    
    cpdef getdata(self, Pattern pattern):
        """Return the indices at which the pattern occurs"""
        cdef cIndexedData cvalue
        if pattern in self:
            cvalue = self.data[pattern.cpattern]
            value = IndexedData()
            value.bind(cvalue)
            return value
        else:
            raise KeyError
    
    
    cpdef add(self, Pattern pattern, indices):
        """Add a pattern to the indexed model
        :param pattern: The pattern to add
        :type pattern: Pattern
        :param indices: list (or other iterable) of 2-tuples specifying the (sentence,index) of each occurrence of the pattern
        """
    
        cdef cIndexedData * cvalue
        cvalue = &(self.data[pattern.cpattern])
        cdef cIndexReference ref
        for sentence,token in indices:
            ref.sentence = <int> sentence
            ref.token = <int> token
        self.data.add(pattern.cpattern, cvalue, ref)
    
    def __iter__(self):
        """Iterate over all patterns in this model"""
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def items(self):
        """Iterate over all patterns and their index data (IndexedData instances) in this model"""
        it = self.data.begin()
        cdef cPattern cpattern
        cdef cIndexedData cvalue
        while it != self.data.end():
            cpattern = deref(it).first
            cvalue = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            value = IndexedData()
            value.bind(cvalue)
            yield (pattern,value)
            inc(it)
    
    
    
    
    
    def covered(self, indexreference):
        if not isinstance(indexreference, tuple) or not len(indexreference) == 2:
            raise ValueError("Expected tuple")
        cdef int sentence = indexreference[0]
        cdef int token = indexreference[1]
        cdef cIndexReference ref = cIndexReference(sentence, token)
        cdef cIndexReference ref2
        cdef unordered_set[cPatternPointer] results = self.data.getreverseindex(ref)
        cdef unordered_set[cPatternPointer] results2
        cdef unordered_set[cPatternPointer].iterator resit
        cdef cPattern cpattern
        if not results.empty():
            return True
        else:
            for i in range(1, token+1):
                if token-i >= 0:
                    ref2 = cIndexReference(sentence, token-i)
                    results2 = self.data.getreverseindex(ref2)
                    resit = results2.begin()
                    while resit != results2.end():
                        cpattern = deref(resit).pattern()
                        if cpattern.n() >= token+1:
                            return True
                        inc(resit)
            return False
    
    
    
    
    
    
    
    cpdef outputrelations(self, Pattern pattern, ClassDecoder decoder):
        """Compute and output (to stdout) all relations for the specified pattern:
    
        :param pattern: The pattern to output relations for
        :type pattern: Pattern
        :param decoder: The class decoder
        :type decoder: ClassDecoder
        """
        self.data.outputrelations(pattern.cpattern,decoder.data,&cout)
    
    
    def getsubchildren(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get subsumption children for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getsubchildren(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
    
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getsubparents(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get subsumption parents for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getsubparents(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getleftneighbours(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0, int cutoff = 0):
        """Get left neighbours for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getleftneighbours(pattern.cpattern, occurrencethreshold, category, size,cutoff)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getrightneighbours(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0, int cutoff = 0):
        """Get right neighbours for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getrightneighbours(pattern.cpattern, occurrencethreshold, category, size,cutoff)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getskipcontent(self, Pattern pattern):
        """Get skip content for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getskipcontent(pattern.cpattern)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def gettemplates(self, Pattern pattern, int occurrencethreshold = 0):
        """Get templates (abstracting skipgrams) for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.gettemplates(pattern.cpattern, occurrencethreshold)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getinstances(self, Pattern pattern, int occurrencethreshold = 0):
        """Get templates (abstracting skipgrams) for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getinstances(pattern.cpattern, occurrencethreshold)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getcooc(self, Pattern pattern,  int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get left-side co-occurrences for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getcooc(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getleftcooc(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get left-side co-occurrences for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getleftcooc(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getrightcooc(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get right-side co-occurrences for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getrightcooc(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def computeflexgrams_fromskipgrams(self):
        """Compute flexgrams from skipgrams in the model. Returns the number of flexgrams found."""
        return self.data.computeflexgrams_fromskipgrams()
    
    def computeflexgrams_fromcooc(self,double threshold):
        """Compute flexgrams based on  co-occurence. The threshold is expressed in normalised pointwise mutual information. Returns the number of flexgrams found. Flexgrams contain at only one gap using this method."""
        return self.data.computeflexgrams_fromcooc(threshold)

cdef class HashOrderedIndexedPatternModel:
    """Indexed Pattern Model. Implemented using an ordered map"""

    cdef cIndexedPatternModel[cHashOrderedPatternMap[cIndexedData,cIndexedDataHandler,uint64_t]] data
    cdef cPatternModel[cIndexedData,cIndexedDataHandler,cHashOrderedPatternMap[cIndexedData,cIndexedDataHandler,uint64_t]].iterator it

    cdef object corpus
    
    def __len__(self):
        """Returns the total number of distinct patterns in the model"""
        return self.data.size()
    
    def __bool__(self):
        return self.data.size() > 0
    
    def types(self):
        """Returns the total number of distinct word types in the training data"""
        return self.data.types()
    
    def tokens(self):
        """Returns the total number of tokens in the training data"""
        return self.data.tokens()
    
    def minlength(self):
        """Returns the minimum pattern length in the model"""
        return self.data.minlength()
    
    def maxlength(self):
        """Returns the maximum pattern length in the model"""
        return self.data.maxlength()
    
    def type(self):
        """Returns the model type (10 = UNINDEXED, 20 = INDEXED)"""
        return self.data.type()
    
    def version(self):
        """Return the version of the model type"""
        return self.data.version()
    
    def occurrencecount(self, Pattern pattern):
        """Returns the number of times the specified pattern occurs in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.occurrencecount(pattern.cpattern)
    
    def coveragecount(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coveragecount(pattern.cpattern)
    
    def coverage(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data, as a fraction of the total amount of tokens
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coverage(pattern.cpattern)
    
    def frequency(self, Pattern pattern):
        """Returns the frequency of the pattern within its category (ngram/skipgram/flexgram) and exact size class. For a bigram it will thus return the bigram frequency.
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.frequency(pattern.cpattern)
    
    
    def totaloccurrencesingroup(self, int category=0, int n=0):
        """Returns the total number of occurrences in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total occurrence count over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaloccurrencesingroup(category,n)
    
    def totalpatternsingroup(self, int category=0, int n=0):
        """Returns the total number of distinct patterns in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of distrinct skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totalpatternsingroup(category,n)
    
    def totaltokensingroup(self, int category=0, int n=0):
        """Returns the total number of covered tokens in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered tokens over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
    
    def totalwordtypesingroup(self, int category=0, int n=0):
        """Returns the total number of covered word types (unigram types) in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered word types over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
        return self.data.totalwordtypesingroup(category,n)
    
    cdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, pattern):
        """Tests if a pattern is in the model:
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: bool
    
        Example::
    
            pattern in patternmodel
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.has(pattern)
    
    def __getitem__(self, pattern):
        """Retrieves the value for the pattern
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int (for Unindexed Models), IndexData (for Indexed models)
    
        Example (unindexed model)::
    
            occurrences = model[pattern]
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.getdata(pattern)
    
    
    
    def __iter__(self):
        """Iterates over all patterns in the model. Also consider using the filter() or top() methods if they suit your needs, as they will be faster than doing it manually.
    
        Example::
    
            for pattern in model:
                print(pattern.tostring(classdecoder))
    
        """
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __init__(self, str filename = "",PatternModelOptions options = None, constrainmodel = None, reverseindex = None):
        """Initialise a pattern model. Either an empty one or loading from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A model to be used as a constraint, only patterns occuring in this constraint model will be loaded/trained
        :type constrainmodel: IndexedPatternModel, UnindexedPatternModel or None (default)
        :param reverseindex: Corpus data to use as reverse index. On indexed models, this is required for various operations, including computation of skipgrams
        :type reverseindex: IndexedCorpus or None
        """
    
        self.corpus = None
        if reverseindex:
            self.loadreverseindex(reverseindex)
    
        if filename:
            if not options:
                options = PatternModelOptions()
            if filename and not os.path.exists(filename):
                raise FileNotFoundError(filename)
            self.load(filename,options, constrainmodel)
    
    def load(self, str filename, PatternModelOptions options=None, constrainmodel = None):
        """Load a patternmodel from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if not options:
            options = PatternModelOptions()
    
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
    
        if isinstance(constrainmodel, IndexedPatternModel):
            self.loadconstrainedbyindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbyunindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbysetmodel(filename,options, constrainmodel)
        else:
            self.data.load(encode(filename), options.coptions, NULL)
    
    def loadreverseindex(self, IndexedCorpus reverseindex):
        self.data.reverseindex = reverseindex.data
        self.corpus = reverseindex #so python doesn't garbage collect the python object
    
    
    cpdef loadconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbysetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)
    
    cpdef write(self, str filename):
        """Write a patternmodel to file
    
        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))
    
    cpdef printmodel(self,ClassDecoder decoder):
        """Print the entire pattern model to stdout, a detailed overview
    
        :param decoder: The class decoder
        :type decoder: ClassDecoder
        """
        self.data.printmodel(&cout, decoder.data )
    
    cpdef train(self, str filename, PatternModelOptions options, constrainmodel = None):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A patternmodel or patternsetmodel to constrain training (default None)
        :type constrainmodel: None, UnindexedPatternModel, IndexedPatternModel, PatternSetModel
        """
    
        if self.data.reverseindex != NULL:
            filename = ""
        if isinstance(self, IndexedPatternModel) and self.data.reverseindex == NULL and options.DOSKIPGRAMS:
            raise ValueError("No reversindex was specified but you are requesting to train skipgrams, set reverseindex to an IndexedCorpus instance upon model construction")
    
    
        if constrainmodel:
            assert len(constrainmodel) >= 0
            if isinstance(constrainmodel, IndexedPatternModel):
                self.trainconstrainedbyindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, UnindexedPatternModel):
                self.trainconstrainedbyunindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternSetModel):
                self.trainconstrainedbypatternsetmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternAlignmentModel_float):
                self.trainconstrainedbyalignmodel(filename, options, constrainmodel)
            else:
                raise ValueError("Invalid type for constrainmodel") #TODO: build patternmodel on the fly from an iterable of patterns or lower level patternstorage
        elif filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, NULL)
    
    cpdef train_filtered(self, str filename, PatternModelOptions options, PatternSet filterset):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param filterset: An instance of PatternSet. A limited set of skipgrams/flexgrams to use as a filter, patterns will only be included if they are an instance of a skipgram in this list (i.e. disjunctive). Ngrams can also be included as filters, if a pattern subsumes one of the ngrams in the filter, it counts as a match (or if it matches it exactly).
        """
        cdef cPatternSet[uint] * cfilterset = address(filterset.data)
    
        if filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, cfilterset)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, cfilterset)
    
    
    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()
    
    cpdef trainconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbypatternsetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyalignmodel(self, str filename, PatternModelOptions options, PatternAlignmentModel_float constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*>  NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef report(self):
        """Print a detailed statistical report to stdout"""
        self.data.report(&cout)
    
    cpdef printhistogram(self):
        """Print a histogram to stdout"""
        self.data.histogram(&cout)
    
    
    
    cpdef prune(self, int threshold, int n=0):
        """Prune all patterns occurring below the threshold.
    
        :param threshold: the threshold value (minimum number of occurrences)
        :type threshold: int
        :param n: prune only patterns of the specified size, use 0 (default) for no size limitation
        :type n: int
        """
        self.data.prune(threshold, n)
    
    
    def reverseindex(self):
        """Returns the reverseindex associated with the model, this will be an instance of IndexedCorpus. Use getreverseindex( (sentence, token) ) instead if you want to query the reverse index."""
        return self.corpus
    
    
    def getreverseindex(self, indexreference):
        """Generator over all patterns occurring at the specified index reference
    
        :param indexreference: a (sentence, tokenoffset) tuple
        """
    
        if not isinstance(indexreference, tuple) or not len(indexreference) == 2:
            raise ValueError("Expected tuple")
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef int sentence = indexreference[0]
        cdef int token = indexreference[1]
        cdef cIndexReference ref = cIndexReference(sentence, token)
        cdef unordered_set[cPatternPointer] results = self.data.getreverseindex(ref)
        cdef unordered_set[cPatternPointer].iterator resit = results.begin()
        cdef cPattern cpattern
        while resit != results.end():
            cpattern = deref(resit).pattern()
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(resit)
    
    def getreverseindex_bysentence(self, int sentence):
        """Generator over all patterns occurring in the specified sentence
    
        :param sentence: a sentence number
        """
    
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef vector[pair[cIndexReference,cPatternPointer]] results = self.data.getreverseindex_bysentence(sentence)
        cdef vector[pair[cIndexReference,cPatternPointer]].iterator resit = results.begin()
        cdef pair[cIndexReference,cPatternPointer] p
        cdef cPattern cpattern
        while resit != results.end():
            p = deref(resit)
            pattern = Pattern()
            cpattern = p.second.pattern()
            pattern.bind(cpattern)
            yield (p.first.sentence, p.first.token), pattern
            inc(resit)
    
    
    def histogram(self, unsigned int threshold=0, unsigned int cap=0, int category = 0, int size = 0):
        """Generator over a histogram of occurrence count data, produces (occurrencecount, frequency) tuples. A minimum threshold may be configured, or a cap on total number of occurrences may be specified (to get only the top occurrences). The histogram can be constrained by category and/or pattern size (if set to >0 values)"""
        cdef stdmap[unsigned int,unsigned int] hist
        cdef stdmap[unsigned int,unsigned int].iterator it
        self.data.histogram(hist,threshold,cap, category, size)
        it = hist.begin()
        while it != hist.end():
            yield deref(it).first, deref(it).second
            inc(it)
    
    
    def top(self, int amount, int category = 0, int size = 0):
        """Generator over the top [amount] most occurring patterns (of specified category and size if set to values above 0). This is faster than iterating manually! Will return (pattern, occurrencecount) tuples (unsorted). Note that this may return less than the specified amount of patterns if there are multiple patterns with the same occurrence count in its tail. """
    
        cdef unsigned int smallest = self.data.topthreshold(amount, category, size)
        return self.filter(smallest, category, size)
    
    
    
    def filter(self, unsigned int threshold, int category = 0, int size = 0):
        """Generator over patterns occurring over the set occurrence threshold (and of specified category and size if set to values above 0). This is faster than iterating and filtering manually! Will return (pattern, occurrencecount) tuples (unsorted)"""
        cdef unsigned int count
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            inc(it)
            if ((category > 0) and (cpattern.category() != category)) or (size > 0) and (size != cpattern.n()):
                continue
            count = self.data.occurrencecount(cpattern)
            if count >= threshold:
                pattern = Pattern()
                pattern.bind(cpattern)
                yield pattern, count
    
    def getinstance(self, tuple pos, Pattern pattern):
        """Gets a specific instance of a pattern (skipgram or flexgram), at the specified position. Raises a KeyError when not found."""
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
        return self.corpus.getinstance(pos, pattern)
    
    cpdef getdata(self, Pattern pattern):
        """Return the indices at which the pattern occurs"""
        cdef cIndexedData cvalue
        if pattern in self:
            cvalue = self.data[pattern.cpattern]
            value = IndexedData()
            value.bind(cvalue)
            return value
        else:
            raise KeyError
    
    
    cpdef add(self, Pattern pattern, indices):
        """Add a pattern to the indexed model
        :param pattern: The pattern to add
        :type pattern: Pattern
        :param indices: list (or other iterable) of 2-tuples specifying the (sentence,index) of each occurrence of the pattern
        """
    
        cdef cIndexedData * cvalue
        cvalue = &(self.data[pattern.cpattern])
        cdef cIndexReference ref
        for sentence,token in indices:
            ref.sentence = <int> sentence
            ref.token = <int> token
        self.data.add(pattern.cpattern, cvalue, ref)
    
    def __iter__(self):
        """Iterate over all patterns in this model"""
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def items(self):
        """Iterate over all patterns and their index data (IndexedData instances) in this model"""
        it = self.data.begin()
        cdef cPattern cpattern
        cdef cIndexedData cvalue
        while it != self.data.end():
            cpattern = deref(it).first
            cvalue = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            value = IndexedData()
            value.bind(cvalue)
            yield (pattern,value)
            inc(it)
    
    
    
    
    
    def covered(self, indexreference):
        if not isinstance(indexreference, tuple) or not len(indexreference) == 2:
            raise ValueError("Expected tuple")
        cdef int sentence = indexreference[0]
        cdef int token = indexreference[1]
        cdef cIndexReference ref = cIndexReference(sentence, token)
        cdef cIndexReference ref2
        cdef unordered_set[cPatternPointer] results = self.data.getreverseindex(ref)
        cdef unordered_set[cPatternPointer] results2
        cdef unordered_set[cPatternPointer].iterator resit
        cdef cPattern cpattern
        if not results.empty():
            return True
        else:
            for i in range(1, token+1):
                if token-i >= 0:
                    ref2 = cIndexReference(sentence, token-i)
                    results2 = self.data.getreverseindex(ref2)
                    resit = results2.begin()
                    while resit != results2.end():
                        cpattern = deref(resit).pattern()
                        if cpattern.n() >= token+1:
                            return True
                        inc(resit)
            return False
    
    
    
    
    
    
    
    cpdef outputrelations(self, Pattern pattern, ClassDecoder decoder):
        """Compute and output (to stdout) all relations for the specified pattern:
    
        :param pattern: The pattern to output relations for
        :type pattern: Pattern
        :param decoder: The class decoder
        :type decoder: ClassDecoder
        """
        self.data.outputrelations(pattern.cpattern,decoder.data,&cout)
    
    
    def getsubchildren(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get subsumption children for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getsubchildren(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
    
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getsubparents(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get subsumption parents for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getsubparents(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getleftneighbours(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0, int cutoff = 0):
        """Get left neighbours for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getleftneighbours(pattern.cpattern, occurrencethreshold, category, size,cutoff)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getrightneighbours(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0, int cutoff = 0):
        """Get right neighbours for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrences for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getrightneighbours(pattern.cpattern, occurrencethreshold, category, size,cutoff)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getskipcontent(self, Pattern pattern):
        """Get skip content for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getskipcontent(pattern.cpattern)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def gettemplates(self, Pattern pattern, int occurrencethreshold = 0):
        """Get templates (abstracting skipgrams) for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.gettemplates(pattern.cpattern, occurrencethreshold)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getinstances(self, Pattern pattern, int occurrencethreshold = 0):
        """Get templates (abstracting skipgrams) for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getinstances(pattern.cpattern, occurrencethreshold)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getcooc(self, Pattern pattern,  int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get left-side co-occurrences for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getcooc(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getleftcooc(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get left-side co-occurrences for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getleftcooc(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def getrightcooc(self, Pattern pattern, int occurrencethreshold = 0, int category = 0, int size = 0):
        """Get right-side co-occurrences for the specified pattern
        :param pattern: The pattern
        :type pattern: Pattern
        :param occurrencethreshold: Constrain by patterns occurring at least this many times in this relationship (default: 0, unconstrained)
        :type occurrencethreshold: int
        :param category: Constrain by patterns of the specified category (colibricore.Category.NGRAM,colibricore.Category.SKIPGRAM, colibricore.Category.FLEXGRAM)
        :param size: Constrain by patterns of the specified size
        :type size: int
        :rtype: generator over (Pattern,value) tuples. The values correspond to the number of occurrence for this particularrelationship
        """
        if self.data.reverseindex == NULL:
            raise ValueError("No reverseindex was specified but this method requires it, set reverseindex to an IndexedCorpus instance upon model construction")
    
        cdef t_relationmap  relations = self.data.getrightcooc(pattern.cpattern, occurrencethreshold, category, size)
        cdef t_relationmap_iterator relit = relations.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while relit != relations.end():
            cpattern = deref(relit).first
            value = deref(relit).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(relit)
    
    def computeflexgrams_fromskipgrams(self):
        """Compute flexgrams from skipgrams in the model. Returns the number of flexgrams found."""
        return self.data.computeflexgrams_fromskipgrams()
    
    def computeflexgrams_fromcooc(self,double threshold):
        """Compute flexgrams based on  co-occurence. The threshold is expressed in normalised pointwise mutual information. Returns the number of flexgrams found. Flexgrams contain at only one gap using this method."""
        return self.data.computeflexgrams_fromcooc(threshold)

cdef class PatternSetModel:
    cdef cPatternSetModel data

    def __bool__(self):
        return self.data.size() > 0
    
    def __len__(self):
        """Return the total number of patterns in the dictionary"""
        return self.data.size()
    
    cpdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, pattern):
        """Test if the pattern is in the dictionary
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: bool
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.has(pattern)
    
    def __iter__(self):
        """Iterate over all patterns in the dictionary"""
        it = self.data.begin()
        cdef cPattern cpattern
        it_end = self.data.end()
        while it != it_end:
            cpattern = deref(it)
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def add(self, Pattern pattern):
        """Adds a pattern to the set
    
        :param pattern: The pattern to add
        :type pattern: Pattern
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        self.data.insert(pattern.cpattern)
    
    #cdef getdatapointer(self):
    #    return address(self.data)

    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()

    def __init__(self, str filename = "",PatternModelOptions options = None):
        """Initialise a pattern model. Either an empty one or loading from file.

        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions

        """
        if filename:
            if not options:
                options = PatternModelOptions()
            self.load(filename,options)

    def load(self, str filename, PatternModelOptions options=None):
        """Load a patternmodel from file

        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if options is None:
            options = PatternModelOptions()
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
        self.data.load(encode(filename), options.coptions)

    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)

    def write(self, str filename):
        """Write a patternmodel to file

        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))

cpdef write(self, str filename):
    """Write a patternmodel to file

    :param filename: The name of the file to write to
    :type filename: str
    """
    self.data.write(encode(filename))

cdef class UnindexedPatternModel:
    """Unindexed Pattern Model, less flexible and powerful than its indexed counterpart, but smaller memory footprint"""
    cdef cPatternModel[uint32_t,cBaseValueHandler[uint32_t],cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint64_t]] data
    cdef cPatternModel[uint32_t,cBaseValueHandler[uint32_t],cPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint64_t]].iterator it

    cdef object corpus
    
    def __len__(self):
        """Returns the total number of distinct patterns in the model"""
        return self.data.size()
    
    def __bool__(self):
        return self.data.size() > 0
    
    def types(self):
        """Returns the total number of distinct word types in the training data"""
        return self.data.types()
    
    def tokens(self):
        """Returns the total number of tokens in the training data"""
        return self.data.tokens()
    
    def minlength(self):
        """Returns the minimum pattern length in the model"""
        return self.data.minlength()
    
    def maxlength(self):
        """Returns the maximum pattern length in the model"""
        return self.data.maxlength()
    
    def type(self):
        """Returns the model type (10 = UNINDEXED, 20 = INDEXED)"""
        return self.data.type()
    
    def version(self):
        """Return the version of the model type"""
        return self.data.version()
    
    def occurrencecount(self, Pattern pattern):
        """Returns the number of times the specified pattern occurs in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.occurrencecount(pattern.cpattern)
    
    def coveragecount(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coveragecount(pattern.cpattern)
    
    def coverage(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data, as a fraction of the total amount of tokens
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coverage(pattern.cpattern)
    
    def frequency(self, Pattern pattern):
        """Returns the frequency of the pattern within its category (ngram/skipgram/flexgram) and exact size class. For a bigram it will thus return the bigram frequency.
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.frequency(pattern.cpattern)
    
    
    def totaloccurrencesingroup(self, int category=0, int n=0):
        """Returns the total number of occurrences in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total occurrence count over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaloccurrencesingroup(category,n)
    
    def totalpatternsingroup(self, int category=0, int n=0):
        """Returns the total number of distinct patterns in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of distrinct skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totalpatternsingroup(category,n)
    
    def totaltokensingroup(self, int category=0, int n=0):
        """Returns the total number of covered tokens in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered tokens over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
    
    def totalwordtypesingroup(self, int category=0, int n=0):
        """Returns the total number of covered word types (unigram types) in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered word types over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
        return self.data.totalwordtypesingroup(category,n)
    
    cdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, pattern):
        """Tests if a pattern is in the model:
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: bool
    
        Example::
    
            pattern in patternmodel
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.has(pattern)
    
    def __getitem__(self, pattern):
        """Retrieves the value for the pattern
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int (for Unindexed Models), IndexData (for Indexed models)
    
        Example (unindexed model)::
    
            occurrences = model[pattern]
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.getdata(pattern)
    
    
    
    def __iter__(self):
        """Iterates over all patterns in the model. Also consider using the filter() or top() methods if they suit your needs, as they will be faster than doing it manually.
    
        Example::
    
            for pattern in model:
                print(pattern.tostring(classdecoder))
    
        """
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __init__(self, str filename = "",PatternModelOptions options = None, constrainmodel = None, reverseindex = None):
        """Initialise a pattern model. Either an empty one or loading from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A model to be used as a constraint, only patterns occuring in this constraint model will be loaded/trained
        :type constrainmodel: IndexedPatternModel, UnindexedPatternModel or None (default)
        :param reverseindex: Corpus data to use as reverse index. On indexed models, this is required for various operations, including computation of skipgrams
        :type reverseindex: IndexedCorpus or None
        """
    
        self.corpus = None
        if reverseindex:
            self.loadreverseindex(reverseindex)
    
        if filename:
            if not options:
                options = PatternModelOptions()
            if filename and not os.path.exists(filename):
                raise FileNotFoundError(filename)
            self.load(filename,options, constrainmodel)
    
    def load(self, str filename, PatternModelOptions options=None, constrainmodel = None):
        """Load a patternmodel from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if not options:
            options = PatternModelOptions()
    
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
    
        if isinstance(constrainmodel, IndexedPatternModel):
            self.loadconstrainedbyindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbyunindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbysetmodel(filename,options, constrainmodel)
        else:
            self.data.load(encode(filename), options.coptions, NULL)
    
    def loadreverseindex(self, IndexedCorpus reverseindex):
        self.data.reverseindex = reverseindex.data
        self.corpus = reverseindex #so python doesn't garbage collect the python object
    
    
    cpdef loadconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbysetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)
    
    cpdef write(self, str filename):
        """Write a patternmodel to file
    
        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))
    
    cpdef printmodel(self,ClassDecoder decoder):
        """Print the entire pattern model to stdout, a detailed overview
    
        :param decoder: The class decoder
        :type decoder: ClassDecoder
        """
        self.data.printmodel(&cout, decoder.data )
    
    cpdef train(self, str filename, PatternModelOptions options, constrainmodel = None):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A patternmodel or patternsetmodel to constrain training (default None)
        :type constrainmodel: None, UnindexedPatternModel, IndexedPatternModel, PatternSetModel
        """
    
        if self.data.reverseindex != NULL:
            filename = ""
        if isinstance(self, IndexedPatternModel) and self.data.reverseindex == NULL and options.DOSKIPGRAMS:
            raise ValueError("No reversindex was specified but you are requesting to train skipgrams, set reverseindex to an IndexedCorpus instance upon model construction")
    
    
        if constrainmodel:
            assert len(constrainmodel) >= 0
            if isinstance(constrainmodel, IndexedPatternModel):
                self.trainconstrainedbyindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, UnindexedPatternModel):
                self.trainconstrainedbyunindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternSetModel):
                self.trainconstrainedbypatternsetmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternAlignmentModel_float):
                self.trainconstrainedbyalignmodel(filename, options, constrainmodel)
            else:
                raise ValueError("Invalid type for constrainmodel") #TODO: build patternmodel on the fly from an iterable of patterns or lower level patternstorage
        elif filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, NULL)
    
    cpdef train_filtered(self, str filename, PatternModelOptions options, PatternSet filterset):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param filterset: An instance of PatternSet. A limited set of skipgrams/flexgrams to use as a filter, patterns will only be included if they are an instance of a skipgram in this list (i.e. disjunctive). Ngrams can also be included as filters, if a pattern subsumes one of the ngrams in the filter, it counts as a match (or if it matches it exactly).
        """
        cdef cPatternSet[uint] * cfilterset = address(filterset.data)
    
        if filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, cfilterset)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, cfilterset)
    
    
    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()
    
    cpdef trainconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbypatternsetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyalignmodel(self, str filename, PatternModelOptions options, PatternAlignmentModel_float constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*>  NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef report(self):
        """Print a detailed statistical report to stdout"""
        self.data.report(&cout)
    
    cpdef printhistogram(self):
        """Print a histogram to stdout"""
        self.data.histogram(&cout)
    
    
    
    cpdef prune(self, int threshold, int n=0):
        """Prune all patterns occurring below the threshold.
    
        :param threshold: the threshold value (minimum number of occurrences)
        :type threshold: int
        :param n: prune only patterns of the specified size, use 0 (default) for no size limitation
        :type n: int
        """
        self.data.prune(threshold, n)
    
    
    def reverseindex(self):
        """Returns the reverseindex associated with the model, this will be an instance of IndexedCorpus. Use getreverseindex( (sentence, token) ) instead if you want to query the reverse index."""
        return self.corpus
    
    
    def getreverseindex(self, indexreference):
        """Generator over all patterns occurring at the specified index reference
    
        :param indexreference: a (sentence, tokenoffset) tuple
        """
    
        if not isinstance(indexreference, tuple) or not len(indexreference) == 2:
            raise ValueError("Expected tuple")
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef int sentence = indexreference[0]
        cdef int token = indexreference[1]
        cdef cIndexReference ref = cIndexReference(sentence, token)
        cdef unordered_set[cPatternPointer] results = self.data.getreverseindex(ref)
        cdef unordered_set[cPatternPointer].iterator resit = results.begin()
        cdef cPattern cpattern
        while resit != results.end():
            cpattern = deref(resit).pattern()
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(resit)
    
    def getreverseindex_bysentence(self, int sentence):
        """Generator over all patterns occurring in the specified sentence
    
        :param sentence: a sentence number
        """
    
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef vector[pair[cIndexReference,cPatternPointer]] results = self.data.getreverseindex_bysentence(sentence)
        cdef vector[pair[cIndexReference,cPatternPointer]].iterator resit = results.begin()
        cdef pair[cIndexReference,cPatternPointer] p
        cdef cPattern cpattern
        while resit != results.end():
            p = deref(resit)
            pattern = Pattern()
            cpattern = p.second.pattern()
            pattern.bind(cpattern)
            yield (p.first.sentence, p.first.token), pattern
            inc(resit)
    
    
    def histogram(self, unsigned int threshold=0, unsigned int cap=0, int category = 0, int size = 0):
        """Generator over a histogram of occurrence count data, produces (occurrencecount, frequency) tuples. A minimum threshold may be configured, or a cap on total number of occurrences may be specified (to get only the top occurrences). The histogram can be constrained by category and/or pattern size (if set to >0 values)"""
        cdef stdmap[unsigned int,unsigned int] hist
        cdef stdmap[unsigned int,unsigned int].iterator it
        self.data.histogram(hist,threshold,cap, category, size)
        it = hist.begin()
        while it != hist.end():
            yield deref(it).first, deref(it).second
            inc(it)
    
    
    def top(self, int amount, int category = 0, int size = 0):
        """Generator over the top [amount] most occurring patterns (of specified category and size if set to values above 0). This is faster than iterating manually! Will return (pattern, occurrencecount) tuples (unsorted). Note that this may return less than the specified amount of patterns if there are multiple patterns with the same occurrence count in its tail. """
    
        cdef unsigned int smallest = self.data.topthreshold(amount, category, size)
        return self.filter(smallest, category, size)
    
    
    
    def filter(self, unsigned int threshold, int category = 0, int size = 0):
        """Generator over patterns occurring over the set occurrence threshold (and of specified category and size if set to values above 0). This is faster than iterating and filtering manually! Will return (pattern, occurrencecount) tuples (unsorted)"""
        cdef unsigned int count
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            inc(it)
            if ((category > 0) and (cpattern.category() != category)) or (size > 0) and (size != cpattern.n()):
                continue
            count = self.data.occurrencecount(cpattern)
            if count >= threshold:
                pattern = Pattern()
                pattern.bind(cpattern)
                yield pattern, count
    
    def getinstance(self, tuple pos, Pattern pattern):
        """Gets a specific instance of a pattern (skipgram or flexgram), at the specified position. Raises a KeyError when not found."""
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
        return self.corpus.getinstance(pos, pattern)
    
    cpdef getdata(self, Pattern pattern):
        if pattern in self:
            return self.data[pattern.cpattern]
        else:
            raise KeyError
    
    def items(self):
        """Iterate over all patterns and their occurrence count in this model"""
        it = self.data.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while it != self.data.end():
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    cpdef add(self, Pattern pattern, int count=1):
        """Add a pattern to the unindexed model
    
        :param pattern: The pattern to add
        :type pattern: Pattern
        :param count: The number of occurrences
        :type count: int
        """
        self.data[pattern.cpattern] = self.data[pattern.cpattern] + count


cdef class OrderedUnindexedPatternModel:
    """Unindexed Pattern Model, implemented using an ordered map, less flexible and powerful than its indexed counterpart, but smaller memory footprint"""
    cdef cPatternModel[uint32_t,cBaseValueHandler[uint32_t],cHashOrderedPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint64_t]] data
    cdef cPatternModel[uint32_t,cBaseValueHandler[uint32_t],cHashOrderedPatternMap[uint32_t,cBaseValueHandler[uint32_t],uint64_t]].iterator it

    cdef object corpus
    
    def __len__(self):
        """Returns the total number of distinct patterns in the model"""
        return self.data.size()
    
    def __bool__(self):
        return self.data.size() > 0
    
    def types(self):
        """Returns the total number of distinct word types in the training data"""
        return self.data.types()
    
    def tokens(self):
        """Returns the total number of tokens in the training data"""
        return self.data.tokens()
    
    def minlength(self):
        """Returns the minimum pattern length in the model"""
        return self.data.minlength()
    
    def maxlength(self):
        """Returns the maximum pattern length in the model"""
        return self.data.maxlength()
    
    def type(self):
        """Returns the model type (10 = UNINDEXED, 20 = INDEXED)"""
        return self.data.type()
    
    def version(self):
        """Return the version of the model type"""
        return self.data.version()
    
    def occurrencecount(self, Pattern pattern):
        """Returns the number of times the specified pattern occurs in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.occurrencecount(pattern.cpattern)
    
    def coveragecount(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coveragecount(pattern.cpattern)
    
    def coverage(self, Pattern pattern):
        """Returns the number of tokens all instances of the specified pattern cover in the training data, as a fraction of the total amount of tokens
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.coverage(pattern.cpattern)
    
    def frequency(self, Pattern pattern):
        """Returns the frequency of the pattern within its category (ngram/skipgram/flexgram) and exact size class. For a bigram it will thus return the bigram frequency.
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: float
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.frequency(pattern.cpattern)
    
    
    def totaloccurrencesingroup(self, int category=0, int n=0):
        """Returns the total number of occurrences in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total occurrence count over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaloccurrencesingroup(category,n)
    
    def totalpatternsingroup(self, int category=0, int n=0):
        """Returns the total number of distinct patterns in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of distrinct skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totalpatternsingroup(category,n)
    
    def totaltokensingroup(self, int category=0, int n=0):
        """Returns the total number of covered tokens in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered tokens over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
    
    def totalwordtypesingroup(self, int category=0, int n=0):
        """Returns the total number of covered word types (unigram types) in the specified group, within the specified category and/or size class, you can set either to zero (default) to consider all. Example, category=Category.SKIPGRAM and n=0 would consider give the total number of covered word types over all skipgrams.
    
        :param category: The category constraint (Category.NGRAM, Category.SKIPGRAM, Category.FLEXGRAM or 0 for no-constraint, default)
        :type category: int
        :param n: The size constraint (0= no constraint, default)
        :type n: int
        :rtype: int
        """
        return self.data.totaltokensingroup(category,n)
        return self.data.totalwordtypesingroup(category,n)
    
    cdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    def __contains__(self, pattern):
        """Tests if a pattern is in the model:
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: bool
    
        Example::
    
            pattern in patternmodel
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.has(pattern)
    
    def __getitem__(self, pattern):
        """Retrieves the value for the pattern
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int (for Unindexed Models), IndexData (for Indexed models)
    
        Example (unindexed model)::
    
            occurrences = model[pattern]
        """
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.getdata(pattern)
    
    
    
    def __iter__(self):
        """Iterates over all patterns in the model. Also consider using the filter() or top() methods if they suit your needs, as they will be faster than doing it manually.
    
        Example::
    
            for pattern in model:
                print(pattern.tostring(classdecoder))
    
        """
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __init__(self, str filename = "",PatternModelOptions options = None, constrainmodel = None, reverseindex = None):
        """Initialise a pattern model. Either an empty one or loading from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A model to be used as a constraint, only patterns occuring in this constraint model will be loaded/trained
        :type constrainmodel: IndexedPatternModel, UnindexedPatternModel or None (default)
        :param reverseindex: Corpus data to use as reverse index. On indexed models, this is required for various operations, including computation of skipgrams
        :type reverseindex: IndexedCorpus or None
        """
    
        self.corpus = None
        if reverseindex:
            self.loadreverseindex(reverseindex)
    
        if filename:
            if not options:
                options = PatternModelOptions()
            if filename and not os.path.exists(filename):
                raise FileNotFoundError(filename)
            self.load(filename,options, constrainmodel)
    
    def load(self, str filename, PatternModelOptions options=None, constrainmodel = None):
        """Load a patternmodel from file.
    
        :param filename: The name of the file to load, must be a valid colibri patternmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if not options:
            options = PatternModelOptions()
    
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
    
        if isinstance(constrainmodel, IndexedPatternModel):
            self.loadconstrainedbyindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbyunindexedmodel(filename,options, constrainmodel)
        elif isinstance(constrainmodel, UnindexedPatternModel):
            self.loadconstrainedbysetmodel(filename,options, constrainmodel)
        else:
            self.data.load(encode(filename), options.coptions, NULL)
    
    def loadreverseindex(self, IndexedCorpus reverseindex):
        self.data.reverseindex = reverseindex.data
        self.corpus = reverseindex #so python doesn't garbage collect the python object
    
    
    cpdef loadconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    cpdef loadconstrainedbysetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        self.data.load(encode(filename),options.coptions,  constrainmodel.getinterface())
    
    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)
    
    cpdef write(self, str filename):
        """Write a patternmodel to file
    
        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))
    
    cpdef printmodel(self,ClassDecoder decoder):
        """Print the entire pattern model to stdout, a detailed overview
    
        :param decoder: The class decoder
        :type decoder: ClassDecoder
        """
        self.data.printmodel(&cout, decoder.data )
    
    cpdef train(self, str filename, PatternModelOptions options, constrainmodel = None):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param constrainmodel: A patternmodel or patternsetmodel to constrain training (default None)
        :type constrainmodel: None, UnindexedPatternModel, IndexedPatternModel, PatternSetModel
        """
    
        if self.data.reverseindex != NULL:
            filename = ""
        if isinstance(self, IndexedPatternModel) and self.data.reverseindex == NULL and options.DOSKIPGRAMS:
            raise ValueError("No reversindex was specified but you are requesting to train skipgrams, set reverseindex to an IndexedCorpus instance upon model construction")
    
    
        if constrainmodel:
            assert len(constrainmodel) >= 0
            if isinstance(constrainmodel, IndexedPatternModel):
                self.trainconstrainedbyindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, UnindexedPatternModel):
                self.trainconstrainedbyunindexedmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternSetModel):
                self.trainconstrainedbypatternsetmodel(filename, options, constrainmodel)
            elif isinstance(constrainmodel, PatternAlignmentModel_float):
                self.trainconstrainedbyalignmodel(filename, options, constrainmodel)
            else:
                raise ValueError("Invalid type for constrainmodel") #TODO: build patternmodel on the fly from an iterable of patterns or lower level patternstorage
        elif filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, NULL)
    
    cpdef train_filtered(self, str filename, PatternModelOptions options, PatternSet filterset):
        """Train the patternmodel on the specified corpus data (a *.colibri.dat file)
    
        :param filename: The name of the file to load, must be a valid colibri.dat file. Can be set to an empty string if a corpus was pre-loaded already.
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        :param filterset: An instance of PatternSet. A limited set of skipgrams/flexgrams to use as a filter, patterns will only be included if they are an instance of a skipgram in this list (i.e. disjunctive). Ngrams can also be included as filters, if a pattern subsumes one of the ngrams in the filter, it counts as a match (or if it matches it exactly).
        """
        cdef cPatternSet[uint] * cfilterset = address(filterset.data)
    
        if filename:
            self.data.train(<string> encode(filename),options.coptions, NULL, cfilterset)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL ,options.coptions, NULL, cfilterset)
    
    
    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()
    
    cpdef trainconstrainedbyindexedmodel(self, str filename, PatternModelOptions options, IndexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyunindexedmodel(self, str filename, PatternModelOptions options, UnindexedPatternModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbypatternsetmodel(self, str filename, PatternModelOptions options, PatternSetModel constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*> NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef trainconstrainedbyalignmodel(self, str filename, PatternModelOptions options, PatternAlignmentModel_float constrainmodel):
        if filename:
            self.data.train(<string> encode(filename),options.coptions,  constrainmodel.getinterface(), NULL)
        elif self.data.reverseindex == NULL:
            raise ValueError("No filename or reverseindex specified!")
        else:
            self.data.train(<istream*>  NULL,options.coptions,  constrainmodel.getinterface(), NULL)
    
    cpdef report(self):
        """Print a detailed statistical report to stdout"""
        self.data.report(&cout)
    
    cpdef printhistogram(self):
        """Print a histogram to stdout"""
        self.data.histogram(&cout)
    
    
    
    cpdef prune(self, int threshold, int n=0):
        """Prune all patterns occurring below the threshold.
    
        :param threshold: the threshold value (minimum number of occurrences)
        :type threshold: int
        :param n: prune only patterns of the specified size, use 0 (default) for no size limitation
        :type n: int
        """
        self.data.prune(threshold, n)
    
    
    def reverseindex(self):
        """Returns the reverseindex associated with the model, this will be an instance of IndexedCorpus. Use getreverseindex( (sentence, token) ) instead if you want to query the reverse index."""
        return self.corpus
    
    
    def getreverseindex(self, indexreference):
        """Generator over all patterns occurring at the specified index reference
    
        :param indexreference: a (sentence, tokenoffset) tuple
        """
    
        if not isinstance(indexreference, tuple) or not len(indexreference) == 2:
            raise ValueError("Expected tuple")
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef int sentence = indexreference[0]
        cdef int token = indexreference[1]
        cdef cIndexReference ref = cIndexReference(sentence, token)
        cdef unordered_set[cPatternPointer] results = self.data.getreverseindex(ref)
        cdef unordered_set[cPatternPointer].iterator resit = results.begin()
        cdef cPattern cpattern
        while resit != results.end():
            cpattern = deref(resit).pattern()
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(resit)
    
    def getreverseindex_bysentence(self, int sentence):
        """Generator over all patterns occurring in the specified sentence
    
        :param sentence: a sentence number
        """
    
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
    
        cdef vector[pair[cIndexReference,cPatternPointer]] results = self.data.getreverseindex_bysentence(sentence)
        cdef vector[pair[cIndexReference,cPatternPointer]].iterator resit = results.begin()
        cdef pair[cIndexReference,cPatternPointer] p
        cdef cPattern cpattern
        while resit != results.end():
            p = deref(resit)
            pattern = Pattern()
            cpattern = p.second.pattern()
            pattern.bind(cpattern)
            yield (p.first.sentence, p.first.token), pattern
            inc(resit)
    
    
    def histogram(self, unsigned int threshold=0, unsigned int cap=0, int category = 0, int size = 0):
        """Generator over a histogram of occurrence count data, produces (occurrencecount, frequency) tuples. A minimum threshold may be configured, or a cap on total number of occurrences may be specified (to get only the top occurrences). The histogram can be constrained by category and/or pattern size (if set to >0 values)"""
        cdef stdmap[unsigned int,unsigned int] hist
        cdef stdmap[unsigned int,unsigned int].iterator it
        self.data.histogram(hist,threshold,cap, category, size)
        it = hist.begin()
        while it != hist.end():
            yield deref(it).first, deref(it).second
            inc(it)
    
    
    def top(self, int amount, int category = 0, int size = 0):
        """Generator over the top [amount] most occurring patterns (of specified category and size if set to values above 0). This is faster than iterating manually! Will return (pattern, occurrencecount) tuples (unsorted). Note that this may return less than the specified amount of patterns if there are multiple patterns with the same occurrence count in its tail. """
    
        cdef unsigned int smallest = self.data.topthreshold(amount, category, size)
        return self.filter(smallest, category, size)
    
    
    
    def filter(self, unsigned int threshold, int category = 0, int size = 0):
        """Generator over patterns occurring over the set occurrence threshold (and of specified category and size if set to values above 0). This is faster than iterating and filtering manually! Will return (pattern, occurrencecount) tuples (unsorted)"""
        cdef unsigned int count
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            inc(it)
            if ((category > 0) and (cpattern.category() != category)) or (size > 0) and (size != cpattern.n()):
                continue
            count = self.data.occurrencecount(cpattern)
            if count >= threshold:
                pattern = Pattern()
                pattern.bind(cpattern)
                yield pattern, count
    
    def getinstance(self, tuple pos, Pattern pattern):
        """Gets a specific instance of a pattern (skipgram or flexgram), at the specified position. Raises a KeyError when not found."""
        if self.data.reverseindex == NULL:
            raise ValueError("No reverse index loaded")
        return self.corpus.getinstance(pos, pattern)
    
    cpdef getdata(self, Pattern pattern):
        if pattern in self:
            return self.data[pattern.cpattern]
        else:
            raise KeyError
    
    def items(self):
        """Iterate over all patterns and their occurrence count in this model"""
        it = self.data.begin()
        cdef cPattern cpattern
        cdef unsigned int value
        while it != self.data.end():
            cpattern = deref(it).first
            value = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            yield (pattern,value)
            inc(it)
    
    cpdef add(self, Pattern pattern, int count=1):
        """Add a pattern to the unindexed model
    
        :param pattern: The pattern to add
        :type pattern: Pattern
        :param count: The number of occurrences
        :type count: int
        """
        self.data[pattern.cpattern] = self.data[pattern.cpattern] + count

cdef class PatternModelOptions:
    """Options for Pattern model, you can get and set the following attributes:

    * MINTOKENS - The token threshold, patterns with an occurrence below this will be pruned
    * MAXLENGTH - Maximum pattern length
    * DOSKIPGRAMS - Compute skipgrams?
    * DOSKIPGRAMS_EXHAUSTIVE - Compute skipgrams exhaustively?
    * MINSKIPTYPES - Minimum amount of different skip content types
    * DOREVERSEINDEX - Build reverse index? (default: True)
    * DOPATTERNPERLINE - Assume each line holds one single pattern.
    * MINTOKENS_UNIGRAMS - Word occurrence threshold (secondary threshold): only count patterns in which the words/unigrams occur at least this many times, only effective when the      primary
    * DOREMOVENGRAMS - Remove n-grams from the model
    * DOREMOVESKIPGRAMS - Remove skipgrams from the model
    * DOREMOVEFLEXGRAMS - Remove flexgrams from the model
    * DORESET - Reset all counts before training
    * DEBUG
    * QUIET (default: False)

    These can also be passed at keyword arguments to the constructor, in a case insensitive fashion::

        options = PatternModelOptions(mintokens=3)
    """
    cdef cPatternModelOptions coptions

    def __init__(self, **kwargs):
        for kwarg, value in kwargs.items():
            setattr(self,kwarg.upper(), value)

    def __setattr__(self,key, value):
        if key == 'MINTOKENS':
            self.coptions.MINTOKENS = value
        elif key == 'MINLENGTH':
            self.coptions.MINLENGTH = value
        elif key == 'MAXLENGTH':
            self.coptions.MAXLENGTH = value
        elif key == 'DOSKIPGRAMS':
            self.coptions.DOSKIPGRAMS = value
        elif key == 'DOSKIPGRAMS_EXHAUSTIVE':
            self.coptions.DOSKIPGRAMS_EXHAUSTIVE = value
        elif key == 'MINTOKENS_UNIGRAMS':
            self.coptions.MINTOKENS_UNIGRAMS = value
        elif key == 'MINSKIPTYPES':
            self.coptions.MINSKIPTYPES = value
        elif key == 'DOREVERSEINDEX':
            self.coptions.DOREVERSEINDEX = value
        elif key == 'DOPATTERNPERLINE':
            self.coptions.DOPATTERNPERLINE = value
        elif key == 'DOREMOVENGRAMS':
            self.coptions.DOREMOVENGRAMS = value
        elif key == 'DOREMOVESKIPGRAMS':
            self.coptions.DOREMOVESKIPGRAMS = value
        elif key == 'DOREMOVEFLEXGRAMS':
            self.coptions.DOREMOVEFLEXGRAMS = value
        elif key == 'DORESET':
            self.coptions.DORESET = value
        elif key == 'DEBUG':
            self.coptions.DEBUG = value
        elif key == 'QUIET':
            self.coptions.QUIET = value
        else:
            raise KeyError

    def __getattr__(self,key):
        if key == 'MINTOKENS':
            return self.coptions.MINTOKENS
        elif key == 'MINLENGTH':
            return self.coptions.MINLENGTH
        elif key == 'MAXLENGTH':
            return self.coptions.MAXLENGTH
        elif key == 'DOSKIPGRAMS':
            return self.coptions.DOSKIPGRAMS
        elif key == 'DOSKIPGRAMS_EXHAUSTIVE':
            return self.coptions.DOSKIPGRAMS_EXHAUSTIVE
        elif key == 'MINTOKENS_UNIGRAMS':
            return self.coptions.MINTOKENS_UNIGRAMS
        elif key == 'MINSKIPTYPES':
            return self.coptions.MINSKIPTYPES
        elif key == 'DOREVERSEINDEX':
            return self.coptions.DOREVERSEINDEX
        elif key == 'DOPATTERNPERLINE':
            return self.coptions.DOPATTERNPERLINE
        elif key == 'DOREMOVENGRAMS':
            return self.coptions.DOREMOVENGRAMS
        elif key == 'DOREMOVESKIPGRAMS':
            return self.coptions.DOREMOVESKIPGRAMS
        elif key == 'DOREMOVEFLEXGRAMS':
            return self.coptions.DOREMOVEFLEXGRAMS
        elif key == 'DORESET':
            return self.coptions.DORESET
        elif key == 'DEBUG':
            return self.coptions.DEBUG
        elif key == 'QUIET':
            return self.coptions.QUIET
        else:
            raise KeyError

cdef class IndexedCorpus:
    """An indexed version of a corpus, reads an entire corpus (colibri.dat file) in memory"""
    cdef cIndexedCorpus * data
    cdef str _filename
    cdef bool unload

    cdef object frommodel #allow assigning python model from which we take the reverse index, to prevent the python garbage collector collecting the model when we are still alive


    def __init__(self, str filename=""):
        """:param filename: The name of the colibri.dat file to load"""
        self._filename = filename
        self.data = new cIndexedCorpus()
        if filename:
            self.data.load(encode(filename), True) #last bool is debug
        self.unload = True


    cdef bind(self, cIndexedCorpus * d, unload=False):
        if self.data != NULL and self.unload:
            del self.data
        self.data = d
        self.unload = unload

    def __dealloc__(self):
        if self.data != NULL and self.unload:
            del self.data

    def filename(self):
        return self._filename

    def __len__(self):
        """Return the total number of tokens in the corpus"""
        return self.data.size()

    cdef has(self,tuple item):
        cdef int sentence = item[0]
        cdef int token = item[1]
        cdef cIndexReference ref = cIndexReference(sentence,token)
        return self.data.has(ref)


    cdef get(self,tuple item):
        cdef int sentence = item[0]
        cdef int token = item[1]
        cdef cIndexReference ref = cIndexReference(sentence,token)
        cdef cPattern cpattern
        cpattern = self.data.getpattern(ref,1)
        pattern = Pattern()
        pattern.bind(cpattern)
        return pattern

    cdef getslice(self,tuple start, tuple stop):
        cdef int startsentence = start[0]
        cdef int starttoken = start[1]
        cdef cIndexReference startref = cIndexReference(startsentence,starttoken)
        cdef int stopsentence = stop[0]
        cdef int stoptoken = stop[1]
        cdef cIndexReference stopref = cIndexReference(stopsentence,stoptoken)
        cdef cPattern cpattern = self.data.getpattern(startref, stopref.token - startref.token)
        pattern = Pattern()
        pattern.bind(cpattern)
        return pattern

    def __contains__(self, tuple indexreference):
        """Test if the indexreference, a (sentence,tokenoffset) tuple is in the corpus."""
        return self.has(indexreference)

    def __iter__(self):
        """Iterate over all indexes in the corpus, generator over (sentence, tokenoffset) tuples"""
        cdef cIndexedCorpus.iterator it = self.data.begin()
        cdef cIndexedCorpus.iterator endit = self.data.end()
        while it != endit:
            yield (it.index().sentence, it.index().token)
            inc(it)

    def __getitem__(self, item):
        """Retrieve the token Pattern given a (sentence, tokenoffset) tuple """
        if isinstance(item, slice):
            start = item.start
            stop = item.stop
            if not isinstance(start, tuple):
                raise ValueError("Expected tuple for start of slice")
            if not isinstance(stop, tuple):
                raise ValueError("Expected tuple for end of slice")
            if start[0] != stop[0]:
                raise ValueError("Slices only supported within the same sentence")
            return self.getslice(start, stop)
        else:
            if not isinstance(item, tuple):
                raise ValueError("Expected tuple")
            return self.get(item)


    def items(self):
        """Iterate over all indexes and their unigram patterns. Yields ((sentence,tokenoffset), unigrampattern) tuples"""
        it = self.data.begin()
        cdef cPattern cpattern
        cdef cIndexReference ref
        while it != self.data.end():
            cpattern = it.pattern()
            ref = it.index()
            pattern = Pattern()
            pattern.bind(cpattern)
            yield ( (ref.sentence, ref.token), pattern )
            inc(it)

    def findpattern(self, Pattern pattern, int sentence = 0, bool instantiate = False):
        """Generator over the indexes in the corpus where this pattern is found. Note that this is much slower than using the forward index on an IndexedPatternModel!!!

        :param pattern: The pattern to find
        :type pattern: Pattern
        :param sentence: Set to a non-zero value to limit the search to a single sentence (default: 0, search entire corpus)
        :type sentence: int
        :param instantiate: Instantiate all skipgrams and flexgrams (i.e, return n-grams) (default: False)
        :type instantiate: bool
        :rtype: generator over ((sentence, tokenoffset),pattern) tuples
        """

        cdef cPattern cpattern
        cdef cIndexReference ref
        matches = self.data.findpattern(pattern.cpattern,sentence,instantiate)
        it = matches.begin()
        while it != matches.end():
            ref = deref(it).first
            cpattern = deref(it).second.pattern()
            foundpattern = Pattern()
            foundpattern.bind(cpattern)
            yield ((ref.sentence, ref.token), foundpattern)
            inc(it)

    def getinstance(self, tuple pos, Pattern pattern):
        """Gets a specific instance of a pattern (skipgram or flexgram), at the specified position. Raises a KeyError when not found."""
        cdef cIndexReference ref = cIndexReference(pos[0],pos[1])
        cdef cPatternPointer ppin = pattern.cpattern.getpointer()
        cdef cPatternPointer ppout = self.data.getinstance(ref,ppin)
        foundpattern = Pattern()
        cdef cPattern cpattern = ppout.pattern()
        foundpattern.bind(cpattern)
        return foundpattern


    def sentencecount(self):
        """Returns the number of sentences. ( The C++ equivalent is called sentences() ) """
        return self.data.sentences()


    def getsentence(self, int i):
        """Get the specified sentence as a pattern, raises KeyError when the sentence, or tokens therein, does not exist"""
        cdef cPattern cpattern = self.data.getsentence(i)
        pattern = Pattern()
        pattern.bind(cpattern)
        return pattern

    def sentences(self):
        """Iterates over all sentences, returning each as a pattern"""
        cdef int sentencecount = self.data.sentences()
        for i in range(1, sentencecount+1):
            yield self.getsentence(i)

    def sentencelength(self,int sentence):
        """Returns the length of the specified sentences, raises KeyError when it doesn't exist"""
        return self.data.sentencelength(sentence)

cdef class PatternVector:
    cdef cPatternVector data

    cdef bind(self, cPatternVector & cvec):
        self.data = cvec

    def __len__(self):
        return self.data.size()

    def __bool__(self):
        return self.data.size() > 0

    cdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)

    def __contains__(self, Pattern pattern):
        return self.has(pattern)

    cdef append(self, Pattern pattern):
        self.data.insert(pattern.cpattern)

    def __iter__(self):
        cdef cPatternVector.iterator it_end = self.data.end()
        cdef cPatternVector.iterator it = self.data.begin()
        while it != it_end:
            pattern = Pattern()
            pattern.bind(deref(it))
            yield pattern
            inc(it)

cdef class PatternFeatureVectorMap_float:
    cdef cPatternFeatureVectorMap[double] data
    cdef cPatternFeatureVectorMap[double].iterator it

    cdef bind(self, cPatternFeatureVectorMap[double] & cmap):
        self.data = cmap

    def __len__(self):
        return self.data.size()


    def __bool__(self):
        return self.data.size() > 0

    cdef has(self, Pattern pattern):
        return self.data.has(pattern.cpattern)

    def __contains__(self, Pattern pattern):
        return self.has(pattern)

    cdef getdata(self, Pattern pattern):
        cdef cPatternFeatureVector[double] * v = self.data.getdata(pattern.cpattern)
        targetpattern = Pattern()
        targetpattern.bind(v.pattern)
        return (targetpattern, v.data)

    def __getitem__(self, pattern):
        if not isinstance(pattern,Pattern):
            raise ValueError("Argument must be Pattern instance")
        return self.getdata(pattern)

    cpdef setdata(self, Pattern pattern, tuple features):
        cdef cPatternFeatureVector[double] * v = self.data.getdata(pattern.cpattern)
        v.data.clear()
        for e in features:
            if isinstance(e,float) or isinstance(e, int):
                v.data.push_back(e)
            else:
                raise ValueError

    def __setitem__(self, pattern, value):
        if not isinstance(pattern,Pattern):
            raise ValueError("Key must be Pattern instance")
        if not isinstance(value,tuple) or all([ isinstance(x,float) or isinstance(x,int) for x in value]):
            raise ValueError("Value must be tuple containing floats")
        self.setdata(pattern, value)

    def items(self):
        cdef cPatternFeatureVector[double] * v
        cdef cPatternFeatureVectorMap[double].iterator it = self.data.begin()
        cdef cPatternFeatureVectorMap[double].iterator it_end = self.data.end()
        while it != it_end:
            v  = deref(it)
            pattern = Pattern()
            pattern.bind(v.pattern)
            yield (pattern, v.data)
            inc(it)

    def __iter__(self):
        cdef cPatternFeatureVector[double] * v
        cdef cPatternFeatureVectorMap[double].iterator it = self.data.begin()
        cdef cPatternFeatureVectorMap[double].iterator it_end = self.data.end()
        while it != it_end:
            v  = deref(it)
            pattern = Pattern()
            pattern.bind(v.pattern)
            yield pattern
            inc(it)




cdef class PatternAlignmentModel_float:
    """Pattern Alignment Model, maps patterns to pattern to score vectors (float)"""
    cdef cPatternAlignmentModel[double] data
    cdef cPatternAlignmentModel[double].iterator it

    def __len__(self):
        """Returns the total number of distinct patterns in the model"""
        return self.data.size()
    
    def __bool__(self):
        return self.data.size() > 0
    
    def types(self):
        """Returns the total number of distinct word types in the training data"""
        return self.data.types()
    
    def tokens(self):
        """Returns the total number of tokens in the training data"""
        return self.data.tokens()
    
    def minlength(self):
        """Returns the minimum pattern length in the model"""
        return self.data.minlength()
    
    def maxlength(self):
        """Returns the maximum pattern length in the model"""
        return self.data.maxlength()
    
    def type(self):
        """Returns the model type (10 = UNINDEXED, 20 = INDEXED)"""
        return self.data.getmodeltype()
    
    def version(self):
        """Return the version of the model type"""
        return self.data.getmodelversion()
    
    cdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    cdef hastuple(self, Pattern pattern, Pattern pattern2):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern, pattern2.cpattern)
    
    def __contains__(self, pattern):
        """Tests if a pattern is in the model:
    
        :param pattern: A pattern or a pair of patterns
        :type pattern: Pattern or 2-tuple of patterns
        :rtype: bool
    
        Example::
    
            sourcepattern in alignmodel
            (sourcepattern, targetpattern) in alignmodel
        """
        if isinstance(pattern, tuple):
            if len(pattern) != 2 or not isinstance(pattern[0], Pattern) or not isinstance(pattern[1], Pattern):
                raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
            return self.hastuple(pattern[0], pattern[1])
    
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
    
        return self.has(pattern)
    
    def __getitem__(self, pattern):
        """Retrieves the value for the pattern
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int (for Unindexed Models), IndexData (for Indexed models)
    
        Example (unindexed model)::
    
            occurrences = model[pattern]
        """
        if isinstance(pattern, tuple):
            if len(pattern) != 2 or not isinstance(pattern[0], Pattern) or not isinstance(pattern[1], Pattern):
                raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
            return self.getdatatuple(pattern[0], pattern[1])
    
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
    
        return self.getdata(pattern)
    
    
    
    def __iter__(self):
        """Iterates over all source patterns in the model.
    
        Example::
    
            for sourcepattern in alignmodel:
                print(pattern.tostring(classdecoder))
    
        """
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __init__(self, str filename = "",PatternModelOptions options = None):
        """Initialise an alignment model. Either an empty one or loading from file.
    
        :param filename: The name of the file to load, must be a valid colibri alignmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
    
        """
        if filename:
            self.load(filename,options)
    
    def load(self, str filename, PatternModelOptions options=None):
        """Load an alignment model from file
    
        :param filename: The name of the file to load, must be a valid colibri alignmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if options is None:
            options = PatternModelOptions()
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
        self.data.load(encode(filename), options.coptions)
    
    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)
    
    cpdef write(self, str filename):
        """Write an alignment model to file
    
        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))
    
    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()

    cdef getdata(self, Pattern pattern):
        cdef cPatternFeatureVectorMap[double] cmap
        if pattern in self:
            cmap = deref(self.data.getdata(pattern.cpattern))
            pmap = PatternFeatureVectorMap_float()
            pmap.bind(cmap)
            return pmap
        else:
            raise KeyError

    cdef getfeatures(self, cPatternFeatureVector[double] * cvec):
        return cvec.data

    cdef getdatatuple(self, Pattern pattern, Pattern pattern2):
        cdef cPatternFeatureVector[double] * cvec
        if self.data.has(pattern.cpattern, pattern2.cpattern):
            cvec = self.data.getfeaturevector(pattern.cpattern, pattern2.cpattern)
            return self.getfeatures(cvec)
        else:
            raise KeyError

    def items(self):
        """Iterate over all patterns and PatternFeatureVectorMaps in this model"""
        it = self.data.begin()
        it_end = self.data.end()
        cdef cPattern cpattern
        cdef cPatternFeatureVectorMap[double] cmap
        while it != it_end:
            cpattern = deref(it).first
            cmap = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            pmap = PatternFeatureVectorMap_float()
            pmap.bind(cmap)
            yield (pattern,pmap)
            inc(it)

    def triples(self):
        """Iterate over sourcepattern, targetpattern, feature triples"""
        it = self.data.begin()
        it_end = self.data.end()
        cdef cPattern cpattern
        cdef cPatternFeatureVectorMap[double] cmap
        while it != it_end:
            cpattern = deref(it).first
            cmap = deref(it).second
            sourcepattern = Pattern()
            sourcepattern.bind(cpattern)

            it2 = cmap.begin()
            it2_end = cmap.end()
            while it2 != it2_end:
                cvec = deref(it2)
                targetpattern = Pattern()
                targetpattern.bind(cvec.pattern)
                yield (sourcepattern, targetpattern, self.getfeatures(cvec) )
                inc(it2)
            inc(it)

    cpdef add(self, Pattern pattern, Pattern pattern2, tuple l):
        """Add a pattern to the unindexed model

        :param pattern: The source pattern to add
        :type pattern: Pattern
        :param pattern: The target pattern to add
        :type pattern: Pattern
        :param l: Feature tuple (homogenously typed)
        :type l: tuple (of floats)
        :type count: int
        """
        cdef vector[double] v
        for e in l:
            if not isinstance(e, float) and not isinstance(e, int):
                raise ValueError("Expected list with instances of float")
            v.push_back(e)

        self.data.add(pattern.cpattern,pattern2.cpattern, v)


cdef class BasicPatternAlignmentModel:
    """Pattern Alignment Model, maps patterns to pattern to score vectors (float)"""
    cdef cBasicPatternAlignmentModel data
    cdef cBasicPatternAlignmentModel.iterator it
    cdef cBasicPatternAlignmentModel.iterator it_end

    def __len__(self):
        """Returns the total number of distinct patterns in the model"""
        return self.data.size()
    
    def __bool__(self):
        return self.data.size() > 0
    
    def types(self):
        """Returns the total number of distinct word types in the training data"""
        return self.data.types()
    
    def tokens(self):
        """Returns the total number of tokens in the training data"""
        return self.data.tokens()
    
    def minlength(self):
        """Returns the minimum pattern length in the model"""
        return self.data.minlength()
    
    def maxlength(self):
        """Returns the maximum pattern length in the model"""
        return self.data.maxlength()
    
    def type(self):
        """Returns the model type (10 = UNINDEXED, 20 = INDEXED)"""
        return self.data.getmodeltype()
    
    def version(self):
        """Return the version of the model type"""
        return self.data.getmodelversion()
    
    cdef has(self, Pattern pattern):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern)
    
    cdef hastuple(self, Pattern pattern, Pattern pattern2):
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern")
        return self.data.has(pattern.cpattern, pattern2.cpattern)
    
    def __contains__(self, pattern):
        """Tests if a pattern is in the model:
    
        :param pattern: A pattern or a pair of patterns
        :type pattern: Pattern or 2-tuple of patterns
        :rtype: bool
    
        Example::
    
            sourcepattern in alignmodel
            (sourcepattern, targetpattern) in alignmodel
        """
        if isinstance(pattern, tuple):
            if len(pattern) != 2 or not isinstance(pattern[0], Pattern) or not isinstance(pattern[1], Pattern):
                raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
            return self.hastuple(pattern[0], pattern[1])
    
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
    
        return self.has(pattern)
    
    def __getitem__(self, pattern):
        """Retrieves the value for the pattern
    
        :param pattern: A pattern
        :type pattern: Pattern
        :rtype: int (for Unindexed Models), IndexData (for Indexed models)
    
        Example (unindexed model)::
    
            occurrences = model[pattern]
        """
        if isinstance(pattern, tuple):
            if len(pattern) != 2 or not isinstance(pattern[0], Pattern) or not isinstance(pattern[1], Pattern):
                raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
            return self.getdatatuple(pattern[0], pattern[1])
    
        if not isinstance(pattern, Pattern):
            raise ValueError("Expected instance of Pattern or 2-tuple of Patterns")
    
        return self.getdata(pattern)
    
    
    
    def __iter__(self):
        """Iterates over all source patterns in the model.
    
        Example::
    
            for sourcepattern in alignmodel:
                print(pattern.tostring(classdecoder))
    
        """
        it = self.data.begin()
        cdef cPattern cpattern
        while it != self.data.end():
            cpattern = deref(it).first
            pattern = Pattern()
            pattern.bind(cpattern)
            yield pattern
            inc(it)
    
    def __init__(self, str filename = "",PatternModelOptions options = None):
        """Initialise an alignment model. Either an empty one or loading from file.
    
        :param filename: The name of the file to load, must be a valid colibri alignmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
    
        """
        if filename:
            self.load(filename,options)
    
    def load(self, str filename, PatternModelOptions options=None):
        """Load an alignment model from file
    
        :param filename: The name of the file to load, must be a valid colibri alignmodel file
        :type filename: str
        :param options: An instance of PatternModelOptions, containing the options used for loading
        :type options: PatternModelOptions
        """
        if options is None:
            options = PatternModelOptions()
        if filename and not os.path.exists(filename):
            raise FileNotFoundError(filename)
        self.data.load(encode(filename), options.coptions)
    
    def read(self, str filename, PatternModelOptions options=None):
        """Alias for load"""
        self.load(filename, options)
    
    cpdef write(self, str filename):
        """Write an alignment model to file
    
        :param filename: The name of the file to write to
        :type filename: str
        """
        self.data.write(encode(filename))
    
    cdef cPatternModelInterface* getinterface(self):
        return self.data.getinterface()

    cdef getdata(self, Pattern pattern):
        cdef cPatternVector cvec
        if pattern in self:
            cvec = deref(self.data.getdata(pattern.cpattern))
            pvec = PatternVector()
            pvec.bind(cvec)
            return pvec
        else:
            raise KeyError

    def items(self):
        """Iterate over all patterns and PatternVectors in this model, yields (Pattern, PatternVector) pairs"""
        it = self.data.begin()
        it_end = self.data.end()
        cdef cPatternVector cvec
        while it != it_end:
            cpattern = deref(it).first
            cvec = deref(it).second
            pattern = Pattern()
            pattern.bind(cpattern)
            pvec = PatternVector()
            pvec.bind(cvec)
            yield (pattern,pvec)
            inc(it)

    def pairs(self):
        """Iterate over sourcepattern, targetpattern pairs"""
        it = self.data.begin()
        it_end = self.data.end()
        cdef cPattern cpattern
        cdef cPattern ctargetpattern
        cdef cPatternVector cvec
        while it != it_end:
            cpattern = deref(it).first
            cvec = deref(it).second
            sourcepattern = Pattern()
            sourcepattern.bind(cpattern)

            it2 = cvec.begin()
            it2_end = cvec.end()
            while it2 != it2_end:
                ctargetpattern = deref(it2)
                targetpattern = Pattern()
                targetpattern.bind(ctargetpattern)
                yield (sourcepattern, targetpattern)
                inc(it2)
            inc(it)

    cpdef add(self, Pattern pattern, Pattern pattern2):
        """Add a pattern to the unindexed model

        :param pattern: The source pattern to add
        :type pattern: Pattern
        :param pattern: The target pattern to add
        :type pattern: Pattern
        :type count: int
        """
        self.data.add(pattern.cpattern,pattern2.cpattern)

UNKPATTERN = Pattern()
UNKPATTERN.bindunk()
SKIPPATTERN = Pattern()
SKIPPATTERN.bindskip()
FLEXPATTERN = Pattern()
FLEXPATTERN.bindflex()
BOUNDARYPATTERN = Pattern()
BOUNDARYPATTERN.bindboundary()
