from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'resizer/resizer.css',
)
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'resizer/jquery.textarearesizer.js',
)
settings.add_uncombined_app_media('resizer')
