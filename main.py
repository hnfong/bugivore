from common.appenginepatch.main import main

# A central place for customized patching
# See the section "Adding custom patches to your project" in
#   http://code.google.com/p/app-engine-patch/wiki/GettingStarted

def patch():
    from djangoutils.patch import patch_django
    patch_django()

patch()

if __name__ == '__main__':
    main()
