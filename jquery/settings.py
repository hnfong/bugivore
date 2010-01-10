from ragendja.settings_post import settings
# Load from google for parallel access and caching
#settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
#    'jquery/jquery-1.3.2.min.js',
#    'jquery/jquery-ui-1.7.2.custom.min.js',
#)
# Use customized UI-CSS
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'jquery/jquery-ui-1.7.2.custom.css',
)
settings.add_uncombined_app_media('jquery.images')
