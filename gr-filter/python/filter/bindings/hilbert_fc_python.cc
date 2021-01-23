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
/* BINDTOOL_HEADER_FILE(hilbert_fc.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(041e266d5e3108f725118a1f581b43f8)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/filter/hilbert_fc.h>
// pydoc.h is automatically generated in the build directory
#include <hilbert_fc_pydoc.h>

void bind_hilbert_fc(py::module& m)
{
    using hilbert_fc = gr::filter::hilbert_fc;


    py::class_<hilbert_fc,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<hilbert_fc>>(m, "hilbert_fc", D(hilbert_fc))

        .def(py::init(&hilbert_fc::make),
             py::arg("ntaps"),
             py::arg("window") = ::gr::fft::window::win_type::WIN_HAMMING,
             py::arg("param") = 6.7599999999999998,
             D(hilbert_fc, make));
}
