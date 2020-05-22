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
/* BINDTOOL_HEADER_FILE(interpolating_resampler_type.h) */
/* BINDTOOL_HEADER_FILE_HASH(87d67f9b33b7ee74737145aca95e7a13)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/digital/interpolating_resampler_type.h>
// pydoc.h is automatically generated in the build directory
#include <interpolating_resampler_type_pydoc.h>

void bind_interpolating_resampler_type(py::module& m)
{

    py::enum_<gr::digital::ir_type>(m, "ir_type")
        .value("IR_NONE", gr::digital::IR_NONE)           // -1
        .value("IR_MMSE_8TAP", gr::digital::IR_MMSE_8TAP) // 0
        .value("IR_PFB_NO_MF", gr::digital::IR_PFB_NO_MF) // 1
        .value("IR_PFB_MF", gr::digital::IR_PFB_MF)       // 2
        .export_values();
}
