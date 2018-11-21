set outputDir ./VivadoBuildOutput
file mkdir $outputDir
set_part xc7a35tcpg236-1
read_verilog ./files/psk_sarma.v
#synthesis
synth_design -top psk_sarma
write_checkpoint -force $outputDir/post_synth
#placement and logic optimization
read_xdc ./files/constraints_psk_sarma.xdc
opt_design
power_opt_design
place_design
phys_opt_design
write_checkpoint -force $outputDir/post_place
#run router,write checkpoint design, run DRCs
route_design
write_checkpoint -force $outputDir/post_route
write_verilog -force $outputDir/fsm_impl_netlist.v
write_xdc -no_fixed_only -force $outputDir/fsm_impl.xdc
write_bitstream -force $outputDir/design.bit
load_features labtools
open_hw
connect_hw_server
open_hw_target
set_property PROGRAM.FILE $outputDir/design.bit [lindex [get_hw_devices] 0]
current_hw_device [lindex [get_hw_devices] 0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]
set_property PROBES.FILE {} [lindex [get_hw_devices] 0]
set_property FULL_PROBES.FILE {} [lindex [get_hw_devices] 0]
set_property PROGRAM.FILE $outputDir/design.bit [lindex [get_hw_devices] 0]
program_hw_devices [lindex [get_hw_devices] 0]