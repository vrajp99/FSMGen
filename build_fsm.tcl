set outputDir ./VivadoBuildOutput
file mkdir $outputDir
set_part xc7a35tcpg236-1
read_verilog FSMmodule.v
#synthesis
synth_design -top FSMmodule
write_checkpoint -force $outputDir/post_synth
#placement and logic optimization
read_xdc constraints.xdc
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
write_bitstream $outputDir/design.bit
#load_features labtools
#connect_hw_server
#open_hw_target
#set current_target current_hw_target
#create_hw_bitstream -hw_device $current_target $outputDir/design.bit