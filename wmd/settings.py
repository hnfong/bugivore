from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'wmd/wmd.css',
)
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'wmd/showdown.js',
)
settings.add_uncombined_app_media('wmd')
