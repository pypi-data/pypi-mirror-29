=======
What is it?
=======

Low-level wrappers for exiv2 for python >= 3.4 that pip installs on Windows.

* it only works on Windows. 
* it only supports Iptc
* low-level exposure of the C++ methods. Feel free to write a more pythonic interface on top.

=======
How do I set it up?
=======

* pip install exiv2

=======
Example
=======

::

    from exiv2 import lowlevel as exiv2

    im = exiv2.ImageFactory_open("out.jpg")
    exiv2.Image_readMetadata(im)               
    iptc_data = exiv2.Image_iptcData(im)
    key = "Iptc.Application2.Caption"
    datum = exiv2.IptcData_operator_bracket(iptc_data, key)
    value = exiv2.Iptcdatum_toString(datum)
    assert value == "*insert title here*"

    # change metadata
    result = exiv2.Iptcdatum_setValue(datum, "Hi Mum!")
    assert result == 0

    # make a new key
    key = "Iptc.Application2.Copyright"
    datum = exiv2.IptcData_operator_bracket(iptc_data, key)
    result = exiv2.Iptcdatum_setValue(datum, "(c) 2018")
    assert result == 0

    # clear exif and xmp data so we're sure we'll see the ipct data in
    # the file properties in windows explorer
    exiv2.Image_clearExifData(im)
    exiv2.Image_clearXmpData(im)

    # write
    exiv2.Image_writeMetadata(im)

    exiv2.Image_delete(im)



