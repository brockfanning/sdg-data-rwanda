from sdg.open_sdg import open_sdg_build
import sdg
import os

def alter_meta(meta):
# Automatically detect global indicators.
    if 'indicator_number' in meta:
        indicator_id = meta['indicator_number']
        id_parts = indicator_id.split('.')

        # Automatically set some predicable properties.
        meta['goal_number'] = id_parts[0]
        meta['target_number'] = id_parts[0] + '.' + id_parts[1]
        meta['target_name'] = 'global_targets.' + id_parts[0] + '-' + id_parts[1] + '-title'
        meta['indicator_name'] = 'global_indicators.' + id_parts[0] + '-' + id_parts[1] + '-' + id_parts[2] + '-title'
    return meta

open_sdg_build(config='config_data.yml', alter_meta=alter_meta)

# Also produce a filtered SDMX output for use by UNSD.
global_dsd = 'https://registry.sdmx.org/ws/public/sdmxapi/rest/datastructure/IAEG-SDGs/SDG/latest/?format=sdmx-2.1&detail=full&references=children'

data_input = sdg.inputs.InputSdmxMl_Multiple(
    path_pattern='sdmx-data/*.xml',
    import_codes=True,
    dsd='RWA_C_V2_SDG DSD.xml',
    drop_singleton_dimensions=False,
)
inputs = [data_input]
schema = sdg.schemas.SchemaInputOpenSdg(schema_path='_prose.yml')
output = sdg.outputs.OutputSdmxMl(inputs, schema,
    output_folder=os.path.join('_site', 'unsd'),
    sender_id='Rwanda',
    structure_specific=True,
    constrain_data=True,
    dsd=global_dsd,
)
output.execute()
