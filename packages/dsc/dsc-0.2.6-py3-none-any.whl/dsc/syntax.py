#!/usr/bin/env python
__author__ = "Gao Wang"
__copyright__ = "Copyright 2016, Stephens lab"
__email__ = "gaow@uchicago.edu"
__license__ = "MIT"
'''
This file defines DSC syntax templates
'''
import re
from sos.syntax import LazyRegex, SOS_DIRECTIVES

DSC_KW = ['DSC_AUTO_OUTPUT_', 'DSC_TIMER'] # engineering keywords, reserved
DSC_KW.extend(SOS_DIRECTIVES)
DSC_MODP = ['^EXEC', '^FILTER', '^ALIAS', '^CONF'] # module properties

DSC_DERIVED_BLOCK = LazyRegex(r'^(.*?)\((.*?)\)$', re.VERBOSE)
DSC_BLOCK_NAME = LazyRegex(r'^[A-Za-z0-9_]+$', re.VERBOSE)
DSC_FILE_OP = LazyRegex(r'^file\((.*?)\)$', re.VERBOSE)
DSC_ASIS_OP = LazyRegex(r'^raw\((.*?)\)$', re.VERBOSE)
DSC_PACK_OP = LazyRegex(r'((?i)list|(?i)dict)\((.*?)\)', re.VERBOSE)
DSC_BLOCK_CONTENT = LazyRegex(r'^\s(.*?)', re.VERBOSE)
