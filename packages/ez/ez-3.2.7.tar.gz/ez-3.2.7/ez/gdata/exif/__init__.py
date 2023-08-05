# -*-*- encoding: utf-8 -*-*-
#
# This is gdata.photos.exif, implementing the exif namespace in gdata
#
# $Id: __init__.py 81 2007-10-03 14:41:42Z havard.gulldahl $
#
# Copyright 2007 Håvard Gulldahl 
# Portions copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module maps elements from the {EXIF} namespace[1] to GData objects. 
These elements describe image data, using exif attributes[2].

Picasa Web Albums uses the exif namespace to represent Exif data encoded 
in a photo [3].

Picasa Web Albums uses the following exif elements:
exif:distance
exif:exposure
exif:flash
exif:focallength
exif:fstop
exif:imageUniqueID
exif:iso
exif:make
exif:model
exif:tags
exif:time

[1]: http://schemas.google.com/photos/exif/2007. 
[2]: http://en.wikipedia.org/wiki/Exif
[3]: http://code.google.com/apis/picasaweb/reference.html#exif_reference
"""


__author__ = u'havard@gulldahl.no'# (Håvard Gulldahl)' #BUG: pydoc chokes on non-ascii chars in __author__
__license__ = 'Apache License v2'


import atom
import gdata

EXIF_NAMESPACE = 'http://schemas.google.com/photos/exif/2007'

class ExifBaseElement(atom.AtomBase):
  """Base class for elements in the EXIF_NAMESPACE (%s). To add new elements, you only need to add the element tag name to self._tag
  """ % EXIF_NAMESPACE
  
  _tag = ''
  _namespace = EXIF_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()

  def __init__(self, name=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.name = name
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

class Distance(ExifBaseElement):
  "(float) The distance to the subject, e.g. 0.0"
  
  _tag = 'distance'
def DistanceFromString(xml_string):
  return atom.CreateClassFromXMLString(Distance, xml_string)
  
class Exposure(ExifBaseElement):
  "(float) The exposure time used, e.g. 0.025 or 8.0E4"
  
  _tag = 'exposure'
def ExposureFromString(xml_string):
  return atom.CreateClassFromXMLString(Exposure, xml_string)
  
class Flash(ExifBaseElement):
  """(string) Boolean value indicating whether the flash was used.
  The .text attribute will either be `true' or `false'

  As a convenience, this object's .bool method will return what you want,
  so you can say:

  flash_used = bool(Flash)

  """
  
  _tag = 'flash'
  def __bool__(self):
    if self.text.lower() in ('true','false'):
      return self.text.lower() == 'true'
def FlashFromString(xml_string):
  return atom.CreateClassFromXMLString(Flash, xml_string)
  
class Focallength(ExifBaseElement):
  "(float) The focal length used, e.g. 23.7"
  
  _tag = 'focallength'
def FocallengthFromString(xml_string):
  return atom.CreateClassFromXMLString(Focallength, xml_string)
  
class Fstop(ExifBaseElement):
  "(float) The fstop value used, e.g. 5.0"
  
  _tag = 'fstop'
def FstopFromString(xml_string):
  return atom.CreateClassFromXMLString(Fstop, xml_string)
  
class ImageUniqueID(ExifBaseElement):
  "(string) The unique image ID for the photo. Generated by Google Photo servers"
  
  _tag = 'imageUniqueID'
def ImageUniqueIDFromString(xml_string):
  return atom.CreateClassFromXMLString(ImageUniqueID, xml_string)
  
class Iso(ExifBaseElement):
  "(int) The iso equivalent value used, e.g. 200"
  
  _tag = 'iso'
def IsoFromString(xml_string):
  return atom.CreateClassFromXMLString(Iso, xml_string)
  
class Make(ExifBaseElement):
  "(string) The make of the camera used, e.g. Fictitious Camera Company"
  
  _tag = 'make'
def MakeFromString(xml_string):
  return atom.CreateClassFromXMLString(Make, xml_string)
  
class Model(ExifBaseElement):
  "(string) The model of the camera used,e.g AMAZING-100D"
  
  _tag = 'model'
def ModelFromString(xml_string):
  return atom.CreateClassFromXMLString(Model, xml_string)
  
class Time(ExifBaseElement):
  """(int) The date/time the photo was taken, e.g. 1180294337000.
  Represented as the number of milliseconds since January 1st, 1970.
  
  The value of this element will always be identical to the value
  of the <gphoto:timestamp>.

  Look at this object's .isoformat() for a human friendly datetime string:

  photo_epoch = Time.text # 1180294337000
  photo_isostring = Time.isoformat() # '2007-05-27T19:32:17.000Z'

  Alternatively: 
  photo_datetime = Time.datetime() # (requires python >= 2.3)
  """
  
  _tag = 'time'
  def isoformat(self):
    """(string) Return the timestamp as a ISO 8601 formatted string,
    e.g. '2007-05-27T19:32:17.000Z'
    """
    import time
    epoch = float(self.text)/1000
    return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(epoch))
  
  def datetime(self):
    """(datetime.datetime) Return the timestamp as a datetime.datetime object

    Requires python 2.3
    """
    import datetime
    epoch = float(self.text)/1000
    return datetime.datetime.fromtimestamp(epoch)
  
def TimeFromString(xml_string):
  return atom.CreateClassFromXMLString(Time, xml_string)
  
class Tags(ExifBaseElement):
  """The container for all exif elements.
  The <exif:tags> element can appear as a child of a photo entry.
  """
  
  _tag = 'tags'
  _children = atom.AtomBase._children.copy()
  _children['{%s}fstop' % EXIF_NAMESPACE] = ('fstop', Fstop) 
  _children['{%s}make' % EXIF_NAMESPACE] = ('make', Make) 
  _children['{%s}model' % EXIF_NAMESPACE] = ('model', Model) 
  _children['{%s}distance' % EXIF_NAMESPACE] = ('distance', Distance) 
  _children['{%s}exposure' % EXIF_NAMESPACE] = ('exposure', Exposure) 
  _children['{%s}flash' % EXIF_NAMESPACE] = ('flash', Flash) 
  _children['{%s}focallength' % EXIF_NAMESPACE] = ('focallength', Focallength) 
  _children['{%s}iso' % EXIF_NAMESPACE] = ('iso', Iso) 
  _children['{%s}time' % EXIF_NAMESPACE] = ('time', Time) 
  _children['{%s}imageUniqueID' % EXIF_NAMESPACE] = ('imageUniqueID', ImageUniqueID) 

  def __init__(self, extension_elements=None, extension_attributes=None, text=None):
    ExifBaseElement.__init__(self, extension_elements=extension_elements,
                            extension_attributes=extension_attributes,
                            text=text)
    self.fstop=None
    self.make=None
    self.model=None
    self.distance=None
    self.exposure=None
    self.flash=None
    self.focallength=None
    self.iso=None
    self.time=None
    self.imageUniqueID=None
def TagsFromString(xml_string):
  return atom.CreateClassFromXMLString(Tags, xml_string)
  
