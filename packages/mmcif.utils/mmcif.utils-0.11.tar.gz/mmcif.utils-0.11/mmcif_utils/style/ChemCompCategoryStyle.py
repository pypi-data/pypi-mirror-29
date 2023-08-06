##
# File: ChemCompCategoryStyle.py
# Date: 4-Nov-2012  John Westbrook
#
# Updates:
#  11-Feb-2013 jdw   add style identifier
#   5-Mar-2018 jdw Py2-Py3 and refactor for Python Packaging
##
"""
Standard style details for chemical component data categories in the
chemical component dictionary.

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"



from mmcif_utils.style.PdbxCategoryStyleBase import PdbxCategoryStyleBase


class ChemCompCategoryStyle(PdbxCategoryStyleBase):
    #
    _styleId = "CHEM_COMP_V1"

    _categoryInfo = [('chem_comp', 'key-value'),
                     ('chem_comp_atom', 'table'),
                     ('chem_comp_bond', 'table'),
                     ('pdbx_chem_comp_identifier', 'table'),
                     ('pdbx_chem_comp_descriptor', 'table'),
                     ('pdbx_chem_comp_audit', 'table'),
                     ('pdbx_chem_comp_import', 'table'),
                     ('pdbx_chem_comp_atom_edit', 'table'),
                     ('pdbx_chem_comp_bond_edit', 'table')
                     ]
    _cDict = {
        'chem_comp': [
            ('_chem_comp.id', '%s', 'str', ''),
            ('_chem_comp.name', '%s', 'str', ''),
            ('_chem_comp.type', '%s', 'str', ''),
            ('_chem_comp.pdbx_type', '%s', 'str', ''),
            ('_chem_comp.formula', '%s', 'str', ''),
            ('_chem_comp.mon_nstd_parent_comp_id', '%s', 'str', ''),
            ('_chem_comp.pdbx_synonyms', '%s', 'str', ''),
            ('_chem_comp.pdbx_formal_charge', '%s', 'str', ''),
            ('_chem_comp.pdbx_initial_date', '%s', 'str', ''),
            ('_chem_comp.pdbx_modified_date', '%s', 'str', ''),
            ('_chem_comp.pdbx_ambiguous_flag', '%s', 'str', ''),
            ('_chem_comp.pdbx_release_status', '%s', 'str', ''),
            ('_chem_comp.pdbx_replaced_by', '%s', 'str', ''),
            ('_chem_comp.pdbx_replaces', '%s', 'str', ''),
            ('_chem_comp.formula_weight', '%s', 'str', ''),
            ('_chem_comp.one_letter_code', '%s', 'str', ''),
            ('_chem_comp.three_letter_code', '%s', 'str', ''),
            ('_chem_comp.pdbx_model_coordinates_details', '%s', 'str', ''),
            ('_chem_comp.pdbx_model_coordinates_missing_flag', '%s', 'str', ''),
            ('_chem_comp.pdbx_ideal_coordinates_details', '%s', 'str', ''),
            ('_chem_comp.pdbx_ideal_coordinates_missing_flag', '%s', 'str', ''),
            ('_chem_comp.pdbx_model_coordinates_db_code', '%s', 'str', ''),
            ('_chem_comp.pdbx_subcomponent_list', '%s', 'str', ''),
            ('_chem_comp.pdbx_processing_site', '%s', 'str', '')
        ],
        'chem_comp_atom': [
            ('_chem_comp_atom.comp_id', '%s', 'str', ''),
            ('_chem_comp_atom.atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.alt_atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.type_symbol', '%s', 'str', ''),
            ('_chem_comp_atom.charge', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_align', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_aromatic_flag', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_leaving_atom_flag', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_stereo_config', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_x', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_y', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_z', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_x_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_y_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_z_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_component_atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_component_comp_id', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_ordinal', '%s', 'str', '')
        ],
        'chem_comp_bond': [
            ('_chem_comp_bond.comp_id', '%s', 'str', ''),
            ('_chem_comp_bond.atom_id_1', '%s', 'str', ''),
            ('_chem_comp_bond.atom_id_2', '%s', 'str', ''),
            ('_chem_comp_bond.value_order', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_aromatic_flag', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_stereo_config', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_ordinal', '%s', 'str', '')
        ],
        'pdbx_chem_comp_descriptor': [
            ('_pdbx_chem_comp_descriptor.comp_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_descriptor.type', '%s', 'str', ''),
            ('_pdbx_chem_comp_descriptor.program', '%s', 'str', ''),
            ('_pdbx_chem_comp_descriptor.program_version', '%s', 'str', ''),
            ('_pdbx_chem_comp_descriptor.descriptor', '%s', 'str', '')
        ],
        'pdbx_chem_comp_identifier': [
            ('_pdbx_chem_comp_identifier.comp_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_identifier.type', '%s', 'str', ''),
            ('_pdbx_chem_comp_identifier.program', '%s', 'str', ''),
            ('_pdbx_chem_comp_identifier.program_version', '%s', 'str', ''),
            ('_pdbx_chem_comp_identifier.identifier', '%s', 'str', '')
        ],
        'pdbx_chem_comp_import': [
            ('_pdbx_chem_comp_identifier.comp_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_identifier.comp_alias_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_identifier.model_path', '%s', 'str', '')
        ],
        'pdbx_chem_comp_audit': [
            ('_pdbx_chem_comp_audit.comp_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_audit.action_type', '%s', 'str', ''),
            ('_pdbx_chem_comp_audit.date', '%s', 'str', ''),
            ('_pdbx_chem_comp_audit.processing_site', '%s', 'str', ''),
            ('_pdbx_chem_comp_audit.annotator', '%s', 'str', ''),
            ('_pdbx_chem_comp_audit.details', '%s', 'str', '')
        ],
        'pdbx_chem_comp_atom_edit': [
            ('_pdbx_chem_comp_atom_edit.ordinal', '%d', 'int', ''),
            ('_pdbx_chem_comp_atom_edit.comp_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_atom_edit.atom_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_atom_edit.edit_op', '%s', 'str', ''),
            ('_pdbx_chem_comp_atom_edit.edit_atom_id', '%s', 'str', ''),
            ('_pdbx_chem_comp_atom_edit.edit_atom_value', '%s', 'str', '')
        ],
        'pdbx_chem_comp_bond_edit': [
            ('_pdbx_chem_comp_bond_edit.ordinal', '%d', 'int', ''),
            ('_pdbx_chem_comp_bond_edit.comp_id_1', '%s', 'str', ''),
            ('_pdbx_chem_comp_bond_edit.atom_id_1', '%s', 'str', ''),
            ('_pdbx_chem_comp_bond_edit.comp_id_2', '%s', 'str', ''),
            ('_pdbx_chem_comp_bond_edit.atom_id_2', '%s', 'str', ''),
            ('_pdbx_chem_comp_bond_edit.edit_op', '%s', 'str', ''),
            ('_pdbx_chem_comp_bond_edit.edit_bond_value', '%s', 'str', '')
        ]
    }

    _suppressList = []
    _excludeList = ['_pdbx_chem_comp_audit.annotator', '_pdbx_chem_comp_audit.details']
    #

    def __init__(self):
        super(ChemCompCategoryStyle, self).__init__(styleId=ChemCompCategoryStyle._styleId,
                                                    catFormatL=ChemCompCategoryStyle._categoryInfo,
                                                    catItemD=ChemCompCategoryStyle._cDict,
                                                    excludeList=ChemCompCategoryStyle._excludeList,
                                                    suppressList=ChemCompCategoryStyle._suppressList)
