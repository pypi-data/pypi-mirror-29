__author__ = "Jeremy Nelson"
import datetime
from flask_wtf import FlaskForm as Form
from wtforms import SelectField, StringField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.fields import FieldList
from wtforms import validators, FileField

DIGITAL_ORIGIN = [('born digital','born digital'),
                  ('reformatted digital', 'reformatted digital'),
                  ('digitized microfilm', 'digitized microfilm'),
                  ('digitized other analog', 'digitized other analog')]

FACETS = [("none", "None"),
          ("typeOfResource", "Format"),
          ("subject.geographic", "Geographic"),
          ("genres", "Genres"),
          ("language", "Languages"),
          ("publicationYear", "Publication Year"),
          ("subject.temporal", "Temporal (Time)"),
          ("subject.topic", "Topic")] 

GENRE = [('choose', 'Choose...'),
         ("abstract or summary", "Abstract or Summary"),
         ("art original", "Art Original"),
         ("art reproduction", "Art Reproduction"),
         ("article", "Article"),
         ("atlas", "Atlas"),
         ("autobiography ", "Autobiography "),
         ("bibliography", "Bibliography"),
         ("biography", "Biography"),
         ("book", "Book "),
         ("calendar", "Calendar"),
         ("catalog", "Catalog"),
         ("chart", "Chart"),
         ("comic or graphic novel ", "Comic or Graphic Novel "),
         ("comic strip", "Comic Strip"),
         ("conference publication", "Conference Publication"),
         ("database", "Database"),
         ("dictionary", "Dictionary"),
         ("diorama", "Diorama"),
         ("directory", "Directory"),
         ("discography", "Discography"),
         ("drama", "Drama"),
         ("encyclopedia", "Encyclopedia"),
         ("essay", "Essay"),
         ("festschrift", "Festschrift"),
         ("fiction", "Fiction"),
         ("filmography", "Filmography"),
         ("filmstrip", "Filmstrip"),
         ("finding aid ", "Finding Aid "),
         ("flash card", "Flash Card"),
         ("folktale ", "Folktale "),
         ("font", "Font"),
         ("game", "Game"),
         ("government publication ", "Government Publication "),
         ("graphic", "Graphic"),
         ("globe", "Globe"),
         ("handbook", "Handbook"),
         ("history ", "History "),
         ("hymnal", "Hymnal"),
         ("humor, satire", "Humor, Satire"),
         ("index", "Index"),
         ("instruction ", "Instruction "),
         ("interview ", "Interview "),
         ("issue", "Issue"),
         ("journal", "Journal"),
         ("kit", "Kit"),
         ("language instruction", "Language Instruction"),
         ("law report or digest", "Law Report or Digest"),
         ("legal article", "Legal Article"),
         ("legal case and case notes", "Legal Case and Case Notes"),
         ("legislation", "Legislation"),
         ("letter ", "Letter "),
         ("loose-leaf ", "Loose-Leaf "),
         ("map", "Map"),
         ("memoir ", "Memoir "),
         ("microscope slide", "Microscope Slide"),
         ("model", "Model"),
         ("motion picture", "Motion Picture"),
         ("multivolume monograph", "Multivolume Monograph"),
         ("newspaper", "Newspaper"),
         ("novel ", "Novel "),
         ("numeric data", "Numeric Data"),
         ("offprint", "Offprint"),
         ("online system or service", "Online System or Service"),
         ("patent", "Patent"),
         ("periodical", "Periodical"),
         ("picture", "Picture"),
         ("poetry ", "Poetry "),
         ("programmed text", "Programmed Text"),
         ("realia", "Realia"),
         ("rehearsal ", "Rehearsal "),
         ("remote sensing image", "Remote Sensing Image"),
         ("reporting ", "Reporting "),
         ("review", "Review"),
         ("script", "Script"),
         ("series", "Series"),
         ("short story", "Short Story"),
         ("slide", "Slide"),
         ("sound ", "Sound "),
         ("speech", "Speech"),
         ("standard or specification", "Standard or Specification"),
         ("statistics", "Statistics"),
         ("survey of literature", "Survey of Literature"),
         ("technical drawing", "Technical Drawing"),
         ("technical report", "Technical Report"),
         ("thesis", "Thesis"),
         ("toy", "Toy"),
         ("transparency", "Transparency"),
         ("treaty", "Treaty"),
         ("videorecording ", "Videorecording "),
         ("web site", "Web Site"),
         ("yearbook", "Yearbook")]
         

CONTENT_MODELS = [('islandora:sp_basic_image', 'Basic Image Content Model'),
                  ('islandora:sp_pdf', 'PDF Content Model'),
                  ('islandora:compoundCModel', 'Compound Object Content Model'),
                  ('islandora:sp-audioCModel', 'Audio Content Model'),
                  ('islandora:sp_videoCModel', 'Video Content Model')]

INSTITUTION_NAME = 'Colorado College'

LANGUAGES = [('English','English'),
             ('Spanish', 'Spanish'),
             ('French', 'French'),
             ('German', 'German'),
             ('Italian', 'Italian'),
             ('Chinese', 'Chinese'),
             ('Japanese', 'Japanese')] 

MARC_FREQUENCY = [('choose', 'Choose...'),
                  ('Semiweekly', 'Semiweekly - 2 times a week'),
                  ('Three times a week', 'Three times a week'),
                  ('Weekly', 'Weekly'),
                  ('Biweekly', 'Biweekly - every 2 weeks'),
                  ('Three times a month', 'Three times a month'),
                  ('Semimonthly', 'Semimonthly - 2 times a month'),
                  ('Monthly', 'Monthly'),
                  ('Bimonthly', 'Bimonthly - every 2 months'),
                  ('Quarterly', 'Quarterly'),
                  ('Three times a year', 'Three times a year'),
                  ('Semiannual', 'Semiannual - 2 times a year'),
                  ('Annual', 'Annual'),
                  ('Biennial', 'Biennial - every 2 years'),
                  ('Triennial', 'Triennial - every 3 years'),
                  ('Completely irregular', 'Completely irregular')]

TYPE_OF_RESOURCE = [('text', 'Text or Language Material'),
                    ('cartographic', 'Maps or other Cartographic Materials'),
                    ('notated music', 'Notated Music'),
                    ('sound recording', 'Sound Recording, mixture of music and non-music recording'),
                    ('sound recording-musical', 'Musical Sound Recording'),
                    ('sound recording-nonmusical', 'Spoken word or other Non-music sound recording'),
                    ('still image', 'Still Image'),
                    ('moving image', 'Video or Film, Moving Image'),
                    ('three dimensional object', 'Three Dimensional Object'),
                    ('software, multimedia', 'Software or other electronic Multimedia'),
                    ('mixed material', 'Mixed Material')]

RIGHTS_STATEMENT = "Copyright restrictions apply. Contact Colorado College for permission to publish."
PLACE = 'Colorado Springs (Colo.)'
PUBLISHER = "Colorado College"
PUBLICATION_PLACE = 'Colorado Springs, Colorado'
SEARCH_INDICES = [('li-testdocker1', 'Test Environment (li-testdocker1)'),
                  ('li-docker1', 'Production Environment (li-docker1)')]

class FedoraObjectFromTemplate(Form):
    abstract = TextAreaField("Abstract",
        description="""A summary of the content of the resource.""",
        validators=[validators.length(max=1500)])
    admin_notes = FieldList(
        TextAreaField('Administrative Notes',
            validators=[validators.length(max=1500)]),
        description="""Administrative Note related to the collection, cataloging,
or management of the resource.""",
        min_entries=1)
    alt_title = StringField('Alternative Title',
        description="""Varying form of the title if it contributes to the 
further identification of the item""")
    collection_pid = StringField("PID of Collection",
        description="""PID of the Collection that the resource belongs too.""",
        validators=[validators.required(), validators.length(max=20)])
    content_models = SelectField('Islandora Content Model',
        choices=CONTENT_MODELS,
        default='compoundCModel',
        validators=[validators.required()])
    contributors = FieldList(StringField("Contributors"), 
        description="""A person responsible for making contributions to the 
resource.""",
        min_entries=1)
    corporate_contributors = FieldList(StringField("Corporate Contributors"), 
        description="""An organization responsible for making contributions to the 
resource.""",
        min_entries=1)
    corporate_creators = FieldList(StringField("Corporate Creators"), 
        description="""An organization responsible for the intellectual or 
artistic content of a resource.""", 
        min_entries=1)
    creators = FieldList(
        StringField("Creators"), 
        min_entries=1,
        description="""A person responsible for the intellectual or artistic 
content of a resource.""" 
    )
    date_created = StringField('Date Created', 
        description="""Date of object creation, NOT the date metadata was entered. 
Use YYYY-MM-DD, YYYY-MM, or YYYY formats""")
    digital_origin = SelectField('Digital Origin',
        choices=DIGITAL_ORIGIN,
        description="""The method by which a resource achieved digital form.""")
    description = TextAreaField('Description',
        description="""General information relating to the physical description of 
the resource.""",
        validators=[validators.optional(), 
            validators.length(max=1500)])
    extent = TextAreaField('Extent',
        description="""A statement of the number and specific material of the units 
of the resource that express physical extent.""",
        validators=[validators.optional(), 
                    validators.length(max=1500)])
    form = StringField('Form')
    frequency_free_form = StringField('Other')
    frequency = SelectField('Frequency',
        choices=MARC_FREQUENCY)
    genre = SelectField('Genre',
        choices=GENRE,
        description="""A term or terms that designate a category characterizing
a particular style, form, or content, such as artistic, musical, literary 
composition, etc.""")
    languages = FieldList(SelectField('Languages', choices=LANGUAGES), 
        min_entries=1,
        description="""A designation of the language in which the content of 
a resource is expressed, NOT the language of cataloging.""")
    ordering = StringField("Order in Compound Object",
        description="Child display order within a Compound Object")
    organizations = StringField("Organizations",
                                validators=[validators.optional(), 
                                            validators.length(max=255)],
                                default=INSTITUTION_NAME)
    parent_pid = StringField("PID of Parent",
        description="""PID of parent object, parent object 
must have the Compound Content Model""")
    publisher = StringField('Publisher', default=PUBLISHER,
        description="""The name of the entity that published, printed, 
distributed, released, issued, or produced the resource""")
    publication_place = StringField("Place of Publication", 
        default=PUBLICATION_PLACE,
        description="""Name of a place associated with the issuing, publication, 
release, distribution, manufacture, production, or origin of a resource""")
    rights_statement = TextAreaField('Rights Statement',
                                      default=RIGHTS_STATEMENT)
    subject_dates = FieldList(StringField('Subject -- Dates'),
        description="""Used for chronological subject terms or temporal coverage.""",
        min_entries=1)

    subject_orgs = FieldList(StringField('Subject -- Organization'),
        description="""A name of an organization that is used as a subject.""",
        label='Subject Organizations',
        min_entries=1)
    subject_people = FieldList(StringField('Subject -- Person'),
        description="""A name of a Person used as a subject.""",
        min_entries=1) 
    subject_places = FieldList(
        StringField('Subject -- Places',
            default=PLACE),
        min_entries=1, 
        description="""Used for geographic subject terms that are not parsed as hierarchical 
    geographics"""
    )
    subject_topics = FieldList(StringField('Subject -- Topic'),
        description=""""topic" is used as the tag for any topical subjects that are not appropriate in the 
<geographic>, <temporal>, <titleInfo>, or <name> subelements.""",
        min_entries=1)
    title = StringField('Title',
        description="""A word, phrase, character, or group of characters that 
constitutes the chief title of a resource, i.e., the title normally used when 
citing the resource.""",
            validators=[validators.length(max=120), validators.required()])
    type_of_resources = FieldList(SelectField('Type of Resource', 
                                              choices=TYPE_OF_RESOURCE),
        min_entries=1,
        description="""A term that specifies the characteristics and general type 
of content of the resource.""")

class AddFedoraObjectFromTemplate(FedoraObjectFromTemplate):
    digital_object = FileField(description="Primary datastream for resource")
    thumbnail = FileField(description="Optional thumbnail image for resource")

class AddFedoraBatchFromTemplate(FedoraObjectFromTemplate):
    number_objects = StringField('Number of stub records', default=1)

class EditFedoraObjectFromTemplate(FedoraObjectFromTemplate):
    pid = StringField("PID")

class IndexRepositoryForm(Form):
    index_choice = SelectField('Incremental or Full',
        choices=[('0', 'Incremental'),( '1', 'Full')])
    indices = SelectField('Search Index',
        choices=SEARCH_INDICES)
    start_from = DateField(
        'Start Index From', 
        format='%Y-%m-%d',
        validators=(validators.Optional(),))

class LoadMODSForm(Form):
    pid = StringField("Enter PID to load MODS",
        validators=[validators.optional(),])


class MODSReplacementForm(Form):
    old_value = StringField("Old Value")
    new_value = StringField("New Value")
    collection_pid = StringField("Collection PID",
        validators=[validators.optional(),])
    indices = SelectField('Search Index',
        choices=SEARCH_INDICES)
    pid_listing = TextAreaField('PID Listing',
            validators=[validators.optional(),])
    select_xpath = StringField("Selection XPath")

class MODSSearchForm(Form):
    facet = SelectField('Facet',
        choices=FACETS)
    indices = SelectField('Search Index',
        choices=SEARCH_INDICES)
    query = StringField("Search")


