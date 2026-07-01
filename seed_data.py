"""
Seed completo: crea las tablas y carga todos los datos iniciales.
  - 21 hierbas del Grimorio (base_conocimiento_salud)
  - 15 plantas nuevas del Botiquín (base_conocimiento_salud)
  - 28 dolencias del Botiquín (botiquin)
  - Vinculación botiquin <-> base_conocimiento_salud

Idempotente: verifica existencia antes de insertar. Seguro de ejecutar
sobre una base ya poblada.

Ejecutar: python seed_data.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'salud_natura.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# ── Tablas ────────────────────────────────────────────────────────────────────

conn.execute('''CREATE TABLE IF NOT EXISTS base_conocimiento_salud (
    id_remedio       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_remedio   TEXT NOT NULL,
    planta_base      TEXT,
    propiedades      TEXT,
    contraindicaciones TEXT,
    dosificacion     TEXT,
    link_articulo_web TEXT,
    imagen_url       TEXT
)''')

conn.execute('''CREATE TABLE IF NOT EXISTS usuarios_y_clientes (
    id_usuario       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo  TEXT NOT NULL,
    celular          TEXT,
    email            TEXT,
    direccion_completa TEXT,
    ciudad_prov_pais TEXT,
    latitud          REAL,
    longitud         REAL
)''')

conn.execute('''CREATE TABLE IF NOT EXISTS botiquin (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    dolencia         TEXT NOT NULL,
    emoji            TEXT,
    categoria        TEXT,
    planta           TEXT,
    nombre_cientifico TEXT,
    preparacion      TEXT,
    nota             TEXT,
    id_remedio       INTEGER REFERENCES base_conocimiento_salud(id_remedio)
)''')

# Agregar columnas nuevas a tablas existentes (migraciones seguras)
for alter in [
    "ALTER TABLE base_conocimiento_salud ADD COLUMN imagen_url TEXT",
    "ALTER TABLE botiquin ADD COLUMN id_remedio INTEGER REFERENCES base_conocimiento_salud(id_remedio)",
]:
    try:
        conn.execute(alter)
        conn.commit()
    except Exception:
        pass

conn.commit()

# ── 1. Grimorio: 21 hierbas originales ───────────────────────────────────────
# nombre_remedio sin tildes para que nombreToImg() del grimorio genere la URL correcta

grimorio = [
    ('Manzanilla',   'Matricaria chamomilla',   'Antiinflamatoria,Sedante suave,Digestiva,Antibacteriana,Antiespasmódica',
     'La infusión debe reposar tapada 10 min para conservar sus aceites esenciales.',
     'Alivia insomnio y nerviosismo, calma cólicos y gastritis. En piel reduce rojeces e irritaciones.',
     None, None),
    ('Menta',        'Mentha x piperita',        'Digestiva,Analgésica,Refrescante,Antiespasmódica,Descongestionante',
     'Evitar en niños menores de 2 años. No usar aceite esencial puro sin diluir.',
     'Reduce náuseas, flatulencias y espasmos intestinales. El mentol actúa sobre cefaleas tensionales.',
     None, None),
    ('Lavanda',      'Lavandula angustifolia',   'Ansiolítica,Sedante,Antifúngica,Cicatrizante,Analgésica',
     'El aceite esencial de lavanda puede aplicarse puro en pequeñas áreas.',
     'Reduce ansiedad e insomnio. Aplicada en piel acelera cicatrización de quemaduras leves.',
     None, None),
    ('Romero',       'Salvia rosmarinus',        'Estimulante circulatorio,Antioxidante,Antibacteriano,Hepatoprotector,Nootrópico suave',
     'Contraindicado en embarazo en dosis altas. No usar en epilepsia.',
     'Mejora la memoria estimulando el flujo cerebral. En fricciones combate la alopecia androgénica.',
     None, None),
    ('Curcuma',      'Curcuma longa',            'Antiinflamatoria potente,Antioxidante,Hepatoprotectora,Anticancerígena,Inmunomoduladora',
     'Absorción máxima combinada con pimienta negra y grasas saludables.',
     'La curcumina bloquea las mismas rutas inflamatorias que antiinflamatorios de síntesis.',
     None, None),
    ('Jengibre',     'Zingiber officinale',      'Antiemético,Antiinflamatorio,Termogénico,Digestivo,Circulatorio',
     'En personas con anticoagulantes consultar al médico antes de usar en dosis altas.',
     'El antiemético más estudiado en náuseas del embarazo. Activa la circulación periférica.',
     None, None),
    ('Eucalipto',    'Eucalyptus globulus',      'Expectorante,Antiséptico,Broncodilatador,Antibacteriano,Febrífugo',
     'No usar aceite esencial internamente. Evitar en niños menores de 6 años.',
     'El eucaliptol fluidifica el moco y dilata bronquios. Fundamental en gripe y bronquitis.',
     None, None),
    ('Valeriana',    'Valeriana officinalis',    'Sedante,Ansiolítica,Antiespasmódica,Hipnótica,Miorelajante',
     'El efecto sedante se potencia con alcohol. Evitar conducir tras su consumo en dosis altas.',
     'Reduce la latencia del sueño sin generar dependencia. Ideal para insomnio de conciliación.',
     None, None),
    ('Cola Caballo', 'Equisetum arvense',        'Diurética,Remineralizante,Cicatrizante,Antiinflamatoria,Hemostática',
     'No usar en insuficiencia renal. Tomar con abundante agua. Máximo 6 semanas continuas.',
     'Rica en sílice orgánico, refuerza huesos, uñas y cabello. Excelente diurético natural.',
     None, None),
    ('Caléndula',    'Calendula officinalis',    'Cicatrizante,Antiinflamatoria,Antifúngica,Emoliente,Antibacteriana',
     'Una de las plantas más seguras. Puede producir dermatitis en alérgicos a asteráceas.',
     'Acelera la cicatrización de heridas y quemaduras. Trata dermatitis atópica y eccemas.',
     None, None),
    ('Tomillo',      'Thymus vulgaris',          'Antibacteriano,Expectorante,Antifúngico,Antioxidante,Antiviral',
     'Rico en hierro y vitamina C. En dosis altas puede irritar la mucosa digestiva.',
     'El timol es uno de los antisépticos naturales más potentes. Trata tos, bronquitis y laringitis.',
     None, None),
    ('Pasiflora',    'Passiflora incarnata',     'Sedante,Ansiolítica,Antiespasmódica,Hipnótica,Analgésica',
     'Compatible con valeriana. Evitar combinación con benzodiacepinas.',
     'Actúa sobre los receptores GABA reduciendo ansiedad. Alivia palpitaciones de origen nervioso.',
     None, None),
    ('Diente Leon',  'Taraxacum officinale',     'Diurético,Depurativo,Digestivo,Hepatoprotector,Prebiótico',
     'Recolectar solo en zonas limpias, ya que absorbe contaminantes del suelo.',
     'Estimula la producción de bilis. Depurativo hepático excepcional, rico en inulina y vitaminas.',
     None, None),
    ('Boldo',        'Peumus boldus',            'Hepatoprotector,Colerético,Digestivo,Antioxidante,Laxante suave',
     'Contraindicado en obstrucción de vías biliares. No usar más de 4 semanas seguidas.',
     'La boldina estimula la secreción de bilis. El hepatoprotector más usado en Latinoamérica.',
     None, None),
    ('Ortiga',       'Urtica dioica',            'Diurética,Antiinflamatoria,Remineralizante,Depurativa,Antihistamínica',
     'Cocida o seca pierde el poder urticante. Las semillas son adaptógenas y energizantes.',
     'Elimina el ácido úrico, aliada en gota y artritis. Extraordinariamente nutritiva.',
     None, None),
    ('Salvia',       'Salvia officinalis',       'Antisudorífica,Antimicrobiana,Estrogénica leve,Digestiva,Neuroprotectora',
     'Evitar en embarazo y lactancia. No superar 15 g/día de hoja seca.',
     'La planta de la menopausia: reduce sofocos y sudoración nocturna. Antiséptico oral potente.',
     None, None),
    ('Anis',         'Pimpinella anisum',        'Carminativo,Espasmolítico,Expectorante,Galactagogo,Estrogénico suave',
     'El aceite esencial puede ser tóxico en dosis altas. La infusión es segura.',
     'Alivia gases y cólicos intestinales. Estimula la producción de leche materna.',
     None, None),
    ('Melisa',       'Melissa officinalis',      'Ansiolítica,Antiviral,Digestiva,Sedante,Antiespasmódica',
     'Combina perfecto con valeriana para el insomnio. Las hojas frescas conservan mejor el aroma.',
     'Combate ansiedad y taquicardias nerviosas. Antiviral demostrado contra herpes labial.',
     None, None),
    ('Echinacea',    'Echinacea purpurea',       'Inmunoestimulante,Antiviral,Antibacteriana,Antiinflamatoria,Cicatrizante',
     'No usar más de 8 semanas continuas. No recomendada en enfermedades autoinmunes.',
     'Reduce duración e intensidad de resfríos. Estimula la producción de glóbulos blancos.',
     None, None),
    ('Te Verde',     'Camellia sinensis',        'Antioxidante potente,Termogénico,Cardioprotector,Neuroprotector,Anticancerígeno',
     'Contiene cafeína. Evitar en embarazo e hipertiroidismo en dosis altas.',
     'Las catequinas (EGCG) neutralizan radicales libres. Protege el corazón reduciendo LDL oxidado.',
     None, None),
    ('Ginkgo Biloba','Ginkgo biloba',            'Vasodilatador,Antioxidante,Neuroprotector,Anticoagulante suave,Nootrópico',
     'Interacción con anticoagulantes (warfarina, aspirina). Consultar al médico.',
     'Mejora la microcirculación cerebral aliviando tinnitus y mareos. El árbol más antiguo del mundo.',
     None, None),
]

for nombre, planta_base, propiedades, contraindicaciones, dosificacion, link, imagen in grimorio:
    existe = conn.execute(
        'SELECT id_remedio FROM base_conocimiento_salud WHERE nombre_remedio=?', (nombre,)
    ).fetchone()
    if not existe:
        conn.execute(
            'INSERT INTO base_conocimiento_salud (nombre_remedio, planta_base, propiedades, contraindicaciones, dosificacion, link_articulo_web, imagen_url) VALUES (?,?,?,?,?,?,?)',
            (nombre, planta_base, propiedades, contraindicaciones, dosificacion, link, imagen)
        )

conn.commit()
grimorio_count = conn.execute('SELECT COUNT(*) FROM base_conocimiento_salud').fetchone()[0]
print(f'Grimorio: {grimorio_count} plantas en base_conocimiento_salud')

# ── 2. Plantas nuevas del Botiquín ────────────────────────────────────────────

plantas_nuevas = [
    ('Sauce Blanco',      'Salix alba',                  'Analgésica, Antiinflamatoria, Antipirética, Anticoagulante suave',                                          'Evitar con alergia a aspirina, anticoagulantes o úlcera gástrica',                                         'Decocción: 1 cucharadita de corteza seca en 300 ml de agua 10 min. 2-3 tazas al día',                      None, None),
    ('Árnica',            'Arnica montana',              'Antiinflamatoria, Analgésica tópica, Cicatrizante, Antihematoma',                                            'Solo uso externo. Nunca ingerir ni aplicar en piel abierta o mucosas',                                     'Infusión concentrada externa: 2 cdas de flores en 200 ml agua. Compresa 20 min x 3 veces al día',         None, None),
    ('Harpagofito',       'Harpagophytum procumbens',    'Antiinflamatoria, Analgésica articular, Antirreumática',                                                    'No usar con úlcera gástrica, embarazo o antihipertensivos sin consulta médica',                            'Decocción: 1 cda de raíz triturada en 250 ml agua 10 min. 2 veces al día por 4 semanas mínimo',           None, None),
    ('Cardo Mariano',     'Silybum marianum',            'Hepatoprotectora, Regeneradora hepática, Antiespasmódica, Antiinflamatoria',                                 'Puede causar efecto laxante leve. Consultar en embarazo',                                                  'Infusión de semillas trituradas en 250 ml agua caliente 10 min. 3 tazas al día',                          None, None),
    ('Malvavisco',        'Althaea officinalis',         'Emoliente, Mucilaginosa, Antiinflamatoria, Expectorante, Protectora mucosas',                                'Puede interferir con absorción de otros medicamentos. Tomar separado de fármacos',                         'Maceración fría: 1 cda de raíz en 200 ml agua fría 8 horas. No hervir. Antes de comidas',                None, None),
    ('Hinojo',            'Foeniculum vulgare',          'Carminativa, Digestiva, Antiespasmódica, Galactogoga, Expectorante',                                         'Evitar en embarazo en dosis altas. No usar aceite esencial en niños pequeños',                            'Infusión: 1 cda de semillas machacadas en 250 ml agua caliente 6-7 min. Después de las comidas',          None, None),
    ('Saúco',             'Sambucus nigra',              'Antiviral, Inmunoestimulante, Diaforética, Expectorante, Antifebril',                                        'No consumir bayas, hojas o corteza crudas. Solo flores o bayas maduras cocidas',                           'Infusión: 2 cdas de flores secas en 350 ml agua caliente 10 min. 3 tazas al día',                         None, None),
    ('Tilo',              'Tilia europaea',              'Sedante suave, Antiespasmódica, Diaforética, Hipotensora suave, Antitusígena',                               'No usar en menores de 3 años. Evitar uso prolongado sin supervisión',                                      'Infusión: 2 cdas de flores en 300 ml agua caliente 10 min tapado. 3 tazas al día',                        None, None),
    ('Eleuterococo',      'Eleutherococcus senticosus',  'Adaptógena, Inmunoestimulante, Antifatiga, Nootrópica, Antiestrés',                                          'Evitar con hipertensión grave, embarazo o insomnio. Ciclos de 3 semanas',                                  'Decocción: 1 cdita de raíz seca en 300 ml agua 15 min. En ayunas por la mañana',                          None, None),
    ('Hierba de San Juan','Hypericum perforatum',        'Antidepresiva suave, Ansiolítica, Antiinflamatoria, Antiviral, Cicatrizante',                                 'No combinar con antidepresivos, anticonceptivos, anticoagulantes ni antivirales. Fotosensibilizante',      'Infusión: 1 cda de flores secas en 250 ml agua caliente 10 min. 3 tazas al día por 4-6 semanas',          None, None),
    ('Aloe Vera',         'Aloe barbadensis',            'Cicatrizante, Hidratante, Antiinflamatoria, Antiséptica, Inmunomoduladora',                                  'Solo gel transparente de uso tópico. La parte látex amarilla es laxante y no se debe ingerir',            'Gel directo de hoja fresca sobre piel. Renovar 3-4 veces al día',                                         None, None),
    ('Llantén',           'Plantago major',              'Antihistamínica, Antiinflamatoria, Expectorante, Antimicrobiana, Cicatrizante',                              'Puede causar reacciones alérgicas en personas sensibles al polen',                                         'Hoja fresca estrujada aplicada directamente. O infusión 1 cda en 250 ml agua 10 min',                     None, None),
    ('Arándano Rojo',     'Vaccinium macrocarpon',       'Antiséptica urinaria, Antiadherente bacteriano, Antioxidante, Antiinflamatoria',                             'Preventivo y coadyuvante, no reemplaza antibióticos en infección activa',                                  'Zumo sin azúcar 200 ml x 3 veces al día. O infusión de hojas secas 10 min',                               None, None),
    ('Olivo',             'Olea europaea',               'Hipotensora, Hipoglucemiante, Antioxidante, Antiinflamatoria, Cardioprotectora',                             'Complemento natural. No suspender medicación antihipertensiva sin supervisión médica',                    'Infusión: 10-15 hojas secas en 300 ml agua caliente 10-15 min. 2-3 tazas al día',                         None, None),
    ('Ajo',               'Allium sativum',              'Hipocolesterolemiante, Antimicrobiana, Antifúngica, Antiviral, Cardioprotectora, Hipotensora',                'Puede potenciar anticoagulantes. Evitar en dosis altas con anticoagulantes o preoperatorio',               '1-2 dientes crudos en ayunas. O infusión de ajo machacado en agua templada 5 min',                        None, None),
]

for nombre, planta_base, propiedades, contraindicaciones, dosificacion, link, imagen in plantas_nuevas:
    existe = conn.execute(
        'SELECT id_remedio FROM base_conocimiento_salud WHERE nombre_remedio=?', (nombre,)
    ).fetchone()
    if not existe:
        conn.execute(
            'INSERT INTO base_conocimiento_salud (nombre_remedio, planta_base, propiedades, contraindicaciones, dosificacion, link_articulo_web, imagen_url) VALUES (?,?,?,?,?,?,?)',
            (nombre, planta_base, propiedades, contraindicaciones, dosificacion, link, imagen)
        )

conn.commit()
total_plantas = conn.execute('SELECT COUNT(*) FROM base_conocimiento_salud').fetchone()[0]
print(f'Grimorio + plantas nuevas: {total_plantas} plantas en total')

# ── 3. Botiquín: 28 dolencias ─────────────────────────────────────────────────

count_botiquin = conn.execute('SELECT COUNT(*) FROM botiquin').fetchone()[0]
if count_botiquin == 0:
    dolencias = [
        ('Dolor de cabeza',      '🤕', 'd',  'Sauce Blanco',      'Salix alba',                 'Hierve 1 cucharadita de corteza seca en 300 ml de agua durante 10 min a fuego lento. Cuela, deja templar y bebe. Repite 2-3 veces al día según necesidad.',                                                                        'Evitar si eres alérgico a la aspirina, tomas anticoagulantes o tienes úlcera gástrica.'),
        ('Dolor muscular',       '💪', 'd',  'Árnica',             'Arnica montana',              'Uso externo únicamente. Prepara infusión concentrada con 2 cucharadas de flores en 200 ml de agua. Empapa una gasa y aplica en compresa sobre la zona afectada 20 min, 3 veces al día.',                                          'Nunca ingerir ni aplicar sobre piel abierta, heridas o mucosas. Solo uso tópico.'),
        ('Dolor articular',      '🦵', 'd',  'Harpagofito',        'Harpagophytum procumbens',    'Hierve 1 cucharada de raíz seca triturada en 250 ml de agua a fuego suave 10 min. Deja reposar 5 min tapado. Cuela y bebe. 2 veces al día durante al menos 4 semanas.',                                                           'No usar con úlcera gástrica, embarazo o medicación antihipertensiva sin consultar al médico.'),
        ('Inflamación crónica',  '🔥', 'd',  'Cúrcuma',            'Curcuma longa',               'Hierve 1 rodaja de cúrcuma fresca con una pizca de pimienta negra en 400 ml de agua 10 min. Cuela, añade miel al gusto. 2 tazas al día durante mínimo 3 semanas.',                                                               'La pimienta negra aumenta la absorción de curcumina hasta un 2.000%. Evitar en cálculos biliares.'),
        ('Cólicos menstruales',  '🌸', 'd',  'Cardo Mariano',      'Silybum marianum',            'Muele 1 cucharadita de semillas. Infusiona en 250 ml de agua caliente 10 min. Bebe 3 tazas al día desde 2 días antes del período hasta el final.',                                                                                 'La silimarina actúa como antiespasmódico y antiinflamatorio uterino natural.'),
        ('Dolor de garganta',    '😮', 'd',  'Salvia',             'Salvia officinalis',          'Infusiona 2 cucharaditas de hojas secas en 200 ml de agua caliente 10 min. Usa templada para gárgaras de 30 seg. No tragar si está muy concentrada. Repite cada 2-3 horas.',                                                      'Sus aceites esenciales (tujona, cineol) tienen propiedades antisépticas potentes y comprobadas.'),
        ('Acidez estomacal',     '🫁', 'di', 'Malvavisco',         'Althaea officinalis',         'Maceración fría: 1 cucharada de raíz seca en 200 ml de agua fría durante 8 horas. Nunca hervir — el calor destruye los mucílagos activos. Cuela y bebe antes de las comidas.',                                                    'El gel mucilaginoso crea una barrera protectora sobre la mucosa del esófago y el estómago.'),
        ('Digestión lenta',      '🍽️','di', 'Hinojo',             'Foeniculum vulgare',          'Machaca 1 cucharadita de semillas de hinojo en un mortero. Infusiona en 250 ml de agua caliente 6-7 min. Bebe caliente después de cada comida principal.',                                                                        'Alivia simultáneamente la pesadez, la hinchazón, los gases y los espasmos intestinales.'),
        ('Náuseas',              '🤢', 'di', 'Jengibre',           'Zingiber officinale',         'Hierve 3-4 rodajas de jengibre fresco en 300 ml de agua 5 min. Deja templar y bebe a sorbos lentos. Alternativa rápida: mastica un trozo pequeño de raíz fresca.',                                                               'Tan eficaz como medicamentos convencionales para náuseas del embarazo y quimioterapia.'),
        ('Gases intestinales',   '💨', 'di', 'Anís Verde',         'Pimpinella anisum',           'Infusiona 1 cucharadita de semillas de anís en 250 ml de agua caliente 6 min. Bebe caliente después de las comidas. Añade una hoja de menta fresca si deseas.',                                                                   'El anetol relaja el músculo liso intestinal y facilita la expulsión de gases acumulados.'),
        ('Mareos y vértigos',    '😵', 'di', 'Jengibre',           'Zingiber officinale',         'Mastica un trozo de raíz fresca 30 min antes de viajar. O infusiona 3 rodajas en 250 ml de agua 5 min y bebe antes del trayecto.',                                                                                                'Tan eficaz como el dimenhidrinato para el mareo por movimiento, sin somnolencia.'),
        ('Hígado graso',         '🫀', 'di', 'Cardo Mariano',      'Silybum marianum',            'Muele las semillas y disuelve 1 cucharada en un vaso de agua tibia. Toma en ayunas. O infusiona semillas trituradas en agua caliente 10 min. 3 veces al día, durante 4-8 semanas.',                                               'La silimarina protege y regenera activamente los hepatocitos dañados por grasa acumulada.'),
        ('Resfriado común',      '🤧', 'r',  'Saúco',              'Sambucus nigra',              'Infusiona 2 cucharadas de flores secas de saúco en 350 ml de agua caliente 10 min. Bebe caliente 3 tazas al día. Más eficaz en las primeras 24-48 horas de síntomas.',                                                            'Sus flavonoides impiden activamente que los virus respiratorios penetren en las células.'),
        ('Tos seca',             '😤', 'r',  'Malvavisco',         'Althaea officinalis',         'Infusiona flores y hojas de malvavisco en 300 ml de agua caliente 10 min sin hervir. Bebe caliente a sorbos lentos añadiendo miel de tomillo. 4-5 tazas al día.',                                                                 'Los mucílagos recubren la mucosa respiratoria irritada como una película protectora calmante.'),
        ('Fiebre',               '🌡️','r',  'Tilo',               'Tilia europaea',              'Infusiona 2 cucharadas de flores de tilo en 300 ml de agua caliente 10 min. Tapa. Bebe caliente para inducir sudoración suave. 3 tazas al día mientras dure la fiebre.',                                                         'Regula la temperatura de forma natural y progresiva. No usar en menores de 3 años.'),
        ('Estrés crónico',       '😰', 'e',  'Melisa',             'Melissa officinalis',         'Calienta agua a 90°C (sin llegar a hervir). Infusiona 1 cucharada de hojas frescas durante 7 min. Tapa para conservar los aceites esenciales volátiles. 3 tazas al día.',                                                        'El ácido rosmarínico reduce el cortisol en sangre demostrado en estudios clínicos controlados.'),
        ('Ansiedad',             '😟', 'e',  'Pasiflora',          'Passiflora incarnata',        'Infusiona 1 cucharada de partes aéreas secas en 250 ml de agua caliente 8-10 min. Bebe 2-3 tazas al día. La última taza, 1 hora antes de acostarte.',                                                                            'Actúa sobre receptores GABA con efecto ansiolítico suave. No crea dependencia ni tolerancia.'),
        ('Insomnio',             '😴', 'e',  'Valeriana',          'Valeriana officinalis',       'Decocción: 1 cucharadita de raíz seca triturada en 300 ml de agua 5 min. Deja reposar tapado 10 min. Cuela y bebe 30-60 min antes de acostarte. No superar la dosis indicada.',                                                  'El efecto óptimo se alcanza tras 2-4 semanas de uso regular. No produce somnolencia diurna.'),
        ('Problemas de memoria', '🧠', 'e',  'Ginkgo Biloba',      'Ginkgo biloba',               'Infusiona 1 cucharada de hojas secas en 250 ml de agua caliente 10 min. Bebe 2 tazas al día: una por la mañana y otra al mediodía. Mínimo 6-8 semanas para evaluar el efecto.',                                                   'Mejora la microcirculación cerebral. No combinar con anticoagulantes ni antiagregantes.'),
        ('Fatiga crónica',       '😫', 'e',  'Eleuterococo',       'Eleutherococcus senticosus',  'Decocción de 1 cucharadita de raíz seca en 300 ml de agua 15 min. Bebe por la mañana en ayunas. Sigue ciclos de 3 semanas de toma seguidas de 1 semana de descanso.',                                                            'Adaptógeno que regula la respuesta al estrés físico y mental sin estimulantes ni efectos rebote.'),
        ('Depresión leve',       '🌤️','e',  'Hierba de San Juan', 'Hypericum perforatum',        'Infusiona 1 cucharada de flores secas en 250 ml de agua caliente 10 min. Bebe 3 tazas al día. Se necesitan mínimo 4-6 semanas de uso continuado para ver efecto terapéutico.',                                                   'No combinar con antidepresivos, anticonceptivos, anticoagulantes ni antivirales. Puede causar fotosensibilidad.'),
        ('Heridas leves',        '🩹', 'p',  'Caléndula',          'Calendula officinalis',       'Prepara infusión concentrada con 3 cucharadas de flores en 200 ml de agua. Empapa una gasa y aplica como compresa sobre la herida durante 20 min. Repite 3-4 veces al día.',                                                     'Antiséptica, antiinflamatoria y cicatrizante potente. Una de las plantas tópicas más versátiles.'),
        ('Quemaduras leves',     '🔆', 'p',  'Aloe Vera',          'Aloe barbadensis',            'Corta una hoja de aloe vera. Aplica el gel transparente del interior directamente sobre la quemadura. No cubrir. Deja actuar. Repite 3-4 veces al día hasta la recuperación.',                                                   'Solo para quemaduras de primer grado (sin ampollas). Quemaduras graves requieren atención médica urgente.'),
        ('Picaduras de insecto', '🦟', 'p',  'Llantén',            'Plantago major',              'Estruja una hoja fresca de llantén entre los dedos para liberar el jugo y aplica directamente sobre la picadura. Mantén 10-15 min con presión suave. Repite según necesidad.',                                                   'Antihistamínico y antiinflamatorio natural. Actúa en minutos sobre el picor, el enrojecimiento y la hinchazón.'),
        ('Retención de líquidos','💧', 'c',  'Diente de León',     'Taraxacum officinale',        'Infusiona 1 cucharada de hojas secas en 250 ml de agua caliente 10 min. Bebe 3 tazas al día repartidas. También puedes consumir las hojas frescas y tiernas en ensalada.',                                                       'Diurético natural que, a diferencia de los fármacos, no provoca pérdida de potasio.'),
        ('Infección urinaria',   '🫧', 'c',  'Arándano Rojo',      'Vaccinium macrocarpon',       'Bebe 200 ml de zumo de arándano rojo sin azúcar 3 veces al día. O infusiona hojas secas 10 min. Acompaña siempre con 2 litros de agua al día.',                                                                                  'Preventivo y coadyuvante — no reemplaza a los antibióticos si hay infección activa diagnosticada.'),
        ('Cálculos renales',     '🪨', 'c',  'Cola de Caballo',    'Equisetum arvense',           'Infusiona 1 cucharada de la planta seca en 300 ml de agua caliente 10-15 min. Bebe 3 tazas al día siempre con abundante agua entre tomas (mínimo 2 litros al día).',                                                             'Acción preventiva y disolvente suave. Ante dolor renal intenso o hematuria, acude a urgencias.'),
        ('Presión alta',         '❤️', 'c',  'Olivo',              'Olea europaea',               'Infusiona 10-15 hojas de olivo secas en 300 ml de agua caliente 10-15 min. Bebe 2-3 tazas al día. El efecto es acumulativo: se aprecia mejoría en 2-4 semanas de uso regular.',                                                  'Complemento natural — nunca suspender la medicación antihipertensiva sin supervisión médica.'),
        ('Colesterol elevado',   '🩸', 'c',  'Ajo',                'Allium sativum',              'Consume 1-2 dientes de ajo crudo al día en ayunas, con agua. El alicina se activa al cortar o machacar. O infusiona ajo machacado en agua templada 5 min. El efecto es a largo plazo.',                                          'La acción hipocolesterolemiante es significativamente mayor con ajo crudo que cocinado.'),
    ]
    conn.executemany(
        'INSERT INTO botiquin (dolencia, emoji, categoria, planta, nombre_cientifico, preparacion, nota) VALUES (?,?,?,?,?,?,?)',
        dolencias
    )
    conn.commit()
    print(f'Botiquín: {len(dolencias)} dolencias cargadas')
else:
    print(f'Botiquín: ya tiene {count_botiquin} dolencias, sin cambios')

# ── 4. Vincular botiquin <-> base_conocimiento_salud ─────────────────────────

conn.execute("""
    UPDATE botiquin SET id_remedio = (
        SELECT id_remedio FROM base_conocimiento_salud
        WHERE nombre_remedio = botiquin.planta
    ) WHERE id_remedio IS NULL
""")
conn.commit()

vinculados = conn.execute('SELECT COUNT(*) FROM botiquin WHERE id_remedio IS NOT NULL').fetchone()[0]
total_bot   = conn.execute('SELECT COUNT(*) FROM botiquin').fetchone()[0]
print(f'Vinculación: {vinculados}/{total_bot} dolencias enlazadas con su planta')

# ── Resumen ───────────────────────────────────────────────────────────────────

total_final = conn.execute('SELECT COUNT(*) FROM base_conocimiento_salud').fetchone()[0]
print(f'\nSeed completado — DB: {DB_PATH}')
print(f'  base_conocimiento_salud : {total_final} plantas')
print(f'  botiquin                : {total_bot} dolencias')
conn.close()
