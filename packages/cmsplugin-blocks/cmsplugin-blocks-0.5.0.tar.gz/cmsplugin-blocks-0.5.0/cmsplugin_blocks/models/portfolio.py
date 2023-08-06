# -*- coding: utf-8 -*-
"""
TODO: This should be like an portfolio but more detailed with optional long text content
      for each object
"""
#from django.db import models
#from django.utils.encoding import force_text, python_2_unicode_compatible
#from django.utils.html import strip_tags
#from django.utils.text import Truncator
#from django.utils.translation import ugettext_lazy as _

#from cms.models.pluginmodel import CMSPlugin

#from cmsplugin_blocks.choices_helpers import (get_portfolio_default_template,
                                              #get_portfolio_template_choices)

#@python_2_unicode_compatible
#class Portfolio(CMSPlugin):
    #"""
    #Portfolio container
    #"""
    #title = models.CharField(
        #_('Title'),
        #blank=False,
        #max_length=50,
        #default="",
    #)
    #brief = models.TextField(
        #_(u"Brief"),
        #blank=True,
        #default="",
    #)
    #template = models.CharField(
        #_('Template'),
        #blank=True,
        #max_length=100,
        #choices=get_portfolio_template_choices(),
        #default=get_portfolio_default_template(),
        #help_text=_('Used template for content formatting.'),
    #)

    #def __str__(self):
        #return self.title

    #def copy_relations(self, oldinstance):
        #"""
        #Copy FK relations when plugin object is copied as another object

        #See:

        #http://docs.django-cms.org/en/latest/how_to/custom_plugins.html#for-foreign-key-relations-from-other-objects
        #"""
        #self.portfolio_item.all().delete()

        #for portfolio_item in oldinstance.portfolio_item.all():
            #portfolio_item.pk = None
            #portfolio_item.portfolio = self
            #portfolio_item.save()

    #class Meta:
        #verbose_name = _('Portfolio')
        #verbose_name_plural = _('Portfolios')


#@python_2_unicode_compatible
#class PortfolioItem(models.Model):
    #"""
    #Portfolio item
    #"""
    #portfolio = models.ForeignKey(
        #Portfolio,
        #related_name="portfolio_item"
    #)

    #image = models.ImageField(
        #_('Image'),
        #upload_to='blocks/portfolio/%y/%m',
        #max_length=255,
        #null=True,
        #blank=False,
        #default=None,
    #)
    #description = models.TextField(
        #_(u"Content"),
        #blank=True,
        #default="",
    #)

    #def __init__(self, *args, **kwargs):
        #super(PortfolioItem, self).__init__(*args, **kwargs)
        #self.description = force_text(self.description)

    #def __str__(self):
        #return Truncator(strip_tags(self.description)).words(4, truncate="...")

    #class Meta:
        #verbose_name = _('Portfolio item')
        #verbose_name_plural = _('Portfolio items')
