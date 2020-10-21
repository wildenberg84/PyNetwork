"""
IPv4 module

Containing all classes that are specific to IPv4.

Classes
-------
    IPv4Packet
    IPv4Header

"""

from pynetwork.custom_exceptions import *

# requires empty, memoryview or IP packet binary
class IPv4Packet:
    """
    A class to represent an IPv4 packet.
    
    Attributes
    ----------
        header: IPv4Header
            header object representing the header of an IPv4 packet
        options: IPv4Options
            [optional] options object representing the options part of an IPv4 packet
        payload: memoryview
            writable byte(s) reperesentation of the payload of the IPv4 packet
        
    """
    
    def __init__(self, packet=None):
        """
        Initializer of the IPv4Packet class.
    
        Parameters
        ----------
            packet : memoryview
                writable bytes representation of an IP packet (in big endian)
        
        """
        
        self.header = None # IPv4Header object
        self.options = None # IPv4Options object
        self.payload = None # memoryview of payload data
        
        # if no packet was given, make a new one
        if packet == None:
            self.header = IPv4Header()
        # else parse the packet data
        else:
            if type(packet) == memoryview:
                # make sure it's read / write
                if packet.readonly:
                    raise NonWritableMemoryviewError(self.__class__.__name__ + " requires a writable memoryview")
                else:
                    self.header = IPv4Header(packet[:20])            
            # wrong argument type
            else:
                raise TypeError(self.__class__.__name__ + ' constructor requires a writable memoryview')  

        assert self.header != None # make sure we actually have something
        
        
    def get_options(self):
        # TODO: implement function
        pass
    
    def set_options(self):
        # TODO: implement function
        pass
    
    def get_payload(self):
        # TODO: implement function
        pass
    
    def set_payload(self, payload):
        # TODO: implement function
        pass
    
    
class IPv4Header:   
    """
    A class to represent an IPv4 header.
    
    Attributes
    ----------
        header: memoryview
            Writable byte(s) reperesentation of the header of an IPv4 packet.
        
    """
    
    # requires a writeable memoryview
    def __init__(self, header=None):  
        """
        Initializer of the IPv4Header class.
    
        Parameters
        ----------
            header : memoryview
                Writable binary representation of an IP packet (in big endian).
                Must be at least 20 bytes in length (minimum of an IPv4 header).
        
        """
                      
        # reserve bytes if we don't have a header
        if header == None:
            self.header = memoryview(bytearray(20))
        elif type(header) == memoryview:
            # make sure it's read / write
            if header.readonly:
                raise NonWritableMemoryviewError(self.__class__.__name__ + " requires a writable memoryview")
            else:
                # header must be at least 20 bytes
                if header.nbytes >= 20:
                    self.header = header
                else:
                    raise IllegalArgumentError("Header size must be 20 bytes or more.")
        # wrong argument type
        else:
            raise TypeError(self.__class__.__name__ + ' constructor requires a writable memoryview')
    
    
    ##### Start of GETTERS / SETTERS for IP header fields #####
    def get_version(self):
        """Return the version."""
        
        return self.header[0] >> 4
    
    def set_version(self, version):
        """Set the version."""
        
        self.header[0] = (version << 4) + self.get_ihl()
    
    def get_ihl(self):
        """Return the Internet Header Length."""
        
        return self.header[0] & 0b00001111
    
    def set_ihl(self, ihl):
        """Set the Internet Header Length."""
        
        self.header[0] = (self.header[0] & 0b11110000) + ihl
    
    def get_dscp(self):
        """Return the Differentiated Services Code Point (Type of Service)."""
        
        return (self.header[1] & 0b11111100) >> 2
    
    def set_dscp(self, dscp):
        """Set the Differentiated Services Code Point (Type of Service)."""
        
        self.header[1] = (dscp << 2) + self.get_ecn()
    
    def get_ecn(self):
        """Return the Explicit Congestion Notification"""
        
        return self.header[1] & 0b00000011
    
    def set_ecn(self, ecn):
        """Set the Explicit Congestion Notification"""
        
        self.header[1] = (self.header[1] & 0b11111100) + ecn
    
    def get_ecn_capable_transport(self):
        """Return the ECN Capable Transport flag."""
        
        # either ECT(0) or ECT(1) -- treated equal by routers
        if (self.header[1] & 0b00000010) >> 1 == 1 or self.header[1] & 0b00000001 == 1:
            return 1
        else:
            return 0
    
    def set_ecn_capable_transport(self, ecn_capable):
        """Set the ECN Capable Transport flag."""
        
        # set one of the 2 bits, but not both
        self.header[1] = (self.header[1] & 0b11111100) + ecn_capable
    
    def get_ecn_congestion_experienced(self):
        """Return ECN congestion excperienced."""
        
        # both bits need to be set to 1 to indicate congestion
        if self.header[1] & 0b00000011 == 3:
            return 1
        else:
            return 0
    
    def set_ecn_congestion_experienced(self, congestion_experienced):
        """Set ECN congestion excperienced."""
        
        self.header[1] = (self.header[1] & 0b11111100) + congestion_experienced

    def get_total_length(self):
        """Return the Total Length of the packet in bytes."""
        
        return int.from_bytes(self.header[2:4], 'big', signed = False)
    
    def set_total_length(self, length):
        """Set the Total Length of the packet in bytes."""
        
        self.header[2:4] = length.to_bytes(2, 'big')
    
    def get_identification(self):
        """Return the Identification."""
        
        return int.from_bytes(self.header[4:6], 'big', signed = False)
    
    def set_identification(self, identification):
        """Set the Identification."""
        
        self.header[4:6] = identification.to_bytes(2, 'big')
    
    def get_flags(self):
        """Return all flags."""
        
        return (self.header[6] & 0b11100000) >> 5
    
    def set_flags(self, flags):
        """Set all flags."""
        
        # first bit should not be set to 1
        self.header[6] = (flags << 5) + self.get_fragment_offset()
    
    def get_flag_df(self):
        """Return the Don't Fragment flag."""
        
        return (self.header[6] & 0b01000000) >> 6 
    
    def set_flag_df(self, flag):
        """Set the Don't Fragment flag."""
        
        self.header[6] = (self.header[6] & 0b10111111) + (flag << 6)
    
    def get_flag_mf(self):
        """Return the More Fragments flag."""
        
        return (self.header[6] & 0b00100000) >> 5
    
    def set_flag_mf(self, flag):
        """Set the More Fragments flag."""
        
        self.header[6] = (self.header[6] & 0b11011111) + (flag << 5)
    
    def get_fragment_offset(self):
        """Return the Fragment Offset."""
        
        return int.from_bytes(self.header[6:8], 'big', signed = False) - (self.get_flags() << 13)
    
    def set_fragment_offset(self, offset):
        """Set the Fragment Offset."""
        
        self.header[6:8] = ((self.get_flags() << 13) + offset).to_bytes(2, 'big')
    
    def get_time_to_live(self):
        """Return the Time To Live."""
        
        return self.header[8]
    
    def set_time_to_live(self, ttl):
        """Set the Time To Live."""
        
        self.header[8] = ttl
    
    def get_protocol(self):
        """Return the Protocol."""
        
        return self.header[9]
    
    def set_protocol(self, protocol):
        """Set the Protocol."""
        
        self.header[9] = protocol
    
    def get_header_checksum(self):
        """Return the Header Checksum."""
        
        return int.from_bytes(self.header[10:12], 'big', signed = False)
    
    def set_header_checksum(self, checksum):
        """Set the Header Checksum."""
        
        self.header[10:12] = checksum.to_bytes(2, 'big')
    
    def get_source_address(self):
        """Return the Source Address."""
        
        return int.from_bytes(self.header[12:16], 'big', signed = False)
    
    def set_source_address(self, address):
        """Set the Source Address."""
        
        self.header[12:16] = address.to_bytes(4, 'big')
    
    def get_destination_address(self):
        """Return the Destination Address."""
        
        return int.from_bytes(self.header[16:20], 'big', signed = False)
    
    def set_destination_address(self, address):
        """Set the Destination Address."""
        
        self.header[16:20] = address.to_bytes(4, 'big')
    ##### End of GETTERS / SETTERS for IP header fields #####