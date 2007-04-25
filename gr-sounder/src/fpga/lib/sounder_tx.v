// -*- verilog -*-
//
//  USRP - Universal Software Radio Peripheral
//
//  Copyright (C) 2007 Corgan Enterprises LLC
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc., 51 Franklin Street, Boston, MA  02110-1301  USA
//

`include "../../../../usrp/firmware/include/fpga_regs_common.v"
`include "../../../../usrp/firmware/include/fpga_regs_standard.v"

`define MAX_VALUE 16'h7FFF // 2s complement
`define MIN_VALUE 16'h8000

module sounder_tx(clk_i,rst_i,ena_i,strobe_i,mask_i,tx_i_o,tx_q_o);
   input         clk_i;
   input         rst_i;
   input         ena_i;
   input         strobe_i;
   input  [15:0] mask_i;
   output [15:0] tx_i_o;
   output [15:0] tx_q_o;

   wire          pn;

   lfsr pn_code
     ( .clk_i(clk_i),.rst_i(rst_i),.ena_i(ena_i),.strobe_i(strobe_i),.mask_i(mask_i),.pn_o(pn) );

   assign tx_i_o = pn ? `MAX_VALUE : `MIN_VALUE; // Bipolar
   assign tx_q_o = 16'b0;

endmodule // sounder_tx
