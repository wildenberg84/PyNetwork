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
        """
        Return the version.
        
        Returns
        -------
            int 
            
        """
        
        return self.header[0] >> 4
    
    def set_version(self, version):
        """
        Set the version.
        
        Parameters
        ----------
            version : int
                Protocol version (0 - 15, inclusive)
        
        """
        
        self.header[0] = (version << 4) + self.get_ihl()
    
    def get_ihl(self):
        """
        Return the Internet Header Length.
        
        Returns
        -------
            int
        
        """
        
        return self.header[0] & 0b00001111
    
    def set_ihl(self, ihl):
        """
        Set the Internet Header Length.
        
        Parameters
        ----------
            ihl : int
                Internet Header Length (0 - 15, inclusive)
        """
        
        self.header[0] = (self.header[0] & 0b11110000) + ihl
    
    def get_dscp(self):
        """
        Return the Differentiated Services Code Point (Type of Service).
        
        Returns
        -------
            int
        
        """
        
        return (self.header[1] & 0b11111100) >> 2
    
    def set_dscp(self, dscp):
        """
        Set the Differentiated Services Code Point (Type of Service).
        
        Parameters
        ----------
            dscp : int
                Differentiated Services Code Point (0 - 63, inclusive)
        
        """
        
        self.header[1] = (dscp << 2) + self.get_ecn()
    
    def get_ecn(self):
        # TODO: Update to RFC 2481
        """
        Return the Explicit Congestion Notification.
        
        Returns
        -------
            int
                00 - Not-ECT
                01 - ECT(1)
                10 - ECT(0)
                11 - CE
            
        """
        
        return self.header[1] & 0b00000011
    
    def set_ecn(self, ecn):
        # TODO: Update to RFC 2481
        """
        Set the Explicit Congestion Notification
        
        Parameters
        ----------
            ecn : int
                Explicit Congestion Notification (0 - 3, inclusive)
                
                00 - Not-ECT
                01 - ECT(1)
                10 - ECT(0)
                11 - CE
                
        """
        
        self.header[1] = (self.header[1] & 0b11111100) + ecn
    
    def get_ecn_capable_transport(self):
        # TODO: Update to RFC 2481
        """
        Return the ECN Capable Transport flag.
        
        Returns
        -------
            bool
                True if ECN Capable, False otherwise
        
        """
        
        # either ECT(0) or ECT(1) -- treated equal by routers
        return (self.header[1] & 0b00000010) >> 1 or self.header[1] & 0b00000001
    
    def set_ecn_capable_transport(self, ecn_capable=True):
        # TODO: Update to RFC 2481
        """
        Set the ECN Capable Transport flag.
        
        Parameters
        ----------
            ecn_capable : bool, optional
                True if transport is ECN capable
                
        """
        
        if ecn_capable:
            # first bit should be set by sender, second by router
            self.header[1] = (self.header[1] & 0b11111100) + 2
        else:
            self.header[1] = (self.header[1] & 0b11111100)
    
    def get_ecn_congestion_experienced(self):
        """
        Return ECN congestion excperienced.
        
        Returns
        -------
            bool
                True if congestion is experienced, False otherwise
            
        """
        
        # both bits need to be set to 1 to indicate congestion
        return self.header[1] & 0b00000011
    
    def set_ecn_congestion_experienced(self, congestion_experienced=True):
        """
        Set ECN congestion excperienced.
        
        Parameters
        ----------
            congestion_experienced : bool, optional
                True if congestion is experienced (default is True)
                
        """
        
        self.header[1] = (self.header[1] & 0b11111100) + congestion_experienced

    def get_total_length(self):
        """
        Return the Total Length of the packet in bytes.
        
        Returns
        -------
            int
        
        """
        
        return int.from_bytes(self.header[2:4], 'big', signed = False)
    
    def set_total_length(self, length):
        """
        Set the Total Length of the packet in bytes.
        
        Parameters
        ----------
            length : int
                length of the packet in bytes (20 - 65535, inclusive)
        
        """
        
        self.header[2:4] = length.to_bytes(2, 'big')
    
    def get_identification(self):
        """
        Return the Identification.
        
        Returns
        -------
            int
            
        """
        
        return int.from_bytes(self.header[4:6], 'big', signed = False)
    
    def set_identification(self, identification):
        """
        Set the Identification.
        
        Parameters
        ----------
            identification : int
                Identification of the packet (0 - 65535, inclusive)
        
        """
        
        self.header[4:6] = identification.to_bytes(2, 'big')
    
    def get_flags(self):
        """
        Return all flags.
        
        Returns
        -------
            int
            
        """
        
        return (self.header[6] & 0b11100000) >> 5
    
    def set_flags(self, flags):
        """
        Set all flags.
        
        Parameters
        ----------
            flags : int
                Fragment(ation) flags (0 - 3)
                
                bit 0: Reserved; must be zero.
                bit 1: Don't Fragment (DF)
                bit 2: More Fragments (MF)
        
        """
        
        # first bit should not be set to 1
        self.header[6] = (flags << 5) + self.get_fragment_offset()
    
    def get_flag_df(self):
        """
        Return the Don't Fragment flag.
        
        Returns
        -------
            bool
                True if Don't Fragment is set, False otherwise
                
        """
        
        return (self.header[6] & 0b01000000) >> 6
    
    def set_flag_df(self, is_set=True):
        """
        Set the Don't Fragment flag.
        
        Parameters
        ----------
            is_set : bool
                True if Don't Fragment should be set, False otherwise
        
        """
        
        if is_set:
            self.header[6] = (self.header[6] & 0b10111111) + (1 << 6)
        else:
            self.header[6] = (self.header[6] & 0b10111111)
    
    def get_flag_mf(self):
        """
        Return the More Fragments flag.
        
        Returns
        -------
            bool
                True if More Fragments is set, False otherwise
        
        """
        
        return (self.header[6] & 0b00100000) >> 5
    
    def set_flag_mf(self, is_set):
        """
        Set the More Fragments flag.
        
        Parameters
        ----------
            is_set : bool
                True if More Fragments should be set, False otherwise
        
        """
        
        if is_set:
            self.header[6] = (self.header[6] & 0b11011111) + (1 << 5)
        else:
            self.header[6] = (self.header[6] & 0b11011111)
    
    def get_fragment_offset(self):
        """
        Return the Fragment Offset.
        
        Returns
        -------
            int
        
        """
        
        return int.from_bytes(self.header[6:8], 'big', signed = False) - (self.get_flags() << 13)
    
    def set_fragment_offset(self, offset):
        """
        Set the Fragment Offset.
        
        Parameters
        ----------
            offset : int
                indicates the offset of the fragment in eight-byte blocks (0 - 8191, inclusive)
                NOTE: 8191 * 8 + 20 = 65548 bytes, which would exceed the maximum IP packet length of 65535 bytes
                
        """
        
        self.header[6:8] = ((self.get_flags() << 13) + offset).to_bytes(2, 'big')
    
    def get_time_to_live(self):
        """
        Return the Time To Live.
        
        Returns
        -------
            int
        
        """
        
        return self.header[8]
    
    def set_time_to_live(self, ttl):
        """
        Set the Time To Live.
        
        Parameters
        ----------
            ttl : int
                indicates the Time To Live (0 - 255, inclusive)
                
        """
        
        self.header[8] = ttl
    
    def get_protocol(self):
        """
        Return the Protocol.
        
        Returns
        -------
            int
            
        """
        
        return self.header[9]
    
    def set_protocol(self, protocol):
        """
        Set the Protocol.
        
        Parameters
        ----------
            protocol : int
                protocol identifier as directed by RFC 790 (0 - 255, inclusive)
        
        """
        
        self.header[9] = protocol
    
    def get_header_checksum(self):
        """
        Return the Header Checksum.
        
        Parameters
        ----------
            int
            
        """
        
        return int.from_bytes(self.header[10:12], 'big', signed = False)
    
    def set_header_checksum(self, checksum):
        """
        Set the Header Checksum.
        
        Parameters
        ----------
            checksum : int
                header checksum used for error checking (0 - 65535, inclusive)
        """
        
        self.header[10:12] = checksum.to_bytes(2, 'big')
    
    def get_source_address(self):
        """
        Return the Source Address.
        
        Returns
        -------
            tuple(int, int, int, int)
            
        """
        
        return (self.header[12], self.header[13], self.header[14], self.header[15]) 
    
    def set_source_address(self, address):
        """
        Set the Source Address.
        
        Parameters
        ----------
            address : tuple(int, int, int, int)
                sender of the packet (0 - 255, inclusive, for each value)
        
        """
        
        self.header[12] = address[0]
        self.header[13] = address[1]
        self.header[14] = address[2]
        self.header[15] = address[3]
    
    def get_destination_address(self):
        """
        Return the Destination Address.
        
        Returns
        -------
            tuple(int, int, int, int)
            
        """
        
        return (self.header[16], self.header[17], self.header[18], self.header[19]) 
    
    def set_destination_address(self, address):
        """
        Set the Destination Address.
        
        Parameters
        ----------
            address : tuple(int, int, int, int)
                receiver of the packet (0 - 255, inclusive, for each value)
        
        """
        
        self.header[16] = address[0]
        self.header[17] = address[1]
        self.header[18] = address[2]
        self.header[19] = address[3]
    ##### End of GETTERS / SETTERS for IP header fields #####