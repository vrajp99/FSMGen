set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets clk_IBUF]

set_property PACKAGE_PIN V16 [get_ports clk]
	set_property IOSTANDARD LVCMOS33 [get_ports clk]
set_property PACKAGE_PIN U16 [get_ports O]
	set_property IOSTANDARD LVCMOS33 [get_ports O]
set_property PACKAGE_PIN T17 [get_ports reset]
	set_property IOSTANDARD LVCMOS33 [get_ports reset]
set_property PACKAGE_PIN V17 [get_ports w]
	set_property IOSTANDARD LVCMOS33 [get_ports w]
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]
set_property CONFIG_MODE SPIx4 [current_design]
    