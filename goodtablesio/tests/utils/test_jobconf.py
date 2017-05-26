# pylama:ignore=E501
import pytest
from goodtablesio import exceptions
from goodtablesio.utils.jobconf import make_validation_conf, verify_validation_conf


# Make validation conf

def test_make_validation_conf():
    job_conf_text = """
    files: '*'
    settings:
      error_limit: 1
    """
    job_files = [
        'file.csv',
        'file.json',
        'file.jsonl',
        'file.ndjson',
        'file.tsv',
        'file.xls',
        'file.ods',
        'file.pdf',
        'goodtables.yml',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file.csv'},
            # {'source': 'http://example.com/file.json'},
            {'source': 'http://example.com/file.jsonl'},
            {'source': 'http://example.com/file.ndjson'},
            {'source': 'http://example.com/file.tsv'},
            {'source': 'http://example.com/file.xls'},
            {'source': 'http://example.com/file.ods'},
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_no_base():
    job_conf_text = """
    files: '*'
    settings:
      error_limit: 1
    """
    job_files = [
        'file.csv',
        'file.json',
        'file.jsonl',
        'file.ndjson',
        'file.tsv',
        'file.xls',
        'file.ods',
        'file.pdf',
        'goodtables.yml',
    ]
    validation_conf = {
        'source': [
            {'source': 'file.csv'},
            # {'source': 'file.json'},
            {'source': 'file.jsonl'},
            {'source': 'file.ndjson'},
            {'source': 'file.tsv'},
            {'source': 'file.xls'},
            {'source': 'file.ods'},
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    assert make_validation_conf(job_conf_text, job_files) == validation_conf


def test_make_validation_conf_subdir():
    job_conf_text = """
    files: '*'
    """
    job_files = [
        'data/file.csv',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_subdir_config():
    job_conf_text = """
    files: data/*
    """
    job_files = [
        'data/file.csv',
        'file.ods',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_subdir_granular():
    job_conf_text = """
    files:
      - source: data/file.csv
        schema: data/schema.json
        delimiter: ';'
        skip_rows: [1, 2, '#', '//']
    settings:
      order_fields: True
    """
    job_files = [
        'data/file.csv',
        'data/schema.json',
        'file.ods',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {
                'source': 'http://example.com/data/file.csv',
                'schema': 'http://example.com/data/schema.json',
                'delimiter': ';',
                'skip_rows': [1, 2, '#', '//'],
            },
        ],
        'settings': {
            'order_fields': True,
        }
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_default_job_conf():
    job_conf_text = None
    job_files = [
        'file1.csv',
        'file2.csv',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file1.csv'},
            {'source': 'http://example.com/file2.csv'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_datapackages():
    job_conf_text = """
    datapackages:
      - datapackage1.json
      - datapackage2.json
    """
    job_files = [
        'datapackage1.json',
        'datapackage2.json',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/datapackage1.json', 'preset': 'datapackage'},
            {'source': 'http://example.com/datapackage2.json', 'preset': 'datapackage'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_files_and_datapackages():
    job_conf_text = """
    files: '*.csv'
    datapackages:
      - datapackage1.json
      - datapackage2.json
    """
    job_files = [
        'file1.csv',
        'file2.csv',
        'datapackage1.json',
        'datapackage2.json',
    ]
    job_base = 'http://example.com'
    # https://github.com/frictionlessdata/goodtables.io/issues/169
    # validation_conf = {
        # 'source': [
            # {'source': 'http://example.com/file1.csv'},
            # {'source': 'http://example.com/file2.csv'},
            # {'source': 'http://example.com/datapackage1.json', 'preset': 'datapackage'},
            # {'source': 'http://example.com/datapackage2.json', 'preset': 'datapackage'},
        # ]
    # }
    # assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf
    with pytest.raises(exceptions.InvalidJobConfiguration):
        make_validation_conf(job_conf_text, job_files, job_base)


def test_make_validation_conf_infer_datapackage_json():
    job_conf_text = None
    job_files = [
        'file1.csv',
        'file2.csv',
        'datapackage.json',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/datapackage.json', 'preset': 'datapackage'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_glob_exlude_json_files():
    job_conf_text = """
    files: '*'
    """
    job_files = [
        'data.csv',
        'data.json',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/data.csv'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_glob_include_json_files_using_pattern():
    job_conf_text = """
    files: '*.json'
    """
    job_files = [
        'data.csv',
        'data.json',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/data.json'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_detect_all_csv_206():
    job_conf_text = None
    job_files = [
        '.DS_Store',
        '.gitiginore',
        'Inspeccion',
        'Inspeccion/.DS_Store',
        'Inspeccion/2011-2013',
        'Inspeccion/2011-2013/.DS_Store',
        'Inspeccion/2011-2013/denuncias.csv',
        'Inspeccion/2011-2013/numero-de-oficiales-federales-de-pesca.csv',
        'Inspeccion/2011-2013/numero-embarcaciones.csv',
        'Inspeccion/2011-2013/pesca-ilegal.csv',
        'Inspeccion/2011-2013/recorridos-inspeccion.csv',
        'Inspeccion/2011-2013/retenidas-provisionalmente.csv',
        'Inspeccion/2011-2013/total-de-actas-y-verificaciones-documentales.csv',
        'Inspeccion/2014-2015',
        'Inspeccion/2014-2015/.DS_Store',
        'Inspeccion/2014-2015/PRESUPUESTO DGIV 2014-2015 (ANEXO 1).ods',
        'Inspeccion/2014-2015/RESULTADOS 2014-2015 (ANEXO 3).ods',
        'Inspeccion/2014-2015/artes_pesca_vehiculos_embarcaciones_decomisadas.csv',
        'Inspeccion/2014-2015/embarcaciones_asignadas_por_entidad_federativa.csv',
        'Inspeccion/2014-2015/oficiales_pesca.csv',
        'Inspeccion/2014-2015/pesca_ilegal_asegurada_o_decomisada.csv',
        'Inspeccion/2014-2015/reporte_denuncias.csv',
        'Inspeccion/2014-2015/sanciones.csv',
        'Otros',
        'Otros/.DS_Store',
        'Otros/Codigos',
        'Otros/Codigos/.DS_Store',
        'Otros/Codigos/ARCH0.CSV',
        'Permisos',
        'Permisos/.DS_Store',
        'Permisos/2_ANEXO_2_2012_MAYORES.csv',
        'Permisos/3_ANEXO_2_2015_MAYORES.csv',
        'Permisos/5_ANEXO_4_2012_MENORES.csv',
        'Permisos/embarcaciones_extranjeras.csv',
        'Permisos/embarcaciones_mayores.csv',
        'Permisos/embarcaciones_menores.csv',
        'Permisos/permisos_concesiones.csv',
        'Permisos/solicitudes_permisos.csv',
        'Permisos/titulares.csv',
        'Produccion',
        'Produccion/.DS_Store',
        'Produccion/2014-2015',
        'Produccion/2014-2015/AvisosArriboNacional2014.csv',
        'Produccion/2014-2015/AvisosArriboNacional2015.csv',
        'Produccion/2014-2015/create.sql',
        'Produccion/2014-2015/metadata.json',
        'README.md',
        'Subsidios',
        'Subsidios/.DS_Store',
        'Subsidios/2014_2015_solicitudes_diesel.csv',
        'Subsidios/2014_2015_solicitudes_gasolina.csv',
        'Subsidios/2014_beneficiarios_modernizacion_embarcaciones_mayores.csv',
        'Subsidios/2015_beneficiarios_modernizacion_embarcaciones_mayores.csv',
        'Subsidios/beneficiarios_embarcaciones_menores.csv',
        'Subsidios/diesel.csv',
        'Subsidios/electricos.csv',
        'Subsidios/gasolina.csv',
        'Subsidios/integral.csv',
        'Subsidios/localidades.csv',
        'Subsidios/motores.csv',
        'Subsidios/pesca.csv',
        'Subsidios/reconversion.csv',
        'Subsidios/solicitudes_embaraciones_mayores.csv',
        'Subsidios/solicitudes_embarcaciones_menores.csv',
        'Subsidios/sustitucion_motores.csv',
        'Subsidios/titulares.csv',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/Inspeccion/2011-2013/denuncias.csv'},
            {'source': 'http://example.com/Inspeccion/2011-2013/numero-de-oficiales-federales-de-pesca.csv'},
            {'source': 'http://example.com/Inspeccion/2011-2013/numero-embarcaciones.csv'},
            {'source': 'http://example.com/Inspeccion/2011-2013/pesca-ilegal.csv'},
            {'source': 'http://example.com/Inspeccion/2011-2013/recorridos-inspeccion.csv'},
            {'source': 'http://example.com/Inspeccion/2011-2013/retenidas-provisionalmente.csv'},
            {'source': 'http://example.com/Inspeccion/2011-2013/total-de-actas-y-verificaciones-documentales.csv'},
            {'source': 'http://example.com/Inspeccion/2014-2015/PRESUPUESTO DGIV 2014-2015 (ANEXO 1).ods'},
            {'source': 'http://example.com/Inspeccion/2014-2015/RESULTADOS 2014-2015 (ANEXO 3).ods'},
            {'source': 'http://example.com/Inspeccion/2014-2015/artes_pesca_vehiculos_embarcaciones_decomisadas.csv'},
            {'source': 'http://example.com/Inspeccion/2014-2015/embarcaciones_asignadas_por_entidad_federativa.csv'},
            {'source': 'http://example.com/Inspeccion/2014-2015/oficiales_pesca.csv'},
            {'source': 'http://example.com/Inspeccion/2014-2015/pesca_ilegal_asegurada_o_decomisada.csv'},
            {'source': 'http://example.com/Inspeccion/2014-2015/reporte_denuncias.csv'},
            {'source': 'http://example.com/Inspeccion/2014-2015/sanciones.csv'},
            {'source': 'http://example.com/Otros/Codigos/ARCH0.CSV'},
            {'source': 'http://example.com/Permisos/2_ANEXO_2_2012_MAYORES.csv'},
            {'source': 'http://example.com/Permisos/3_ANEXO_2_2015_MAYORES.csv'},
            {'source': 'http://example.com/Permisos/5_ANEXO_4_2012_MENORES.csv'},
            {'source': 'http://example.com/Permisos/embarcaciones_extranjeras.csv'},
            {'source': 'http://example.com/Permisos/embarcaciones_mayores.csv'},
            {'source': 'http://example.com/Permisos/embarcaciones_menores.csv'},
            {'source': 'http://example.com/Permisos/permisos_concesiones.csv'},
            {'source': 'http://example.com/Permisos/solicitudes_permisos.csv'},
            {'source': 'http://example.com/Permisos/titulares.csv'},
            {'source': 'http://example.com/Produccion/2014-2015/AvisosArriboNacional2014.csv'},
            {'source': 'http://example.com/Produccion/2014-2015/AvisosArriboNacional2015.csv'},
            {'source': 'http://example.com/Subsidios/2014_2015_solicitudes_diesel.csv'},
            {'source': 'http://example.com/Subsidios/2014_2015_solicitudes_gasolina.csv'},
            {'source': 'http://example.com/Subsidios/2014_beneficiarios_modernizacion_embarcaciones_mayores.csv'},
            {'source': 'http://example.com/Subsidios/2015_beneficiarios_modernizacion_embarcaciones_mayores.csv'},
            {'source': 'http://example.com/Subsidios/beneficiarios_embarcaciones_menores.csv'},
            {'source': 'http://example.com/Subsidios/diesel.csv'},
            {'source': 'http://example.com/Subsidios/electricos.csv'},
            {'source': 'http://example.com/Subsidios/gasolina.csv'},
            {'source': 'http://example.com/Subsidios/integral.csv'},
            {'source': 'http://example.com/Subsidios/localidades.csv'},
            {'source': 'http://example.com/Subsidios/motores.csv'},
            {'source': 'http://example.com/Subsidios/pesca.csv'},
            {'source': 'http://example.com/Subsidios/reconversion.csv'},
            {'source': 'http://example.com/Subsidios/solicitudes_embaraciones_mayores.csv'},
            {'source': 'http://example.com/Subsidios/solicitudes_embarcaciones_menores.csv'},
            {'source': 'http://example.com/Subsidios/sustitucion_motores.csv'},
            {'source': 'http://example.com/Subsidios/titulares.csv'},
        ]
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_non_valid_yaml():
    job_conf_text = """
    - [bad
    """
    job_files = [
        'data.csv',
        'data.json',
    ]
    job_base = 'http://example.com'
    with pytest.raises(exceptions.InvalidJobConfiguration):
        make_validation_conf(job_conf_text, job_files, job_base)


def test_make_validation_just_a_string_yaml():
    job_conf_text = """
    string
    """
    job_files = [
        'data.csv',
        'data.json',
    ]
    job_base = 'http://example.com'
    with pytest.raises(exceptions.InvalidJobConfiguration):
        make_validation_conf(job_conf_text, job_files, job_base)


# Verify validation conf

def test_verify_validation_conf():
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file.csv'},
            {'source': 'http://example.com/datapackage.json', 'preset': 'datapackage'},
        ]
    }
    assert verify_validation_conf(validation_conf)


def test_verify_validation_conf_invalid_bad_preset():
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file.csv', 'preset': 'bad-preset'},
        ]
    }
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        verify_validation_conf(validation_conf)


def test_verify_validation_conf_invalid_empty_source():
    validation_conf = {
        'source': []
    }
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        verify_validation_conf(validation_conf)
