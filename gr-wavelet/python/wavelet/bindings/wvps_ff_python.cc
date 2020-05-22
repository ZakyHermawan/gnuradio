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
/* BINDTOOL_HEADER_FILE(wvps_ff.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(1f4a9460066d197782a59a0fa164ae03)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/wavelet/wvps_ff.h>
// pydoc.h is automatically generated in the build directory
#include <wvps_ff_pydoc.h>

void bind_wvps_ff(py::module& m)
{

    using wvps_ff = ::gr::wavelet::wvps_ff;


    py::class_<wvps_ff,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<wvps_ff>>(m, "wvps_ff", D(wvps_ff))

        .def(py::init(&wvps_ff::make), py::arg("ilen"), D(wvps_ff, make))


        ;
}
