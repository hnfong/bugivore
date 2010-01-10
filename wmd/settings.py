from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'wmd/wmd.css',
)
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'wmd/showdown.js',
)
settings.add_app_media('wmd/wmd.js',
    'wmd/wmd.js',
)
# for use in admin site, which does not include the usual combined css
settings.add_app_media('admin_media/css/combined-%(LANGUAGE_DIR)s.css',
    'wmd/wmd.css',
)
