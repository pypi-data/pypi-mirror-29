/* "uniprop" module for Python.
 *
 * This module reports the Unicode properties of codepoints.
 *
 * Copyright 2016 Matthew Barnett
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "Python.h"
#include <stdlib.h>
#include "structmember.h" /* offsetof */

#include "unicode_tables.h"

#define UNIPROP_VERSION "1.3"

/* Returns the Alphabetic property for a codepoint. */
static PyObject* get_alphabetic(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_alphabetic((Py_UCS4)codepoint);
    name = value_names[UP_ALPHABETIC_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_alphabetic_doc,
    "alphabetic(property, chr) --> string.\n\
    Return the Alphabetic value of a character.");

/* Returns the Alphanumeric property for a codepoint. */
static PyObject* get_alphanumeric(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_alphanumeric((Py_UCS4)codepoint);
    name = value_names[UP_ALPHANUMERIC_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_alphanumeric_doc,
    "alphanumeric(property, chr) --> string.\n\
    Return the Alphanumeric value of a character.");

/* Returns the Any property for a codepoint. */
static PyObject* get_any(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_any((Py_UCS4)codepoint);
    name = value_names[UP_ANY_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_any_doc,
    "any(property, chr) --> string.\n\
    Return the Any value of a character.");

/* Returns the ASCII_Hex_Digit property for a codepoint. */
static PyObject* get_ascii_hex_digit(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_ascii_hex_digit((Py_UCS4)codepoint);
    name = value_names[UP_ASCII_HEX_DIGIT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_ascii_hex_digit_doc,
    "ascii_hex_digit(property, chr) --> string.\n\
    Return the ASCII_Hex_Digit value of a character.");

/* Returns the Bidi_Class property for a codepoint. */
static PyObject* get_bidi_class(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_bidi_class((Py_UCS4)codepoint);
    name = value_names[UP_BIDI_CLASS_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_bidi_class_doc,
    "bidi_class(property, chr) --> string.\n\
    Return the Bidi_Class value of a character.");

/* Returns the Bidi_Control property for a codepoint. */
static PyObject* get_bidi_control(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_bidi_control((Py_UCS4)codepoint);
    name = value_names[UP_BIDI_CONTROL_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_bidi_control_doc,
    "bidi_control(property, chr) --> string.\n\
    Return the Bidi_Control value of a character.");

/* Returns the Bidi_Mirrored property for a codepoint. */
static PyObject* get_bidi_mirrored(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_bidi_mirrored((Py_UCS4)codepoint);
    name = value_names[UP_BIDI_MIRRORED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_bidi_mirrored_doc,
    "bidi_mirrored(property, chr) --> string.\n\
    Return the Bidi_Mirrored value of a character.");

/* Returns the Blank property for a codepoint. */
static PyObject* get_blank(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_blank((Py_UCS4)codepoint);
    name = value_names[UP_BLANK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_blank_doc,
    "blank(property, chr) --> string.\n\
    Return the Blank value of a character.");

/* Returns the Block property for a codepoint. */
static PyObject* get_block(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_block((Py_UCS4)codepoint);
    name = value_names[UP_BLOCK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_block_doc,
    "block(property, chr) --> string.\n\
    Return the Block value of a character.");

/* Returns the Canonical_Combining_Class property for a codepoint. */
static PyObject* get_canonical_combining_class(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_canonical_combining_class((Py_UCS4)codepoint);
    name = value_names[UP_CANONICAL_COMBINING_CLASS_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_canonical_combining_class_doc,
    "canonical_combining_class(property, chr) --> string.\n\
    Return the Canonical_Combining_Class value of a character.");

/* Returns the Cased property for a codepoint. */
static PyObject* get_cased(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_cased((Py_UCS4)codepoint);
    name = value_names[UP_CASED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_cased_doc,
    "cased(property, chr) --> string.\n\
    Return the Cased value of a character.");

/* Returns the Case_Ignorable property for a codepoint. */
static PyObject* get_case_ignorable(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_case_ignorable((Py_UCS4)codepoint);
    name = value_names[UP_CASE_IGNORABLE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_case_ignorable_doc,
    "case_ignorable(property, chr) --> string.\n\
    Return the Case_Ignorable value of a character.");

/* Returns the Changes_When_Casefolded property for a codepoint. */
static PyObject* get_changes_when_casefolded(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_changes_when_casefolded((Py_UCS4)codepoint);
    name = value_names[UP_CHANGES_WHEN_CASEFOLDED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_changes_when_casefolded_doc,
    "changes_when_casefolded(property, chr) --> string.\n\
    Return the Changes_When_Casefolded value of a character.");

/* Returns the Changes_When_Casemapped property for a codepoint. */
static PyObject* get_changes_when_casemapped(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_changes_when_casemapped((Py_UCS4)codepoint);
    name = value_names[UP_CHANGES_WHEN_CASEMAPPED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_changes_when_casemapped_doc,
    "changes_when_casemapped(property, chr) --> string.\n\
    Return the Changes_When_Casemapped value of a character.");

/* Returns the Changes_When_Lowercased property for a codepoint. */
static PyObject* get_changes_when_lowercased(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_changes_when_lowercased((Py_UCS4)codepoint);
    name = value_names[UP_CHANGES_WHEN_LOWERCASED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_changes_when_lowercased_doc,
    "changes_when_lowercased(property, chr) --> string.\n\
    Return the Changes_When_Lowercased value of a character.");

/* Returns the Changes_When_Titlecased property for a codepoint. */
static PyObject* get_changes_when_titlecased(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_changes_when_titlecased((Py_UCS4)codepoint);
    name = value_names[UP_CHANGES_WHEN_TITLECASED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_changes_when_titlecased_doc,
    "changes_when_titlecased(property, chr) --> string.\n\
    Return the Changes_When_Titlecased value of a character.");

/* Returns the Changes_When_Uppercased property for a codepoint. */
static PyObject* get_changes_when_uppercased(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_changes_when_uppercased((Py_UCS4)codepoint);
    name = value_names[UP_CHANGES_WHEN_UPPERCASED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_changes_when_uppercased_doc,
    "changes_when_uppercased(property, chr) --> string.\n\
    Return the Changes_When_Uppercased value of a character.");

/* Returns the Cntrl property for a codepoint. */
static PyObject* get_cntrl(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_cntrl((Py_UCS4)codepoint);
    name = value_names[UP_CNTRL_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_cntrl_doc,
    "cntrl(property, chr) --> string.\n\
    Return the Cntrl value of a character.");

/* Returns the Dash property for a codepoint. */
static PyObject* get_dash(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_dash((Py_UCS4)codepoint);
    name = value_names[UP_DASH_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_dash_doc,
    "dash(property, chr) --> string.\n\
    Return the Dash value of a character.");

/* Returns the Decomposition_Type property for a codepoint. */
static PyObject* get_decomposition_type(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_decomposition_type((Py_UCS4)codepoint);
    name = value_names[UP_DECOMPOSITION_TYPE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_decomposition_type_doc,
    "decomposition_type(property, chr) --> string.\n\
    Return the Decomposition_Type value of a character.");

/* Returns the Default_Ignorable_Code_Point property for a codepoint. */
static PyObject* get_default_ignorable_code_point(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_default_ignorable_code_point((Py_UCS4)codepoint);
    name = value_names[UP_DEFAULT_IGNORABLE_CODE_POINT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_default_ignorable_code_point_doc,
    "default_ignorable_code_point(property, chr) --> string.\n\
    Return the Default_Ignorable_Code_Point value of a character.");

/* Returns the Deprecated property for a codepoint. */
static PyObject* get_deprecated(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_deprecated((Py_UCS4)codepoint);
    name = value_names[UP_DEPRECATED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_deprecated_doc,
    "deprecated(property, chr) --> string.\n\
    Return the Deprecated value of a character.");

/* Returns the Diacritic property for a codepoint. */
static PyObject* get_diacritic(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_diacritic((Py_UCS4)codepoint);
    name = value_names[UP_DIACRITIC_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_diacritic_doc,
    "diacritic(property, chr) --> string.\n\
    Return the Diacritic value of a character.");

/* Returns the Digit property for a codepoint. */
static PyObject* get_digit(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_digit((Py_UCS4)codepoint);
    name = value_names[UP_DIGIT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_digit_doc,
    "digit(property, chr) --> string.\n\
    Return the Digit value of a character.");

/* Returns the East_Asian_Width property for a codepoint. */
static PyObject* get_east_asian_width(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_east_asian_width((Py_UCS4)codepoint);
    name = value_names[UP_EAST_ASIAN_WIDTH_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_east_asian_width_doc,
    "east_asian_width(property, chr) --> string.\n\
    Return the East_Asian_Width value of a character.");

/* Returns the Extender property for a codepoint. */
static PyObject* get_extender(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_extender((Py_UCS4)codepoint);
    name = value_names[UP_EXTENDER_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_extender_doc,
    "extender(property, chr) --> string.\n\
    Return the Extender value of a character.");

/* Returns the General_Category property for a codepoint. */
static PyObject* get_general_category(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_general_category((Py_UCS4)codepoint);
    name = value_names[UP_GENERAL_CATEGORY_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_general_category_doc,
    "general_category(property, chr) --> string.\n\
    Return the General_Category value of a character.");

/* Returns the Graph property for a codepoint. */
static PyObject* get_graph(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_graph((Py_UCS4)codepoint);
    name = value_names[UP_GRAPH_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_graph_doc,
    "graph(property, chr) --> string.\n\
    Return the Graph value of a character.");

/* Returns the Grapheme_Base property for a codepoint. */
static PyObject* get_grapheme_base(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_grapheme_base((Py_UCS4)codepoint);
    name = value_names[UP_GRAPHEME_BASE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_grapheme_base_doc,
    "grapheme_base(property, chr) --> string.\n\
    Return the Grapheme_Base value of a character.");

/* Returns the Grapheme_Cluster_Break property for a codepoint. */
static PyObject* get_grapheme_cluster_break(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_grapheme_cluster_break((Py_UCS4)codepoint);
    name = value_names[UP_GRAPHEME_CLUSTER_BREAK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_grapheme_cluster_break_doc,
    "grapheme_cluster_break(property, chr) --> string.\n\
    Return the Grapheme_Cluster_Break value of a character.");

/* Returns the Grapheme_Extend property for a codepoint. */
static PyObject* get_grapheme_extend(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_grapheme_extend((Py_UCS4)codepoint);
    name = value_names[UP_GRAPHEME_EXTEND_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_grapheme_extend_doc,
    "grapheme_extend(property, chr) --> string.\n\
    Return the Grapheme_Extend value of a character.");

/* Returns the Grapheme_Link property for a codepoint. */
static PyObject* get_grapheme_link(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_grapheme_link((Py_UCS4)codepoint);
    name = value_names[UP_GRAPHEME_LINK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_grapheme_link_doc,
    "grapheme_link(property, chr) --> string.\n\
    Return the Grapheme_Link value of a character.");

/* Returns the Hangul_Syllable_Type property for a codepoint. */
static PyObject* get_hangul_syllable_type(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_hangul_syllable_type((Py_UCS4)codepoint);
    name = value_names[UP_HANGUL_SYLLABLE_TYPE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_hangul_syllable_type_doc,
    "hangul_syllable_type(property, chr) --> string.\n\
    Return the Hangul_Syllable_Type value of a character.");

/* Returns the Hex_Digit property for a codepoint. */
static PyObject* get_hex_digit(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_hex_digit((Py_UCS4)codepoint);
    name = value_names[UP_HEX_DIGIT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_hex_digit_doc,
    "hex_digit(property, chr) --> string.\n\
    Return the Hex_Digit value of a character.");

/* Returns the Hyphen property for a codepoint. */
static PyObject* get_hyphen(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_hyphen((Py_UCS4)codepoint);
    name = value_names[UP_HYPHEN_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_hyphen_doc,
    "hyphen(property, chr) --> string.\n\
    Return the Hyphen value of a character.");

/* Returns the ID_Continue property for a codepoint. */
static PyObject* get_id_continue(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_id_continue((Py_UCS4)codepoint);
    name = value_names[UP_ID_CONTINUE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_id_continue_doc,
    "id_continue(property, chr) --> string.\n\
    Return the ID_Continue value of a character.");

/* Returns the Ideographic property for a codepoint. */
static PyObject* get_ideographic(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_ideographic((Py_UCS4)codepoint);
    name = value_names[UP_IDEOGRAPHIC_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_ideographic_doc,
    "ideographic(property, chr) --> string.\n\
    Return the Ideographic value of a character.");

/* Returns the IDS_Binary_Operator property for a codepoint. */
static PyObject* get_ids_binary_operator(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_ids_binary_operator((Py_UCS4)codepoint);
    name = value_names[UP_IDS_BINARY_OPERATOR_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_ids_binary_operator_doc,
    "ids_binary_operator(property, chr) --> string.\n\
    Return the IDS_Binary_Operator value of a character.");

/* Returns the ID_Start property for a codepoint. */
static PyObject* get_id_start(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_id_start((Py_UCS4)codepoint);
    name = value_names[UP_ID_START_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_id_start_doc,
    "id_start(property, chr) --> string.\n\
    Return the ID_Start value of a character.");

/* Returns the IDS_Trinary_Operator property for a codepoint. */
static PyObject* get_ids_trinary_operator(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_ids_trinary_operator((Py_UCS4)codepoint);
    name = value_names[UP_IDS_TRINARY_OPERATOR_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_ids_trinary_operator_doc,
    "ids_trinary_operator(property, chr) --> string.\n\
    Return the IDS_Trinary_Operator value of a character.");

/* Returns the Indic_Positional_Category property for a codepoint. */
static PyObject* get_indic_positional_category(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_indic_positional_category((Py_UCS4)codepoint);
    name = value_names[UP_INDIC_POSITIONAL_CATEGORY_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_indic_positional_category_doc,
    "indic_positional_category(property, chr) --> string.\n\
    Return the Indic_Positional_Category value of a character.");

/* Returns the Indic_Syllabic_Category property for a codepoint. */
static PyObject* get_indic_syllabic_category(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_indic_syllabic_category((Py_UCS4)codepoint);
    name = value_names[UP_INDIC_SYLLABIC_CATEGORY_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_indic_syllabic_category_doc,
    "indic_syllabic_category(property, chr) --> string.\n\
    Return the Indic_Syllabic_Category value of a character.");

/* Returns the Join_Control property for a codepoint. */
static PyObject* get_join_control(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_join_control((Py_UCS4)codepoint);
    name = value_names[UP_JOIN_CONTROL_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_join_control_doc,
    "join_control(property, chr) --> string.\n\
    Return the Join_Control value of a character.");

/* Returns the Joining_Group property for a codepoint. */
static PyObject* get_joining_group(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_joining_group((Py_UCS4)codepoint);
    name = value_names[UP_JOINING_GROUP_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_joining_group_doc,
    "joining_group(property, chr) --> string.\n\
    Return the Joining_Group value of a character.");

/* Returns the Joining_Type property for a codepoint. */
static PyObject* get_joining_type(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_joining_type((Py_UCS4)codepoint);
    name = value_names[UP_JOINING_TYPE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_joining_type_doc,
    "joining_type(property, chr) --> string.\n\
    Return the Joining_Type value of a character.");

/* Returns the Line_Break property for a codepoint. */
static PyObject* get_line_break(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_line_break((Py_UCS4)codepoint);
    name = value_names[UP_LINE_BREAK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_line_break_doc,
    "line_break(property, chr) --> string.\n\
    Return the Line_Break value of a character.");

/* Returns the Logical_Order_Exception property for a codepoint. */
static PyObject* get_logical_order_exception(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_logical_order_exception((Py_UCS4)codepoint);
    name = value_names[UP_LOGICAL_ORDER_EXCEPTION_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_logical_order_exception_doc,
    "logical_order_exception(property, chr) --> string.\n\
    Return the Logical_Order_Exception value of a character.");

/* Returns the Lowercase property for a codepoint. */
static PyObject* get_lowercase(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_lowercase((Py_UCS4)codepoint);
    name = value_names[UP_LOWERCASE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_lowercase_doc,
    "lowercase(property, chr) --> string.\n\
    Return the Lowercase value of a character.");

/* Returns the Math property for a codepoint. */
static PyObject* get_math(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_math((Py_UCS4)codepoint);
    name = value_names[UP_MATH_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_math_doc,
    "math(property, chr) --> string.\n\
    Return the Math value of a character.");

/* Returns the NFC_Quick_Check property for a codepoint. */
static PyObject* get_nfc_quick_check(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_nfc_quick_check((Py_UCS4)codepoint);
    name = value_names[UP_NFC_QUICK_CHECK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_nfc_quick_check_doc,
    "nfc_quick_check(property, chr) --> string.\n\
    Return the NFC_Quick_Check value of a character.");

/* Returns the NFD_Quick_Check property for a codepoint. */
static PyObject* get_nfd_quick_check(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_nfd_quick_check((Py_UCS4)codepoint);
    name = value_names[UP_NFD_QUICK_CHECK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_nfd_quick_check_doc,
    "nfd_quick_check(property, chr) --> string.\n\
    Return the NFD_Quick_Check value of a character.");

/* Returns the NFKC_Quick_Check property for a codepoint. */
static PyObject* get_nfkc_quick_check(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_nfkc_quick_check((Py_UCS4)codepoint);
    name = value_names[UP_NFKC_QUICK_CHECK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_nfkc_quick_check_doc,
    "nfkc_quick_check(property, chr) --> string.\n\
    Return the NFKC_Quick_Check value of a character.");

/* Returns the NFKD_Quick_Check property for a codepoint. */
static PyObject* get_nfkd_quick_check(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_nfkd_quick_check((Py_UCS4)codepoint);
    name = value_names[UP_NFKD_QUICK_CHECK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_nfkd_quick_check_doc,
    "nfkd_quick_check(property, chr) --> string.\n\
    Return the NFKD_Quick_Check value of a character.");

/* Returns the Noncharacter_Code_Point property for a codepoint. */
static PyObject* get_noncharacter_code_point(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_noncharacter_code_point((Py_UCS4)codepoint);
    name = value_names[UP_NONCHARACTER_CODE_POINT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_noncharacter_code_point_doc,
    "noncharacter_code_point(property, chr) --> string.\n\
    Return the Noncharacter_Code_Point value of a character.");

/* Returns the Numeric_Type property for a codepoint. */
static PyObject* get_numeric_type(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_numeric_type((Py_UCS4)codepoint);
    name = value_names[UP_NUMERIC_TYPE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_numeric_type_doc,
    "numeric_type(property, chr) --> string.\n\
    Return the Numeric_Type value of a character.");

/* Returns the Numeric_Value property for a codepoint. */
static PyObject* get_numeric_value(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_numeric_value((Py_UCS4)codepoint);
    name = value_names[UP_NUMERIC_VALUE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_numeric_value_doc,
    "numeric_value(property, chr) --> string.\n\
    Return the Numeric_Value value of a character.");

/* Returns the Other_Alphabetic property for a codepoint. */
static PyObject* get_other_alphabetic(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_alphabetic((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_ALPHABETIC_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_alphabetic_doc,
    "other_alphabetic(property, chr) --> string.\n\
    Return the Other_Alphabetic value of a character.");

/* Returns the Other_Default_Ignorable_Code_Point property for a codepoint. */
static PyObject* get_other_default_ignorable_code_point(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_default_ignorable_code_point((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_DEFAULT_IGNORABLE_CODE_POINT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_default_ignorable_code_point_doc,
    "other_default_ignorable_code_point(property, chr) --> string.\n\
    Return the Other_Default_Ignorable_Code_Point value of a character.");

/* Returns the Other_Grapheme_Extend property for a codepoint. */
static PyObject* get_other_grapheme_extend(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_grapheme_extend((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_GRAPHEME_EXTEND_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_grapheme_extend_doc,
    "other_grapheme_extend(property, chr) --> string.\n\
    Return the Other_Grapheme_Extend value of a character.");

/* Returns the Other_ID_Continue property for a codepoint. */
static PyObject* get_other_id_continue(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_id_continue((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_ID_CONTINUE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_id_continue_doc,
    "other_id_continue(property, chr) --> string.\n\
    Return the Other_ID_Continue value of a character.");

/* Returns the Other_ID_Start property for a codepoint. */
static PyObject* get_other_id_start(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_id_start((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_ID_START_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_id_start_doc,
    "other_id_start(property, chr) --> string.\n\
    Return the Other_ID_Start value of a character.");

/* Returns the Other_Lowercase property for a codepoint. */
static PyObject* get_other_lowercase(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_lowercase((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_LOWERCASE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_lowercase_doc,
    "other_lowercase(property, chr) --> string.\n\
    Return the Other_Lowercase value of a character.");

/* Returns the Other_Math property for a codepoint. */
static PyObject* get_other_math(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_math((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_MATH_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_math_doc,
    "other_math(property, chr) --> string.\n\
    Return the Other_Math value of a character.");

/* Returns the Other_Uppercase property for a codepoint. */
static PyObject* get_other_uppercase(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_other_uppercase((Py_UCS4)codepoint);
    name = value_names[UP_OTHER_UPPERCASE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_other_uppercase_doc,
    "other_uppercase(property, chr) --> string.\n\
    Return the Other_Uppercase value of a character.");

/* Returns the Pattern_Syntax property for a codepoint. */
static PyObject* get_pattern_syntax(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_pattern_syntax((Py_UCS4)codepoint);
    name = value_names[UP_PATTERN_SYNTAX_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_pattern_syntax_doc,
    "pattern_syntax(property, chr) --> string.\n\
    Return the Pattern_Syntax value of a character.");

/* Returns the Pattern_White_Space property for a codepoint. */
static PyObject* get_pattern_white_space(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_pattern_white_space((Py_UCS4)codepoint);
    name = value_names[UP_PATTERN_WHITE_SPACE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_pattern_white_space_doc,
    "pattern_white_space(property, chr) --> string.\n\
    Return the Pattern_White_Space value of a character.");

/* Returns the Posix_Alphanumeric property for a codepoint. */
static PyObject* get_posix_alphanumeric(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_posix_alphanumeric((Py_UCS4)codepoint);
    name = value_names[UP_POSIX_ALPHANUMERIC_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_posix_alphanumeric_doc,
    "posix_alphanumeric(property, chr) --> string.\n\
    Return the Posix_Alphanumeric value of a character.");

/* Returns the Posix_Digit property for a codepoint. */
static PyObject* get_posix_digit(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_posix_digit((Py_UCS4)codepoint);
    name = value_names[UP_POSIX_DIGIT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_posix_digit_doc,
    "posix_digit(property, chr) --> string.\n\
    Return the Posix_Digit value of a character.");

/* Returns the Posix_Punct property for a codepoint. */
static PyObject* get_posix_punct(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_posix_punct((Py_UCS4)codepoint);
    name = value_names[UP_POSIX_PUNCT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_posix_punct_doc,
    "posix_punct(property, chr) --> string.\n\
    Return the Posix_Punct value of a character.");

/* Returns the Posix_XDigit property for a codepoint. */
static PyObject* get_posix_xdigit(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_posix_xdigit((Py_UCS4)codepoint);
    name = value_names[UP_POSIX_XDIGIT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_posix_xdigit_doc,
    "posix_xdigit(property, chr) --> string.\n\
    Return the Posix_XDigit value of a character.");

/* Returns the Prepended_Concatenation_Mark property for a codepoint. */
static PyObject* get_prepended_concatenation_mark(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_prepended_concatenation_mark((Py_UCS4)codepoint);
    name = value_names[UP_PREPENDED_CONCATENATION_MARK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_prepended_concatenation_mark_doc,
    "prepended_concatenation_mark(property, chr) --> string.\n\
    Return the Prepended_Concatenation_Mark value of a character.");

/* Returns the Print property for a codepoint. */
static PyObject* get_print(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_print((Py_UCS4)codepoint);
    name = value_names[UP_PRINT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_print_doc,
    "print(property, chr) --> string.\n\
    Return the Print value of a character.");

/* Returns the Punct property for a codepoint. */
static PyObject* get_punct(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_punct((Py_UCS4)codepoint);
    name = value_names[UP_PUNCT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_punct_doc,
    "punct(property, chr) --> string.\n\
    Return the Punct value of a character.");

/* Returns the Quotation_Mark property for a codepoint. */
static PyObject* get_quotation_mark(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_quotation_mark((Py_UCS4)codepoint);
    name = value_names[UP_QUOTATION_MARK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_quotation_mark_doc,
    "quotation_mark(property, chr) --> string.\n\
    Return the Quotation_Mark value of a character.");

/* Returns the Radical property for a codepoint. */
static PyObject* get_radical(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_radical((Py_UCS4)codepoint);
    name = value_names[UP_RADICAL_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_radical_doc,
    "radical(property, chr) --> string.\n\
    Return the Radical value of a character.");

/* Returns the Regional_Indicator property for a codepoint. */
static PyObject* get_regional_indicator(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_regional_indicator((Py_UCS4)codepoint);
    name = value_names[UP_REGIONAL_INDICATOR_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_regional_indicator_doc,
    "regional_indicator(property, chr) --> string.\n\
    Return the Regional_Indicator value of a character.");

/* Returns the Script property for a codepoint. */
static PyObject* get_script(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_script((Py_UCS4)codepoint);
    name = value_names[UP_SCRIPT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_script_doc,
    "script(property, chr) --> string.\n\
    Return the Script value of a character.");

/* Returns the Sentence_Break property for a codepoint. */
static PyObject* get_sentence_break(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_sentence_break((Py_UCS4)codepoint);
    name = value_names[UP_SENTENCE_BREAK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_sentence_break_doc,
    "sentence_break(property, chr) --> string.\n\
    Return the Sentence_Break value of a character.");

/* Returns the Sentence_Terminal property for a codepoint. */
static PyObject* get_sentence_terminal(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_sentence_terminal((Py_UCS4)codepoint);
    name = value_names[UP_SENTENCE_TERMINAL_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_sentence_terminal_doc,
    "sentence_terminal(property, chr) --> string.\n\
    Return the Sentence_Terminal value of a character.");

/* Returns the Soft_Dotted property for a codepoint. */
static PyObject* get_soft_dotted(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_soft_dotted((Py_UCS4)codepoint);
    name = value_names[UP_SOFT_DOTTED_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_soft_dotted_doc,
    "soft_dotted(property, chr) --> string.\n\
    Return the Soft_Dotted value of a character.");

/* Returns the Terminal_Punctuation property for a codepoint. */
static PyObject* get_terminal_punctuation(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_terminal_punctuation((Py_UCS4)codepoint);
    name = value_names[UP_TERMINAL_PUNCTUATION_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_terminal_punctuation_doc,
    "terminal_punctuation(property, chr) --> string.\n\
    Return the Terminal_Punctuation value of a character.");

/* Returns the Unified_Ideograph property for a codepoint. */
static PyObject* get_unified_ideograph(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_unified_ideograph((Py_UCS4)codepoint);
    name = value_names[UP_UNIFIED_IDEOGRAPH_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_unified_ideograph_doc,
    "unified_ideograph(property, chr) --> string.\n\
    Return the Unified_Ideograph value of a character.");

/* Returns the Uppercase property for a codepoint. */
static PyObject* get_uppercase(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_uppercase((Py_UCS4)codepoint);
    name = value_names[UP_UPPERCASE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_uppercase_doc,
    "uppercase(property, chr) --> string.\n\
    Return the Uppercase value of a character.");

/* Returns the Variation_Selector property for a codepoint. */
static PyObject* get_variation_selector(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_variation_selector((Py_UCS4)codepoint);
    name = value_names[UP_VARIATION_SELECTOR_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_variation_selector_doc,
    "variation_selector(property, chr) --> string.\n\
    Return the Variation_Selector value of a character.");

/* Returns the White_Space property for a codepoint. */
static PyObject* get_white_space(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_white_space((Py_UCS4)codepoint);
    name = value_names[UP_WHITE_SPACE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_white_space_doc,
    "white_space(property, chr) --> string.\n\
    Return the White_Space value of a character.");

/* Returns the Word property for a codepoint. */
static PyObject* get_word(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_word((Py_UCS4)codepoint);
    name = value_names[UP_WORD_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_word_doc,
    "word(property, chr) --> string.\n\
    Return the Word value of a character.");

/* Returns the Word_Break property for a codepoint. */
static PyObject* get_word_break(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_word_break((Py_UCS4)codepoint);
    name = value_names[UP_WORD_BREAK_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_word_break_doc,
    "word_break(property, chr) --> string.\n\
    Return the Word_Break value of a character.");

/* Returns the XDigit property for a codepoint. */
static PyObject* get_xdigit(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_xdigit((Py_UCS4)codepoint);
    name = value_names[UP_XDIGIT_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_xdigit_doc,
    "xdigit(property, chr) --> string.\n\
    Return the XDigit value of a character.");

/* Returns the XID_Continue property for a codepoint. */
static PyObject* get_xid_continue(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_xid_continue((Py_UCS4)codepoint);
    name = value_names[UP_XID_CONTINUE_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_xid_continue_doc,
    "xid_continue(property, chr) --> string.\n\
    Return the XID_Continue value of a character.");

/* Returns the XID_Start property for a codepoint. */
static PyObject* get_xid_start(PyObject* self_, PyObject* args, PyObject*
  kwargs) {
    int codepoint;
    Py_ssize_t val_id;
    char* name;

    static char* kwlist[] = { "chr", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "C", kwlist, &codepoint))
        return NULL;

    val_id = lookup_xid_start((Py_UCS4)codepoint);
    name = value_names[UP_XID_START_NAMES + val_id];

    return PyUnicode_FromString(name);
}

PyDoc_STRVAR(lookup_xid_start_doc,
    "xid_start(property, chr) --> string.\n\
    Return the XID_Start value of a character.");

/* The table of the module's functions. */
static PyMethodDef functions[] = {
    {"alphabetic", (PyCFunction)get_alphabetic, METH_VARARGS|METH_KEYWORDS,
      lookup_alphabetic_doc},
    {"alphanumeric", (PyCFunction)get_alphanumeric, METH_VARARGS|METH_KEYWORDS,
      lookup_alphanumeric_doc},
    {"any", (PyCFunction)get_any, METH_VARARGS|METH_KEYWORDS,
      lookup_any_doc},
    {"ascii_hex_digit", (PyCFunction)get_ascii_hex_digit, METH_VARARGS|METH_KEYWORDS,
      lookup_ascii_hex_digit_doc},
    {"bidi_class", (PyCFunction)get_bidi_class, METH_VARARGS|METH_KEYWORDS,
      lookup_bidi_class_doc},
    {"bidi_control", (PyCFunction)get_bidi_control, METH_VARARGS|METH_KEYWORDS,
      lookup_bidi_control_doc},
    {"bidi_mirrored", (PyCFunction)get_bidi_mirrored, METH_VARARGS|METH_KEYWORDS,
      lookup_bidi_mirrored_doc},
    {"blank", (PyCFunction)get_blank, METH_VARARGS|METH_KEYWORDS,
      lookup_blank_doc},
    {"block", (PyCFunction)get_block, METH_VARARGS|METH_KEYWORDS,
      lookup_block_doc},
    {"canonical_combining_class", (PyCFunction)get_canonical_combining_class, METH_VARARGS|METH_KEYWORDS,
      lookup_canonical_combining_class_doc},
    {"cased", (PyCFunction)get_cased, METH_VARARGS|METH_KEYWORDS,
      lookup_cased_doc},
    {"case_ignorable", (PyCFunction)get_case_ignorable, METH_VARARGS|METH_KEYWORDS,
      lookup_case_ignorable_doc},
    {"changes_when_casefolded", (PyCFunction)get_changes_when_casefolded, METH_VARARGS|METH_KEYWORDS,
      lookup_changes_when_casefolded_doc},
    {"changes_when_casemapped", (PyCFunction)get_changes_when_casemapped, METH_VARARGS|METH_KEYWORDS,
      lookup_changes_when_casemapped_doc},
    {"changes_when_lowercased", (PyCFunction)get_changes_when_lowercased, METH_VARARGS|METH_KEYWORDS,
      lookup_changes_when_lowercased_doc},
    {"changes_when_titlecased", (PyCFunction)get_changes_when_titlecased, METH_VARARGS|METH_KEYWORDS,
      lookup_changes_when_titlecased_doc},
    {"changes_when_uppercased", (PyCFunction)get_changes_when_uppercased, METH_VARARGS|METH_KEYWORDS,
      lookup_changes_when_uppercased_doc},
    {"cntrl", (PyCFunction)get_cntrl, METH_VARARGS|METH_KEYWORDS,
      lookup_cntrl_doc},
    {"dash", (PyCFunction)get_dash, METH_VARARGS|METH_KEYWORDS,
      lookup_dash_doc},
    {"decomposition_type", (PyCFunction)get_decomposition_type, METH_VARARGS|METH_KEYWORDS,
      lookup_decomposition_type_doc},
    {"default_ignorable_code_point", (PyCFunction)get_default_ignorable_code_point, METH_VARARGS|METH_KEYWORDS,
      lookup_default_ignorable_code_point_doc},
    {"deprecated", (PyCFunction)get_deprecated, METH_VARARGS|METH_KEYWORDS,
      lookup_deprecated_doc},
    {"diacritic", (PyCFunction)get_diacritic, METH_VARARGS|METH_KEYWORDS,
      lookup_diacritic_doc},
    {"digit", (PyCFunction)get_digit, METH_VARARGS|METH_KEYWORDS,
      lookup_digit_doc},
    {"east_asian_width", (PyCFunction)get_east_asian_width, METH_VARARGS|METH_KEYWORDS,
      lookup_east_asian_width_doc},
    {"extender", (PyCFunction)get_extender, METH_VARARGS|METH_KEYWORDS,
      lookup_extender_doc},
    {"general_category", (PyCFunction)get_general_category, METH_VARARGS|METH_KEYWORDS,
      lookup_general_category_doc},
    {"graph", (PyCFunction)get_graph, METH_VARARGS|METH_KEYWORDS,
      lookup_graph_doc},
    {"grapheme_base", (PyCFunction)get_grapheme_base, METH_VARARGS|METH_KEYWORDS,
      lookup_grapheme_base_doc},
    {"grapheme_cluster_break", (PyCFunction)get_grapheme_cluster_break, METH_VARARGS|METH_KEYWORDS,
      lookup_grapheme_cluster_break_doc},
    {"grapheme_extend", (PyCFunction)get_grapheme_extend, METH_VARARGS|METH_KEYWORDS,
      lookup_grapheme_extend_doc},
    {"grapheme_link", (PyCFunction)get_grapheme_link, METH_VARARGS|METH_KEYWORDS,
      lookup_grapheme_link_doc},
    {"hangul_syllable_type", (PyCFunction)get_hangul_syllable_type, METH_VARARGS|METH_KEYWORDS,
      lookup_hangul_syllable_type_doc},
    {"hex_digit", (PyCFunction)get_hex_digit, METH_VARARGS|METH_KEYWORDS,
      lookup_hex_digit_doc},
    {"hyphen", (PyCFunction)get_hyphen, METH_VARARGS|METH_KEYWORDS,
      lookup_hyphen_doc},
    {"id_continue", (PyCFunction)get_id_continue, METH_VARARGS|METH_KEYWORDS,
      lookup_id_continue_doc},
    {"ideographic", (PyCFunction)get_ideographic, METH_VARARGS|METH_KEYWORDS,
      lookup_ideographic_doc},
    {"ids_binary_operator", (PyCFunction)get_ids_binary_operator, METH_VARARGS|METH_KEYWORDS,
      lookup_ids_binary_operator_doc},
    {"id_start", (PyCFunction)get_id_start, METH_VARARGS|METH_KEYWORDS,
      lookup_id_start_doc},
    {"ids_trinary_operator", (PyCFunction)get_ids_trinary_operator, METH_VARARGS|METH_KEYWORDS,
      lookup_ids_trinary_operator_doc},
    {"indic_positional_category", (PyCFunction)get_indic_positional_category, METH_VARARGS|METH_KEYWORDS,
      lookup_indic_positional_category_doc},
    {"indic_syllabic_category", (PyCFunction)get_indic_syllabic_category, METH_VARARGS|METH_KEYWORDS,
      lookup_indic_syllabic_category_doc},
    {"join_control", (PyCFunction)get_join_control, METH_VARARGS|METH_KEYWORDS,
      lookup_join_control_doc},
    {"joining_group", (PyCFunction)get_joining_group, METH_VARARGS|METH_KEYWORDS,
      lookup_joining_group_doc},
    {"joining_type", (PyCFunction)get_joining_type, METH_VARARGS|METH_KEYWORDS,
      lookup_joining_type_doc},
    {"line_break", (PyCFunction)get_line_break, METH_VARARGS|METH_KEYWORDS,
      lookup_line_break_doc},
    {"logical_order_exception", (PyCFunction)get_logical_order_exception, METH_VARARGS|METH_KEYWORDS,
      lookup_logical_order_exception_doc},
    {"lowercase", (PyCFunction)get_lowercase, METH_VARARGS|METH_KEYWORDS,
      lookup_lowercase_doc},
    {"math", (PyCFunction)get_math, METH_VARARGS|METH_KEYWORDS,
      lookup_math_doc},
    {"nfc_quick_check", (PyCFunction)get_nfc_quick_check, METH_VARARGS|METH_KEYWORDS,
      lookup_nfc_quick_check_doc},
    {"nfd_quick_check", (PyCFunction)get_nfd_quick_check, METH_VARARGS|METH_KEYWORDS,
      lookup_nfd_quick_check_doc},
    {"nfkc_quick_check", (PyCFunction)get_nfkc_quick_check, METH_VARARGS|METH_KEYWORDS,
      lookup_nfkc_quick_check_doc},
    {"nfkd_quick_check", (PyCFunction)get_nfkd_quick_check, METH_VARARGS|METH_KEYWORDS,
      lookup_nfkd_quick_check_doc},
    {"noncharacter_code_point", (PyCFunction)get_noncharacter_code_point, METH_VARARGS|METH_KEYWORDS,
      lookup_noncharacter_code_point_doc},
    {"numeric_type", (PyCFunction)get_numeric_type, METH_VARARGS|METH_KEYWORDS,
      lookup_numeric_type_doc},
    {"numeric_value", (PyCFunction)get_numeric_value, METH_VARARGS|METH_KEYWORDS,
      lookup_numeric_value_doc},
    {"other_alphabetic", (PyCFunction)get_other_alphabetic, METH_VARARGS|METH_KEYWORDS,
      lookup_other_alphabetic_doc},
    {"other_default_ignorable_code_point", (PyCFunction)get_other_default_ignorable_code_point, METH_VARARGS|METH_KEYWORDS,
      lookup_other_default_ignorable_code_point_doc},
    {"other_grapheme_extend", (PyCFunction)get_other_grapheme_extend, METH_VARARGS|METH_KEYWORDS,
      lookup_other_grapheme_extend_doc},
    {"other_id_continue", (PyCFunction)get_other_id_continue, METH_VARARGS|METH_KEYWORDS,
      lookup_other_id_continue_doc},
    {"other_id_start", (PyCFunction)get_other_id_start, METH_VARARGS|METH_KEYWORDS,
      lookup_other_id_start_doc},
    {"other_lowercase", (PyCFunction)get_other_lowercase, METH_VARARGS|METH_KEYWORDS,
      lookup_other_lowercase_doc},
    {"other_math", (PyCFunction)get_other_math, METH_VARARGS|METH_KEYWORDS,
      lookup_other_math_doc},
    {"other_uppercase", (PyCFunction)get_other_uppercase, METH_VARARGS|METH_KEYWORDS,
      lookup_other_uppercase_doc},
    {"pattern_syntax", (PyCFunction)get_pattern_syntax, METH_VARARGS|METH_KEYWORDS,
      lookup_pattern_syntax_doc},
    {"pattern_white_space", (PyCFunction)get_pattern_white_space, METH_VARARGS|METH_KEYWORDS,
      lookup_pattern_white_space_doc},
    {"posix_alphanumeric", (PyCFunction)get_posix_alphanumeric, METH_VARARGS|METH_KEYWORDS,
      lookup_posix_alphanumeric_doc},
    {"posix_digit", (PyCFunction)get_posix_digit, METH_VARARGS|METH_KEYWORDS,
      lookup_posix_digit_doc},
    {"posix_punct", (PyCFunction)get_posix_punct, METH_VARARGS|METH_KEYWORDS,
      lookup_posix_punct_doc},
    {"posix_xdigit", (PyCFunction)get_posix_xdigit, METH_VARARGS|METH_KEYWORDS,
      lookup_posix_xdigit_doc},
    {"prepended_concatenation_mark", (PyCFunction)get_prepended_concatenation_mark, METH_VARARGS|METH_KEYWORDS,
      lookup_prepended_concatenation_mark_doc},
    {"print", (PyCFunction)get_print, METH_VARARGS|METH_KEYWORDS,
      lookup_print_doc},
    {"punct", (PyCFunction)get_punct, METH_VARARGS|METH_KEYWORDS,
      lookup_punct_doc},
    {"quotation_mark", (PyCFunction)get_quotation_mark, METH_VARARGS|METH_KEYWORDS,
      lookup_quotation_mark_doc},
    {"radical", (PyCFunction)get_radical, METH_VARARGS|METH_KEYWORDS,
      lookup_radical_doc},
    {"regional_indicator", (PyCFunction)get_regional_indicator, METH_VARARGS|METH_KEYWORDS,
      lookup_regional_indicator_doc},
    {"script", (PyCFunction)get_script, METH_VARARGS|METH_KEYWORDS,
      lookup_script_doc},
    {"sentence_break", (PyCFunction)get_sentence_break, METH_VARARGS|METH_KEYWORDS,
      lookup_sentence_break_doc},
    {"sentence_terminal", (PyCFunction)get_sentence_terminal, METH_VARARGS|METH_KEYWORDS,
      lookup_sentence_terminal_doc},
    {"soft_dotted", (PyCFunction)get_soft_dotted, METH_VARARGS|METH_KEYWORDS,
      lookup_soft_dotted_doc},
    {"terminal_punctuation", (PyCFunction)get_terminal_punctuation, METH_VARARGS|METH_KEYWORDS,
      lookup_terminal_punctuation_doc},
    {"unified_ideograph", (PyCFunction)get_unified_ideograph, METH_VARARGS|METH_KEYWORDS,
      lookup_unified_ideograph_doc},
    {"uppercase", (PyCFunction)get_uppercase, METH_VARARGS|METH_KEYWORDS,
      lookup_uppercase_doc},
    {"variation_selector", (PyCFunction)get_variation_selector, METH_VARARGS|METH_KEYWORDS,
      lookup_variation_selector_doc},
    {"white_space", (PyCFunction)get_white_space, METH_VARARGS|METH_KEYWORDS,
      lookup_white_space_doc},
    {"word", (PyCFunction)get_word, METH_VARARGS|METH_KEYWORDS,
      lookup_word_doc},
    {"word_break", (PyCFunction)get_word_break, METH_VARARGS|METH_KEYWORDS,
      lookup_word_break_doc},
    {"xdigit", (PyCFunction)get_xdigit, METH_VARARGS|METH_KEYWORDS,
      lookup_xdigit_doc},
    {"xid_continue", (PyCFunction)get_xid_continue, METH_VARARGS|METH_KEYWORDS,
      lookup_xid_continue_doc},
    {"xid_start", (PyCFunction)get_xid_start, METH_VARARGS|METH_KEYWORDS,
      lookup_xid_start_doc},
    {NULL, NULL}
};

/* The module definition. */
static struct PyModuleDef uniprop_module = {
    PyModuleDef_HEAD_INIT,
    "uniprop",
    NULL,
    -1,
    functions,
    NULL,
    NULL,
    NULL,
    NULL
};

/* Initialises the module. */
PyMODINIT_FUNC PyInit_uniprop(void) {
    PyObject* m;
    PyObject* version;

    m = PyModule_Create(&uniprop_module);
    if (!m)
        return NULL;

    version = PyUnicode_FromString(UNICODE_VERSION);
    if (!version)
        goto error;

    PyObject_SetAttrString(m, "unicode_version", version);
    Py_DECREF(version);

    version = PyUnicode_FromString(UNIPROP_VERSION);
    if (!version)
        goto error;

    PyObject_SetAttrString(m, "version", version);
    Py_DECREF(version);

    return m;

error:
    Py_DECREF(m);
    return NULL;
}
