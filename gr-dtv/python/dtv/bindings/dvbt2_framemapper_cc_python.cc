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
/* BINDTOOL_GEN_AUTOMATIC(1)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(dvbt2_framemapper_cc.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(9ba36658362b995ce077d00e03fc9c7f)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/dtv/dvbt2_framemapper_cc.h>
// pydoc.h is automatically generated in the build directory
#include <dvbt2_framemapper_cc_pydoc.h>

void bind_dvbt2_framemapper_cc(py::module& m)
{

    using dvbt2_framemapper_cc = ::gr::dtv::dvbt2_framemapper_cc;


    py::class_<dvbt2_framemapper_cc,
               gr::block,
               gr::basic_block,
               std::shared_ptr<dvbt2_framemapper_cc>>(
        m, "dvbt2_framemapper_cc", D(dvbt2_framemapper_cc))

        .def(py::init(&dvbt2_framemapper_cc::make),
             py::arg("framesize"),
             py::arg("rate"),
             py::arg("constellation"),
             py::arg("rotation"),
             py::arg("fecblocks"),
             py::arg("tiblocks"),
             py::arg("carriermode"),
             py::arg("fftsize"),
             py::arg("guardinterval"),
             py::arg("l1constellation"),
             py::arg("pilotpattern"),
             py::arg("t2frames"),
             py::arg("numdatasyms"),
             py::arg("paprmode"),
             py::arg("version"),
             py::arg("preamble"),
             py::arg("inputmode"),
             py::arg("reservedbiasbits"),
             py::arg("l1scrambled"),
             py::arg("inband"),
             D(dvbt2_framemapper_cc, make))


        ;
}
