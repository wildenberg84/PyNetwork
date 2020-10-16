# requires empty, memoryview or IP packet binary
class IPv4_Packet:
    
    def __init__(self, packet=None):
        self.header = None
        self.options = None
        self.payload = None
        
        # if no packet was given, make a new one
        if (packet == None):
            # initialize 20 bytes of zeroes
            self.header = IPv4_Header()
        # else parse the packet data
        else:
            # if we have a memoryview
            if (type(packet) == memoryview):
                self.header = IPv4_Header(packet[:20])
            # else create a memoryview first
            else:
                pass    

    
    def get_options(self):
        pass
    
    def set_options(self):
        pass
    
    def get_payload(self):
        pass
    
    def set_payload(self, payload):
        pass
    
    
    
    
class IPv4_Header:   
    # requires a memoryview
    def __init__(self, header=None):
        self.header = header 
    
    
    def get_version(self):
        return self.header[0] >> 4
    
    def set_version(self, version):
        pass
    
    def get_ihl(self):
        pass
    
    def set_ihl(self, ihl):
        pass
    
    def get_dscp(self):
        pass
    
    def set_dscp(self, dscp):
        pass
    
    def get_ecn(self):
        pass
    
    def set_ecn(self, ecn):
        pass
    
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