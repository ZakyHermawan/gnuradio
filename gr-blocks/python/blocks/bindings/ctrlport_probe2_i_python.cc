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
/* BINDTOOL_HEADER_FILE(ctrlport_probe2_i.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(ce4e413b7a813ec65fd2887c50f27ea0)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/blocks/ctrlport_probe2_i.h>
// pydoc.h is automatically generated in the build directory
#include <ctrlport_probe2_i_pydoc.h>

void bind_ctrlport_probe2_i(py::module& m)
{

    using ctrlport_probe2_i = ::gr::blocks::ctrlport_probe2_i;


    py::class_<ctrlport_probe2_i,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<ctrlport_probe2_i>>(
        m, "ctrlport_probe2_i", D(ctrlport_probe2_i))

        .def(py::init(&ctrlport_probe2_i::make),
             py::arg("id"),
             py::arg("desc"),
             py::arg("len"),
             py::arg("disp_mask"),
             D(ctrlport_probe2_i, make))


        .def("get", &ctrlport_probe2_i::get, D(ctrlport_probe2_i, get))


        .def("set_length",
             &ctrlport_probe2_i::set_length,
             py::arg("len"),
             D(ctrlport_probe2_i, set_length))

        ;
}
