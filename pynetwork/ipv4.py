"""
This is the IPv4 module.

This module does IPv4 stuff.

TODO: rewrite module description
"""

from pynetwork.custom_exceptions import NonWritableMemoryviewError

# TODO: write class description
# requires empty, memoryview or IP packet binary
class IPv4Packet:
    
    def __init__(self, packet=None):
        self.header = None # IPv4Header object
        self.options = None # IPv4Options object
        self.payload = None # memoryview of payload data
        
        # if no packet was given, make a new one
        if packet == None:
            self.header = IPv4Header()
        # else parse the packet data
        else:
            self.header = IPv4Header(packet[:20])    

        assert self.header != None # make sure we actually have something
        
        
    def get_options(self):
        pass
    
    def set_options(self):
        pass
    
    def get_payload(self):
        pass
    
    def set_payload(self, payload):
        pass
    
    
    
# TODO: write class description    
class IPv4Header:   
    # requires a writeable memoryview
    def __init__(self, header=None):                
        # reserve bytes if we don't have a header
        if header == None:
            self.header = memoryview(bytearray(20))
        elif type(header) == memoryview:
            # make sure it's read / write
            if header.readonly:
                raise NonWritableMemoryviewError(self.__class__.__name__ + " requires a writable memoryview")
            else:
                self.header = header
        # wrong argument type
        else:
            raise TypeError(self.__class__.__name__ + ' constructor requires a writable memoryview')
    
    
    ##### Start of GETTERS / SETTERS for IP header fields #####
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
        self.header[1] = (self.header[1] & 0b11111100) + ecn
    
    def get_ecn_capable_transport(self):
        return (self.header[1] & 0b00000010) >> 1
    
    def set_ecn_capable_transport(self, ecn_capable):
        self.header[1] = (self.header[1] & 0b11111101) + (ecn_capable << 1)
    
    def get_congestion_experienced(self):
        return self.header[1] & 0b00000001
    
    def set_congestion_experienced(self, congestion_experienced):
        self.header[1] = (self.header[1] & 0b11111110) + congestion_experienced

    def get_total_length(self):
        return int.from_bytes(self.header[2:4], 'big', signed = False)
    
    def set_total_length(self, length):
        self.header[2:4] = length.to_bytes(2, 'big')
    
    def get_identification(self):
        return int.from_bytes(self.header[4:6], 'big', signed = False)
    
    def set_identification(self, identification):
        self.header[4:6] = identification.to_bytes(2, 'big')
    
    def get_flags(self):
        return (self.header[6] & 0b11100000) >> 5
    
    def set_flags(self, flags):
        self.header[6] = (flags << 5) + self.get_fragment_offset()
    
    def get_flag_df(self):
        return (self.header[6] & 0b01000000) >> 6 
    
    def set_flag_df(self, flag):
        self.header[6] = (self.header[6] & 0b10111111) + (flag << 6)
    
    def get_flag_mf(self):
        return (self.header[6] & 0b00100000) >> 5
    
    def set_flag_mf(self, flag):
        self.header[6] = (self.header[6] & 0b11011111) + (flag << 5)
    
    def get_fragment_offset(self):
        return int.from_bytes(self.header[6:8], 'big', signed = False) - (self.get_flags() << 13)
    
    def set_fragment_offset(self, offset):
        self.header[6:8] = ((self.get_flags() << 13) + offset).to_bytes(2, 'big')
    
    def get_time_to_live(self):
        return self.header[8]
    
    def set_time_to_live(self, ttl):
        self.header[8] = ttl
    
    def get_protocol(self):
        return self.header[9]
    
    def set_protocol(self, protocol):
        self.header[9] = protocol
    
    def get_header_checksum(self):
        return int.from_bytes(self.header[10:12], 'big', signed = False)
    
    def set_header_checksum(self, checksum):
        self.header[10:12] = checksum.to_bytes(2, 'big')
    
    def get_source_address(self):
        return int.from_bytes(self.header[12:16], 'big', signed = False)
    
    def set_source_address(self, address):
        self.header[12:16] = address.to_bytes(4, 'big')
    
    def get_destination_address(self):
        return int.from_bytes(self.header[16:20], 'big', signed = False)
    
    def set_destination_address(self, address):
        self.header[16:20] = address.to_bytes(4, 'big')
    ##### End of GETTERS / SETTERS for IP header fields #####