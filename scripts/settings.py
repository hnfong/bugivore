from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'scripts/watch_unsaved_edits.js',
)
settings.add_app_media('admin_media/js/combined-%(LANGUAGE_CODE)s.js',
    'scripts/admin_watch_unsaved_edits.js',
)
