"""This is the IPv4 module.

This module does IPv4 stuff.

TODO: rewrite module description
"""

from pynetwork.custom_exceptions import NonWritableMemoryviewError

# requires empty, memoryview or IP packet binary
class IPv4Packet:
    
    def __init__(self, packet=None):
        self.header = None # IPv4Header object
        self.options = None # IPv4Options object
        self.payload = None # memoryview of payload data
        
        # if no packet was given, make a new one
        if(packet == None):
            self.header = IPv4Header()
        # else parse the packet data
        else:
            self.header = IPv4Header(packet[:20])    

        assert(self.header != None) # make sure we actually have something
        
        
    def get_options(self):
        pass
    
    def set_options(self):
        pass
    
    def get_payload(self):
        pass
    
    def set_payload(self, payload):
        pass
    
    
    
    
class IPv4Header:   
    # requires a writeable memoryview
    def __init__(self, header=None):                
        # reserve bytes if we don't have a header
        if(header == None):
            self.header = memoryview(bytearray(20))
        elif(type(header) == memoryview):
            # make sure it's read / write
            if(header.readonly):
                raise NonWritableMemoryviewError(self.__class__.__name__ + " requires a writable memoryview")
            else:
                self.header = header
        # wrong argument type
        else:
            raise TypeError(self.__class__.__name__ + ' constructor requires a writable memoryview')
    
    
    def get_version(self):
        return self.header[0] >> 4
    
    def set_version(self, version):
        self.header[0] = (version << 4) + self.get_ihl()
    
    def get_ihl(self):
        return self.header[0] & 0b00001111
    
    def set_ihl(self, ihl):
        self.header[0] = (self.header[0] & 0b11110000) + ihl
    
    def get_dscp(self):
        return (self.header[1] & 0b11111100) >> 2
    
    def set_dscp(self, dscp):
        self.header[1] = (dscp << 2) + self.get_ecn()
    
    def get_ecn(self):
        return self.header[1] & 0b00000011
    
    def set_ecn(self, ecn):
        self.header[1] = (self.header[0] & 0b11111100) + ecn
    
    def get_total_length(self):
        pass
    
    def set_total_length(self, length):
        pass
    
    def get_identification(self):
        pass
    
    def set_identification(self, identification):
        pass
    
    def get_flags(self):
        pass
    
    def set_flags(self, flags):
        pass
    
    def get_flag_df(self):
        pass
    
    def set_flag_df(self, flag):
        pass
    
    def get_flag_mf(self):
        pass
    
    def set_flag_mf(self, flag):
        pass
    
    def get_fragment_offset(self):
        pass
    
    def set_fragment_offset(self, offset):
        pass
    
    def get_time_to_live(self):
        pass
    
    def set_time_to_live(self, ttl):
        pass
    
    def get_protocol(self):
        pass
    
    def set_protocol(self, protocol):
        pass
    
    def get_header_checksum(self):
        pass
    
    def set_header_checksum(self, checksum):
        pass
    
    def get_source_address(self):
        pass
    
    def set_source_address(self, address):
        pass
    
    def get_destination_address(self):
        pass
    
    def set_destination_address(self, address):
        pass