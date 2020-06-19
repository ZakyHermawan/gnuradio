/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(ldpc_gen_mtrx_encoder.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(9098a1e7d9b9af930a68831223e6a648)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/fec/ldpc_gen_mtrx_encoder.h>
// pydoc.h is automatically generated in the build directory
#include <ldpc_gen_mtrx_encoder_pydoc.h>

void bind_ldpc_gen_mtrx_encoder(py::module& m)
{


    py::module m_code = m.def_submodule("code");

    using ldpc_gen_mtrx_encoder = ::gr::fec::code::ldpc_gen_mtrx_encoder;


    py::class_<ldpc_gen_mtrx_encoder,
               gr::fec::generic_encoder,
               std::shared_ptr<ldpc_gen_mtrx_encoder>>(
        m_code, "ldpc_gen_mtrx_encoder", D(code, ldpc_gen_mtrx_encoder))

        .def_static("make",
                    &ldpc_gen_mtrx_encoder::make,
                    py::arg("G_obj"),
                    D(code, ldpc_gen_mtrx_encoder, make))


        .def("set_frame_size",
             &ldpc_gen_mtrx_encoder::set_frame_size,
             py::arg("frame_size"),
             D(code, ldpc_gen_mtrx_encoder, set_frame_size))


        .def("rate", &ldpc_gen_mtrx_encoder::rate, D(code, ldpc_gen_mtrx_encoder, rate))

        ;
}
