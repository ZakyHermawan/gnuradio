
`define DSP_CORE_RX_BASE 160

module rx_control
  #(parameter FIFOSIZE = 10)
    (input clk, input rst,
     input set_stb, input [7:0] set_addr, input [31:0] set_data,
     
     input [31:0] master_time,
     output overrun,
     
     // To Buffer interface
     output [31:0] wr_dat_o,
     output wr_write_o,
     output wr_done_o,
     output wr_error_o,

     input wr_ready_i,
     input wr_full_i,
     
     // From DSP Core
     input [31:0] sample,
     output run,
     input strobe,

     // FIFO Levels
     output [15:0] fifo_occupied,
     output fifo_full,
     output fifo_empty,
     
     // Debug
     output [31:0] debug_rx
     );

   wire [31:0] 	   new_time, new_command;
   wire 	   sc_pre1, clear_overrun;
   wire [31:0] 	   rcvtime_pre;
   reg [31:0] 	   rcvtime;
   wire [8:0] 	   lines_per_frame;
   wire [20:0] 	   numlines;
   wire 	   send_imm_pre, chain_pre;
   reg 		   send_imm, chain;
   wire 	   full_ctrl, read_ctrl, empty_ctrl, write_ctrl;

   setting_reg #(.my_addr(`DSP_CORE_RX_BASE+3)) sr_3
     (.clk(clk),.rst(rst),.strobe(set_stb),.addr(set_addr),
      .in(set_data),.out(new_time),.changed(sc_pre1));
   
   setting_reg #(.my_addr(`DSP_CORE_RX_BASE+4)) sr_4
     (.clk(clk),.rst(rst),.strobe(set_stb),.addr(set_addr),
      .in(set_data),.out(new_command),.changed());

   setting_reg #(.my_addr(`DSP_CORE_RX_BASE+5)) sr_5
     (.clk(clk),.rst(rst),.strobe(set_stb),.addr(set_addr),
      .in(set_data),.out(),.changed(clear_overrun));

   reg 	       sc_pre2;
   always @(posedge clk)
     sc_pre2 <= sc_pre1;
   assign      write_ctrl = sc_pre1 & ~sc_pre2;
   
   shortfifo #(.WIDTH(64)) commandfifo
     (.clk(clk),.rst(rst),.clear(clear_overrun),
      .datain({new_command,new_time}), .write(write_ctrl), .full(full_ctrl),
      .dataout({send_imm_pre,chain_pre,numlines,lines_per_frame,rcvtime_pre}), 
      .read(read_ctrl), .empty(empty_ctrl) );

   // Buffer interface to internal FIFO
   wire    write, full, read, empty;
   wire    sop_o, eop_o;

   reg 	   xfer_state;
   localparam XFER_IDLE = 1'b0;
   localparam XFER_GO = 1'b1;

   always @(posedge clk)
     if(rst)
       xfer_state <= XFER_IDLE;
     else
       if(clear_overrun)
	 xfer_state <= XFER_IDLE;
       else
	 case(xfer_state)
	   XFER_IDLE :
	     if(wr_ready_i)
	       xfer_state <= XFER_GO;
	   XFER_GO :
	     if((eop_o | wr_full_i) & wr_write_o)
	       xfer_state <= XFER_IDLE;
	   default :
	     xfer_state <= XFER_IDLE;
	 endcase // case(xfer_state)
   
   assign     wr_write_o = (xfer_state == XFER_GO) & ~empty;
   assign     wr_done_o = (eop_o & wr_write_o);
   assign     wr_error_o = 0;   // FIXME add check here for eop if we have wr_full_i once we have IBS

   assign     read = wr_write_o | (~empty & ~sop_o);   // FIXME  what if there is junk between packets?

   wire [33:0] fifo_line;
   
   // Internal FIFO, size 9 is 2K, size 10 is 4K
   cascadefifo2 #(.WIDTH(34),.SIZE(FIFOSIZE)) rxfifo
     (.clk(clk),.rst(rst),.clear(clear_overrun),
      .datain(fifo_line), .write(write), .full(full),
      .dataout({sop_o,eop_o,wr_dat_o}), .read(read), .empty(empty),
      .space(),.occupied(fifo_occupied) );
   assign      fifo_full = full;
   assign      fifo_empty = empty;

   // Internal FIFO to DSP interface
   reg [22:0] lines_left;
   reg [8:0]  lines_left_frame;
   localparam IBS_IDLE = 0;
   localparam IBS_WAITING = 1;
   localparam IBS_FIRSTLINE = 2;
   localparam IBS_RUNNING = 3;
   localparam IBS_OVERRUN = 4;
   
   reg [2:0] ibs_state;
  
   wire [32:0] delta_time = {1'b0,rcvtime}-{1'b0,master_time};
   wire        too_late = (delta_time[32:31] == 2'b11) & ~send_imm;
   wire        go_now = send_imm | ( master_time == rcvtime );
 
   always @(posedge clk)
     if(rst)
       begin
	  ibs_state <= IBS_IDLE;
	  lines_left <= 0;
	  lines_left_frame <= 0;
	  rcvtime <= 0;
	  send_imm <= 0;
	  chain <= 0;
       end
     else
       if(clear_overrun)
	 begin
	  ibs_state <= IBS_IDLE;
	  lines_left <= 0;
	  lines_left_frame <= 0;
	  rcvtime <= 0;
	  send_imm <= 0;
	  chain <= 0;
	 end
       else 
	 case(ibs_state)
	   IBS_IDLE :
	     if(~empty_ctrl)
	       begin
		  lines_left <= numlines;
		  lines_left_frame <= lines_per_frame;
		  rcvtime <= rcvtime_pre;
		  ibs_state <= IBS_WAITING;
		  send_imm <= send_imm_pre;
		  chain <= chain_pre;
	       end
	   IBS_WAITING :
	     if(go_now)
	       ibs_state <= IBS_FIRSTLINE;
	     else if(too_late)
	       ibs_state <= IBS_OVERRUN;
	   IBS_FIRSTLINE :
	     if(full | strobe)
	       ibs_state <= IBS_OVERRUN;
	     else
	       ibs_state <= IBS_RUNNING;
	   IBS_RUNNING :
	     if(strobe)
	       if(full)
		 ibs_state <= IBS_OVERRUN;
	       else
		 begin
		    lines_left <= lines_left - 1;
		    if(lines_left == 1)
		      if(~chain)
			ibs_state <= IBS_IDLE;
		      else if(empty_ctrl)
			ibs_state <= IBS_OVERRUN;
		      else
			begin
			   lines_left <= numlines;
			   lines_left_frame <= lines_per_frame;
			   rcvtime <= rcvtime_pre;
			   ibs_state <= IBS_FIRSTLINE;
			   send_imm <= send_imm_pre;
			   chain <= chain_pre;
			end
		    else if(lines_left_frame == 1)
		      begin
			 lines_left_frame <= lines_per_frame;
			 ibs_state <= IBS_FIRSTLINE;
		      end
		    else
		      lines_left_frame <= lines_left_frame - 1;
		 end // else: !if(full)
	 endcase // case(ibs_state)
   
   assign fifo_line = (ibs_state == IBS_FIRSTLINE) ? {1'b1,1'b0,master_time} :
		      {1'b0,((lines_left==1)|(lines_left_frame==1)),sample};
   
   assign write = ((ibs_state == IBS_FIRSTLINE) | strobe) & ~full;  // & (ibs_state == IBS_RUNNING) should strobe only when running
   assign overrun = (ibs_state == IBS_OVERRUN);
   assign run = (ibs_state == IBS_RUNNING) | (ibs_state == IBS_FIRSTLINE);
   assign read_ctrl = ( (ibs_state == IBS_IDLE) | 
			((ibs_state == IBS_RUNNING) & strobe & ~full & (lines_left==1) & chain) )
	  & ~empty_ctrl;
   
   assign debug_rx = { 6'd0,send_imm,chain,
		       wr_write_o, wr_done_o, wr_ready_i, wr_full_i,xfer_state,eop_o, sop_o, run,
		       write,full,read,empty,write_ctrl,full_ctrl,read_ctrl,empty_ctrl,
		       sc_pre1, clear_overrun, go_now, too_late, overrun, ibs_state[2:0] };
endmodule // rx_control
