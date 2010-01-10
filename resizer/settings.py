from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'resizer/resizer.css',
)
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'resizer/jquery.textarearesizer.js',
    'resizer/resizer.js',
)
# for use in admin site, which does not include the usual combined css
settings.add_app_media('admin_media/css/combined-%(LANGUAGE_DIR)s.css',
    'resizer/resizer.css',
)
