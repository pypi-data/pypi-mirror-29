# to be run from `.../dm/zope/reseller`
i18ndude rebuild-pot -p locales/dm_zope_reseller.pot -m locales/dm_zope_reseller-manual.pot .
i18ndude sync -p locales/dm_zope_reseller.pot locales/*/LC_MESSAGES/*.po
