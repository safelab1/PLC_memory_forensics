CONF_FIELDS = [
    ['time_zone_addr' , '00023c10' ], # 1st dword is size, then ascii follows
    ['ip_address_locality' ,'00080000'], # fetch via string and search in region
    ['proj_name' , '00024000'] , # 1st byte is size, then ascii for current project in plc
    ['device_catalog' , '000241c4'], # 1st byte is size, then ascii
    ['revision' , '000241f0'],  # fetch till ascii found; confidence LOW
    ['xml_file_addr' , '0004b1c0'] ,  # file would terminate when stream of FFFFFF starts; confidence LOW
    ['xml_file_size_location' , '0004b1b0'], # the size of xml file is mentioned here L.Endian dword; confidence LOW
   [ 'SD_card_files' ,'000244D0','100'], # Fetch 0x100 bytes; run string to find filenames by searching(file1)".p5k"  (2) "Executive.bin"
   [ 'load_image' , '00024438'], # Extract string till printable
    ['load_mode'  , ' 00024460'], # Extract string till printable
    ['time_since_restart' , '0027A9D2'], #6 bytes in little endian format (provides ms)
    ['desktop_name' , '0004C044'], # 1st word (16 bytes LEndian) is size of words; next UTF-16 format letters
    ]
